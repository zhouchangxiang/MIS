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
from models.SystemManagement.system import EarlyWarningLimitMaintain, EarlyWarning, EarlyWarningPercentMaintain
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
        time.sleep(60)
        print("Redis数据开始写入数据库")
        redis_conn = redis.Redis(connection_pool=pool, password=constant.REDIS_PASSWORD,decode_responses=True)
        keys = db_session.query(TagDetail).filter(TagDetail.TagClassValue != None).all()
        for key in keys:
            try:
                k = key.TagClassValue[0:1]
                if k == "E":
                    ZGL = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_ZGL"))
                    AU = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_AU"))
                    AI = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_AI"))
                    BU = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_BU"))
                    BI = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_BI"))
                    CU = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_CU"))
                    CI = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "_CI"))
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
                    # 实时预电压电流故障
                    if AU == 0.0 or BU == 0.0 or CU == 0.0:
                        earw = EarlyWarning()
                        earw.AreaName = key.AreaName
                        EQPName = db_session.query(TagClassType).filter(
                            TagClassType.TagClassValue == key.TagClassValue).first()
                        if EQPName != None:
                            EQPName = EQPName[0]
                        else:
                            EQPName = ""
                        earw.EQPName = EQPName
                        earw.WarningType = "三相电压中缺相"
                        WarningDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        db_session.commit()
                    else:
                        avgI_list = [AI,BI,CI]
                        percentI = 100*((max(avgI_list) - min(avgI_list))/max(avgI_list))
                        EQPName = db_session.query(TagClassType).filter(
                            TagClassType.TagClassValue == key.TagClassValue).first()
                        if EQPName != None:
                            EQPName = EQPName[0]
                        else:
                            EQPName = ""
                        percent = db_session(EarlyWarningPercentMaintain.Percent).filter(EarlyWarningPercentMaintain.AreaName == key.AreaName,
                            EarlyWarningPercentMaintain.EQPName == EQPName).first()
                        if percent != None:
                            percent = percent[0]
                            if percentI > percent:
                                earw = EarlyWarning()
                                earw.AreaName = key.AreaName
                                earw.EQPName = EQPName
                                earw.WarningType = "三相电流不平衡"
                                WarningDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                db_session.commit()
                elif k == "S":
                    valueWD = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "WD"))  # 蒸汽温度

                    #实时预警判断温度是否达到设定值
                    warn = db_session.query(EarlyWarningLimitMaintain).filter(EarlyWarningLimitMaintain.AreaName == key.AreaName,
                                                                       EarlyWarningLimitMaintain.EnergyClass == key.EnergyClass).first()
                    if valueWD < warn.LowerLimit or valueWD > warn.UpperLimit:
                        earw = EarlyWarning()
                        earw.AreaName = key.AreaName
                        EQPName = db_session.query(TagClassType).filter(TagClassType.TagClassValue == key.TagClassValue).first()
                        if EQPName != None:
                            EQPName = EQPName[0]
                        else:
                            EQPName = ""
                        earw.EQPName = EQPName
                        if valueWD < warn.LowerLimit:
                            earw.WarningType = "温度低于最低限值"
                        if valueWD > warn.UpperLimit:
                            earw.WarningType = "温度高于最高限值"
                        WarningDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        db_session.commit()

                    valueF = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "F"))  # 蒸汽瞬时流量
                    valueS = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "S"))  # 蒸汽累计流量

                    ste = db_session.query(SteamEnergy).filter(SteamEnergy.TagClassValue == key.TagClassValue).first()
                    unitf = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "汽瞬时流量单位").first()
                    units = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "汽累计量体积单位").first()
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
                        sl.FlowUnit = unitf[0]
                        sl.SumUnit = units[0]
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
                        sl.FlowUnit = unitf[0]
                        sl.SumUnit = units[0]
                        # sl.EquipmnetID = equip[0]
                        sl.PriceID = price[0]
                        db_session.add(sl)
                        db_session.commit()
                elif k == "W":
                    valueS = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "S"))  # 水的累计流量
                    valueF = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, key.TagClassValue + "F"))  # 水的瞬时流量
                    wat = db_session.query(WaterEnergy).filter(WaterEnergy.TagClassValue == key.TagClassValue).first()
                    unitf = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "水瞬时流量单位").first()
                    units = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "水累计量体积单位").first()
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
                        wa.FlowWUnit = unitf[0]
                        wa.SumWUnit = units[0]
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