import redis
from flask import Blueprint, render_template, request, make_response, send_file
import json
import datetime
from sqlalchemy import desc
from dbset.database.db_operate import db_session, pool
from dbset.main.BSFramwork import AlchemyEncoder
from flask_login import login_required, logout_user, login_user, current_user, LoginManager
import calendar
from models.SystemManagement.core import RedisKey, ElectricEnergy, WaterEnergy, SteamEnergy, LimitTable, Equipment, \
    AreaTable, Unit, TagClassType, TagDetail, BatchMaintain
from models.SystemManagement.system import EarlyWarning, EarlyWarningLimitMaintain, WaterSteamBatchMaintain, \
    AreaTimeEnergyColour, ElectricProportion, PUIDMaintain, ElectricPrice, ElectricVolumeMaintain, WaterSteamPrice
from tools.common import insert, delete, update
from dbset.database import constant
from dbset.log.BK2TLogger import logger, insertSyslog
import datetime
import arrow
import time
import numpy as np
import pandas as pd
from io import BytesIO
from flask import Flask, send_file, make_response
import math
import models

energy = Blueprint('energy', __name__, template_folder='templates')

arro = arrow.now()
pool = redis.ConnectionPool(host=constant.REDIS_HOST)
redis_conn = redis.Redis(connection_pool=pool)


@energy.route('/energyRedisData')
def energyRedisData():
    return render_template('./energyRedisData.html')


@energy.route('/energyDataChart')
def energyDataChart():
    return render_template('./energyDataChart.html')


@energy.route('/energyAreaTable')
def energyAreaTable():
    return render_template('./energyAreaTable.html')


@energy.route('/costCenter')
def costCenter():
    return render_template('./costCenter.html')


# 器件管理
@energy.route('/DeviceManage')
def DeviceManage():
    return render_template('./DeviceManage.html')


# 价格管理
@energy.route('/PriceManage')
def PriceManage():
    return render_template('./PriceManage.html')


# 单位管理
@energy.route('/UnitManage')
def UnitManage():
    return render_template('./UnitManage.html')


from datetime import timedelta


def getWeekDaysByNum(m, n):  # 获取第几周到第几周每周的第一天和最后一天
    # 当前日期
    now = datetime.now().date()
    dayDict = {}
    for x in range(m, n + 1):
        # 前几周
        if x < 0:
            lDay = now - timedelta(days=now.weekday() + (7 * abs(x)))
        # 本周
        elif x == 0:
            lDay = now - timedelta(days=now.weekday())
        # 后几周
        else:
            lDay = now + timedelta(days=(7 - now.weekday()) + 7 * (x - 1))
        rDay = lDay + timedelta(days=6)
        dayDict[x] = [str(lDay), str(rDay)]
    return dayDict


def getMonthFirstDayAndLastDay(year, month):
    """
    :param year: 年份，默认是本年，可传int或str类型
    :param month: 月份，默认是本月，可传int或str类型
    :return: firstDay: 当月的第一天，datetime.date类型
              lastDay: 当月的最后一天，datetime.date类型
    """
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)

    # 获取当月的第一天
    firstDay = datetime.date(year=year, month=month, day=1)
    lastDay = datetime.date(year=year, month=month, day=monthRange)
    return firstDay, lastDay


def addzero(j):
    if j < 10:
        return "0" + str(j)
    else:
        return str(j)

def returnb(rod):
    if rod == None or rod == "" or rod == b'':
        return ""
    else:
        return rod.decode()

def accumulation(EnergyValues):
    eleY = 0.0
    for EnergyValue in EnergyValues:
        eleY = eleY + float(EnergyValue[0])
    return eleY


def strlastMonth(currmonth):
    curr = currmonth.split("-")
    str0 = curr[0]
    str1 = curr[1]
    if "0" in str1:
        str00 = str1[1]
    else:
        str00 = str1
    if str00 == "1":
        return str(int(str0) - 1) + "-" + "12"
    else:
        las = int(str00) - 1
        if las < 10:
            la = "0" + str(las)
        else:
            la = str(las)
        return str0 + "-" + la


def appendcur(cur, las):
    if cur is None:
        return 0.0
    else:
        cur = cur[0]
        if las is None:
            las = 0.0
        else:
            las = las[0]
        diff = round(float(cur) - float(las), 2)
        if diff < 0:
            return 0.0
        else:
            return round(diff, 2)


def curcutlas(cur, las, count, energy):
    if cur is None:
        return count
    else:
        cur = cur[0]
        if las is None:
            las = 0.0
        else:
            las = las[0]
        if energy == "水":
            cur = abs(float(cur))
            las = abs(float(las))
        diff = round(float(cur) - float(las), 2)
        if diff < 0:
            return count
        else:
            propor = db_session.query(ElectricProportion).filter(ElectricProportion.ProportionType == energy).first()
            if propor is not None:
                pro = float(propor.Proportion)
                return round(count + diff * pro, 2)


def energyStatistics(oc_list, StartTime, EndTime, energy):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy: 水，电 ，气
    :return:获取水电汽增量值
    '''
    propor = db_session.query(ElectricProportion).filter(ElectricProportion.ProportionType == energy).first()
    pro = float(propor.Proportion)
    if energy == "水":
        sql = "SELECT SUM(Cast(t.IncremenValue as float)) as count  FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    elif energy == "电":
        sql = "SELECT SUM(Cast(t.IncremenValue as float)) as count  FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.IncremenValue as float)) as count  FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    if len(re) > 0:
        if re[0][0] != 0.0 and re[0][0] != None:
            return round(float(re[0][0]) * pro, 2)
        else:
            return 0.0
    else:
        return 0.0

def energyStatisticsCost(oc_list, StartTime, EndTime, energy):
    '''
    获取某段时间水电汽的成本
    :param oc_list:
    :param StartTime:
    :param EndTime:
    :param energy:
    :return:
    '''
    propor = db_session.query(ElectricProportion).filter(ElectricProportion.ProportionType == energy).first()
    pro = float(propor.Proportion)
    if energy == "水":
        sql = "select SUM(Cast(t1.IncremenValue as float)) * Cast(t2.PriceValue as float) FROM [DB_MICS].[dbo].[IncrementWaterTable] t1 with (INDEX =IX_IncrementWaterTable) INNER JOIN [DB_MICS].[dbo].[WaterSteamPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                        1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue"
    elif energy == "电":
        sql = "select SUM(Cast(t1.IncremenValue as float)) * Cast(t2.PriceValue as float) FROM [DB_MICS].[dbo].[IncrementElectricTable] t1 with (INDEX =IX_IncrementElectricTable) INNER JOIN [DB_MICS].[dbo].[ElectricPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                        1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue"
    elif energy == "汽":
        sql = "select SUM(Cast(t1.IncremenValue as float)) * Cast(t2.PriceValue as float) FROM [DB_MICS].[dbo].[IncrementStreamTable] t1 with (INDEX =IX_IncrementStreamTable) INNER JOIN [DB_MICS].[dbo].[WaterSteamPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                        1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    if len(re) > 0:
        count = 0.0
        for i in re:
            count = count + float(i[0])
        return round(count * pro, 2)
    else:
        return 0.0

def energyStatisticsFlowSumWD(oc_list, StartTime, EndTime, energy):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy: 水，电 ，气
    :return:历史表的瞬时值、温度、体积
    '''
    propor = db_session.query(ElectricProportion).filter(ElectricProportion.ProportionType == energy).first()
    pro = float(propor.Proportion)
    if energy == "水":
        sql = "SELECT SUM(Cast(t.WaterFlow as float)) as WaterFlow,MAX(Cast(t.WaterSum as float)),MIN(Cast(t.WaterSum as float))  FROM [DB_MICS].[dbo].[WaterEnergy] t with (INDEX =IX_WaterEnergy)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    elif energy == "电":
        sql = "SELECT MAX(Cast(t.ZGL as float)),MIN(Cast(t.ZGL as float))  FROM [DB_MICS].[dbo].[ElectricEnergy] t with (INDEX =IX_ElectricEnergy)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.FlowValue as float)) as FlowValue,SUM(Cast(t.Volume as float)) as Volume,AVG(Cast(t.WD as float)) AS WD,MAX(Cast(t.SumValue as float)),MIN(Cast(t.SumValue as float))  FROM [DB_MICS].[dbo].[SteamEnergy] t with (INDEX =IX_SteamEnergy)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    return re

