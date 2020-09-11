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
    ElectricPrice, WaterSteamPrice, IncrementElectricTable, IncrementWaterTable, IncrementStreamTable, \
    IncrementStreamVolume
from tools.common import insert, delete, update
from dbset.database import constant
from dbset.log.BK2TLogger import logger, insertSyslog
from dbset.database.db_operate import engine,conn
pool = redis.ConnectionPool(host=constant.REDIS_HOST)
redis_conn = redis.Redis(connection_pool=pool, password=constant.REDIS_PASSWORD, decode_responses=True)
def run():
    runcount = 0
    failcount = 0
    redis_conn.hset(constant.REDIS_TABLENAME, "redis_incremeninsertdb_server_start",
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    while True:
        time.sleep(60)
        print("数据开始写入增量数据库")
        try:
            #水------------------------------------------------------------------------------------------
            water_value = list()
            elekeys = db_session.query(WaterEnergy).filter(WaterEnergy.IncrementFlag == "0",
                                                           WaterEnergy.WaterSum != "0.0").order_by(desc("CollectionDate")).all()
            for key in elekeys:
                proWsumValue = db_session.query(WaterEnergy.WaterSum).filter(WaterEnergy.ID == key.PrevID).first()
                if proWsumValue != None:
                    proWsumValue = proWsumValue[0]
                else:
                    proWsumValue = 0
                wsumvalue = abs(round(float(key.WaterSum) - float(proWsumValue), 2))
                if proWsumValue == 0:
                    wt = (wsumvalue, "水", key.ID,
                          key.PriceID, key.SumWUnit, key.EquipmnetID,
                          key.TagClassValue, key.CollectionDate, key.CollectionYear, key.CollectionMonth,
                          key.CollectionDay, str(key.CollectionDate)[0:13], key.AreaName, "0")
                    water_value.append(wt)
                else:
                    if float(key.WaterSum) < float(proWsumValue):#去除清零情况，统计累计值减小就认为是脏数据
                        if wsumvalue/float(proWsumValue) > 0.2:
                            wt = (wsumvalue, "水", key.ID,
                                  key.PriceID, key.SumWUnit, key.EquipmnetID,
                                  key.TagClassValue, key.CollectionDate, key.CollectionYear, key.CollectionMonth,
                                  key.CollectionDay, str(key.CollectionDate)[0:13], key.AreaName, "0")
                            water_value.append(wt)
                    else:
                        if wsumvalue/float(proWsumValue) < 0.8:
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
                conn.rollback()
                print(e)
            # 更新增量库原始数据库
            water_IDS = list()
            waterInitial = list()
            upwatskeys = db_session.query(IncrementWaterTable).filter(
                IncrementWaterTable.insertFlag == "0").order_by(desc("CollectionDate")).all()
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
                    conn.rollback()
                    print(e)
            #汽能插入-----------------------------------------------------------------------------------增量库
            steam_value = list()
            stekeys = db_session.query(SteamEnergy).filter(SteamEnergy.IncrementFlag == "0",
                                                           SteamEnergy.SumValue != "0.0").order_by(desc("CollectionDate")).all()
            for key in stekeys:
                proSumValue = db_session.query(SteamEnergy.SumValue).filter(SteamEnergy.ID == key.PrevID).first()
                if proSumValue != None:
                    proSumValue = proSumValue[0]
                else:
                    proSumValue = 0
                sumvalue = round(float(key.SumValue) - float(proSumValue), 2)

                if sumvalue < 0:
                    continue

                if proSumValue == 0:
                    ss = (sumvalue, "汽", key.ID,
                          key.PriceID, key.SumUnit, key.EquipmnetID,
                          key.TagClassValue, key.CollectionDate, key.CollectionYear, key.CollectionMonth,
                          key.CollectionDay, str(key.CollectionDate)[0:13], key.AreaName, "0")
                    steam_value.append(ss)
                else:
                    if float(key.SumValue) < float(proSumValue):#去除清零情况，统计累计值减小就认为是脏数据
                        if sumvalue/float(proSumValue) > 0.04:
                            ss = (sumvalue, "汽", key.ID,
                                  key.PriceID, key.SumUnit, key.EquipmnetID,
                                  key.TagClassValue, key.CollectionDate, key.CollectionYear, key.CollectionMonth,
                                  key.CollectionDay, str(key.CollectionDate)[0:13], key.AreaName, "0")
                            steam_value.append(ss)
                    else:
                        if sumvalue / float(proSumValue) < 0.8:#去除增长量过大的数据
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
                conn.rollback()
                print(e)
            #更新增量库原始数据库
            steam_IDS = list()
            steamInitial = list()
            upstekeys = db_session.query(IncrementStreamTable).filter(IncrementStreamTable.insertFlag == "0").order_by(desc("CollectionDate")).all()
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
                    conn.rollback()
                    print(e)
            #电能----------------------------------------------------------------------------------KU
            electric_value = list()
            elekeys = db_session.query(ElectricEnergy).filter(ElectricEnergy.IncrementFlag == "0", ElectricEnergy.ZGL != "0.0").order_by(desc("CollectionDate")).all()
            for key in elekeys:
                proZGLmValue = db_session.query(ElectricEnergy.ZGL).filter(ElectricEnergy.ID == key.PrevID).first()
                if proZGLmValue != None:
                    proZGLmValue = proZGLmValue[0]
                else:
                    proZGLmValue = 0
                ZGLvalue = abs(round(float(key.ZGL) - float(proZGLmValue), 2))
                if proZGLmValue == 0:
                    el = (ZGLvalue, "电", key.ID,
                          key.PriceID, key.Unit, key.EquipmnetID,
                          key.TagClassValue, key.CollectionDate, key.CollectionYear, key.CollectionMonth,
                          key.CollectionDay, str(key.CollectionDate)[0:13], key.AreaName, "0")
                    electric_value.append(el)
                else:
                    if float(key.ZGL) < float(proZGLmValue):#去除清零情况，统计累计值减小就认为是脏数据
                        if ZGLvalue/float(proZGLmValue) > 0.2:
                            el = (ZGLvalue, "电", key.ID,
                                  key.PriceID, key.Unit, key.EquipmnetID,
                                  key.TagClassValue, key.CollectionDate, key.CollectionYear, key.CollectionMonth,
                                  key.CollectionDay, str(key.CollectionDate)[0:13], key.AreaName, "0")
                            electric_value.append(el)
                    else:
                        if ZGLvalue/float(proZGLmValue) < 0.8:
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
                conn.rollback()
                print(e)
            # 更新增量库原始数据库
            electric_IDS = list()
            electricInitial = list()
            upeleskeys = db_session.query(IncrementElectricTable).filter(
                IncrementElectricTable.insertFlag == "0").order_by(desc("CollectionDate")).all()
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
                    conn.rollback()
                    print(e)

            runcount = runcount + 1
        except Exception as e:
            conn.rollback()
            print("写入增量库报错：" + str(e))
            insertSyslog("error", "写入增量库报错Error：" + str(e), "")
            failcount = failcount + 1
            redis_conn.hset(constant.REDIS_TABLENAME, "redis_incremeninsertdb_server_status", "执行失败")
        finally:
            pass
        print("数据开始写入增量库结束")
        redis_conn.hset(constant.REDIS_TABLENAME, "redis_incremeninsertdb_server_end",
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        redis_conn.hset(constant.REDIS_TABLENAME, "redis_incremeninsertdb_server_runcount", str(runcount))
        redis_conn.hset(constant.REDIS_TABLENAME, "redis_incremeninsertdb_server_failcount", str(failcount))
        redis_conn.hset(constant.REDIS_TABLENAME, "redis_incremeninsertdb_server_status", "执行成功")

if __name__ == '__main__':
    run()
