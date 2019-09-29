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
    WaterEnergy
from tools.common import insert,delete,update
from dbset.database import constant
from dbset.log.BK2TLogger import logger,insertSyslog

pool = redis.ConnectionPool(host=constant.REDIS_HOST, password=constant.REDIS_PASSWORD)
a = arrow.now()
currentyear = str(a.shift(years=0))[0:4]
currentmonth = str(a.shift(years=0))[0:7]
currentday = str(a.shift(days=0))[0:10]
def run():
    while True:
        data_dict = {}
        redis_conn = redis.Redis(connection_pool=pool)
        keys = db_session.query(TagClassType.TagClassValue).filter().all()
        for key in keys:
            value = redis_conn.hget(constant.REDIS_TABLENAME, key[0]).decode('utf-8')
            k = key[0][0:1]
            if k == "E":
                ele = db_session.query(ElectricEnergy).filter(ElectricEnergy.TagClassValue == key[0]).first()
                unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "电").first()
                equip = db_session.query(TagClassType.EquipmnetID).filter(TagClassType.TagClassValue == key).first()
                price = db_session.query(PriceList.PriceValue).filter(PriceList.PriceName == "电",PriceList.IsEnabled == "是").first()
                if ele == None:
                    el = ElectricEnergy()
                    el.TagClassValue = key[0]
                    el.CollectionYear = currentyear
                    el.CollectionMonth = currentmonth
                    el.CollectionDay = currentday
                    el.ElectricEnergyValue = value
                    el.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    el.Unit = unit[0]
                    el.EquipmnetID = equip[0]
                    el.PriceID =price[0]
                    db_session.add(el)
                    db_session.commit()
                elif ele.ElectricEnergyValue != value:
                    el = ElectricEnergy()
                    el.TagClassValue = key[0]
                    el.CollectionYear = currentyear
                    el.CollectionMonth = currentmonth
                    el.CollectionDay = currentday
                    el.ElectricEnergyValue = value
                    el.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    el.Unit = unit[0]
                    el.EquipmnetID = equip[0]
                    el.PriceID = price[0]
                    db_session.add(el)
                    db_session.commit()
            elif k == "S":
                ste = db_session.query(SteamEnergy).filter(SteamEnergy.TagClassValue == key).first()
                unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "汽").first()
                equip = db_session.query(TagClassType.EquipmnetID).filter(TagClassType.TagClassValue == key).first()
                price = db_session.query(PriceList.PriceValue).filter(PriceList.PriceName == "汽",
                                                                      PriceList.IsEnabled == "是").first()
                if ste == None:
                    sl = SteamEnergy()
                    sl.TagClassValue = key[0]
                    sl.CollectionYear = currentyear
                    sl.CollectionMonth = currentmonth
                    sl.CollectionDay = currentday
                    sl.SteamValue = value
                    sl.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    sl.Unit = unit[0]
                    sl.EquipmnetID = equip[0]
                    sl.PriceID = price[0]
                    db_session.add(sl)
                    db_session.commit()
                elif ste.SteamValue != value:
                    sl = SteamEnergy()
                    sl.TagClassValue = key[0]
                    sl.CollectionYear = currentyear
                    sl.CollectionMonth = currentmonth
                    sl.CollectionDay = currentday
                    sl.SteamValue = value
                    sl.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    sl.Unit = unit[0]
                    sl.EquipmnetID = equip[0]
                    sl.PriceID = price[0]
                    db_session.add(sl)
                    db_session.commit()
            elif k == "W":
                wat = db_session.query(WaterEnergy).filter(WaterEnergy.TagClassValue == key).first()
                unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "水").first()
                equip = db_session.query(TagClassType.EquipmnetID).filter(TagClassType.TagClassValue == key).first()
                price = db_session.query(PriceList.PriceValue).filter(PriceList.PriceName == "水",
                                                                      PriceList.IsEnabled == "是").first()
                if wat == None:
                    wa = WaterEnergy()
                    wa.TagClassValue = key[0]
                    wa.CollectionYear = currentyear
                    wa.CollectionMonth = currentmonth
                    wa.CollectionDay = currentday
                    wa.WaterMeterValue = value
                    wa.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    wa.Unit = unit[0]
                    wa.EquipmnetID = equip[0]
                    wa.PriceID = price[0]
                    db_session.add(wa)
                    db_session.commit()
                elif wat.WaterMeterValue != value:
                    wa = WaterEnergy()
                    wa.TagClassValue = key[0]
                    wa.CollectionYear = currentyear
                    wa.CollectionMonth = currentmonth
                    wa.CollectionDay = currentday
                    wa.WaterMeterValue = value
                    wa.CollectionDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    wa.Unit = unit[0]
                    wa.EquipmnetID = equip[0]
                    wa.PriceID = price[0]
                    db_session.add(wa)
                    db_session.commit()
        time.sleep(1)
if __name__ == '__main__':
    run()