def energyStatisticshour(oc_list, StartTime, EndTime, energy):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy: 水，电 ，气
    :return:获取水电汽增量值以collecthour分组
    '''
    if energy == "水":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionHour FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionHour order by t.CollectionHour"
    elif energy == "电":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionHour  FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionHour order by t.CollectionHour"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionHour  FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionHour order by t.CollectionHour"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    return re

def energyStatisticsday(oc_list, StartTime, EndTime, energy):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy: 水，电 ，气
    :return:获取水电汽增量值以collectday分组
    '''
    if energy == "水":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionDay FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionDay order by t.CollectionDay"
    elif energy == "电":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionDay  FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionDay order by t.CollectionDay"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionDay  FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionDay order by t.CollectionDay"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    return re
def energyStatisticsmonth(oc_list, StartTime, EndTime, energy):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy: 水，电 ，气
    :return:获取水电汽增量值以CollectionMonth分组
    '''
    if energy == "水":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionMonth FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionMonth order by t.CollectionMonth"
    elif energy == "电":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionMonth  FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionMonth order by t.CollectionMonth"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionMonth  FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionMonth order by t.CollectionMonth"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    return re
def energyStatisticsyear(oc_list, StartTime, EndTime, energy):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy: 水，电 ，气
    :return:获取水电汽增量值以CollectionYear分组
    '''
    if energy == "水":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionYear FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionYear order by t.CollectionYear"
    elif energy == "电":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionYear  FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionYear order by t.CollectionYear"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionYear  FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionYear order by t.CollectionYear"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    return re

def energyStatisticsyearde(StartTime, EndTime, energy):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy: 水，电 ，气
    :return:获取水电汽增量值
    '''
    propor = db_session.query(ElectricProportion).filter(ElectricProportion.ProportionType == energy).first()
    pro = float(propor.Proportion)
    if energy == "水":
        sql = "SELECT SUM(Cast(t.IncremenValue as float)) as count  FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    elif energy == "电":
        sql = "SELECT SUM(Cast(t.IncremenValue as float)) as count  FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable)  WHERE t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.IncremenValue as float)) as count  FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable)  WHERE t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    if len(re) > 0:
        if re[0][0] != 0.0 and re[0][0] != None:
            return round(float(re[0][0]) * pro, 2)
        else:
            return 0.0
    else:
        return 0.0

def energyStatisticsbyarea(StartTime, EndTime, energy):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy: 水，电 ，气
    :return:通过区域分组获取水电汽增量值
    '''
    if energy == "水":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.AreaName  FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE  t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.AreaName"
    elif energy == "电":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.AreaName  FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable)  WHERE t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.AreaName"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.AreaName  FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable)  WHERE t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.AreaName"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    return re
