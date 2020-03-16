import redis
from flask import Blueprint, render_template, request, make_response, send_file
import json
import datetime
from sqlalchemy import desc
from dbset.database.db_operate import db_session,pool
from dbset.main.BSFramwork import AlchemyEncoder
from flask_login import login_required, logout_user, login_user,current_user,LoginManager
import calendar
from models.SystemManagement.core import RedisKey, ElectricEnergy, WaterEnergy, SteamEnergy, LimitTable, Equipment, \
    PriceList, AreaTable, Unit, TagClassType, TagDetail, BatchMaintain
from models.SystemManagement.system import EarlyWarning, EarlyWarningLimitMaintain, WaterSteamBatchMaintain, \
    AreaTimeEnergyColour, ElectricProportion
from tools.common import insert,delete,update
from dbset.database import constant
from dbset.log.BK2TLogger import logger,insertSyslog
import datetime
import arrow
import time
import numpy as np
import pandas as pd
from io import BytesIO
from flask import Flask, send_file,make_response

energyWater = Blueprint('energyWater', __name__, template_folder='templates')

arro = arrow.now()
pool = redis.ConnectionPool(host=constant.REDIS_HOST)
redis_conn = redis.Redis(connection_pool=pool)

from datetime import timedelta
def getWeekDaysByNum(m, n):#获取第几周到第几周每周的第一天和最后一天
    # 当前日期
    now = datetime.now().date()
    dayDict = {}
    for x in range(m, n + 1):
    	#前几周
        if x < 0:
            lDay = now - timedelta(days=now.weekday() + (7 * abs(x)))
        #本周
        elif x == 0:
            lDay = now - timedelta(days=now.weekday())
        #后几周
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
        return str(int(str0)-1)+"-"+"12"
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
def energymoney(count, name):
    prices = db_session.query(PriceList).filter(PriceList.IsEnabled == "是").all()
    for pr in prices:
        if pr.PriceName == name:
            return float(count)*float(pr.PriceValue)
def wattongji(oc, EndTime, StartTime, elecount):
    cur = \
        db_session.query(WaterEnergy.WaterSum).filter(
            WaterEnergy.TagClassValue == oc.TagClassValue,
            WaterEnergy.CollectionDate.like("%"+EndTime+"%")).order_by(
            desc("CollectionDate")).first()
    las = db_session.query(WaterEnergy.WaterSum).filter(
        WaterEnergy.TagClassValue == oc.TagClassValue,
        WaterEnergy.CollectionDate.like("%"+StartTime+"%")).order_by(("CollectionDate")).first()
    return curcutlas(cur, las, elecount)
