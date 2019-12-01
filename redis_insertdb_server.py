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
    WaterEnergy, TagDetail
from tools.common import insert,delete,update
from dbset.database import constant
from dbset.log.BK2TLogger import logger,insertSyslog

pool = redis.ConnectionPool(host=constant.REDIS_HOST)
a = arrow.now()
currentyear = str(a.shift(years=0))[0:4]
currentmonth = str(a.shift(years=0))[0:7]
currentday = str(a.shift(days=0))[0:10]
def run():
    while True:
        # time.sleep(10)
        data_dict = {}
        redis_conn = redis.Redis(connection_pool=pool, password=constant.REDIS_PASSWORD,decode_responses=True)
<<<<<<< HEAD
        keys = db_session.query(TagDetail).filter(TagDetail.TagClassValue == "E_Area_JK_28_1_16").all()
=======
        keys = db_session.query(TagDetail).filter(TagDetail.TagClassValue != None).all()
>>>>>>> 942ff2b1e0b26774f7453ebca74b067d9aaa33a6
        for key in keys:
            try:
                k = key.TagClassValue[0:1]
                if k == "E":
                    ZGL = float(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_ZGL"))
                    AU = float(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_AU"))
                    AI = float(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_AI"))
                    BU = float(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_BU"))
                    BI = float(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_BI"))
                    CU = float(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_CU"))
                    CI = float(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_CI"))
                    ele = db_session.query(ElectricEnergy).filter(ElectricEnergy.TagClassValue == key.TagClassValue).first()
                    unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "电").first()
                    # equip = db_session.query(TagClassType.EquipmnetID).filter(TagClassType.TagClassValue == key.TagClassValue).first()
                    price = db_session.query(PriceList.PriceValue).filter(PriceList.PriceName == "电",PriceList.IsEnabled == "是").first()
                    if ele == None:
                        el = ElectricEnergy()
                        el.TagClassValue = key.TagClassValue
                        el.CollectionYear = currentyear
                        el.CollectionMonth = currentmonth
                        el.CollectionDay = currentday
                        el.ZGL = ZGL
                        el.AU = AU
                        el.AI = AI
                        el.AI = ZGL
                        el.BU = BU
                        el.BI = BI
                        el.CU = CU
                        el.CI = CI
                        el.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        el.Unit = unit[0]
                        # el.EquipmnetID = equip[0]
                        el.PriceID =price[0]
                        db_session.add(el)
                        db_session.commit()
                    else:
                        el = ElectricEnergy()
                        el.TagClassValue = key.TagClassValue
                        el.CollectionYear = currentyear
                        el.CollectionMonth = currentmonth
                        el.CollectionDay = currentday
                        el.ZGL = ZGL
                        el.AU = AU
                        el.AI = AI
                        el.AI = ZGL
                        el.BU = BU
                        el.BI = BI
                        el.CU = CU
                        el.CI = CI
                        el.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        el.Unit = unit[0]
                        # el.EquipmnetID = equip[0]
                        el.PriceID = price[0]
                        db_session.add(el)
                        db_session.commit()
                elif k == "S":
                    valueWD = float(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "WD"))  # 蒸汽温度
                    valueF = float(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "F"))  # 蒸汽瞬时流量
                    valueS = float(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "S"))  # 蒸汽累计流量

                    ste = db_session.query(SteamEnergy).filter(SteamEnergy.TagClassValue == key.TagClassValue).first()
                    unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "汽").first()
                    # equip = db_session.query(TagClassType.EquipmnetID).filter(TagClassType.TagClassValue == key.TagClassValue).first()
                    price = db_session.query(PriceList.PriceValue).filter(PriceList.PriceName == "汽",
                                                                          PriceList.IsEnabled == "是").first()
                    if ste == None:
                        sl = SteamEnergy()
                        sl.TagClassValue = key.TagClassValue
                        sl.CollectionYear = currentyear
                        sl.CollectionMonth = currentmonth
                        sl.CollectionDay = currentday
                        sl.WD = valueWD
                        sl.FlowValue = valueF
                        sl.SumValue = valueS
                        sl.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        sl.Unit = unit[0]
                        # sl.EquipmnetID = equip[0]
                        sl.PriceID = price[0]
                        db_session.add(sl)
                        db_session.commit()
                    else:
                        sl = SteamEnergy()
                        sl.TagClassValue = key.TagClassValue
                        sl.CollectionYear = currentyear
                        sl.CollectionMonth = currentmonth
                        sl.CollectionDay = currentday
                        sl.FlowValue = valueF
                        sl.SumValue = valueS
                        sl.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        sl.Unit = unit[0]
                        # sl.EquipmnetID = equip[0]
                        sl.PriceID = price[0]
                        db_session.add(sl)
                        db_session.commit()
                elif k == "W":
                    valueS = float(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "S"))  # 水的累计流量
                    valueF = float(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "F"))  # 水的瞬时流量
                    wat = db_session.query(WaterEnergy).filter(WaterEnergy.TagClassValue == key.TagClassValue).first()
                    unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "水").first()
                    # equip = db_session.query(TagClassType.EquipmnetID).filter(TagClassType.TagClassValue == key.TagClassValue).first()
                    price = db_session.query(PriceList.PriceValue).filter(PriceList.PriceName == "水",
                                                                          PriceList.IsEnabled == "是").first()
                    if wat == None:
                        wa = WaterEnergy()
                        wa.TagClassValue = key.TagClassValue
                        wa.CollectionYear = currentyear
                        wa.CollectionMonth = currentmonth
                        wa.CollectionDay = currentday
                        wa.WaterFlow = valueF
                        wa.WaterSum = valueS
                        wa.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        wa.Unit = unit[0]
                        # wa.EquipmnetID = equip[0]
                        wa.PriceID = price[0]
                        db_session.add(wa)
                        db_session.commit()
                    else:
                        wa = WaterEnergy()
                        wa.TagClassValue = key.TagClassValue
                        wa.CollectionYear = currentyear
                        wa.CollectionMonth = currentmonth
                        wa.CollectionDay = currentday
                        wa.WaterFlow = valueF
                        wa.WaterSum = valueS
                        wa.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        wa.Unit = unit[0]
                        # wa.EquipmnetID = equip[0]
                        wa.PriceID = price[0]
                        db_session.add(wa)
                        db_session.commit()
            except Exception as e:
                print("报错tag："+key.TagClassValue+" |报错IP："+key.IP+"  |报错端口："+key.COMNum+"  |错误："+str(e))
                logger.error(e)
                insertSyslog("error", "实时数据写入DB报错Error：" + str(e),"")
            finally:
                pass
if __name__ == '__main__':
    run()