def energyselect(data):
    if request.method == 'GET':
        try:
            dir = {}
            currentyear = datetime.datetime.now().year
            currentmonth = datetime.datetime.now().month
            currentday = datetime.datetime.now().day
            data = request.values
            EnergyClass = data.get("EnergyClass")
            ModelFlag = data.get("ModelFlag")
            TimeClass = data.get("TimeClass")
            if ModelFlag == "能耗预览":
                dir_list = []
                dir_month_list = []
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()
                oc_list = []
                for oc in oclass:
                    oc_list.append(oc.TagClassValue)
                compareday = data.get("CompareDate")
                comparehour = str(compareday) + " 23:59:59"
                lastcomparehour = str(compareday) + " 00:00:00"
                curr = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(
                    int(currentday)) + " 23:59:59"
                last = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(
                    int(currentday)) + " 00:00:00"
                recurr = energyStatisticshour(oc_list, last, curr, EnergyClass)
                recomper = energyStatisticshour(oc_list, lastcomparehour, comparehour, EnergyClass)
                dictcurr = {letter: score for score, letters in recurr for letter in letters.split(",")}
                dictpre  = {letter: score for score, letters in recomper for letter in letters.split(",")}
                for myHour in constant.myHours:
                    scurrtime = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(int(currentday)) + " " + myHour
                    spretime = compareday + " " + myHour
                    dir_list_dict = {}
                    dir_list_dict["时间"] = scurrtime
                    currcount = 0
                    comparecount = 0
                    if scurrtime in dictcurr.keys():
                        currcount = round(float(dictcurr[scurrtime]), 2)
                    if spretime in dictpre.keys():
                        comparecount = round(float(dictpre[spretime]), 2)
                    dir_list_dict["今日能耗"] = currcount
                    dir_list_dict["对比日能耗"] = comparecount
                    dir_list.append(dir_list_dict)
                fistendday = getMonthFirstDayAndLastDay(currentyear, currentmonth)
                lastfistendday = getMonthFirstDayAndLastDay(strlastMonth(str(currentyear) + "-" + addzero(int(currentmonth)))[0:4],
                                                   strlastMonth(str(currentyear) + "-" + addzero(int(currentmonth)))[5:7])
                recurrdays = energyStatisticsday(oc_list, fistendday[0].strftime('%Y-%m-%d %H:%M:%S'), fistendday[1].strftime('%Y-%m-%d %H:%M:%S'), EnergyClass)
                recomperdays = energyStatisticsday(oc_list, lastfistendday[0].strftime('%Y-%m-%d %H:%M:%S'), lastfistendday[1].strftime('%Y-%m-%d %H:%M:%S'), EnergyClass)
                dictrecurrdays = {letter: score for score, letters in recurrdays for letter in letters.split(",")}
                dictrecomperdays = {letter: score for score, letters in recomperdays for letter in letters.split(",")}
                for myday in constant.mydays:
                    mycurrday = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + myday
                    mycompareday = strlastMonth(mycurrday[0:7]) + "-"+ myday
                    dirmonth_list_dict = {}
                    dirmonth_list_dict["日期"] = mycurrday
                    if mycurrday in dictrecurrdays.keys():
                        dirmonth_list_dict["本月能耗"] = round(float(dictrecurrdays[mycurrday]), 2)
                    else:
                        dirmonth_list_dict["本月能耗"] = 0
                    if mycompareday in dictrecomperdays.keys():
                        dirmonth_list_dict["上月能耗"] = round(float(dictrecomperdays[mycompareday]), 2)
                    else:
                        dirmonth_list_dict["上月能耗"] = 0
                    dir_month_list.append(dirmonth_list_dict)
                dir["compareTodayRow"] = dir_list
                dir["lastMonthRow"] = dir_month_list
            elif ModelFlag == "在线检测情况":
                # pipe = redis_conn.pipeline(transaction=False)
                oclass = db_session.query(TagDetail).filter().all()
                watstatust = 0
                elestatust = 0
                stestatust = 0
                watstatuss = 0
                elestatuss = 0
                stestatuss = 0
                for i in oclass:
                    Tag = i.TagClassValue[0:1]
                    ret = returnb(redis_conn.hget("run_status", i.TagClassValue))
                    if Tag == "E":
                        elestatust = elestatust + 1
                        if ret == "1":
                            elestatuss = elestatuss + 1
                    elif Tag == "S":
                        stestatust = stestatust + 1
                        if ret == "1":
                            stestatuss = stestatuss + 1
                    elif Tag == "W":
                        watstatust = watstatust + 1
                        if ret == "1":
                            watstatuss = watstatuss + 1
                data_list = []
                data_list.append({"name": "电表", "online": elestatuss, "rate": int(100 * (elestatuss/elestatust)), "total":elestatust})
                data_list.append({"name": "水表", "online": watstatuss, "rate": int(100 * (watstatuss / watstatust)), "total":watstatust})
                data_list.append({"name": "汽表", "online": stestatuss, "rate": int(100 * (stestatuss / stestatust)), "total":stestatust})
                return json.dumps(data_list, cls=AlchemyEncoder, ensure_ascii=False)
            elif ModelFlag == "实时预警":
                oclass = db_session.query(EarlyWarning).filter().order_by(desc("WarningDate")).all()
                dir["data"] = oclass
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            insertSyslog("error", "能耗查询报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)


@energy.route('/areaTimeEnergy', methods=['POST', 'GET'])
def areaTimeEnergy():
    '''
    能耗看板的区域时段
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            currentyear = datetime.datetime.now().year
            currentmonth = datetime.datetime.now().month
            currentday = datetime.datetime.now().day
            currenthour = datetime.datetime.now().hour
            EnergyClass = data.get("energyType")
            compareday = data.get("CompareDate")
            AreaNames = db_session.query(AreaTable.AreaName).filter().all()
            araeY_list = []
            wit = db_session.query(AreaTimeEnergyColour).filter(
                AreaTimeEnergyColour.ColourName == "无").first()
            wu = wit.ColourValue
            for AreaName in AreaNames:
                valuelist = []
                value_dirc = {}
                oclass = db_session.query(TagDetail).filter(TagDetail.AreaName == AreaName[0],
                                                            TagDetail.EnergyClass == EnergyClass).all()
                oc_list = []
                for oc in oclass:
                    oc_list.append(oc.TagClassValue)
                if len(oc_list) > 0:
                    colourclass = db_session.query(AreaTimeEnergyColour).filter(
                        AreaTimeEnergyColour.AreaName == AreaName[0]).all()
                    stop = ""
                    high = ""
                    middle = ""
                    low = ""
                    stopColourValue = ""
                    highColourValue = ""
                    middleColourValue = ""
                    lowColourValue = ""
                    for co in colourclass:
                        if co.ColourName == "停":
                            stop = co.ColourSum
                            stopColourValue = co.ColourValue
                        elif co.ColourName == "高":
                            high = co.ColourSum
                            highColourValue = co.ColourValue
                        elif co.ColourName == "中":
                            middle = co.ColourSum
                            middleColourValue = co.ColourValue
                        elif co.ColourName == "低":
                            low = co.ColourSum
                            lowColourValue = co.ColourValue
                    colour = ""
                    curr = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(
                        int(currentday)) + " 23:59:59"
                    last = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(
                        int(currentday)) + " 00:00:00"
                    recurr = energyStatisticshour(oc_list, last, curr, EnergyClass)
                    recomper = energyStatisticshour(oc_list, compareday+" 00:00:00", compareday+" 23:59:59", EnergyClass)
                    dictcurr = {letter: score for score, letters in recurr for letter in letters.split(",")}
                    dictpre = {letter: score for score, letters in recomper for letter in letters.split(",")}
                    for myHour in constant.myHours:
                        scurrtime = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(
                            int(currentday)) + " " + myHour
                        vlaue = 0
                        if compareday != None and compareday != "":
                            spretime = compareday + " " + myHour
                            if spretime in dictpre.keys():
                                vlaue = round(float(dictpre[spretime]), 2)
                        else:
                            if scurrtime in dictcurr.keys():
                                vlaue = round(float(dictcurr[scurrtime]), 2)
                        dict_valuelist = {}
                        dict_valuelist["date"] = myHour
                        if vlaue == None or vlaue < 0:
                            colour = colour + "," + wu
                        elif 0 <= vlaue <= float(stop):
                            colour = colour + "," + stopColourValue
                        elif float(low) <= vlaue < float(middle):
                            colour = colour + "," + lowColourValue
                        elif float(middle) <= vlaue < float(high):
                            colour = colour + "," + middleColourValue
                        elif vlaue > float(high) or vlaue == float(high):
                            colour = colour + "," + highColourValue
                        dict_valuelist["value"] = round(vlaue, 2)
                        valuelist.append(dict_valuelist)
                    value_dirc["AreaName"] = AreaName[0]
                    value_dirc["valuelist"] = valuelist
                    value_dirc["backgroundColor"] = "-webkit-linear-gradient(left," + colour[1:] + ")"
                    araeY_list.append(value_dirc)
                else:
                    value_dirc["AreaName"] = AreaName[0]
                    value_dirc["valuelist"] = []
                    value_dirc["backgroundColor"] = "-webkit-linear-gradient(left," + wu + ")"
                    araeY_list.append(value_dirc)
            return json.dumps(araeY_list, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "区域时段能耗查询报错Error：" + str(e), current_user.Name)


@energy.route('/trendChart', methods=['POST', 'GET'])
def trendChart():
    '''
    趋势图
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            currentyear = datetime.datetime.now().year
            currentmonth = datetime.datetime.now().month
            currentday = datetime.datetime.now().day
            currenthour = datetime.datetime.now().hour
            EnergyClass = data.get("energyType")
            AreaNames = db_session.query(AreaTable.AreaName).filter().all()
            dir = {}
            diarea = {}
            araeY_list = []
            TimeClass = data.get("TimeClass")
            if TimeClass == "本周":
                re = getWeekDaysByNum(0, 0)
                first_week_day = re[0][0]
                end_week_day = re[0][1]
                bats = db_session.query(BatchMaintain).filter(
                    BatchMaintain.ProductionDate.between(first_week_day, end_week_day)).all()
                countw = 0.0
                counte = 0.0
                countbat = 0
                for bat in bats:
                    countw = countw + bat.WaterConsumption
                    counte = counte + bat.ElectricConsumption
                    countbat = countbat + 1
            elif TimeClass == "本月":
                currmonth = str(currentyear) + "-" + addzero(int(currentmonth))
                BatchMaintain
                WaterSteamBatchMaintain
            elif TimeClass == "本年":
                curryear = str(currentyear)
                BatchMaintain
                WaterSteamBatchMaintain
            dir["countw"] = countw
            dir["counte"] = counte
            dir["countbat"] = countbat
            return json.dumps(araeY_list, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "区域时段能耗查询报错Error：" + str(e), current_user.Name)

class Statistic():
    def __init__(self, Area, Water, Electric, Steam, CollectDate):
        self.Area = Area
        self.Water = Water
        self.Electric = Electric
        self.Steam = Steam
        self.CollectDate = CollectDate


@energy.route('/exceloutstatistic', methods=['POST', 'GET'])
def exceloutstatistic():
    '''
    导出统计数据
    :return:
    '''
    data = request.values
    if request.method == 'GET':
        StartTime = data.get("StartTime")
        EndTime = data.get("EndTime")
        EnergyClass = data.get("EnergyClass")
        output = exportxstatistic(StartTime, EndTime, EnergyClass)
        resp = make_response(output.getvalue())
        resp.headers["Content-Disposition"] = "attachment; filename=consumption.xlsx"
        resp.headers['Content-Type'] = 'application/x-xlsx'
        return resp


def exportxstatistic(StartTime, EndTime, EnergyClass):
    # 创建数据流
    output = BytesIO()
    # 创建excel work book
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    # 创建excel sheet
    worksheet = workbook.add_worksheet('sheet1')

    cell_format = workbook.add_format({
        'font_size': 18,
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#006633'})
    worksheet.set_column('A:F', 24)
    col = 0
    row = 1
    # 写入列名
    columns = ['区域', '能耗表', '能耗值', '单位', '统计开始时间', '统计截止时间']
    for item in columns:
        worksheet.write(0, col, item, cell_format)
        col += 1
    AreaNames = db_session.query(AreaTable).filter().all()
    oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass ==EnergyClass).all()
    unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == EnergyClass).first()[0]
    i = 0
    for oc in oclass:
        oc_list = []
        Tag = oc.TagClassValue[0:1]
        if Tag == "E":
            oc_list.append(oc.TagClassValue)
        elif Tag == "W":
            oc_list.append(oc.TagClassValue)
        elif Tag == "S":
            oc_list.append(oc.TagClassValue)
        if len(oc_list) > 0:
            count = energyStatistics(oc_list, StartTime, EndTime, EnergyClass)
        else:
            count = 0.0
        for cum in columns:
            if cum == '区域':
                worksheet.write(i + 1, columns.index(cum), oc.AreaName)
            if cum == '能耗表':
                worksheet.write(i + 1, columns.index(cum), oc.FEFportIP)
            if cum == '能耗值':
                worksheet.write(i + 1, columns.index(cum), str(count))
            if cum == '单位':
                worksheet.write(i + 1, columns.index(cum), unit)
            if cum == '统计开始时间':
                worksheet.write(i + 1, columns.index(cum), StartTime + "0:00")
            if cum == '统计截止时间':
                worksheet.write(i + 1, columns.index(cum), EndTime + "0:00")
        i = i + 1
    writer.close()
    output.seek(0)
    return output


@energy.route('/excelout', methods=['POST', 'GET'])
def excelout():
    '''
    导出原始数据
    :return:
    '''
    data = request.values
    if request.method == 'GET':
        Area = data.get("Area")
        EnergyClass = data.get("EnergyClass")
        StartTime = data.get("StartTime")
        EndTime = data.get("EndTime")
        output = exportx(Area, EnergyClass, StartTime, EndTime)
        resp = make_response(output.getvalue())
        resp.headers["Content-Disposition"] = "attachment; filename=testing.xlsx"
        resp.headers['Content-Type'] = 'application/x-xlsx'
        return resp


def exportx(Area, EnergyClass,  StartTime, EndTime):
    # 创建数据流
    output = BytesIO()
    # 创建excel work book
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    # 创建excel sheet
    worksheet = workbook.add_worksheet('sheet1')
    # cell 样式
    cell_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#006633'})

    col = 0
    row = 1
    tag = []
    if Area != "" and Area !=None:
        tas = db_session.query(TagDetail).filter(TagDetail.AreaName == Area).all()
    else:
        tas = db_session.query(TagDetail).filter().all()
    for ta in tas:
        tag.append(ta.TagClassValue)
    # 写入列名
    if EnergyClass == "水":
        columns = ['单位', '仪表ID', '价格ID', '采集点', '采集时间', '采集年', '采集月', '采集天', '瞬时流量', '累计流量']
        oclass = db_session.query(WaterEnergy).filter(WaterEnergy.TagClassValue.in_(tag),
                                                      WaterEnergy.CollectionDate.between(StartTime, EndTime)).all()
    elif EnergyClass == "电":
        columns = ['单位', '仪表ID', '价格ID', '采集点', '采集时间', '采集年', '采集月', '采集天', '总功率', 'A相电压', 'A相电流', 'B相电压', 'B相电流',
                   'C相电压', 'C相电压']
        oclass = db_session.query(ElectricEnergy).filter(ElectricEnergy.TagClassValue.in_(tag),
                                                         ElectricEnergy.CollectionDate.between(StartTime, EndTime)).all()
    else:
        columns = ['蒸汽值', '单位', '仪表ID', '价格ID', '采集点', '采集时间', '采集年', '采集月', '采集天', '温度', '蒸汽瞬时值', '蒸汽累计值']
        oclass = db_session.query(SteamEnergy).filter(SteamEnergy.TagClassValue.in_(tag),
                                                      SteamEnergy.CollectionDate.between(StartTime, EndTime)).all()
    for item in columns:
        worksheet.write(0, col, item, cell_format)
        col += 1
    # 写入数据
    for i in range(1, len(oclass)):
        if EnergyClass == "水":
            for cum in columns:
                if cum == '单位':
                    worksheet.write(i, columns.index(cum), oclass[i].Unit)
                if cum == '仪表ID':
                    worksheet.write(i, columns.index(cum), oclass[i].EquipmnetID)
                if cum == '价格ID':
                    worksheet.write(i, columns.index(cum), oclass[i].PriceID)
                if cum == '采集点':
                    worksheet.write(i, columns.index(cum), oclass[i].TagClassValue)
                if cum == '采集时间':
                    worksheet.write(i, columns.index(cum), oclass[i].CollectionDate)
                if cum == '采集年':
                    worksheet.write(i, columns.index(cum), oclass[i].CollectionYear)
                if cum == '采集月':
                    worksheet.write(i, columns.index(cum), oclass[i].CollectionMonth)
                if cum == '采集天':
                    worksheet.write(i, columns.index(cum), oclass[i].CollectionDay)
                if cum == '瞬时流量':
                    worksheet.write(i, columns.index(cum), oclass[i].WaterFlow)
                if cum == '累计流量':
                    worksheet.write(i, columns.index(cum), oclass[i].WaterSum)
        elif EnergyClass == "电":
            for cum in columns:
                if cum == '单位':
                    worksheet.write(i, columns.index(cum), oclass[i].Unit)
                if cum == '仪表ID':
                    worksheet.write(i, columns.index(cum), oclass[i].EquipmnetID)
                if cum == '价格ID':
                    worksheet.write(i, columns.index(cum), oclass[i].PriceID)
                if cum == '采集点':
                    worksheet.write(i, columns.index(cum), oclass[i].TagClassValue)
                if cum == '采集时间':
                    worksheet.write(i, columns.index(cum), oclass[i].CollectionDate)
                if cum == '采集年':
                    worksheet.write(i, columns.index(cum), oclass[i].CollectionYear)
                if cum == '采集月':
                    worksheet.write(i, columns.index(cum), oclass[i].CollectionMonth)
                if cum == '采集天':
                    worksheet.write(i, columns.index(cum), oclass[i].CollectionDay)
                if cum == '总功率':
                    worksheet.write(i, columns.index(cum), oclass[i].ZGL)
                if cum == 'A相电压':
                    worksheet.write(i, columns.index(cum), oclass[i].AU)
                if cum == 'A相电流':
                    worksheet.write(i, columns.index(cum), oclass[i].AI)
                if cum == 'B相电压':
                    worksheet.write(i, columns.index(cum), oclass[i].BU)
                if cum == 'B相电流':
                    worksheet.write(i, columns.index(cum), oclass[i].BI)
                if cum == 'C相电压':
                    worksheet.write(i, columns.index(cum), oclass[i].CU)
                if cum == 'C相电压':
                    worksheet.write(i, columns.index(cum), oclass[i].CI)
        elif EnergyClass == "汽":
            for cum in columns:
                if cum == '蒸汽值':
                    worksheet.write(i, columns.index(cum), oclass[i].SteamValue)
                if cum == '单位':
                    worksheet.write(i, columns.index(cum), oclass[i].Unit)
                if cum == '仪表ID':
                    worksheet.write(i, columns.index(cum), oclass[i].EquipmnetID)
                if cum == '价格ID':
                    worksheet.write(i, columns.index(cum), oclass[i].PriceID)
                if cum == '采集点':
                    worksheet.write(i, columns.index(cum), oclass[i].TagClassValue)
                if cum == '采集时间':
                    worksheet.write(i, columns.index(cum), oclass[i].CollectionDate)
                if cum == '采集年':
                    worksheet.write(i, columns.index(cum), oclass[i].CollectionYear)
                if cum == '采集月':
                    worksheet.write(i, columns.index(cum), oclass[i].CollectionMonth)
                if cum == '采集天':
                    worksheet.write(i, columns.index(cum), oclass[i].CollectionDay)
                if cum == '温度':
                    worksheet.write(i, columns.index(cum), oclass[i].WD)
                if cum == '蒸汽瞬时值':
                    worksheet.write(i, columns.index(cum), oclass[i].FlowValue)
                if cum == '蒸汽累计值':
                    worksheet.write(i, columns.index(cum), oclass[i].SumValue)
    writer.close()
    output.seek(0)
    return output

@energy.route('/trendlookboard', methods=['POST', 'GET'])
def trendlookboard():
    '''
    能耗看板的能耗趋势
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            EnergyClass = data.get("EnergyClass")
            CompareTime = data.get("CompareTime")
            oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()
            oc_list = []
            for oc in oclass:
                oc_list.append(oc.TagClassValue)
            rows_list = []
            recomper = energyStatisticshour(oc_list, CompareTime+" 00:00:00", CompareTime+" 23:59:59", EnergyClass)
            dictpre = {letter: score for score, letters in recomper for letter in letters.split(",")}
            for myHour in constant.myHours:
                spretime = CompareTime + " " + myHour
                dir_rows = {}
                dir_rows["时间"] = spretime
                comparecount = 0
                if spretime in dictpre.keys():
                    comparecount = round(float(dictpre[spretime]), 2)
                dir_rows["能耗量"] = comparecount
                rows_list.append(dir_rows)
            dir["rows"] = rows_list
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "能耗看板的能耗趋势查询报错Error：" + str(e), current_user.Name)

@energy.route('/areatimeenergycount', methods=['POST', 'GET'])
def areatimeenergycount():
    '''
    区域时段能耗
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            EnergyClass = data.get("EnergyClass")
            CompareTime = data.get("CompareTime")
            start = CompareTime + " 00:00:00"
            end = CompareTime + " 23:59:59"
            areas = db_session.query(AreaTable).filter().all()
            rows_list = []
            for area in areas:
                AreaName = area.AreaName
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass, TagDetail.AreaName == AreaName).all()
                oc_list = []
                for oc in oclass:
                    oc_list.append(oc.TagClassValue)
                dir_rows = {}
                dir_rows["区域"] = AreaName
                if len(oc_list) > 0:
                    count = energyStatistics(oc_list, start, end, EnergyClass)
                else:
                    count = 0.0
                dir_rows["能耗量"] = count
                rows_list.append(dir_rows)
            if len(rows_list)>0:
                array = sorted(rows_list, key=lambda obj: -obj["能耗量"])
            dir["rows"] = array
            unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == EnergyClass).first()[0]
            dir["unit"] = unit
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "区域时段能耗查询报错Error：" + str(e), current_user.Name)