def energyWaterSelect(data):
    if request.method == 'GET':
        try:
            dir = {}
            data = request.values
            Area = data.get("Area")
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            if EndTime is None:
                EndTime = StartTime
            watcount = 0.0
            if Area is not None and Area != "":
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == "水",
                                                            TagDetail.AreaName == Area).all()
            else:
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == "水").all()
            for oc in oclass:
                watcount = wattongji(oc, StartTime, EndTime, watcount)
            dir["type"] = "水"
            dir["wattongji"] = wattongji
            unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == "水").first()[0]
            dir["unit"] = unit
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            insertSyslog("error", "能耗查询报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@energyWater.route('/energyPreview', methods=['POST', 'GET'])
def energyPreview():
    '''
    能耗预览
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
            curryear = str(currentyear)
            lastyear = str(int(curryear) - 1)
            currmonth = str(currentyear) + "-" + addzero(int(currentmonth))
            lastmonth = strlastMonth(currmonth)
            currday = str(currentyear) + "-" + addzero(currentmonth) + "-" + addzero(currentday)
            vv = datetime.datetime.strptime(currday, "%Y-%m-%d")
            lastday = str(vv + datetime.timedelta(days=-1))[0:10]
            EnergyType = data.get("energyType")
            elecount = 0.0
            watcount = 0.0
            stecount = 0.0
            laststecount = 0.0
            lastwatcount = 0.0
            lastelecount = 0.0
            oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == "水").all()
            # if datime == "年":
            zerocurrMonth = str(currentyear) + addzero(currentmonth)
            lastYMonth = str(int(currentyear)-1) + addzero(currentmonth)
            zerolastYMonth = str(int(currentyear) - 1) + "-01"
            for oc in oclass:
                Tag = oc.TagClassValue[0:1]
                if Tag == "W":
                    watcount = wattongji(oc, currmonth, zerocurrMonth, watcount)
                    lastwatcount = wattongji(oc, lastYMonth, zerolastYMonth, lastwatcount)
            curryeartotal = round(elecount + watcount + stecount, 2)
            lastyeartotal = round(lastelecount + lastwatcount + laststecount, 2)
            dir["thisYearCon"] =curryeartotal#年能耗量
            dir["lastYearCon"] =lastyeartotal  # 上年同期能耗
            cl = curryeartotal - lastyeartotal
            if cl > 0:
                percen = round((cl / lastyeartotal) * 100, 2)
            else:
                percen = 0
            dir["lastYearCompare"] = str(percen) + "%"
            if percen < 0:
                dir["lastYearCompareState"] = "bottom"
            elif percen == 0:
                dir["lastYearCompareState"] = ""
            else:
                dir["lastYearCompareState"] = "top"
            # elif datime == "月":
            zerocurrday = str(currentyear) + "-" + addzero(int(currentmonth)) + "-01"
            lastMday = strlastMonth(currmonth) + "-" + addzero(currentday)
            zerolastMday = strlastMonth(currmonth) + "-01"
            thisMonthCon = 0.0
            lastMonthCon = 0.0
            for oc in oclass:
                Tag = oc.TagClassValue[0:1]
                if Tag == "W":
                    thisMonthCon = wattongji(oc, currday, zerocurrday, thisMonthCon)
                    lastMonthCon = wattongji(oc, lastMday, zerolastMday, lastMonthCon)
            currMont = round(thisMonthCon, 2)
            lastMont = round(lastMonthCon, 2)
            dir["thisMonthCon"] = currMont#本月能耗量
            dir["lastMonthCon"] =   lastMont# 上月同期能耗量
            #上月同期百分比
            cla = currMont - lastMont
            if cla > 0:
                perce = round((cla/lastMont)*100, 2)
            else:
                perce = 0
            dir["lastMonthCompare"] = str(perce) + "%"
            if perce < 0:
                dir["lastMonthCompareState"] = "bottom"
            elif perce == 0:
                dir["lastMonthCompareState"] = ""
            else:
                dir["lastMonthCompareState"] = "top"
            month_data_list = []
            month_data_dir = {}
            for j in range(1, int(currentday) + 1):
                currdayxin = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(j)
                vv = datetime.datetime.strptime(currdayxin, "%Y-%m-%d")
                lastdayxin = str(vv + datetime.timedelta(days=-1))[0:10]
                month_data_list.append(str(j))
                count = 0.0
                month_data_dir["日期"] = currdayxin
                for oc in oclass:
                    Tag = oc.TagClassValue[0:1]
                    if Tag == "W":
                        count = wattongji(oc, currdayxin, lastdayxin, count)
                month_data_dir["本月能耗"] = count
                lastcount = 0.0
                lastMondayxin = strlastMonth(currmonth) + "-" + addzero(j)
                mm = datetime.datetime.strptime(currday, "%Y-%m-%d")
                laMondayxin = str(mm + datetime.timedelta(days=-1))[0:10]
                for oc in oclass:
                    Tag = oc.TagClassValue[0:1]
                    if Tag == "W":
                        lastcount = wattongji(oc, lastMondayxin, laMondayxin, lastcount)
                month_data_dir["上月能耗"] = lastcount
                month_data_list.append(month_data_dir)
            dir["lastMonthRow"] = month_data_list
            # elif datime == "日":
            compareday = data.get("compareDate")
            cv = datetime.datetime.strptime(compareday, "%Y-%m-%d")
            lastcompareday = str(cv + datetime.timedelta(days=-1))[0:10]
            comparedaycount = 0.0
            currdaycounts = 0.0
            for oc in oclass:
                Tag = oc.TagClassValue[0:1]
                if Tag == "W":
                    comparedaycount = wattongji(oc, compareday, lastcompareday, comparedaycount)
                    currdaycounts = wattongji(oc, currday, lastday, currdaycounts)
            dir["compareDateCon"] = round(comparedaycount, 2)
            pccss = comparedaycount - currdaycounts
            if pccss > 0:
                percencc = round((pccss/comparedaycount) * 100, 2)
            else:
                percencc = 0
            dir["comparePer"] = str(percencc) + "%"
            if percencc < 0:
                dir["comparePerState"] = "bottom"
            elif percencc == 0:
                dir["comparePerState"] = ""
            else:
                dir["comparePerState"] = "top"
            currhour = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(
                int(currentday)) + " " + addzero(currenthour)
            currzero = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(
                int(currentday)) + " " + "00"
            time_list = []
            compare_dict = {}
            for j in range(0, currenthour):
                currhour = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(
                    int(currentday)) + " " + addzero(j)
                vvc = datetime.datetime.strptime(currhour, "%Y-%m-%d %H")
                lasthour = str((vvc + datetime.timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M:%S"))[0:13]
                comparehour = compareday + " " + addzero(j)
                vxc = datetime.datetime.strptime(comparehour, "%Y-%m-%d %H")
                comparelasthour = str((vxc + datetime.timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M:%S"))[0:13]
                compare_dict["时间"] = str(j)
                current_countr = 0.0
                compare_count = 0.0
                for oc in oclass:
                    Tag = oc.TagClassValue[0:1]
                    if Tag == "W":
                        current_countr = wattongji(oc, currhour, lasthour, current_countr)
                        compare_count = wattongji(oc, comparehour, comparelasthour, compare_count)
                compare_dict["今日能耗"] = str(current_countr)
                compare_dict["对比日能耗"] = str(compare_count)
                time_list.append(compare_dict)
            dir["compareTodayRow"] = time_list
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "能耗预览查询报错Error：" + str(e), current_user.Name)

@energyWater.route('/areaTimeEnergy', methods=['POST', 'GET'])
def areaTimeEnergy():
    '''
    区域时段能耗
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
            currdate = data.get("date")#当前时间
            compareDate = data.get("compareDate")#对比日期
            AreaNames = db_session.query(AreaTable.AreaName).filter().all()
            diarea = {}
            araeY_list = []
            for AreaName in AreaNames:
                diarea["name"] = AreaName[0]
                valuelist = []
                value_dirc = {}
                oclass = db_session.query(TagDetail).filter(TagDetail.AreaName == AreaName[0],
                                                            TagDetail.EnergyClass == "水").all()
                colourclass = db_session.query(AreaTimeEnergyColour).filter(AreaTimeEnergyColour.AreaName == AreaName[0]).all()
                stop = ""
                high = ""
                middle = ""
                low = ""
                for co in colourclass:
                    if co.ColourName == "停":
                        stop = co.Colour
                    elif co.ColourName == "高":
                        high = co.Colour
                    elif co.ColourName == "中":
                        middle = co.Colour
                    elif co.ColourName == "低":
                        low = co.Colour
                colour = ""
                for j in range(0, currenthour):
                    currhour = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(
                        int(currentday)) + " " + addzero(j)
                    vv = datetime.datetime.strptime(currhour, "%Y-%m-%d %H")
                    lasthour = str((vv + datetime.timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M:%S"))[0:13]
                    dict_valuelist = {}
                    dict_valuelist["date"] = str(j)
                    vlaue = 0.0
                    for oc in oclass:
                        Tag = oc.TagClassValue[0:1]
                        if Tag == "W":
                            vlaue = wattongji(oc, currhour, lasthour, vlaue)
                    if vlaue < float(stop) or vlaue == float(stop):
                        colour = colour + "#ECF1F4"
                    elif vlaue < float(low) or vlaue == float(low):
                        colour = colour + "#F5E866"
                    elif  vlaue < float(middle) or vlaue == float(middle):
                        colour = colour + "#FBBA06"
                    elif vlaue < float(high) or vlaue == float(high):
                        colour = colour + "#FB3A06"
                    dict_valuelist["value"] = round(vlaue, 2)
                    valuelist.append(dict_valuelist)
                value_dirc["valuelist"] = valuelist
                value_dirc["backgroundColor"] = "-webkit-linear-gradient(left," + colour + ")"
                araeY_list.append(value_dirc)
            return json.dumps(araeY_list, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "区域时段能耗查询报错Error：" + str(e), current_user.Name)

@energyWater.route('/trendChart', methods=['POST', 'GET'])
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

@energyWater.route('/energyHistory', methods=['POST', 'GET'])
def energyHistory():
    '''
    能源历史数据
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            Energy = data.get("Energy")
            dir = {}
            dire = {}
            dire["name"] = Energy
            diy = []
            dix = []
            eng = {}
            uni = db_session.query(Unit.UnitValue).filter(Unit.UnitName == Energy).first()[0]
            dir["Unit"] = uni
            if Energy == "水":
                # 能耗历史数据
                CollectionDates = db_session.query(WaterEnergy.CollectionDate).distinct().filter(WaterEnergy.CollectionDate.between(StartTime,EndTime)).order_by(("CollectionDate")).all()
                for CollectionDate in CollectionDates:
                    dicss = []
                    timeArray = time.strptime(CollectionDate[0], "%Y-%m-%d %H:%M:%S")
                    timeStamp = int(time.mktime(timeArray))
                    dicss.append(1000 * timeStamp)
                    watEnergyValues = db_session.query(WaterEnergy.WaterFlow).filter(WaterEnergy.CollectionDate == CollectionDate[0]).all()
                    towatEnergyValue = 0.0
                    for watEnergyValue in watEnergyValues:
                        towatEnergyValue = towatEnergyValue + float(watEnergyValue[0])
                    dicss.append(round(float(towatEnergyValue), 2))
                    diy.append(dicss)
                #区域能耗排名
                AreaNames = db_session.query(AreaTable.AreaName).filter().all()
                totalflow = 0.0
                for AreaName in AreaNames:
                    TagClassValues = db_session.query(TagDetail.TagClassValue).filter(TagDetail.AreaName == AreaName[0]).all()
                    engsum = 0.0
                    for TagClassValue in TagClassValues:
                        watEnergyValues = db_session.query(WaterEnergy.WaterFlow).filter(WaterEnergy.TagClassValue == TagClassValue,
                            WaterEnergy.CollectionDate.between(StartTime, EndTime)).all()
                        engsum = engsum + accumulation(watEnergyValues)
                    eng[AreaName[0]] = str(round(engsum, 2))
                    totalflow = totalflow + engsum
                # 累积量
                dir["total"] = str(round(totalflow, 2))
            en = sorted(eng.items(), key=lambda x: float(x[1]), reverse=True)
            eny = []
            enx = []
            dien = {}
            dien["name"] = Energy
            for i in en:
                enx.append(i[0])
                eny.append(float(i[1]))
            dien["data"] = eny
            dir["energyRankY"] = [dien]
            dir["energyRankX"] = enx
            dire["data"] = diy
            dix.append(dire)
            dir["HistorySeries"] = dix
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "能源历史数据查询报错Error：" + str(e), current_user.Name)
