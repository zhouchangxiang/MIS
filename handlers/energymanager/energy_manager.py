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
    AreaTimeEnergyColour, ElectricProportion, PUIDMaintain, ElectricPrice, ElectricVolumeMaintain, WaterSteamPrice, \
    SteamTotalMaintain, ElectricSiteURL
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
    sql = ''
    if energy == "水":
        sql = "SELECT SUM(Cast(t.IncremenValue as float)) as count  FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                     1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    elif energy == "电":
        total = 0
        for tag in oc_list:
            ratios = db_session.query(ElectricSiteURL).filter(ElectricSiteURL.TagClassValue == tag).first()
            value = ratios.Value
            sql = "SELECT SUM(Cast(t.IncremenValue as float))*" + value + " FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable) WHERE t.TagClassValue=" + "'" + tag + "'" + "AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
            re = db_session.execute(sql).fetchall()
            db_session.close()
            zgl = 0 if re[0][0] is None else re[0][0]
            total += zgl
        return round(total, 2)
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

def timeelectricprice(oc_list, StartTime, EndTime, energy):
    re_list = []
    jtotal = 0.0
    ftotal = 0.0
    ptotal = 0.0
    gtotal = 0.0
    for tag in oc_list:
        ratios = db_session.query(ElectricSiteURL).filter(ElectricSiteURL.TagClassValue == tag).first()
        value = ratios.Value
        sql = "select t2.PriceName,SUM(Cast(t1.IncremenValue as float))*" + value + "* Cast(t2.PriceValue as float) FROM [DB_MICS].[dbo].[IncrementElectricTable] t1 with (INDEX =IX_IncrementElectricTable) INNER JOIN [DB_MICS].[dbo].[ElectricPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue='" + tag + "' and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue, t2.PriceName"
        res = db_session.execute(sql).fetchall()
        for re in res:
            if re[0] == "尖时刻":
                j = re[1] if re[1] is not None else 0.0
                jtotal = jtotal + j
            elif re[0] == "峰时刻":
                f = re[1] if re[1] is not None else 0.0
                ftotal = ftotal + f
            elif re[0] == "平时刻":
                p = re[1] if re[1] is not None else 0.0
                ptotal = ptotal + p
            elif re[0] == "谷时刻":
                g = re[1] if re[1] is not None else 0.0
                gtotal = gtotal + g
        # if len(re) > 0:
        #     price_name = re[0][0]
        #     zgl = re[0][1] if re[0][1] is not None else 0.0
        #     total += zgl
        db_session.close()
    re_list.append(("尖时刻",jtotal))
    re_list.append(("峰时刻",ftotal))
    re_list.append(("平时刻",ptotal))
    re_list.append(("谷时刻",gtotal))
    return re_list
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
    sql = ''
    if energy == "水":
        sql = "select SUM(Cast(t1.IncremenValue as float)) * Cast(t2.PriceValue as float) FROM [DB_MICS].[dbo].[IncrementWaterTable] t1 with (INDEX =IX_IncrementWaterTable) INNER JOIN [DB_MICS].[dbo].[WaterSteamPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                   1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue"
    elif energy == "电":
        res = timeelectricprice(oc_list, StartTime, EndTime, energy)
        count = 0.0
        for re in res:
            count = count + float(re[1])
        return round(count, 2)
        # sql = "select SUM(Cast(t1.IncremenValue as float)) * Cast(t2.PriceValue as float) FROM [DB_MICS].[dbo].[IncrementElectricTable] t1 with (INDEX =IX_IncrementElectricTable) INNER JOIN [DB_MICS].[dbo].[ElectricPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
        #     oc_list)[
        #                                                                                                                                                                                                                                                                                1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue"
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