@energy.route('/createzyplanzytaskrelease', methods=['POST', 'GET'])
def createzyplanzytaskrelease():
    '''
    创建计划任务
    :return:
    '''
    if request.method == 'POST':
        data = request.values
        try:
            PlanNum = data.get("PlanNum")
            BatchID = data.get("BatchID")
            BrandName = data.get('BrandName')
            WaterConsumption = data.get("WaterConsumption")
            SteamConsumption = data.get("SteamConsumption")
            ProductionDate = data.get('ProductionDate')
            CreateDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            PlanQuantity = data.get("PlanQuantity")
            PlanCreate = ctrlPlan('PlanCreate')
            re = PlanCreate.createBatchMaintain(PlanNum, BatchID, BrandName, PlanQuantity, WaterConsumption, SteamConsumption, CreateDate, ProductionDate, StartTime, EndTime)
            if re==True:
                return json.dumps("OK", cls=AlchemyEncoder, ensure_ascii=False)
            else:
                return json.dumps("创建计划任务失败!", cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "创建计划任务报错Error：" + str(e), current_user.Name)

class ctrlPlan:
    def __init__(self, name):
        self.name = name

    def createBatchMaintain(self, PlanNum, BatchID, BrandName, PlanQuantity, WaterConsumption, SteamConsumption, CreateDate, ProductionDate, StartTime, EndTime):
        bReturn = True
        try:
            db_session.add(
                models.SystemManagement.core.BatchMaintain(
                    PlanNum=PlanNum,
                    BatchID=BatchID,
                    BrandName=BrandName,
                    PlanQuantity=PlanQuantity,
                    WaterConsumption=WaterConsumption,
                    SteamConsumption=SteamConsumption,
                    CreateDate=CreateDate,
                    ProductionDate=ProductionDate,
                    StartTime=StartTime,
                    EndTime=EndTime))
            db_session.commit()
            puids = db_session.query(PUIDMaintain).filter(PUIDMaintain.BrandName == BrandName).all()
            if puids:
                for puid in puids:
                    bReturn = self.BatchMaintainTask(puid.PUIDName, PlanNum, BatchID, BrandName, PlanQuantity, WaterConsumption, SteamConsumption, CreateDate, ProductionDate, StartTime, EndTime)
                    if bReturn == False:
                        return False
            return bReturn
        except Exception as e:
            db_session.rollback()
            print(e)
            insertSyslog("error", "创建计划报错Error：" + str(e), current_user.Name)
            return False


    def BatchMaintainTask(self, PuidName, PlanNum, BatchID, BrandName, PlanQuantity, WaterConsumption, SteamConsumption, CreateDate, ProductionDate, StartTime, EndTime):
        bReturn = True;
        try:
            db_session.add(
                models.SystemManagement.system.BatchMaintainTask(
                    PuidName=PuidName,
                    PlanNum=PlanNum,
                    BatchID=BatchID,
                    BrandName=BrandName,
                    PlanQuantity=PlanQuantity,
                    WaterConsumption=WaterConsumption,
                    SteamConsumption=SteamConsumption,
                    CreateDate=CreateDate,
                    ProductionDate=ProductionDate,
                    StartTime=StartTime,
                    EndTime=EndTime))
            db_session.commit()
            return bReturn
        except Exception as e:
            db_session.rollback()
            print(e)
            insertSyslog("error", "创建任务报错Error：" + str(e), current_user.Name)
            return  False

