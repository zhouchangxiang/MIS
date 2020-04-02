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
from dbset.database.db_operate import db_session, pool
from dbset.main.BSFramwork import AlchemyEncoder
from flask_login import login_required, logout_user, login_user, current_user, LoginManager
import arrow
from models.SystemManagement.core import RedisKey, TagClassType, ElectricEnergy, Unit, SteamEnergy, \
    WaterEnergy, TagDetail, Equipment
from models.SystemManagement.system import EarlyWarningLimitMaintain, EarlyWarning, EarlyWarningPercentMaintain, \
    ElectricPrice, WaterSteamPrice, IncrementElectricTable, IncrementWaterTable, IncrementStreamTable
from tools.common import insert, delete, update
from dbset.database import constant
from dbset.log.BK2TLogger import logger, insertSyslog


def run():
    while True:
        # time.sleep(60)
        print("数据开始写入增量数据库")
        try:
            stekeys = db_session.query(SteamEnergy).filter(SteamEnergy.IncrementFlag == "0",
                                                           SteamEnergy.SumValue != "0.0").order_by(desc("ID")).all()
            for key in stekeys:
                ine = IncrementStreamTable()
                ine.TagClassValue = key.TagClassValue
                ine.CollectionYear = key.CollectionYear
                ine.CollectionMonth = key.CollectionMonth
                ine.CollectionDay = key.CollectionDay
                ine.CollectionHour = str(key.CollectionDate)[0:13]
                proSumValue = db_session.query(SteamEnergy.SumValue).filter(SteamEnergy.ID == key.PrevID).first()
                if proSumValue != None:
                    proSumValue = proSumValue[0]
                else:
                    proSumValue = 0
                ine.IncremenValue = abs(round(float(key.SumValue) - float(proSumValue), 2))
                ine.CalculationID = key.ID
                ine.IncremenType = "汽"
                ine.CollectionDate = key.CollectionDate
                ine.Unit = key.SumUnit
                ine.EquipmnetID = key.EquipmnetID
                ine.PriceID = key.PriceID
                ine.AreaName = key.AreaName
                db_session.add(ine)
                key.IncrementFlag = "1"
                db_session.commit()
            elekeys = db_session.query(ElectricEnergy).filter(ElectricEnergy.IncrementFlag == "0", ElectricEnergy.ZGL != "0.0").order_by(desc("ID")).all()
            for key in elekeys:
                inc = IncrementElectricTable()
                inc.TagClassValue = key.TagClassValue
                inc.CollectionYear = key.CollectionYear
                inc.CollectionMonth = key.CollectionMonth
                inc.CollectionDay = key.CollectionDay
                inc.CollectionHour = str(key.CollectionDate)[0:13]
                prozgl = db_session.query(ElectricEnergy.ZGL).filter(ElectricEnergy.ID == key.PrevID).first()
                if prozgl != None:
                    prozgl = prozgl[0]
                else:
                    prozgl = 0
                inc.IncremenValue = abs(round(float(key.ZGL) - float(prozgl), 2))
                inc.CalculationID = key.ID
                inc.IncremenType = "电"
                inc.CollectionDate = key.CollectionDate
                inc.Unit = key.Unit
                inc.EquipmnetID = key.EquipmnetID
                inc.PriceID = key.PriceID
                inc.AreaName = key.AreaName
                db_session.add(inc)
                key.IncrementFlag = "1"
                db_session.commit()
            watkeys = db_session.query(WaterEnergy).filter(WaterEnergy.IncrementFlag == "0", WaterEnergy.WaterSum != "0.0").order_by(desc("ID")).all()
            for key in watkeys:
                inw = IncrementWaterTable()
                inw.TagClassValue = key.TagClassValue
                inw.CollectionYear = key.CollectionYear
                inw.CollectionMonth = key.CollectionMonth
                inw.CollectionDay = key.CollectionDay
                inw.CollectionHour = str(key.CollectionDate)[0:13]
                proWaterSum = db_session.query(WaterEnergy.WaterSum).filter(WaterEnergy.ID == key.PrevID).first()
                if proWaterSum != None:
                    proWaterSum = proWaterSum[0]
                else:
                    proWaterSum = 0
                inw.IncremenValue = abs(round(float(key.WaterSum) - float(proWaterSum), 2))
                inc.CalculationID = key.ID
                inw.IncremenType = "水"
                inw.CollectionDate = key.CollectionDate
                inw.Unit = key.SumWUnit
                inw.EquipmnetID = key.EquipmnetID
                inw.PriceID = key.PriceID
                inw.AreaName = key.AreaName
                db_session.add(inw)
                key.IncrementFlag = "1"
                db_session.commit()
        except Exception as e:
            print("写入增量库报错：" + str(e))
            logger.errro(e)
            insertSyslog("error", "写入增量库报错Error：" + str(e), "")
        finally:
            pass
        print("数据开始写入增量库结束")


if __name__ == '__main__':
    run()