def energyStatisticshour(oc_list, StartTime, EndTime, energy):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy: 水，电 ，气
    :return:获取水电汽增量值以collecthour分组
    '''
    if energy == "水":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.CollectionHour FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                     1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionHour order by t.CollectionHour"
    elif energy == "电":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.CollectionHour  FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                            1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionHour order by t.CollectionHour"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.CollectionHour  FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable)  WHERE t.TagClassValue in (" + str(
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
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.CollectionDay FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                    1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionDay order by t.CollectionDay"
    elif energy == "电":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.CollectionDay  FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionDay order by t.CollectionDay"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.CollectionDay  FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable)  WHERE t.TagClassValue in (" + str(
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
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.CollectionMonth FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                      1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionMonth order by t.CollectionMonth"
    elif energy == "电":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.CollectionMonth  FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                             1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionMonth order by t.CollectionMonth"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.CollectionMonth  FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable)  WHERE t.TagClassValue in (" + str(
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
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.CollectionYear FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                     1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionYear order by t.CollectionYear"
    elif energy == "电":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.CollectionYear  FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                            1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionYear order by t.CollectionYear"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.CollectionYear  FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable)  WHERE t.TagClassValue in (" + str(
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
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.AreaName  FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE  t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.AreaName"
    elif energy == "电":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.AreaName  FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable)  WHERE t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.AreaName"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "'),t.AreaName  FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable)  WHERE t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.AreaName"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    return re


def energyStatisticsCostbyhour(oc_list, StartTime, EndTime, energy):
    '''
    获取某段时间水电汽的成本
    :param oc_list:
    :param StartTime:
    :param EndTime:
    :param energy:
    :return:
    '''
    if energy == "水":
        sql = "select SUM(Cast(t1.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "') * Cast(t2.PriceValue as float), t1.CollectionHour FROM [DB_MICS].[dbo].[IncrementWaterTable] t1 with (INDEX =IX_IncrementWaterTable) INNER JOIN [DB_MICS].[dbo].[WaterSteamPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                                                                                                                               1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue, t1.CollectionHour"
    elif energy == "电":
        sql = "select SUM(Cast(t1.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "') * Cast(t2.PriceValue as float), t1.CollectionHour FROM [DB_MICS].[dbo].[IncrementElectricTable] t1 with (INDEX =IX_IncrementElectricTable) INNER JOIN [DB_MICS].[dbo].[ElectricPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                                                                                                                                   1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue, t1.CollectionHour"
    elif energy == "汽":
        sql = "select SUM(Cast(t1.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "') * Cast(t2.PriceValue as float), t1.CollectionHour FROM [DB_MICS].[dbo].[IncrementStreamTable] t1 with (INDEX =IX_IncrementStreamTable) INNER JOIN [DB_MICS].[dbo].[WaterSteamPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                                                                                                                                 1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue, t1.CollectionHour"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    return re


def energyStatisticsCostbyday(oc_list, StartTime, EndTime, energy):
    '''
    获取某段时间水电汽的成本
    :param oc_list:
    :param StartTime:
    :param EndTime:
    :param energy:
    :return:
    '''
    if energy == "水":
        sql = "select SUM(Cast(t1.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "') * Cast(t2.PriceValue as float), t1.CollectionDay FROM [DB_MICS].[dbo].[IncrementWaterTable] t1 with (INDEX =IX_IncrementWaterTable) INNER JOIN [DB_MICS].[dbo].[WaterSteamPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                                                                                                                              1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue, t1.CollectionDay"
    elif energy == "电":
        sql = "select SUM(Cast(t1.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "') * Cast(t2.PriceValue as float), t1.CollectionDay FROM [DB_MICS].[dbo].[IncrementElectricTable] t1 with (INDEX =IX_IncrementElectricTable) INNER JOIN [DB_MICS].[dbo].[ElectricPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                                                                                                                                  1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue, t1.CollectionDay"
    elif energy == "汽":
        sql = "select SUM(Cast(t1.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "') * Cast(t2.PriceValue as float), t1.CollectionDay FROM [DB_MICS].[dbo].[IncrementStreamTable] t1 with (INDEX =IX_IncrementStreamTable) INNER JOIN [DB_MICS].[dbo].[WaterSteamPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                                                                                                                                1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue, t1.CollectionDay"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    return re


def energyStatisticsCostbymonth(oc_list, StartTime, EndTime, energy):
    '''
    获取某段时间水电汽的成本
    :param oc_list:
    :param StartTime:
    :param EndTime:
    :param energy:
    :return:
    '''
    if energy == "水":
        sql = "select SUM(Cast(t1.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "') * Cast(t2.PriceValue as float), t1.CollectionMonth FROM [DB_MICS].[dbo].[IncrementWaterTable] t1 with (INDEX =IX_IncrementWaterTable) INNER JOIN [DB_MICS].[dbo].[WaterSteamPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                                                                                                                                1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue, t1.CollectionMonth"
    elif energy == "电":
        sql = "select SUM(Cast(t1.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "') * Cast(t2.PriceValue as float), t1.CollectionMonth FROM [DB_MICS].[dbo].[IncrementElectricTable] t1 with (INDEX =IX_IncrementElectricTable) INNER JOIN [DB_MICS].[dbo].[ElectricPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                                                                                                                                    1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue, t1.CollectionMonth"
    elif energy == "汽":
        sql = "select SUM(Cast(t1.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + energy + "') * Cast(t2.PriceValue as float), t1.CollectionMonth FROM [DB_MICS].[dbo].[IncrementStreamTable] t1 with (INDEX =IX_IncrementStreamTable) INNER JOIN [DB_MICS].[dbo].[WaterSteamPrice] t2 ON t1.PriceID = t2.ID where  t1.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                                                                                                                                                                                                                                                                                  1:-1] + ") and t1.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t1.PriceID, t2.PriceValue, t1.CollectionMonth"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    return re


def energyStatisticsteamtotal(StartTime, EndTime):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy:
    :return:获取某段时间汽能总值
    '''
    reend = db_session.query(SteamTotalMaintain).filter(
        SteamTotalMaintain.SumValue != None, SteamTotalMaintain.SumValue != '0.0', SteamTotalMaintain.SumValue != '',
        SteamTotalMaintain.CollectionDate.between(StartTime, EndTime)).order_by(desc("CollectionDate")).first()
    restar = db_session.query(SteamTotalMaintain).filter(
        SteamTotalMaintain.SumValue != None, SteamTotalMaintain.SumValue != '0.0', SteamTotalMaintain.SumValue != '',
        SteamTotalMaintain.CollectionDate.between(StartTime, EndTime)).order_by(("CollectionDate")).first()
    if reend != None and restar != None:
        return round(float(reend.SumValue) - float(restar.SumValue), 2)
    else:
        return 0


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
                dictpre = {letter: score for score, letters in recomper for letter in letters.split(",")}
                for myHour in constant.myHours:
                    scurrtime = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(
                        int(currentday)) + " " + myHour
                    spretime = compareday + " " + myHour
                    dir_list_dict = {}
                    dir_list_dict["时间"] = scurrtime
                    currcount = 0
                    comparecount = 0
                    if scurrtime in dictcurr.keys():
                        currcount = round(float(dictcurr[scurrtime]), 2)
                    else:
                        if datetime.datetime.strptime(scurrtime, '%Y-%m-%d %H') > datetime.datetime.now():
                            currcount = ""
                    if spretime in dictpre.keys():
                        comparecount = round(float(dictpre[spretime]), 2)
                    dir_list_dict["今日能耗"] = currcount
                    dir_list_dict["对比日能耗"] = comparecount
                    dir_list.append(dir_list_dict)
                fistendday = getMonthFirstDayAndLastDay(currentyear, currentmonth)
                lastfistendday = getMonthFirstDayAndLastDay(
                    strlastMonth(str(currentyear) + "-" + addzero(int(currentmonth)))[0:4],
                    strlastMonth(str(currentyear) + "-" + addzero(int(currentmonth)))[5:7])
                recurrdays = energyStatisticsday(oc_list, fistendday[0].strftime('%Y-%m-%d %H:%M:%S'),
                                                 fistendday[1].strftime('%Y-%m-%d %H:%M:%S'), EnergyClass)
                recomperdays = energyStatisticsday(oc_list, lastfistendday[0].strftime('%Y-%m-%d %H:%M:%S'),
                                                   lastfistendday[1].strftime('%Y-%m-%d %H:%M:%S'), EnergyClass)
                dictrecurrdays = {letter: score for score, letters in recurrdays for letter in letters.split(",")}
                dictrecomperdays = {letter: score for score, letters in recomperdays for letter in letters.split(",")}
                for myday in constant.mydays:
                    mycurrday = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + myday
                    mycompareday = strlastMonth(mycurrday[0:7]) + "-" + myday
                    dirmonth_list_dict = {}
                    dirmonth_list_dict["日期"] = mycurrday
                    if mycurrday in dictrecurrdays.keys():
                        dirmonth_list_dict["本月能耗"] = round(float(dictrecurrdays[mycurrday]), 2)
                    else:
                        reday = getMonthFirstDayAndLastDay(currentyear, currentmonth)
                        if int(myday) > int(str(reday[1])[8:10]):
                            dirmonth_list_dict["本月能耗"] = ""
                        else:
                            if datetime.datetime.strptime(mycurrday, '%Y-%m-%d') > datetime.datetime.now():
                                dirmonth_list_dict["本月能耗"] = ""
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
                data_list.append({"name": "电表", "online": elestatuss, "rate": int(100 * (elestatuss / elestatust)),
                                  "total": elestatust})
                data_list.append({"name": "水表", "online": watstatuss, "rate": int(100 * (watstatuss / watstatust)),
                                  "total": watstatust})
                data_list.append({"name": "汽表", "online": stestatuss, "rate": int(100 * (stestatuss / stestatust)),
                                  "total": stestatust})
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
                    recomper = energyStatisticshour(oc_list, compareday + " 00:00:00", compareday + " 23:59:59",
                                                    EnergyClass)
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
                    value_dirc["backgroundColor"] = "-webkit-linear-gradient(left," + wu + "," + wu + ")"
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
    oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()
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


