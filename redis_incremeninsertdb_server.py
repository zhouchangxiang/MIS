#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import base64
import hashlib
import time
import redis
from flask import Blueprint, render_template, request, make_response
import json
import datetime
from sqlalchemy import desc
from dbset.database.db_operate import db_session,pool
from dbset.main.BSFramwork import AlchemyEncoder
from flask_login import login_required, logout_user, login_user,current_user,LoginManager
import arrow
from models.SystemManagement.core import RedisKey, TagClassType, ElectricEnergy, Unit, PriceList, SteamEnergy, \
    WaterEnergy, TagDetail, Equipment
from models.SystemManagement.system import EarlyWarningLimitMaintain, EarlyWarning, EarlyWarningPercentMaintain, \
    ElectricPrice, IncremenTable, WaterSteamPrice
from tools.common import insert,delete,update
from dbset.database import constant
from dbset.log.BK2TLogger import logger,insertSyslog

pool = redis.ConnectionPool(host=constant.REDIS_HOST)
def run():
    while True:
        time.sleep(60)
        print("Redis数据开始写入增量数据库")
        a = arrow.now()
        currentyear = str(a.shift(years=0))[0:4]
        currentmonth = str(a.shift(years=0))[0:7]
        currentday = str(a.shift(days=0))[0:10]
        redis_conn = redis.Redis(connection_pool=pool, password=constant.REDIS_PASSWORD,decode_responses=True)
        keys = db_session.query(TagDetail).filter(TagDetail.TagClassValue == "E_Area_BGL_36_1_26").all()
        for key in keys:
            try:
                k = key.TagClassValue[0:1]
                if k == "E":
                    ZGL = roundtwo(redis_conn.hget(constant.REDIS_ZENGLIANG, key.TagClassValue + "_ZGL"))
                    unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "电").first()
                    # equip = db_session.query(TagClassType.EquipmnetID).filter(TagClassType.TagClassValue == key.TagClassValue).first()
                    timeprices = db_session.query(ElectricPrice).filter(ElectricPrice.PriceName == "电",PriceList.IsEnabled == "是").first()
                    PriceID = ""
                    if timeprices is not None:
                        for timeprice in timeprices:
                            a = int(time.time())  # 当前时间
                            ststr = currentday + timeprice.StartTime
                            endstr = currentday + timeprice.EndTime
                            sttimeArray = time.strptime(ststr, '%Y-%m-%d%H:%M')
                            endtimeArray = time.strptime(endstr, '%Y-%m-%d%H:%M')
                            sttime = int(time.mktime(sttimeArray))
                            endtime = int(time.mktime(endtimeArray))
                            if endtime<sttime:
                                #如果结束时间小于开始时间，说明已经跨天，往后加一天再比大小
                                cuday = str(a.shift(days=1))[0:10]
                                endstr = cuday + timeprice.EndTime
                                endArray = time.strptime(endstr, '%Y-%m-%d%H:%M')
                                endtime = int(time.mktime(endArray))
                            if sttime<a<endtime:
                                PriceID = timeprice.ID
                    inc = IncremenTable()
                    inc.TagClassValue = key.TagClassValue
                    inc.CollectionYear = currentyear
                    inc.CollectionMonth = currentmonth
                    inc.CollectionDay = currentday
                    inc.IncremenValue = ZGL
                    inc.IncremenType = "电"
                    inc.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    inc.Unit = unit[0]
                    # el.EquipmnetID = equip[0]
                    inc.PriceID = PriceID
                    db_session.add(inc)
                    db_session.commit()
                elif k == "S":
                    Liul = roundtwo(redis_conn.hget(constant.REDIS_ZENGLIANG, key.TagClassValue + "S"))  # 蒸汽累计流量
                    unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "汽累计量体积单位").first()
                    # equip = db_session.query(TagClassType.EquipmnetID).filter(TagClassType.TagClassValue == key.TagClassValue).first()
                    prices = db_session.query(WaterSteamPrice).filter(WaterSteamPrice.PriceType == "汽",
                                                                                WaterSteamPrice.IsEnabled == "是").all()
                    for price in prices:
                        sttimeArray = time.strptime(price.StartTime, '%Y-%m-%d%H:%M')
                        endtimeArray = time.strptime(price.EndTime, '%Y-%m-%d%H:%M')
                        sttime = int(time.mktime(sttimeArray))
                        endtime = int(time.mktime(endtimeArray))
                        if sttime<a<endtime:
                            PriceID = price.ID
                    inc = IncremenTable()
                    inc.TagClassValue = key.TagClassValue
                    inc.CollectionYear = currentyear
                    inc.CollectionMonth = currentmonth
                    inc.CollectionDay = currentday
                    inc.IncremenValue = Liul
                    inc.IncremenType = "汽"
                    inc.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    inc.Unit = unit[0]
                    # el.EquipmnetID = equip[0]
                    inc.PriceID = PriceID
                    db_session.add(inc)
                    db_session.commit()
                elif k == "W":
                    wLiul = roundtwo(redis_conn.hget(constant.REDIS_ZENGLIANG, key.TagClassValue + "S"))  # 水的累计流量
                    unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "水累计量体积单位").first()
                    # equip = db_session.query(TagClassType.EquipmnetID).filter(TagClassType.TagClassValue == key.TagClassValue).first()
                    prices = db_session.query(WaterSteamPrice).filter(WaterSteamPrice.PriceType == "水",
                                                                                 WaterSteamPrice.IsEnabled == "是").all()
                    for price in prices:
                        sttimeArray = time.strptime(price.StartTime, '%Y-%m-%d%H:%M')
                        endtimeArray = time.strptime(price.EndTime, '%Y-%m-%d%H:%M')
                        sttime = int(time.mktime(sttimeArray))
                        endtime = int(time.mktime(endtimeArray))
                        if sttime < a < endtime:
                            PriceID = price.ID
                    inc = IncremenTable()
                    inc.TagClassValue = key.TagClassValue
                    inc.CollectionYear = currentyear
                    inc.CollectionMonth = currentmonth
                    inc.CollectionDay = currentday
                    inc.IncremenValue = wLiul
                    inc.IncremenType = "水"
                    inc.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    inc.Unit = unit[0]
                    # el.EquipmnetID = equip[0]
                    inc.PriceID = PriceID
                    db_session.add(inc)
                    db_session.commit()
            except Exception as e:
                print("报错tag："+key.TagClassValue+" |报错IP："+key.IP+"  |报错端口："+key.COMNum+"  |错误："+str(e))
                logger.error(e)
                insertSyslog("error", "实时数据写入DB报错Error：" + str(e),"")
            finally:
                pass
        print("Redis数据开始写入数据库结束")

def roundtwo(rod):
    if rod == None or rod == "" or rod == b'':
        return 0.0
    else:
        if float(rod) < 0:
            return 0.0
        return round(float(rod), 2)
if __name__ == '__main__':
    run()