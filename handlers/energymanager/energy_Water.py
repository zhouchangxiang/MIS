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
from models.SystemManagement.core import RedisKey, ElectricEnergy, WaterEnergy, WaterEnergy, LimitTable, Equipment, \
    AreaTable, Unit, TagClassType, TagDetail, BatchMaintain
from models.SystemManagement.system import EarlyWarning, EarlyWarningLimitMaintain, WaterSteamBatchMaintain, \
    AreaTimeEnergyColour, ElectricProportion, IncrementWaterTable, WaterSteamPrice
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

energyWater = Blueprint('energyWater', __name__, template_folder='templates')

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


def energyWaterSelect(data):
    if request.method == 'GET':
        try:
            dir = {}
            data = request.values
            Area = data.get("Area")
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            energy = "水"
            watcount = 0.0
            if Area is not None and Area != "":
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == energy,
                                                            TagDetail.AreaName == Area).all()
            else:
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == energy).all()
            oc_list = []
            for oc in oclass:
                oc_list.append(oc.TagClassValue)
            if len(oc_list) > 0:
                wattongji = energyStatistics(oc_list, StartTime, EndTime, energy)
            else:
                wattongji = 0.0
            dir["type"] = "水"
            dir["value"] = wattongji
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


@energyWater.route('/water_report', methods=['GET'])
def get_water():
    """
    获取水报表的数据接口
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
                   'from [DB_MICS].[dbo].[IncrementWaterTable] where ID not in ' + '(select top ' + str((current_page-1) * pagesize) + ' ID from ' \
                    '[DB_MICS].[dbo].[IncrementWaterTable] where cast(IncremenValue as float) != 0.0 ' + 'and AreaName=' + "'" + area_name + "'" + ' and CollectionDate between ' + "'" + start_time + "'" + " and " \
                   "'" + end_time + "'" + ' order by CollectionDate asc, ID asc)' + 'and AreaName=' + "'" + area_name + "'" + 'and cast(IncremenValue as float) != 0.0 and CollectionDate between ' + "'" + start_time + "'" + " and " + "'" + end_time + "'" + ' order by CollectionDate asc, ID asc'

            result3 = db_session.execute(rows).fetchall()
            total = 'select count(ID) as total from [DB_MICS].[dbo].[IncrementWaterTable] where cast(IncremenValue as float) != 0.0 and AreaName=' + "'" + area_name + "'" + ' and CollectionDate between ' + "'" + start_time + "'" + " and" + "'" + end_time + "'"
            result2 = db_session.execute(total).fetchall()
            tag_list = db_session.query(TagDetail).filter(TagDetail.AreaName == area_name, TagDetail.EnergyClass == '水').all()
            tag_point = [index.TagClassValue for index in tag_list]
            data = []
            for item in result3:
                query_steam = db_session.query(WaterEnergy).filter(WaterEnergy.ID == item.CalculationID).first()
                query_tagdetai = db_session.query(TagDetail).filter(TagDetail.TagClassValue == item.TagClassValue).first()
                tag_area = query_tagdetai.FEFportIP
                dict1 = {'ID': query_steam.ID, 'WaterFlow': query_steam.WaterFlow, 'WaterSum': query_steam.WaterSum, 'SumWUnit': query_steam.SumWUnit,
                         'AreaName': item.AreaName, 'CollectionDate': str(item.CollectionDate),
                         'IncremenValue': item.IncremenValue, 'TagClassValue': tag_area}
                data.append(dict1)
            if tag_point:
                price_sql = "select sum(t1.price)*0.0001*1.2 total_price from (select TagClassValue,sum(cast(IncremenValue" \
                            " as float)) as price from [DB_MICS].[dbo].[IncrementWaterTable] where cast(IncremenValue as" \
                            " float) != 0.0 and TagClassValue in " + (str(tag_point).replace('[', '(')).replace(']', ')') + " and CollectionDate between " + "'" + start_time + "'" + " and " + "'" + end_time + "'" + "group by TagClassValue) t1"
                total_price = db_session.execute(price_sql).fetchall()
                price = 0 if total_price[0]['total_price'] is None else str(round(total_price[0]['total_price'], 2))
                return json.dumps({'rows': data, 'total_column': result2[0]['total'], 'price': price}, cls=AlchemyEncoder, ensure_ascii=False)
            else:
                price_sql = "select sum(t1.price)*0.0001*1.2 total_price from (select TagClassValue,sum(cast(IncremenValue" \
                           " as float)) as price from [DB_MICS].[dbo].[IncrementWaterTable] where cast(IncremenValue as" \
                           " float) != 0.0 and AreaName=" + "'" + area_name + "'" + " and CollectionDate between " + "'" + start_time + "'" + " and " + "'" + end_time + "'" + "group by TagClassValue) t1"
                total_price = db_session.execute(price_sql).fetchall()
                price = 0 if total_price[0]['total_price'] is None else str(round(total_price[0]['total_price'], 2))
                return json.dumps({'rows': result3, 'total_column': result2[0]['total'], 'price': price}, cls=AlchemyEncoder, ensure_ascii=False)
        else:
            price_sql = "select sum(t1.price)*0.0001*1.2 total_price from (select TagClassValue,sum(cast(IncremenValue" \
                        " as float)) as price from [DB_MICS].[dbo].[IncrementWaterTable] where cast(IncremenValue as" \
                        " float) != 0.0 and CollectionDate between " + "'" + start_time + "'" + " and " + "'" + end_time + "'" + "group by TagClassValue) t1"
            total_price = db_session.execute(price_sql).fetchall()
            price = 0 if total_price[0]['total_price'] is None else str(round(total_price[0]['total_price'], 2))
            rows = 'select top ' + str(pagesize) + ' CalculationID,TagClassValue,AreaName,IncremenValue,CollectionDate ' + 'from [DB_MICS].[dbo].[IncrementWaterTable] where ' \
                   'ID not in ' + '(select top ' + str((current_page-1) * pagesize) + ' ID from ' \
                   '[DB_MICS].[dbo].[IncrementWaterTable] where cast(IncremenValue as float) != 0.0 and CollectionDate between ' + "'" + start_time + "'" + " and " +\
                   "'" + end_time + "'" + ' order by CollectionDate asc, ID asc)' + 'and cast(IncremenValue as float) != 0.0 and CollectionDate between ' + "'" + start_time + "'" + " and " + "'" + end_time + "'" + ' order by CollectionDate asc, ID asc'
            result3 = db_session.execute(rows).fetchall()
            total = 'select count(ID) as total from [DB_MICS].[dbo].[IncrementWaterTable] where cast(IncremenValue as float) != 0.0 and CollectionDate between ' + "'" + start_time + "'" + " and" + "'" + end_time + "'"
            result2 = db_session.execute(total).fetchall()
            data = []
            for item in result3:
                if item.CalculationID and item.TagClassValue:
                    query_water = db_session.query(WaterEnergy).filter(WaterEnergy.ID == item.CalculationID).first()
                    query_tagdetai = db_session.query(TagDetail).filter(TagDetail.TagClassValue == item.TagClassValue).first()
                    tag_area = query_tagdetai.FEFportIP
                    dict1 = {'ID': query_water.ID, 'WaterFlow': query_water.WaterFlow, 'WaterSum': query_water.WaterSum, 'SumWUnit': query_water.SumWUnit,
                             'AreaName': item.AreaName, 'CollectionDate': str(item.CollectionDate),
                             'IncremenValue': item.IncremenValue, 'TagClassValue': tag_area}
                    data.append(dict1)
            return json.dumps({'rows': data, 'total_column': result2[0]['total'], 'price': price}, cls=AlchemyEncoder, ensure_ascii=False)
    except Exception as e:
        print(e)
        insertSyslog("error", "能耗查询报错Error：" + str(e), current_user.Name)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@energyWater.route('/watertrendlookboard', methods=['POST', 'GET'])
def watertrendlookboard():
    '''
    能耗看板的水能分类
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            AreaName = data.get("AreaName")
            EnergyClass = "水"
            if AreaName == None or AreaName == "":
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()
            else:
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass, TagDetail.AreaName == AreaName).all()
            oc_list_S = []
            oc_list_G = []
            oc_list_Y = []
            for oc in oclass:
                if "深井水" in oc.FEFportIP:
                    oc_list_S.append(oc.TagClassValue)
                elif "灌溉水" in oc.FEFportIP:
                    oc_list_G.append(oc.TagClassValue)
                elif "饮用水" in oc.FEFportIP:
                    oc_list_Y.append(oc.TagClassValue)
            if len(oc_list_S)>0:
                re_sum_S = energyStatistics(oc_list_S, StartTime, EndTime, EnergyClass)
                sj = db_session.query(WaterSteamPrice.PriceValue).filter(WaterSteamPrice.PriceType == "深井水", WaterSteamPrice.IsEnabled == "是").first()
                dir["SJ"] = round(re_sum_S, 2)
                dir["SJcost"] = round((0 if sj is None else float(sj[0]))*re_sum_S, 2)
            else:
                dir["SJ"] = 0
                dir["SJcost"] = 0
            if len(oc_list_G)>0:
                re_sum_G = energyStatistics(oc_list_G, StartTime, EndTime, EnergyClass)
                gg = db_session.query(WaterSteamPrice.PriceValue).filter(WaterSteamPrice.PriceType == "灌溉水",
                                                         WaterSteamPrice.IsEnabled == "是").first()
                dir["GG"] =round(re_sum_G, 2)
                dir["GGcost"] = round((0 if gg is None else float(gg[0])) * re_sum_G, 2)
            else:
                dir["GG"] = 0
                dir["GGcost"] = 0
            if len(oc_list_Y)>0:
                re_sum_Y = energyStatistics(oc_list_Y, StartTime, EndTime, EnergyClass)
                yy = db_session.query(WaterSteamPrice.PriceValue).filter(WaterSteamPrice.PriceType == "饮用水",
                                                         WaterSteamPrice.IsEnabled == "是").first()
                dir["YY"] = round(re_sum_Y, 2)
                dir["YYcost"] = round((0 if yy is None else float(yy[0])) * re_sum_Y, 2)
            else:
                dir["YY"] = 0
                dir["YYcost"] = 0
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "能耗看板的能耗看板的水能分类查询报错Error：" + str(e), current_user.Name)

@energyWater.route('/flowvaluebaobiao', methods=['POST', 'GET'])
def flowvaluebaobiao():
    '''
    瞬时报表
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            TagClassValue = data.get("TagClassValue")
            EnergyClass = data.get("EnergyClass")
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            tag = db_session.query(TagDetail).filter(TagDetail.TagClassValue == TagClassValue).first()
            data_list = []
            oclass = flowvaluesql(EnergyClass, TagClassValue, StartTime, EndTime)
            for oc in oclass:
                tag = db_session.query(TagDetail).filter(TagDetail.TagClassValue == oc.TagClassValue).first()
                dict_data = {"TagClassValue": tag.FEFportIP, "FlowValue": round(0 if oc[0]['FlowValue'] is None else float(oc[0]['FlowValue']), 2), "AreaName": tag.AreaName, "Unit": oc[0]['FlowUnit'], "CollectionDate": oc[0]['CollectionDate']}
                data_list.append(dict_data)
            dir["row"] = data_list
            dir["total"] = len(oclass)
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "统计报表查询报错Error：" + str(e), current_user.Name)
@energyWater.route('/flowvalueexcelout', methods=['POST', 'GET'])
def flowvalueexcelout():
    '''
    导出原始数据
    :return:
    '''
    data = request.values
    if request.method == 'GET':
        TagClassValue = data.get("TagClassValue")
        EnergyClass = data.get("EnergyClass")
        StartTime = data.get("StartTime")
        EndTime = data.get("EndTime")
        output = exportxflow(TagClassValue, EnergyClass, StartTime, EndTime)
        resp = make_response(output.getvalue())
        resp.headers["Content-Disposition"] = "attachment; filename=testing.xlsx"
        resp.headers['Content-Type'] = 'application/x-xlsx'
        return resp


def exportxflow(TagClassValue, EnergyClass,  StartTime, EndTime):
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
    tag = db_session.query(TagDetail).filter(TagDetail.TagClassValue == TagClassValue).first()

    # 写入列名
    columns = ['采集点', '瞬时量', '单位', '区域', '采集时间']
    for item in columns:
        worksheet.write(0, col, item, cell_format)
        col += 1
    # 写入数据
    i = 1
    reclass = flowvaluesql(EnergyClass, tag.TagClassValue, StartTime, EndTime)
    for oc in reclass:
        for cum in columns:
            if cum == '采集点':
                worksheet.write(i, columns.index(cum), tag.FEFportIP)
            if cum == '瞬时量':
                worksheet.write(i, columns.index(cum), round(0 if oc[0]['FlowValue'] is None else float(oc[0]['FlowValue']), 2))
            if cum == '区域':
                worksheet.write(i, columns.index(cum), tag.AreaName)
            if cum == '单位':
                worksheet.write(i, columns.index(cum), oc[0]['FlowUnit'])
            if cum == '采集时间':
                worksheet.write(i, columns.index(cum), oc[0]['CollectionDate'])
        i = i + 1
    writer.close()
    output.seek(0)
    return output

def flowvaluesql(EnergyClass, TagClassValue, StartTime, EndTime):
    if EnergyClass == "水":
        sql = "SELECT t.WaterFlow AS FlowValue,t.FlowWUnit AS FlowUnit,t.CollectionDate AS CollectionDate FROM [DB_MICS].[dbo].[WaterEnergy] t with (INDEX =IX_WaterEnergy) " \
              "WHERE t.TagClassValue = '" + TagClassValue + "' AND t.CollectionDate BETWEEN " + "'" + StartTime + "' AND " + "'" + EndTime + "' ORDER BY t.CollectionDate"
        oclass = db_session.execute(sql).fetchall()
        db_session.close()
    elif EnergyClass == "汽":
        if TagClassValue == "S_AllArea_Value":
            sql = "SELECT t.FlowValue AS FlowValue,t.FlowUnit AS FlowUnit,t.CollectionDate AS CollectionDate FROM [DB_MICS].[dbo].[SteamTotalMaintain] t with (INDEX =IX_SteamTotalMaintain) " \
                  "WHERE t.CollectionDate BETWEEN " + "'" + StartTime + "' AND " + "'" + EndTime + "' ORDER BY t.CollectionDate"
        else:
            sql = "SELECT t.FlowValue AS FlowValue,t.FlowUnit AS FlowUnit,t.CollectionDate AS CollectionDate FROM [DB_MICS].[dbo].[SteamEnergy] t with (INDEX =IX_SteamEnergy) " \
                  "WHERE t.TagClassValue = '" + TagClassValue + "' AND t.CollectionDate BETWEEN " + "'" + StartTime + "' AND " + "'" + EndTime + "' ORDER BY t.CollectionDate"
        oclass = db_session.execute(sql).fetchall()
        db_session.close()
    return oclass