def exportx(Area, EnergyClass, StartTime, EndTime):
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
    if Area != "" and Area != None:
        tas = db_session.query(TagDetail).filter(TagDetail.AreaName == Area, TagDetail.EnergyClass == EnergyClass).all()
    else:
        tas = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()

    # 写入列名
    columns = ['区域', '采集点', '增量值', '单位', '开始时间', '结束时间']
    for item in columns:
        worksheet.write(0, col, item, cell_format)
        col += 1
    UnitValue = db_session.query(Unit.UnitValue).filter(Unit.UnitName == EnergyClass).first()
    if UnitValue:
        unit = UnitValue[0]
    else:
        unit = ""
    if EnergyClass == "汽":
        totaltag = db_session.query(TagDetail).filter(TagDetail.TagClassValue == "S_AllArea_Value").first()
        totalm = energyStatisticsteamtotal(StartTime, EndTime)
        for cum in columns:
            if cum == '采集点':
                worksheet.write(1, columns.index(cum), totaltag.FEFportIP)
            if cum == '增量值':
                worksheet.write(1, columns.index(cum), totalm)
            if cum == '区域':
                worksheet.write(1, columns.index(cum), totaltag.AreaName)
            if cum == '单位':
                worksheet.write(1, columns.index(cum), unit)
            if cum == '开始时间':
                worksheet.write(1, columns.index(cum), StartTime)
            if cum == '结束时间':
                worksheet.write(1, columns.index(cum), EndTime)
    # 写入数据
    i = 1
    if EnergyClass == "汽":
        i = 2
    for ta in tas:
        reclass = tongjibaobiaosql(EnergyClass, ta.TagClassValue, StartTime, EndTime)
        for cum in columns:
            if cum == '采集点':
                worksheet.write(i, columns.index(cum), ta.FEFportIP)
            if cum == '增量值':
                worksheet.write(i, columns.index(cum),
                                round(0 if reclass[0]['IncremenValue'] is None else float(reclass[0]['IncremenValue']),
                                      2))
            if cum == '区域':
                worksheet.write(i, columns.index(cum), ta.AreaName)
            if cum == '单位':
                worksheet.write(i, columns.index(cum), unit)
            if cum == '开始时间':
                worksheet.write(i, columns.index(cum), StartTime)
            if cum == '结束时间':
                worksheet.write(i, columns.index(cum), EndTime)
        i = i + 1
    writer.close()
    output.seek(0)
    return output