@energy.route('/batchMaintainEnergy', methods=['POST', 'GET'])
def batchMaintainEnergy():
    '''
    单位批次能耗查询
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            AreaName = data.get("AreaName")
            batinfos = db_session.query(BatchMaintain).filter(BatchMaintain.ProductionDate.between(StartTime,EndTime), BatchMaintain.AreaName == AreaName).all()
            brandSum = db_session.query(BatchMaintain.BrandName).distinct().filter(BatchMaintain.ProductionDate.between(StartTime, EndTime),
                                                              BatchMaintain.AreaName == AreaName).count()
            batchcont = 0
            waterCon = 0
            steamCon = 0
            for bat in batinfos:
                waterCon = waterCon + float(bat.WaterConsumption)
                steamCon = steamCon + float(bat.SteamConsumption)
                batchcont = batchcont + 1
            waterEveryBatch = 0
            if waterCon != 0:
                waterEveryBatch = waterCon/batchcont
            steamEveryBatch = 0
            if steamCon != 0:
                steamEveryBatch = steamCon / batchcont
            if waterEveryBatch != 0:
                waterEveryBatch = round(waterEveryBatch,2)
            if waterCon != 0:
                waterCon = round(waterCon,2)
            if steamCon != 0:
                steamCon = round(steamCon,2)
            if steamEveryBatch != 0:
                steamEveryBatch = round(steamEveryBatch,2)
            dir["typeNum"] = brandSum
            dir["batchCount"] = batchcont
            dir["waterCon"] = str(waterCon)
            dir["steamCon"] = str(steamCon)
            dir["waterEveryBatch"] = str(waterEveryBatch)
            dir["steamEveryBatch"] = str(steamEveryBatch)
            dir["waterUnit"] = "t"
            dir["steamUnit"] = "t"
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "单位批次能耗查询报错Error：" + str(e), current_user.Name)

@energy.route('/batchMaintainEnergyEcharts', methods=['POST', 'GET'])
def batchMaintainEnergyEcharts():
    '''
    单位批次能耗柱状图
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            TimeClass = data.get("TimeClass")
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            EnergyClass = data.get("EnergyClass")
            AreaName = data.get("AreaName")
            if AreaName == None or AreaName == "":
                batinfos = db_session.query(BatchMaintain).filter(
                    BatchMaintain.EndTime.between(StartTime, EndTime)).all()
            else:
                batinfos = db_session.query(BatchMaintain).filter(
                    BatchMaintain.EndTime.between(StartTime, EndTime), BatchMaintain.AreaName == AreaName).all()
            dir_list = []
            if TimeClass == "年":
                nowm = int(EndTime[5:7])+1
                for i in range(1,nowm):
                    re = getMonthFirstDayAndLastDay(StartTime[0:4], i)
                    if AreaName == None or AreaName == "":
                        batyears = db_session.query(BatchMaintain).filter(
                            BatchMaintain.EndTime.between(datetime.datetime.strftime(re[0], "%Y-%m-%d")+" 00:00:00", datetime.datetime.strftime(re[1], "%Y-%m-%d")+" 00:00:00"+" 23:59:59")).all()
                    else:
                        batyears = db_session.query(BatchMaintain).filter(
                            BatchMaintain.EndTime.between(datetime.datetime.strftime(re[0], "%Y-%m-%d")+" 00:00:00"+" 00:00:00", datetime.datetime.strftime(re[1], "%Y-%m-%d")+" 23:59:59"), BatchMaintain.AreaName == AreaName).all()
                    waterSum = 0.0
                    steamSum = 0.0
                    for baty in batyears:
                        if baty.WaterConsumption != None and baty.WaterConsumption != "":
                            waterSum = waterSum + float(baty.WaterConsumption)
                        if baty.SteamConsumption != None and baty.SteamConsumption != "":
                            steamSum = steamSum + float(baty.SteamConsumption)
                    bat_energy = {}
                    bat_energy["日期"] = StartTime[0:4] +"-"+ addzero(i)
                    if EnergyClass == "水":
                        bat_energy["批次能耗量"] = round(waterSum, 2)
                        dir_list.append(bat_energy)
                    elif EnergyClass == "汽":
                        bat_energy["批次能耗量"] = round(steamSum, 2)
                        dir_list.append(bat_energy)
            else:
                for bat in batinfos:
                    bat_dir = {}
                    bat_dir["批次"] = bat.BatchID
                    if EnergyClass == "水":
                        energy = bat.WaterConsumption
                    elif EnergyClass == "汽":
                        energy = bat.SteamConsumption
                    bat_dir["批次能耗量"] = round(float(energy), 2)
                    dir_list.append(bat_dir)
            dir["row"] = dir_list
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "单位批次能耗单位批次能耗柱状图查询报错Error：" + str(e), current_user.Name)

