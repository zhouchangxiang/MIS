import redis
from flask import Blueprint, render_template, request, make_response, send_file
import json
import datetime
from sqlalchemy import desc
from dbset.database.db_operate import db_session, pool
from dbset.main.BSFramwork import AlchemyEncoder
from flask_login import login_required, logout_user, login_user, current_user, LoginManager
import calendar

from handlers.energymanager.energy_manager import energyStatistics, energyStatisticsCost
from models.SystemManagement.core import RedisKey, ElectricEnergy, WaterEnergy, SteamEnergy, LimitTable, Equipment, \
    AreaTable, Unit, TagClassType, TagDetail, BatchMaintain
from models.SystemManagement.system import EarlyWarning, EarlyWarningLimitMaintain, WaterSteamBatchMaintain, \
    AreaTimeEnergyColour, ElectricProportion, IncrementStreamTable, SteamTotal
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
            oc_list = []
            if AreaName == "" or AreaName == None:
                tags = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()
            else:
                tags = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass,
                                                          TagDetail.AreaName == AreaName).all()
            for tag in tags:
                oc_list.append(tag.TagClassValue)
            dic_lisct = []
            if EnergyClass == "水":
                sql = "SELECT distinct(t.CollectionDate),t.WaterSum,t.WaterFlow FROM [DB_MICS].[dbo].[WaterEnergy] t with (INDEX =IX_WaterEnergy)  WHERE t.TagClassValue in (" + str(
                    oc_list)[
                                                                                                                                                                             1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' order by t.CollectionDate"
                re = db_session.execute(sql).fetchall()
                db_session.close()
                for i in re:
                    dic_lisct_i = {}
                    dic_lisct_i["时间"] = i[0]
                    dic_lisct_i["累计量"] = roundtwo(i[1])
                    dic_lisct_i["瞬时量"] = roundtwo(i[2])
                    dic_lisct.append(dic_lisct_i)
            elif EnergyClass == "电":
                sql = "SELECT distinct(t.CollectionDate),t.ZGL FROM [DB_MICS].[dbo].[ElectricEnergy] t with (INDEX =IX_ElectricEnergy)  WHERE t.TagClassValue in (" + str(
                    oc_list)[
                                                                                                                                                                       1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' order by t.CollectionDate"

                re = db_session.execute(sql).fetchall()
                db_session.close()
                for i in re:
                    dic_lisct_i = {}
                    dic_lisct_i["时间"] = i[0]
                    dic_lisct_i["总功率"] = roundtwo(i[1])
                    dic_lisct.append(dic_lisct_i)
            elif EnergyClass == "汽":
                sql = "SELECT distinct(t.CollectionDate),t.SumValue,t.FlowValue,t.Volume,t.WD  FROM [DB_MICS].[dbo].[SteamEnergy] t with (INDEX =IX_SteamEnergy)  WHERE t.TagClassValue in (" + str(
                    oc_list)[
                                                                                                                                                                                                                                                   1:-1] + ") AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "' order by t.CollectionDate"
                re = db_session.execute(sql).fetchall()
                db_session.close()
                for i in re:
                    dic_lisct_i = {}
                    dic_lisct_i["时间"] = i[0]
                    dic_lisct_i["累计量"] = roundtwo(i[1])
                    dic_lisct_i["瞬时量"] = roundtwo(i[2])
                    dic_lisct_i["体积"] = roundtwo(i[3])
                    dic_lisct_i["温度"] = roundtwo(i[4])
                    dic_lisct.append(dic_lisct_i)
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
            sts = db_session.query(SteamTotal).filter(SteamTotal.MaintainTime.between(StartTime, EndTime)).all()
            total = 0.0
            for st in sts:
                total = total + float(st.TotalSumValue)
            dir["inputSteam"] = total
            dir["outputSteam"] = reto
            if reto > 0:
                losst = total - reto
                if losst > 0:
                    lossr = str(round((losst/total)*100, 2)) + "%"
                else:
                    lossr = "100%"
            else:
                losst = total
                lossr = "100%"
            dir["PipeDamageRate"] = lossr
            dir["PipeDamage"] = losst
            unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == EnergyClass).first()[0]
            dir["Unit"] = unit
            dir_list = []
            if TimeClass == "日":
                for i in range(int(StartTime[11:13]), int(EndTime[11:13]) + 1):
                    stasH = StartTime[0:11] + addzero(i) + ":00:00"
                    endsH = StartTime[0:11] + addzero(i) + ":59:59"
                    dir_list_i = {}
                    dir_list_i["时间"] = StartTime[0:11] + addzero(i)
                    re = energyStatistics(oc_list, stasH, endsH, EnergyClass)
                    stsm = db_session.query(SteamTotal).filter(
                        SteamTotal.MaintainTime.between(StartTime, EndTime)).all()
                    totalm = 0.0
                    for stm in stsm:
                        totalm = totalm + float(stm.TotalSumValue)
                    loss = totalm - re
                    dir_list_i["管损"] = loss
                    dir_list.append(dir_list_i)
            elif TimeClass == "月":
                for i in range(int(StartTime[8:10]), int(EndTime[8:10])+1):
                    stae = StartTime[0:8] + addzero(i) + " 00:00:00"
                    ende = StartTime[0:8] + addzero(i) + " 23:59:59"
                    dir_list_i = {}
                    dir_list_i["时间"] = StartTime[0:8] + addzero(i)
                    re = energyStatistics(oc_list, stae, ende, EnergyClass)
                    stsm = db_session.query(SteamTotal).filter(SteamTotal.MaintainTime.between(StartTime, EndTime)).all()
                    totalm = 0.0
                    for stm in stsm:
                        totalm = totalm + float(stm.TotalSumValue)
                    loss = totalm - re
                    dir_list_i["管损"] = loss
                    dir_list.append(dir_list_i)
            elif TimeClass == "年":
                for i in range(int(StartTime[5:7]), int(EndTime[5:7])+1):
                    emonth = getMonthFirstDayAndLastDay(StartTime[0:4], i)
                    staeM = datetime.datetime.strftime(emonth[0], "%Y-%m-%d %H:%M:%S")
                    endeM = datetime.datetime.strftime(emonth[0], "%Y-%m-%d") + " 23:59:59"
                    dir_list_i = {}
                    dir_list_i["时间"] = StartTime[0:8] + addzero(i)
                    re = energyStatistics(oc_list, staeM, endeM, EnergyClass)
                    stsm = db_session.query(SteamTotal).filter(
                        SteamTotal.MaintainTime.between(StartTime, EndTime)).all()
                    totalm = 0.0
                    for stm in stsm:
                        totalm = totalm + float(stm.TotalSumValue)
                    loss = totalm - re
                    dir_list_i["管损"] = loss
                    dir_list.append(dir_list_i)
            dir["row"] = dir_list
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "管损分析查询报错Error：" + str(e), current_user.Name)