def tongjibaobiaosql(EnergyClass, TagClassValue, StartTime, EndTime):
    if EnergyClass == "水":
        sql = "SELECT (SUM(Cast(t.IncremenValue as float)))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + EnergyClass + "') AS IncremenValue FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable) " \
                                                                                                                                                                                      "WHERE t.TagClassValue = '" + TagClassValue + "' AND t.CollectionDate BETWEEN " + "'" + StartTime + "' AND " + "'" + EndTime + "'"
        oclass = db_session.execute(sql).fetchall()
        db_session.close()
    elif EnergyClass == "电":
        ratios = db_session.query(ElectricSiteURL).filter(ElectricSiteURL.TagClassValue == TagClassValue).first()
        value = ratios.Value
        s = "SELECT SUM(Cast(t.IncremenValue as float))*" + value + " AS IncremenValue FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable) WHERE t.TagClassValue = '" + TagClassValue + "' AND t.CollectionDate BETWEEN " + "'" + StartTime + "' AND " + "'" + EndTime + "'"
        oclass = db_session.execute(s).fetchall()
        # sql = "SELECT (SUM(Cast(t.IncremenValue as float)))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+EnergyClass+"') AS IncremenValue FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable) " \
        #       "WHERE t.TagClassValue = '" + TagClassValue + "' AND t.CollectionDate BETWEEN " + "'" + StartTime + "' AND " + "'" + EndTime + "'"
        # oclass = db_session.execute(sql).fetchall()
        db_session.close()
    else:
        sql = "SELECT (SUM(Cast(t.IncremenValue as float)))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '" + EnergyClass + "') AS IncremenValue FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable) " \
                                                                                                                                                                                      "WHERE t.TagClassValue = '" + TagClassValue + "' AND t.CollectionDate BETWEEN " + "'" + StartTime + "' AND " + "'" + EndTime + "'"
        oclass = db_session.execute(sql).fetchall()
        db_session.close()
    return oclass