@energy.route('/batchMaintainExcelSelect', methods=['POST', 'GET'])
def batchMaintainExcelSelect():
    '''
    单位批次能耗报表查询
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            pages = int(data.get("offset"))  # 页数
            rowsnumber = int(data.get("limit"))  # 行数
            inipage = pages * rowsnumber + 0  # 起始页
            endpage = pages * rowsnumber + rowsnumber  # 截止页
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            AreaName = data.get("AreaName")
            BrandName = data.get("BrandName")
            if AreaName == "" and BrandName == "":
                batinfos = db_session.query(BatchMaintain).filter(
                    BatchMaintain.ProductionDate.between(StartTime, EndTime)).all()[inipage:endpage]
                count = db_session.query(BatchMaintain).filter(BatchMaintain.ProductionDate.between(StartTime, EndTime)).count()
            elif AreaName != "" and BrandName == "":
                batinfos = db_session.query(BatchMaintain).filter(
                    BatchMaintain.ProductionDate.between(StartTime, EndTime), BatchMaintain.AreaName == AreaName).all()[inipage:endpage]
                count = db_session.query(BatchMaintain).filter(BatchMaintain.ProductionDate.between(StartTime, EndTime),
                                                               BatchMaintain.AreaName == AreaName).count()
            elif AreaName == "" and BrandName != "":
                batinfos = db_session.query(BatchMaintain).filter(
                    BatchMaintain.ProductionDate.between(StartTime, EndTime),
                    BatchMaintain.BrandName == BrandName).all()[inipage:endpage]
                count = db_session.query(BatchMaintain).filter(BatchMaintain.ProductionDate.between(StartTime, EndTime),
                                                               BatchMaintain.BrandName == BrandName).count()
            else:
                batinfos = db_session.query(BatchMaintain).filter(BatchMaintain.ProductionDate.between(StartTime,EndTime), BatchMaintain.AreaName == AreaName, BatchMaintain.BrandName == BrandName).all()[inipage:endpage]
                count = db_session.query(BatchMaintain).filter(BatchMaintain.ProductionDate.between(StartTime,EndTime), BatchMaintain.AreaName == AreaName, BatchMaintain.BrandName == BrandName).count()
            jsonbatinfos = json.dumps(batinfos, cls=AlchemyEncoder, ensure_ascii=False)
            return '{"total"' + ":" + str(count) + ',"rows"' + ":\n" + jsonbatinfos + "}"
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "单位批次能耗报表查询报错Error：" + str(e), current_user.Name)

@energy.route('/todayAreaRingCharts', methods=['POST', 'GET'])
def todayAreaRingCharts():
    '''
    实时数据柱状图环形图
    return:
    '''
    if request.method == 'GET':
        try:
            dir = {}
            currentdayend = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            currentdayestart = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")[0:10]+" 00:00:00"
            araes = db_session.query(AreaTable).filter().all()
            water_areas = energyStatisticsbyarea(currentdayestart, currentdayend, "水")
            dict_water_areas = {letter: score for score, letters in water_areas for letter in letters.split(",")}
            elect_areas = energyStatisticsbyarea(currentdayestart, currentdayend, "电")
            dict_elect_areas = {letter: score for score, letters in elect_areas for letter in letters.split(",")}
            steam_areas = energyStatisticsbyarea(currentdayestart, currentdayend, "汽")
            dict_steam_areas = {letter: score for score, letters in steam_areas for letter in letters.split(",")}
            wdir_list = []
            edir_list = []
            sdir_list = []
            for area in araes:
                wdir_coll = {}
                edir_coll = {}
                sdir_coll = {}
                if area.AreaName in dict_water_areas.keys():
                    wdir_coll["区域"] = area.AreaName
                    wdir_coll["能耗量"] = dict_water_areas[area.AreaName]
                if area.AreaName in dict_elect_areas.keys():
                    edir_coll["区域"] = area.AreaName
                    edir_coll["能耗量"] = dict_elect_areas[area.AreaName]
                if area.AreaName in dict_steam_areas.keys():
                    sdir_coll["区域"] = area.AreaName
                    sdir_coll["能耗量"] = dict_steam_areas[area.AreaName]
                wdir_list.append(wdir_coll)
                edir_list.append(edir_coll)
                sdir_list.append(sdir_coll)
            dir["wrow"] = wdir_list
            dir["erow"] = edir_list
            dir["srow"] = sdir_list
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "实时数据柱状图环形图查询报错Error：" + str(e), current_user.Name)

@energy.route('/energycost', methods=['POST', 'GET'])
def energycost():
    '''
    成本中心
    return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            EnergyClass = data.get("EnergyClass")
            TimeClass = data.get("TimeClass")
            AreaName = data.get("AreaName")
            dir_list = []
            oc_list = []
            if AreaName == "" or AreaName == None:
                tags = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()
            else:
                tags = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass,
                                                          TagDetail.AreaName == AreaName).all()
            for tag in tags:
                oc_list.append(tag.TagClassValue)
            if EnergyClass == "电":
                volum = db_session.query(ElectricVolumeMaintain).filter(ElectricVolumeMaintain.IsEnabled == "是").first()
                zgltotal = 0.0
                costtotal = 0.0
                if TimeClass == "日":
                    for i in range(int(StartTime[8:10]), int(EndTime[8:10])+1):
                        stae = StartTime[0:8] + addzero(i) + " 00:00:00"
                        ende = StartTime[0:8] + addzero(i) + " 23:59:59"
                        dir_list_i = {}
                        dir_list_i["时间"] = StartTime[0:8] + addzero(i)
                        dir_list_i["容量"] = round(float(volum.Volume), 2)
                        zgl = energyStatistics(oc_list, stae, ende, EnergyClass)
                        zgltotal = zgltotal + zgl
                        cost = energyStatisticsCost(oc_list, stae, ende, EnergyClass)
                        costtotal = costtotal + cost
                        dir_list_i["耗量"] = round(zgl, 2)
                        dir_list_i["成本"] = round(cost, 2)
                        dir_list.append(dir_list_i)
                elif TimeClass == "月":
                    for i in range(int(StartTime[5:7]), int(EndTime[5:7])+1):
                        emonth = getMonthFirstDayAndLastDay(StartTime[0:4], i)
                        staeM = datetime.datetime.strftime(emonth[0], "%Y-%m-%d %H:%M:%S")
                        endeM = datetime.datetime.strftime(emonth[0], "%Y-%m-%d") + " 23:59:59"
                        dir_list_i = {}
                        dir_list_i["时间"] = StartTime[0:8] + addzero(i)
                        dir_list_i["容量"] = round(float(volum.Volume)*30, 2)
                        zgl = energyStatistics(oc_list, staeM, endeM, EnergyClass)
                        zgltotal = zgltotal + zgl
                        cost = energyStatisticsCost(oc_list, staeM, endeM, EnergyClass)
                        costtotal = costtotal + cost
                        dir_list_i["耗量"] = round(zgl, 2)
                        dir_list_i["成本"] = round(cost, 2)
                        dir_list.append(dir_list_i)
                elif TimeClass == "年":
                    for i in range(int(StartTime[0:4]), int(EndTime[0:4])+1):
                        staeY = str(i) + "-01-01 00:00:00"
                        eyear = getMonthFirstDayAndLastDay(i, 12)
                        endeY = datetime.datetime.strftime(eyear[1], "%Y-%m-%d") + " 23:59:59"
                        dir_list_i = {}
                        dir_list_i["时间"] = str(i)
                        dir_list_i["容量"] = round(float(volum.Volume)*365, 2)
                        zgl = energyStatistics(oc_list, staeY, endeY, EnergyClass)
                        zgltotal = zgltotal + zgl
                        cost = energyStatisticsCost(oc_list, staeY, endeY, EnergyClass)
                        costtotal = costtotal + cost
                        dir_list_i["耗量"] = round(zgl, 2)
                        dir_list_i["成本"] = round(cost, 2)
                        dir_list.append(dir_list_i)
                elif TimeClass == "时":
                    for i in range(int(StartTime[11:13]), int(EndTime[11:13])+1):
                        staeH = StartTime[0:11] + addzero(i) + ":00:00"
                        endeH = StartTime[0:11] + addzero(i) + ":59:59"
                        dir_list_i = {}
                        dir_list_i["时间"] = StartTime[0:11] + addzero(i)
                        dir_list_i["容量"] = round(float(volum.Volume)/24, 2)
                        zgl = energyStatistics(oc_list, staeH, endeH, EnergyClass)
                        zgltotal = zgltotal + zgl
                        cost = energyStatisticsCost(oc_list, staeH, endeH, EnergyClass)
                        costtotal = costtotal + cost
                        dir_list_i["耗量"] = round(zgl, 2)
                        dir_list_i["成本"] = round(cost, 2)
                        dir_list.append(dir_list_i)
                dir["expend"] = round(zgltotal, 2)
                dir["expendCost"] = round(costtotal, 2)
                dir["expendUnit"] = volum.Unit
                dir["transformerStorage"] = round(float(volum.Volume), 2)
                dir["transformerUnit"] = volum.Unit
                dir["storageCost"] = round(float(volum.UnitPrice) * float(volum.Volume), 2)
            elif EnergyClass == "水":
                wsumtotal = 0.0
                wsumcosttotal = 0.0
                if TimeClass == "日":
                    for i in range(int(StartTime[8:10]), int(EndTime[8:10]) + 1):
                        staw = StartTime[0:8] + addzero(i) + " 00:00:00"
                        endw = StartTime[0:8] + addzero(i) + " 23:59:59"
                        dir_list_i = {}
                        dir_list_i["时间"] = StartTime[0:8] + addzero(i)
                        wsum = energyStatistics(oc_list, staw, endw, EnergyClass)
                        wsumtotal = wsumtotal + wsum
                        wsumcost = energyStatisticsCost(oc_list, staw, endw, EnergyClass)
                        costtotal = wsumcosttotal + wsumcost
                        dir_list_i["耗量"] = round(wsum, 2)
                        dir_list_i["成本"] = round(wsumcost, 2)
                        dir_list.append(dir_list_i)
                elif TimeClass == "月":
                    for i in range(int(StartTime[5:7]), int(EndTime[5:7]) + 1):
                        wmonth = getMonthFirstDayAndLastDay(StartTime[0:4], i)
                        stawM = datetime.datetime.strftime(wmonth[0], "%Y-%m-%d %H:%M:%S")
                        endwM = datetime.datetime.strftime(wmonth[0], "%Y-%m-%d") + " 23:59:59"
                        dir_list_i = {}
                        dir_list_i["时间"] = StartTime[0:8] + addzero(i)
                        wsum = energyStatistics(oc_list, stawM, endwM, EnergyClass)
                        wsumtotal = wsumtotal + wsum
                        wsumcost = energyStatisticsCost(oc_list, stawM, endwM, EnergyClass)
                        wsumcosttotal = wsumcosttotal + wsumcost
                        dir_list_i["耗量"] = round(wsum, 2)
                        dir_list_i["成本"] = round(wsumcost, 2)
                        dir_list.append(dir_list_i)
                elif TimeClass == "年":
                    for i in range(int(StartTime[0:4]), int(EndTime[0:4]) + 1):
                        stawY = str(i) + "-01-01 00:00:00"
                        wyear = getMonthFirstDayAndLastDay(i, 12)
                        wndeY = datetime.datetime.strftime(wyear[1], "%Y-%m-%d") + " 23:59:59"
                        dir_list_i = {}
                        dir_list_i["时间"] = str(i)
                        wsum = energyStatistics(oc_list, stawY, wndeY, EnergyClass)
                        wsumtotal = wsumtotal + wsum
                        wsumcost = energyStatisticsCost(oc_list, stawY, wndeY, EnergyClass)
                        wsumcosttotal = wsumcosttotal + wsumcost
                        dir_list_i["耗量"] = round(wsum, 2)
                        dir_list_i["成本"] = round(wsumcost, 2)
                        dir_list.append(dir_list_i)
                elif TimeClass == "时":
                    for i in range(int(StartTime[11:13]), int(EndTime[11:13]) + 1):
                        stawH = StartTime[0:11] + addzero(i) + ":00:00"
                        endwH = StartTime[0:11] + addzero(i) + ":59:59"
                        dir_list_i = {}
                        dir_list_i["时间"] = StartTime[0:11] + addzero(i)
                        wsum = energyStatistics(oc_list, stawH, endwH, EnergyClass)
                        wsumtotal = wsumtotal + wsum
                        wsumcost = energyStatisticsCost(oc_list, stawH, endwH, EnergyClass)
                        wsumcosttotal = wsumcosttotal + wsumcost
                        dir_list_i["耗量"] = round(wsum, 2)
                        dir_list_i["成本"] = round(wsumcost, 2)
                        dir_list.append(dir_list_i)
                wunit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "水").first()[0]
                dir["unit"] = wunit
            elif EnergyClass == "汽":
                ssumtotal = 0.0
                ssumcosttotal = 0.0
                if TimeClass == "日":
                    for i in range(int(StartTime[8:10]), int(EndTime[8:10]) + 1):
                        stas = StartTime[0:8] + addzero(i) + " 00:00:00"
                        ends = StartTime[0:8] + addzero(i) + " 23:59:59"
                        dir_list_i = {}
                        dir_list_i["时间"] = StartTime[0:8] + addzero(i)
                        ssum = energyStatistics(oc_list, stas, ends, EnergyClass)
                        ssumtotal = ssumtotal + ssum
                        ssumcost = energyStatisticsCost(oc_list, stas, ends, EnergyClass)
                        ssumcosttotal = ssumcosttotal + ssumcost
                        dir_list_i["耗量"] = round(ssum, 2)
                        dir_list_i["成本"] = round(ssumcost, 2)
                        dir_list.append(dir_list_i)
                elif TimeClass == "月":
                    for i in range(int(StartTime[5:7]), int(EndTime[5:7]) + 1):
                        smonth = getMonthFirstDayAndLastDay(StartTime[0:4], i)
                        stasM = datetime.datetime.strftime(smonth[0], "%Y-%m-%d %H:%M:%S")
                        endsM = datetime.datetime.strftime(smonth[0], "%Y-%m-%d") + " 23:59:59"
                        dir_list_i = {}
                        dir_list_i["时间"] = StartTime[0:8] + addzero(i)
                        ssum = energyStatistics(oc_list, stasM, endsM, EnergyClass)
                        ssumtotal = ssumtotal + ssum
                        ssumcost = energyStatisticsCost(oc_list, stasM, endsM, EnergyClass)
                        ssumcosttotal = ssumcosttotal + ssumcost
                        dir_list_i["耗量"] = round(ssum, 2)
                        dir_list_i["成本"] = round(ssumcost, 2)
                        dir_list.append(dir_list_i)
                elif TimeClass == "年":
                    for i in range(int(StartTime[0:4]), int(EndTime[0:4]) + 1):
                        stawY = str(i) + "-01-01 00:00:00"
                        syear = getMonthFirstDayAndLastDay(i, 12)
                        sndeY = datetime.datetime.strftime(syear[1], "%Y-%m-%d") + " 23:59:59"
                        dir_list_i = {}
                        dir_list_i["时间"] = str(i)
                        ssum = energyStatistics(oc_list, stawY, sndeY, EnergyClass)
                        ssumtotal = ssumtotal + ssum
                        ssumcost = energyStatisticsCost(oc_list, stawY, sndeY, EnergyClass)
                        ssumcosttotal = ssumcosttotal + ssumcost
                        dir_list_i["耗量"] = round(ssum, 2)
                        dir_list_i["成本"] = round(ssumcost, 2)
                        dir_list.append(dir_list_i)
                elif TimeClass == "时":
                    for i in range(int(StartTime[11:13]), int(EndTime[11:13]) + 1):
                        stasH = StartTime[0:11] + addzero(i) + ":00:00"
                        endsH = StartTime[0:11] + addzero(i) + ":59:59"
                        dir_list_i = {}
                        dir_list_i["时间"] = StartTime[0:11] + addzero(i)
                        ssum = energyStatistics(oc_list, stasH, endsH, EnergyClass)
                        ssumtotal = ssumtotal + ssum
                        ssumcost = energyStatisticsCost(oc_list, stasH, endsH, EnergyClass)
                        ssumcosttotal = ssumcosttotal + ssumcost
                        dir_list_i["耗量"] = round(ssum, 2)
                        dir_list_i["成本"] = round(ssumcost, 2)
                        dir_list.append(dir_list_i)
                wunit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "汽").first()[0]
                dir["unit"] = wunit
            dir["rows"] = dir_list
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "成本中心查询报错Error：" + str(e), current_user.Name)


@energy.route('/souyeselectyear', methods=['POST', 'GET'])
def souyeselectyear():
    '''
    首页查询年
    return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            EnergyClass = data.get("EnergyClass")
            dir["value"] = energyStatisticsyearde(StartTime, EndTime, EnergyClass)
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "首页查询年查询报错Error：" + str(e), current_user.Name)


