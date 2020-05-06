import redis
from flask import Blueprint, render_template, request, make_response, send_file
import json
import datetime
from sqlalchemy import desc
from dbset.database.db_operate import db_session, pool
from dbset.main.BSFramwork import AlchemyEncoder
from flask_login import login_required, logout_user, login_user, current_user, LoginManager
import calendar

from handlers.energymanager.energy_manager import energyStatistics, energyStatisticsCost, energyStatisticshour, \
    energyStatisticsday, energyStatisticsmonth, energyStatisticsbyarea
from models.SystemManagement.core import RedisKey, ElectricEnergy, WaterEnergy, SteamEnergy, LimitTable, Equipment, \
    AreaTable, Unit, TagClassType, TagDetail, BatchMaintain
from models.SystemManagement.system import EarlyWarning, EarlyWarningLimitMaintain, WaterSteamBatchMaintain, \
    AreaTimeEnergyColour, ElectricProportion, IncrementStreamTable, SteamTotal, SteamTotalMaintain
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

energySteam = Blueprint('energySteam', __name__, template_folder='templates')

arro = arrow.now()
pool = redis.ConnectionPool(host=constant.REDIS_HOST)
redis_conn = redis.Redis(connection_pool=pool)

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


def energySteamSelect(data):
    if request.method == 'GET':
        try:
            dir = {}
            data = request.values
            Area = data.get("Area")
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            energy = "汽"
            if Area is not None and Area != "":
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == energy,
                                                            TagDetail.AreaName == Area).all()
            else:
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == energy).all()
            oc_list = []
            for oc in oclass:
                oc_list.append(oc.TagClassValue)
            if len(oc_list) > 0:
                stecount = energyStatistics(oc_list, StartTime, EndTime, energy)
            else:
                stecount = 0.0
            dir["type"] = energy
            dir["value"] = stecount
            unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == energy).first()[0]
            dir["unit"] = unit
            # 成本
            if len(oc_list) > 0:
                cost = energyStatisticsCost(oc_list, StartTime, EndTime, energy)
            else:
                cost = 0.0
            dir["cost"] = cost
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            insertSyslog("error", "能耗查询报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)


@energySteam.route('/steam_report', methods=['GET'])
def get_steam():
    """
    获取蒸汽报表的数据接口
    """
    try:
        start_time = request.values.get('start_time')
        end_time = request.values.get('end_time')
        # 当前页数
        current_page = int(request.values.get('offset'))
        # 每页显示条数
        pagesize = int(request.values.get('limit'))
        area_name = request.values.get('area_name')
        if area_name:
            rows = 'select top ' + str(pagesize) + ' CalculationID,TagClassValue,AreaName,IncremenValue,CollectionDate ' + \
                   'from [DB_MICS].[dbo].[IncrementStreamTable] where ID not in ' + '(select top ' + str(
                (current_page - 1) * pagesize) + \
                   ' ID from [DB_MICS].[dbo].[IncrementStreamTable] where cast(IncremenValue as float) != 0.0 ' + \
                   'and AreaName=' + "'" + area_name + "'" + ' and CollectionDate between ' + "'" + start_time + "'" + \
                   " and " + "'" + end_time + "'" + ' order by CollectionDate asc, ID asc)' + 'and AreaName=' + "'" + \
                   area_name + "'" + 'and cast(IncremenValue as float) != 0.0 and CollectionDate between ' + "'" + \
                   start_time + "'" + " and " + "'" + end_time + "'" + ' order by CollectionDate asc, ID asc'
            result3 = db_session.execute(rows).fetchall()
            total = 'select count(ID) as total from [DB_MICS].[dbo].[IncrementStreamTable] where cast(IncremenValue as' \
                    ' float) != 0.0 and AreaName=' + "'" + area_name + "'" + ' and CollectionDate between ' + "'" + \
                    start_time + "'" + " and" + "'" + end_time + "'"
            result2 = db_session.execute(total).fetchall()
            tag_list = db_session.query(TagDetail).filter(TagDetail.AreaName == area_name,
                                                          TagDetail.EnergyClass == '汽').all()
            tag_point = [index.TagClassValue for index in tag_list]
            data = []
            for item in result3:
                query_steam = db_session.query(SteamEnergy).filter(SteamEnergy.ID == item.CalculationID).first()
                query_tagdetai = db_session.query(TagDetail).filter(TagDetail.TagClassValue == item.TagClassValue).first()
                tag_area = query_tagdetai.FEFportIP
                dict1 = {'ID': query_steam.ID, 'SumValue': query_steam.SumValue, 'WD': query_steam.WD,
                         'Volume': query_steam.Volume,
                         'AreaName': item.AreaName, 'CollectionDate': str(item.CollectionDate),
                         'IncremenValue': item.IncremenValue, 'TagClassValue': tag_area}
                data.append(dict1)
            if tag_point:
                price_sql = "select sum(t1.price)*0.0001*1.2 total_price from (select TagClassValue,sum(cast(IncremenValue" \
                            " as float)) as price from [DB_MICS].[dbo].[IncrementStreamTable] where cast(IncremenValue as" \
                            " float) != 0.0 and TagClassValue in " + (str(tag_point).replace('[', '(')).replace(']', ')') + \
                            " and CollectionDate between " + "'" + start_time + "'" + " and " + "'" + end_time + "'" + \
                            " group by TagClassValue) t1"
                total_price = db_session.execute(price_sql).fetchall()
                price = 0 if total_price[0]['total_price'] is None else str(round(total_price[0]['total_price'], 2))
                return json.dumps({'rows': data, 'total_column': result2[0]['total'], 'price': price}, cls=AlchemyEncoder,
                                  ensure_ascii=False)
            else:
                price_sql = "select sum(t1.price)*0.0001*1.2 total_price from (select TagClassValue,sum(cast(IncremenValue" \
                            " as float)) as price from [DB_MICS].[dbo].[IncrementStreamTable] where cast(IncremenValue as" \
                            " float) != 0.0 and AreaName=" + "'" + area_name + "'" + " and CollectionDate between " +\
                            "'" + start_time + "'" + " and " + "'" + end_time + "'" + "group by TagClassValue) t1"
                total_price = db_session.execute(price_sql).fetchall()
                price = 0 if total_price[0]['total_price'] is None else str(round(total_price[0]['total_price'], 2))
                return json.dumps({'rows': result3, 'total_column': result2[0]['total'], 'price': price},
                                  cls=AlchemyEncoder, ensure_ascii=False)
        else:
            price_sql = "select sum(t1.price)*0.0001*1.2 total_price from (select TagClassValue,sum(cast(IncremenValue" \
                        " as float)) as price from [DB_MICS].[dbo].[IncrementStreamTable] where cast(IncremenValue as" \
                        " float) != 0.0 and CollectionDate between " + "'" + start_time + "'" + " and " + "'" + end_time + \
                        "'" + "group by TagClassValue) t1"
            total_price = db_session.execute(price_sql).fetchall()
            price = 0 if total_price[0]['total_price'] is None else str(round(total_price[0]['total_price'], 2))
            rows = 'select top ' + str(pagesize) + ' CalculationID,TagClassValue,AreaName,IncremenValue,CollectionDate ' + \
                   'from [DB_MICS].[dbo].[IncrementStreamTable] where ID not in ' + '(select top ' + str(
                (current_page - 1) * pagesize) + ' ID from [DB_MICS].[dbo].[IncrementStreamTable] where cast(IncremenValue' \
                ' as float) != 0.0 and CollectionDate between ' + "'" + start_time + "'" + " and " + "'" + end_time + "'" + \
                ' order by CollectionDate asc, ID asc)' + 'and cast(IncremenValue as float) != 0.0 and CollectionDate' \
                ' between ' + "'" + start_time + "'" + " and " + "'" + end_time + "'" + ' order by CollectionDate asc, ID asc'

            result3 = db_session.execute(rows).fetchall()
            total = 'select count(ID) as total from [DB_MICS].[dbo].[IncrementStreamTable] where cast(IncremenValue as' \
                    ' float) != 0.0 and CollectionDate between ' + "'" + start_time + "'" + " and" + "'" + end_time + "'"
            result2 = db_session.execute(total).fetchall()
            data = []
            for item in result3:
                if item.CalculationID and item.TagClassValue:
                    query_steam = db_session.query(SteamEnergy).filter(SteamEnergy.ID == item.CalculationID).first()
                    query_tagdetai = db_session.query(TagDetail).filter(
                        TagDetail.TagClassValue == item.TagClassValue).first()
                    tag_area = query_tagdetai.FEFportIP
                    dict1 = {'ID': query_steam.ID, 'SumValue': query_steam.SumValue, 'WD': query_steam.WD,
                             'Volume': query_steam.Volume,
                             'AreaName': item.AreaName, 'CollectionDate': str(item.CollectionDate),
                             'IncremenValue': item.IncremenValue, 'TagClassValue': tag_area}
                    data.append(dict1)
            return json.dumps({'rows': data, 'total_column': result2[0]['total'], 'price': price}, cls=AlchemyEncoder,
                              ensure_ascii=False)
    except Exception as e:
        print(e)
        insertSyslog("error", "能耗查询报错Error：" + str(e), current_user.Name)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

def energydetailStatistics(oc_list, StartTime, EndTime, energy):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy: 水，电 ，气
    :return:获取水电汽增量值以TagClassValue分组
    '''
    if energy == "水":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.TagClassValue FROM [DB_MICS].[dbo].[IncrementWaterTable] t with (INDEX =IX_IncrementWaterTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.TagClassValue"
    elif energy == "电":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.TagClassValue  FROM [DB_MICS].[dbo].[IncrementElectricTable] t with (INDEX =IX_IncrementElectricTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.TagClassValue"
    elif energy == "汽":
        sql = "SELECT SUM(Cast(t.IncremenValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.TagClassValue  FROM [DB_MICS].[dbo].[IncrementStreamTable] t with (INDEX =IX_IncrementStreamTable)  WHERE t.TagClassValue in (" + str(
            oc_list)[
                                                                                                                                                                           1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.TagClassValue"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    return re
def energydetailStatisticsbytag(TagClassValue, StartTime, EndTime, energy):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy: 水，电 ，气
    :return:获取水电汽增量值以TagClassValue分组
    '''
    if energy == "水":
        sql = "SELECT (Cast(t.WaterSum as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionDate FROM [DB_MICS].[dbo].[WaterEnergy] t with (INDEX =IX_WaterEnergy)  WHERE t.TagClassValue = '" + TagClassValue + "' AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionDate,t.WaterSum order by t.CollectionDate"
    elif energy == "电":
        sql = "SELECT (Cast(t.ZGL as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionDate  FROM [DB_MICS].[dbo].[ElectricEnergy] t with (INDEX =IX_ElectricEnergy)  WHERE t.TagClassValue = '" + TagClassValue + "' AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionDate,t.ZGL order by t.CollectionDate"
    elif energy == "汽":
        sql = "SELECT (Cast(t.SumValue as float))*(select Cast([Proportion] as float) from [DB_MICS].[dbo].[ElectricProportion] where [ProportionType] = '"+energy+"'),t.CollectionDate  FROM [DB_MICS].[dbo].[SteamEnergy] t with (INDEX =IX_SteamEnergy)  WHERE t.TagClassValue = '" + TagClassValue + "' AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' group by t.CollectionDate,t.SumValue order by t.CollectionDate"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    return re
@energySteam.route('/energydetail', methods=['POST', 'GET'])
def energydetail():
    '''
    能耗明细
    return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            EnergyClass = data.get("EnergyClass")
            AreaName = data.get("AreaName")
            TagClassValue = data.get("TagClassValue")
            dic_lisct = []
            if TagClassValue != None and TagClassValue != "":
                tagsoclass = energydetailStatisticsbytag(TagClassValue, StartTime, EndTime, EnergyClass)
                for tagvalue in tagsoclass:
                    tag_dict = {}
                    tag_dict["时间"] = tagvalue[1]
                    tag_dict["能耗量"] = roundtwo(tagvalue[0])
                    dic_lisct.append(tag_dict)
            else:
                if AreaName == "" or AreaName == None:
                    energy_areas = energyStatisticsbyarea(StartTime, EndTime, EnergyClass)
                    dict_energy_areas = {letter: score for score, letters in energy_areas for letter in letters.split(",")}
                    areas = db_session.query(AreaTable).filter().all()
                    for area in areas:
                        dic_lisct_i = {}
                        dic_lisct_i["车间"] = area.AreaName
                        if area.AreaName in dict_energy_areas.keys():
                            dic_lisct_i["能耗量"] = roundtwo(dict_energy_areas[area.AreaName])
                        else:
                            dic_lisct_i["能耗量"] = ""
                        dic_lisct.append(dic_lisct_i)
                # else:
                #     oc_list = []
                #     oclass = db_session.query(TagDetail).filter(TagDetail.AreaName == AreaName).all()
                #     for oc in oclass:
                #         oc_list.append(oc.TagClassValue)
                #     energy_tags = energydetailStatistics(oc_list, StartTime, EndTime, EnergyClass)
                #     dict_energy_areas = {letter: score for score, letters in energy_tags for letter in letters.split(",")}
                #     dic_lisct_i = {}
                #     for oc in oclass:
                #         if oc.TagClassValue in dict_energy_areas.keys():
                #             dic_lisct_i[oc.TagClassValue] = dict_energy_areas[oc.TagClassValue]
                #         else:
                #             dic_lisct_i[oc.TagClassValue] = ""
            dir["row"] = dic_lisct
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "能耗明细查询报错Error：" + str(e), current_user.Name)

def roundtwo(rod):
    if rod == None or rod == "" or rod == b'':
        return 0.0
    else:
        if float(rod) < 0:
            return 0.0
        return round(float(rod), 2)
def energyStatisticsteamtotal(StartTime, EndTime, TimeClass):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy:
    :return:获取某段时间汽能总值
    '''
    if TimeClass == "日":
        reend = db_session.query(SteamTotalMaintain.SumValue).filter(
            SteamTotalMaintain.SumValue != None, SteamTotalMaintain.SumValue != '0.0',
            SteamTotalMaintain.CollectionDay == EndTime[0:10]).order_by(desc("CollectionDate")).first()
        restar = db_session.query(SteamTotalMaintain.SumValue).filter(
            SteamTotalMaintain.SumValue != None, SteamTotalMaintain.SumValue != '0.0',
            SteamTotalMaintain.CollectionDay == StartTime[0:10]).order_by(("CollectionDate")).first()
    elif TimeClass == "月":
        reend = db_session.query(SteamTotalMaintain.SumValue).filter(
            SteamTotalMaintain.SumValue != None, SteamTotalMaintain.SumValue != '0.0',
            SteamTotalMaintain.CollectionMonth == EndTime[0:7]).order_by(desc("CollectionDate")).first()
        restar = db_session.query(SteamTotalMaintain.SumValue).filter(
            SteamTotalMaintain.SumValue != None, SteamTotalMaintain.SumValue != '0.0',
            SteamTotalMaintain.CollectionMonth == StartTime[0:7]).order_by(("CollectionDate")).first()
    else:
        reend = db_session.query(SteamTotalMaintain.SumValue).filter(
            SteamTotalMaintain.SumValue != None, SteamTotalMaintain.SumValue != '0.0',
            SteamTotalMaintain.CollectionYear == EndTime[0:4]).order_by(desc("CollectionDate")).first()
        restar = db_session.query(SteamTotalMaintain.SumValue).filter(
            SteamTotalMaintain.SumValue != None, SteamTotalMaintain.SumValue != '0.0',
            SteamTotalMaintain.CollectionYear == StartTime[0:4]).order_by(("CollectionDate")).first()
    if reend != None and restar != None:
        return round(float(reend[0]) - float(restar[0]), 2)
    else:
        return 0

@energySteam.route('/steamlossanalysis', methods=['POST', 'GET'])
def steamlossanalysis():
    '''
    管损分析
    return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            EnergyClass = "汽"
            AreaName = data.get("AreaName")
            TimeClass = data.get("TimeClass")
            oc_list = []
            if AreaName == "" or AreaName == None:
                tags = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()
            else:
                tags = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass,
                                                          TagDetail.AreaName == AreaName).all()
            for tag in tags:
                oc_list.append(tag.TagClassValue)
            reto = energyStatistics(oc_list, StartTime, EndTime, EnergyClass)
            totalm = energyStatisticsteamtotal(StartTime, EndTime, TimeClass)
            dir["inputSteam"] = totalm
            dir["outputSteam"] = reto
            if reto > 0:
                losst = totalm - reto
                if losst > 0:
                    lossr = str(round((losst/totalm)*100, 2)) + "%"
                else:
                    lossr = "100%"
            else:
                losst = totalm
                lossr = "100%"
            dir["PipeDamageRate"] = lossr
            dir["PipeDamage"] = round(float(losst), 2)
            unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == EnergyClass).first()[0]
            dir["Unit"] = unit
            dir_list = []
            if TimeClass == "日":
                recurr = energyStatisticshour(oc_list, StartTime, EndTime, EnergyClass)
                dictcurr = {letter: score for score, letters in recurr for letter in letters.split(",")}
                for myhour in constant.myHours:
                    dir_list_i = {}
                    timehou = StartTime[0:11] + myhour
                    dir_list_i["时间"] = timehou
                    stem = 0
                    if timehou in dictcurr.keys():
                        stem = round(float(dictcurr[timehou]), 2)
                    lossh = totalm - stem
                    sttimeArray = time.strptime(timehou, '%Y-%m-%d %H')
                    sttime = int(time.mktime(sttimeArray))
                    nowtime = int(round(time.time()))
                    if sttime > nowtime:
                        lossh = ""
                    dir_list_i["管损"] = lossh
                    dir_list.append(dir_list_i)
            elif TimeClass == "月":
                recurry = energyStatisticsday(oc_list, StartTime, EndTime, EnergyClass)
                dictcurry = {letter: score for score, letters in recurry for letter in letters.split(",")}
                for myday in constant.mydays:
                    dir_list_i = {}
                    timeday = StartTime[0:8] + myday
                    dir_list_i["时间"] = timeday
                    stemy = 0
                    if timeday in dictcurry.keys():
                        stemy = round(float(dictcurry[timeday]), 2)
                    lossd = totalm - stemy
                    sttimeArray = time.strptime(timeday, '%Y-%m-%d')
                    sttime = int(time.mktime(sttimeArray))
                    nowtime = int(round(time.time()))
                    if sttime > nowtime:
                        lossd = ""
                    dir_list_i["管损"] = lossd
                    dir_list.append(dir_list_i)
            elif TimeClass == "年":
                recurrm = energyStatisticsmonth(oc_list, StartTime, EndTime, EnergyClass)
                dictcurrm = {letter: score for score, letters in recurrm for letter in letters.split(",")}
                for mymonth in constant.mymonths:
                    dir_list_i = {}
                    timemonth = StartTime[0:5] + mymonth
                    dir_list_i["时间"] = timemonth
                    stemm = 0
                    if timemonth in dictcurrm.keys():
                        stemm = round(float(dictcurrm[timemonth]), 2)
                    lossy = totalm - stemm
                    sttimeArray = time.strptime(timemonth, '%Y-%m')
                    sttime = int(time.mktime(sttimeArray))
                    nowtime = int(round(time.time()))
                    if sttime > nowtime:
                        lossy = ""
                    dir_list_i["管损"] = lossy
                    dir_list.append(dir_list_i)
            dir["row"] = dir_list
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "管损分析查询报错Error：" + str(e), current_user.Name)

@energySteam.route('/steamtotal', methods=['POST', 'GET'])
def steamtotal():
    '''
    return:
    '''
    if request.method == 'GET':
        try:
            dir = {}
            oclass = db_session.query(SteamTotalMaintain).filter(SteamTotalMaintain.SumValue != None, SteamTotalMaintain.SumValue != '0.0').order_by(desc("ID")).first()
            dir_oc = {}
            dir_oc["flowValue"] = round(float(oclass.FlowValue), 2)
            dir_oc["sumValue"] = round(float(oclass.SumValue), 2)
            dir_oc["SteamWD"] = round(float(oclass.WD), 2)
            dir[oclass.TagClassValue] = dir_oc
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "SteamTotalMaintain查询报错Error：" + str(e), current_user.Name)