@energy.route('/tongjibaobiao', methods=['POST', 'GET'])
def tongjibaobiao():
    '''
    统计报表
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            Area = data.get("Area")
            EnergyClass = data.get("EnergyClass")
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            if Area == None or Area == "":
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()
            else:
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass,
                                                            TagDetail.AreaName == Area).all()
            UnitValue = db_session.query(Unit.UnitValue).filter(Unit.UnitName == EnergyClass).first()
            if UnitValue:
                unit = UnitValue[0]
            else:
                unit = ""
            data_list = []
            if EnergyClass == "汽":
                totaltag = db_session.query(TagDetail).filter(TagDetail.TagClassValue == "S_AllArea_Value").first()
                totalm = energyStatisticsteamtotal(StartTime, EndTime)
                dict_data_total = {"TagClassValue": totaltag.FEFportIP,
                                   "IncremenValue": totalm,
                                   "AreaName": totaltag.AreaName, "Unit": unit, "StartTime": StartTime,
                                   "EndTime": EndTime}
                data_list.append(dict_data_total)
            for oc in oclass:
                reclass = tongjibaobiaosql(EnergyClass, oc.TagClassValue, StartTime, EndTime)
                tag = db_session.query(TagDetail).filter(TagDetail.TagClassValue == oc.TagClassValue).first()
                dict_data = {"TagClassValue": tag.FEFportIP, "Equipment": tag.Equipment, "IncremenValue": round(
                    0 if reclass[0]['IncremenValue'] is None else float(reclass[0]['IncremenValue']), 2),
                             "AreaName": tag.AreaName, "Unit": unit, "StartTime": StartTime, "EndTime": EndTime}
                data_list.append(dict_data)
            dir["row"] = data_list
            print(dir)
            dir["total"] = len(oclass)
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "统计报表查询报错Error：" + str(e), current_user.Name)


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
            AreaName = data.get("AreaName")
            if AreaName == None or AreaName == "":
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()
            else:
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass,
                                                            TagDetail.AreaName == AreaName).all()

            oc_list = []
            for oc in oclass:
                oc_list.append(oc.TagClassValue)
            rows_list = []
            if oc_list:
                recomper = energyStatisticshour(oc_list, CompareTime + " 00:00:00", CompareTime + " 23:59:59",
                                                EnergyClass)
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
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass,
                                                            TagDetail.AreaName == AreaName).all()
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
            if len(rows_list) > 0:
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
            re = PlanCreate.createBatchMaintain(PlanNum, BatchID, BrandName, PlanQuantity, WaterConsumption,
                                                SteamConsumption, CreateDate, ProductionDate, StartTime, EndTime)
            if re == True:
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

    def createBatchMaintain(self, PlanNum, BatchID, BrandName, PlanQuantity, WaterConsumption, SteamConsumption,
                            CreateDate, ProductionDate, StartTime, EndTime):
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
                    bReturn = self.BatchMaintainTask(puid.PUIDName, PlanNum, BatchID, BrandName, PlanQuantity,
                                                     WaterConsumption, SteamConsumption, CreateDate, ProductionDate,
                                                     StartTime, EndTime)
                    if bReturn == False:
                        return False
            return bReturn
        except Exception as e:
            db_session.rollback()
            print(e)
            insertSyslog("error", "创建计划报错Error：" + str(e), current_user.Name)
            return False

    def BatchMaintainTask(self, PuidName, PlanNum, BatchID, BrandName, PlanQuantity, WaterConsumption, SteamConsumption,
                          CreateDate, ProductionDate, StartTime, EndTime):
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
            return False


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
            batinfos = db_session.query(BatchMaintain).filter(BatchMaintain.ProductionDate.between(StartTime, EndTime),
                                                              BatchMaintain.AreaName == AreaName).all()
            brandSum = db_session.query(BatchMaintain.BrandName).distinct().filter(
                BatchMaintain.ProductionDate.between(StartTime, EndTime),
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
                waterEveryBatch = waterCon / batchcont
            steamEveryBatch = 0
            if steamCon != 0:
                steamEveryBatch = steamCon / batchcont
            if waterEveryBatch != 0:
                waterEveryBatch = round(waterEveryBatch, 2)
            if waterCon != 0:
                waterCon = round(waterCon, 2)
            if steamCon != 0:
                steamCon = round(steamCon, 2)
            if steamEveryBatch != 0:
                steamEveryBatch = round(steamEveryBatch, 2)
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
                nowm = int(EndTime[5:7]) + 1
                for i in range(1, nowm):
                    re = getMonthFirstDayAndLastDay(StartTime[0:4], i)
                    if AreaName == None or AreaName == "":
                        batyears = db_session.query(BatchMaintain).filter(
                            BatchMaintain.EndTime.between(datetime.datetime.strftime(re[0], "%Y-%m-%d") + " 00:00:00",
                                                          datetime.datetime.strftime(re[1],
                                                                                     "%Y-%m-%d") + " 00:00:00" + " 23:59:59")).all()
                    else:
                        batyears = db_session.query(BatchMaintain).filter(
                            BatchMaintain.EndTime.between(
                                datetime.datetime.strftime(re[0], "%Y-%m-%d") + " 00:00:00" + " 00:00:00",
                                datetime.datetime.strftime(re[1], "%Y-%m-%d") + " 23:59:59"),
                            BatchMaintain.AreaName == AreaName).all()
                    waterSum = 0.0
                    steamSum = 0.0
                    for baty in batyears:
                        if baty.WaterConsumption != None and baty.WaterConsumption != "":
                            waterSum = waterSum + float(baty.WaterConsumption)
                        if baty.SteamConsumption != None and baty.SteamConsumption != "":
                            steamSum = steamSum + float(baty.SteamConsumption)
                    bat_energy = {}
                    bat_energy["日期"] = StartTime[0:4] + "-" + addzero(i)
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
                count = db_session.query(BatchMaintain).filter(
                    BatchMaintain.ProductionDate.between(StartTime, EndTime)).count()
            elif AreaName != "" and BrandName == "":
                batinfos = db_session.query(BatchMaintain).filter(
                    BatchMaintain.ProductionDate.between(StartTime, EndTime), BatchMaintain.AreaName == AreaName).all()[
                           inipage:endpage]
                count = db_session.query(BatchMaintain).filter(BatchMaintain.ProductionDate.between(StartTime, EndTime),
                                                               BatchMaintain.AreaName == AreaName).count()
            elif AreaName == "" and BrandName != "":
                batinfos = db_session.query(BatchMaintain).filter(
                    BatchMaintain.ProductionDate.between(StartTime, EndTime),
                    BatchMaintain.BrandName == BrandName).all()[inipage:endpage]
                count = db_session.query(BatchMaintain).filter(BatchMaintain.ProductionDate.between(StartTime, EndTime),
                                                               BatchMaintain.BrandName == BrandName).count()
            else:
                batinfos = db_session.query(BatchMaintain).filter(
                    BatchMaintain.ProductionDate.between(StartTime, EndTime), BatchMaintain.AreaName == AreaName,
                    BatchMaintain.BrandName == BrandName).all()[inipage:endpage]
                count = db_session.query(BatchMaintain).filter(BatchMaintain.ProductionDate.between(StartTime, EndTime),
                                                               BatchMaintain.AreaName == AreaName,
                                                               BatchMaintain.BrandName == BrandName).count()
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
            currentdayestart = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")[0:10] + " 00:00:00"
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
                    if dict_water_areas[area.AreaName] != None and dict_water_areas[area.AreaName] != 0:
                        wdir_coll["区域"] = area.AreaName
                        wdir_coll["能耗量"] = dict_water_areas[area.AreaName]
                if area.AreaName in dict_elect_areas.keys():
                    if dict_elect_areas[area.AreaName] != None and dict_elect_areas[area.AreaName] != 0:
                        edir_coll["区域"] = area.AreaName
                        edir_coll["能耗量"] = dict_elect_areas[area.AreaName]
                if area.AreaName in dict_steam_areas.keys():
                    if dict_steam_areas[area.AreaName] != None and dict_steam_areas[area.AreaName] != 0:
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
            if oc_list:
                if TimeClass == "日":
                    hours = energyStatisticshour(oc_list, StartTime, EndTime, EnergyClass)
                    cost_hours = energyStatisticsCostbyhour(oc_list, StartTime, EndTime, EnergyClass)
                    dict_hours = {letter: score for score, letters in hours for letter in letters.split(",")}
                    dict_cost_hours = {letter: score for score, letters in cost_hours for letter in
                                       letters.split(",")}
                    for myHour in constant.myHours:
                        dir_list_i = {}
                        scurrtime = StartTime[0:11] + myHour
                        dir_list_i["时间"] = scurrtime
                        hcount = 0
                        hcostcount = 0
                        if scurrtime in dict_hours.keys():
                            hcount = round(float(dict_hours[scurrtime]), 2)
                        if scurrtime in dict_cost_hours.keys():
                            hcostcount = round(float(dict_cost_hours[scurrtime]), 2)
                        dir_list_i["耗量"] = hcount
                        dir_list_i["成本"] = hcostcount
                        dir_list.append(dir_list_i)
                elif TimeClass == "月":
                    days = energyStatisticsday(oc_list, StartTime, EndTime, EnergyClass)
                    cost_days = energyStatisticsCostbyday(oc_list, StartTime, EndTime, EnergyClass)
                    dict_days = {letter: score for score, letters in days for letter in letters.split(",")}
                    dict_cost_days = {letter: score for score, letters in cost_days for letter in
                                      letters.split(",")}
                    for myday in constant.mydays:
                        dir_list_i = {}
                        daytime = StartTime[0:8] + myday
                        dir_list_i["时间"] = daytime
                        daycount = 0
                        daycostcount = 0
                        if daytime in dict_days.keys():
                            daycount = round(float(dict_days[daytime]), 2)
                        if daytime in dict_cost_days.keys():
                            daycostcount = round(float(dict_cost_days[daytime]), 2)
                        dir_list_i["耗量"] = daycount
                        dir_list_i["成本"] = daycostcount
                        dir_list.append(dir_list_i)
                elif TimeClass == "年":
                    monts = energyStatisticsmonth(oc_list, StartTime, EndTime, EnergyClass)
                    cost_months = energyStatisticsCostbymonth(oc_list, StartTime, EndTime, EnergyClass)
                    dict_monts = {letter: score for score, letters in monts for letter in letters.split(",")}
                    dict_cost_months = {letter: score for score, letters in cost_months for letter in
                                        letters.split(",")}
                    for mymonth in constant.mymonths:
                        dir_list_i = {}
                        monthtime = StartTime[0:5] + mymonth
                        dir_list_i["时间"] = monthtime
                        monthcount = 0
                        monthcostcount = 0
                        if monthtime in dict_monts.keys():
                            monthcount = round(float(dict_monts[monthtime]), 2)
                        if monthtime in dict_cost_months.keys():
                            monthcostcount = round(float(dict_cost_months[monthtime]), 2)
                        dir_list_i["耗量"] = monthcount
                        dir_list_i["成本"] = monthcostcount
                        dir_list.append(dir_list_i)
            wunit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == EnergyClass).first()[0]
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
