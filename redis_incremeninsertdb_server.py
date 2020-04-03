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
from dbset.database.db_operate import engine,conn

def run():
    while True:
        # time.sleep(60)
        print("数据开始写入增量数据库")
        try:
            #汽能插入增量库
            steam_value = list()
            stekeys = db_session.query(SteamEnergy).filter(SteamEnergy.IncrementFlag == "0",
                                                           SteamEnergy.SumValue != "0.0").order_by(desc("ID")).all()
            for key in stekeys:
                proSumValue = db_session.query(SteamEnergy.SumValue).filter(SteamEnergy.ID == key.PrevID).first()
                if proSumValue != None:
                    proSumValue = proSumValue[0]
                else:
                    proSumValue = 0
                sumvalue = abs(round(float(key.SumValue) - float(proSumValue), 2))
                ss = (sumvalue, "汽", key.ID,
                      key.PriceID, key.SumUnit, key.EquipmnetID,
                      key.TagClassValue, key.CollectionDate, key.CollectionYear, key.CollectionMonth,
                      key.CollectionDay, str(key.CollectionDate)[0:13], key.AreaName, "0")
                steam_value.append(ss)
            try:
                cursor = conn.cursor()
                cursor.executemany(
                    "INSERT INTO IncrementStreamTable VALUES (%s,%s,%d,%d,%s,%d,%s,%s,%s,%s,%s,%s,%s,%s)",
                    steam_value)
                conn.commit()
            except Exception as e:
                print(e)
            #更新增量库原始数据库
            steam_IDS = list()
            steamInitial = list()
            upstekeys = db_session.query(IncrementStreamTable).filter(IncrementStreamTable.insertFlag == "0").order_by(desc("ID")).all()
            for upskey in upstekeys:
                st = ("1", upskey.ID)
                stin = ("1", upskey.CalculationID)
                steam_IDS.append(st)
                steamInitial.append(stin)
            if len(steam_IDS) > 0:
                try:
                    cursor = conn.cursor()
                    cursor.executemany(
                        "update IncrementStreamTable SET insertFlag=(%s) where id=(%d)", steam_IDS)
                    cursor.executemany(
                        "update SteamEnergy SET IncrementFlag=(%s) where id=(%d)", steamInitial)
                    conn.commit()
                except Exception as e:
                    print(e)
            #电能
            electric_value = list()
            elekeys = db_session.query(ElectricEnergy).filter(ElectricEnergy.IncrementFlag == "0",
                                                              ElectricEnergy.ZGL != "0.0").order_by(desc("ID")).all()
            for key in elekeys:
                proZGLmValue = db_session.query(ElectricEnergy.ZGL).filter(ElectricEnergy.ID == key.PrevID).first()
                if proZGLmValue != None:
                    proZGLmValue = proZGLmValue[0]
                else:
                    proZGLmValue = 0
                ZGLvalue = abs(round(float(key.ZGL) - float(proZGLmValue), 2))
                el = (ZGLvalue, "电", key.ID,
                      key.PriceID, key.Unit, key.EquipmnetID,
                      key.TagClassValue, key.CollectionDate, key.CollectionYear, key.CollectionMonth,
                      key.CollectionDay, str(key.CollectionDate)[0:13], key.AreaName, "0")
                electric_value.append(el)
            try:
                cursor = conn.cursor()
                cursor.executemany(
                    "INSERT INTO IncrementElectricTable VALUES (%s,%s,%d,%d,%s,%d,%s,%s,%s,%s,%s,%s,%s,%s)",
                    electric_value)
                conn.commit()
            except Exception as e:
                print(e)
            # 更新增量库原始数据库
            electric_IDS = list()
            electricInitial = list()
            upeleskeys = db_session.query(IncrementElectricTable).filter(
                IncrementElectricTable.insertFlag == "0").order_by(desc("ID")).all()
            for upelekey in upeleskeys:
                ele = ("1", upelekey.ID)
                elein = ("1", upelekey.CalculationID)
                electric_IDS.append(ele)
                electricInitial.append(elein)
            if len(electric_IDS) > 0:
                try:
                    cursor = conn.cursor()
                    cursor.executemany(
                        "update IncrementElectricTable SET insertFlag=(%s) where id=(%d)", electric_IDS)
                    cursor.executemany(
                        "update ElectricEnergy SET IncrementFlag=(%s) where id=(%d)", electricInitial)
                    conn.commit()
                except Exception as e:
                    print(e)
            #水
            water_value = list()
            elekeys = db_session.query(WaterEnergy).filter(WaterEnergy.IncrementFlag == "0",
                                                           WaterEnergy.ZGL != "0.0").order_by(desc("ID")).all()
            for key in elekeys:
                proWsumValue = db_session.query(WaterEnergy.WaterSum).filter(WaterEnergy.ID == key.PrevID).first()
                if proWsumValue != None:
                    proWsumValue = proWsumValue[0]
                else:
                    proWsumValue = 0
                wsumvalue = abs(round(float(key.WaterSum) - float(proWsumValue), 2))
                wt = (wsumvalue, "水", key.ID,
                      key.PriceID, key.SumWUnit, key.EquipmnetID,
                      key.TagClassValue, key.CollectionDate, key.CollectionYear, key.CollectionMonth,
                      key.CollectionDay, str(key.CollectionDate)[0:13], key.AreaName, "0")
                water_value.append(wt)
            try:
                cursor = conn.cursor()
                cursor.executemany(
                    "INSERT INTO IncrementWaterTable VALUES (%s,%s,%d,%d,%s,%d,%s,%s,%s,%s,%s,%s,%s,%s)",
                    water_value)
                conn.commit()
            except Exception as e:
                print(e)
            # 更新增量库原始数据库
            water_IDS = list()
            waterInitial = list()
            upwatskeys = db_session.query(IncrementWaterTable).filter(
                IncrementElectricTable.insertFlag == "0").order_by(desc("ID")).all()
            for upwkey in upwatskeys:
                wat = ("1", upwkey.ID)
                watin = ("1", upwkey.CalculationID)
                water_IDS.append(wat)
                waterInitial.append(watin)
            if len(water_IDS) > 0:
                try:
                    cursor = conn.cursor()
                    cursor.executemany(
                        "update IncrementWaterTable SET insertFlag=(%s) where id=(%d)", water_IDS)
                    cursor.executemany(
                        "update WaterEnergy SET IncrementFlag=(%s) where id=(%d)", waterInitial)
                    conn.commit()
                except Exception as e:
                    print(e)
        except Exception as e:
            print("写入增量库报错：" + str(e))
            logger.errro(e)
            insertSyslog("error", "写入增量库报错Error：" + str(e), "")
        finally:
            pass
        print("数据开始写入增量库结束")

if __name__ == '__main__':
    run()
