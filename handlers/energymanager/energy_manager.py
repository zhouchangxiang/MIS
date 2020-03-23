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
import math

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
#器件管理
@energy.route('/DeviceManage')
def DeviceManage():
    return render_template('./DeviceManage.html')
#价格管理
@energy.route('/PriceManage')
def PriceManage():
    return render_template('./PriceManage.html')
#单位管理
@energy.route('/UnitManage')
def UnitManage():
    return render_template('./UnitManage.html')

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
def energyStatistics(oc_list, StartTime, EndTime, energy):
    propor = db_session.query(ElectricProportion).filter(ElectricProportion.ProportionType == energy).first()
    pro = float(propor.Proportion)
    sql = "SELECT SUM(Cast(t.IncremenValue as float)) as count  FROM [DB_MICS].[dbo].[IncrementTable] t with (INDEX =IX_IncrementTable)  WHERE t.TagClassValue in ("+str(oc_list)[1:-1]+") AND t.IncremenType = " + "'" + energy + "'" + " AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    re = db_session.execute(sql).fetchall()
    print(db_session.execute(sql).fetchall())
    db_session.close()
    if len(re) > 0:
        if re[0][0] != 0.0 and re[0][0] != None:
            return round(float(re[0][0]) * pro, 2)
        else:
            return 0.0
    else:
        return 0.0
def energyselect(data):
    if request.method == 'GET':
        try:
            print(datetime.datetime.now())
            dir = {}
            currentyear = datetime.datetime.now().year
            currentmonth = datetime.datetime.now().month
            currentday = datetime.datetime.now().day
            currenthour = datetime.datetime.now().hour
            currenthour = datetime.datetime.now().hour
            curryear = str(currentyear)
            lastyear = str(int(curryear) - 1)
            currmonth = str(currentyear) + "-" + addzero(int(currentmonth))
            lastmonth = strlastMonth(currmonth)
            currday = str(currentyear) + "-" + addzero(currentmonth) + "-" + addzero(currentday)
            vv = datetime.datetime.strptime(currday, "%Y-%m-%d")
            lastday = str(vv + datetime.timedelta(days=-1))[0:10]
            data = request.values
            Area = data.get("Area")
            datime = data.get("DateTime")
            EnergyClass = data.get("EnergyClass")
            ModelFlag = data.get("ModelFlag")
            CurrentTime = data.get("CurrentTime")
            TimeClass = data.get("TimeClass")
            elecount = 0.0
            watcount = 0.0
            stecount = 0.0
            if ModelFlag == "能耗预览":
                dir_list = []
                dir_month_list = []
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()
                oc_list = []
                for oc in oclass:
                    oc_list.append(oc.TagClassValue)
                compareday = data.get("CompareDate")
                for j in range(24):
                    dir_list_dict = {}
                    dir_list_dict["日期"] = str(j)
                    comparehour = str(compareday) + " " +addzero(j)+ ":59:59"
                    lastcomparehour = str(compareday) + " " +addzero(j)+ ":00:00"
                    currhour = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(
                        int(currentday)) + " " + addzero(j)+":59:59"
                    lasthour = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(
                        int(currentday)) + " " + addzero(j)+":00:00"
                    count = energyStatistics(oc_list, lasthour, currhour, EnergyClass)
                    comperacount = energyStatistics(oc_list, lastcomparehour, comparehour, EnergyClass)
                    dir_list_dict["今日能耗"] = count
                    dir_list_dict["对比日能耗"] = comperacount
                    dir_list.append(dir_list_dict)
                curmonthdays = str(getMonthFirstDayAndLastDay(currentyear, currentmonth)[1])[8:10]
                lasmonthdays = str(getMonthFirstDayAndLastDay(strlastMonth(str(currentyear) + "-" + addzero(int(currentmonth)))[0:4], strlastMonth(str(currentyear) + "-" + addzero(int(currentmonth)))[5:7])[1])[8:10]
                for i in range(1, 32):
                    dirmonth_list_dict = {}
                    currmonthcurrday = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(int(i))+" 23:59:59"
                    currmonthlasday = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(
                        int(i)) + " 00:00:00"
                    lastmonthcurrday = strlastMonth(str(currentyear) + "-" + addzero(int(currentmonth))) + "-" + addzero(int(i))+" 23:59:59"
                    lastmonthlasday = strlastMonth(
                        str(currentyear) + "-" + addzero(int(currentmonth))) + "-" + addzero(int(i)) + " 00:0:00"
                    dirmonth_list_dict["日期"] = str(currentyear) + "-" + addzero(int(currentmonth)) + "-" + addzero(int(i))
                    if i <= int(curmonthdays):
                        monthcount = energyStatistics(oc_list, currmonthlasday, currmonthcurrday, EnergyClass)
                    else:
                        monthcount = 0.0
                    if i <= int(lasmonthdays):
                        lastmonthcount = energyStatistics(oc_list, lastmonthlasday, lastmonthcurrday, EnergyClass)
                    else:
                        lastmonthcount = 0.0
                    dirmonth_list_dict["上月能耗"] = lastmonthcount
                    dirmonth_list_dict["本月能耗"] = monthcount
                    dir_month_list.append(dirmonth_list_dict)
                dir["compareTodayRow"] = dir_list
                dir["lastMonthRow"] = dir_month_list
            elif ModelFlag == "区域能耗":
                oclass = db_session.query(TagDetail).filter(TagDetail.AreaName == Area).all()
                if datime == "年":
                    for oc in oclass:
                        Tag = oc.TagClassValue[0:1]
                        if Tag == "E":
                            elecount = eletongji(oc, curryear, lastyear, elecount)
                        elif Tag == "W":
                            watcount = wattongji(oc, curryear, lastyear, elecount)
                        elif Tag == "S":
                            stecount = stetongji(oc, curryear, lastyear, elecount)
                elif datime == "月":
                    for oc in oclass:
                        Tag = oc.TagClassValue[0:1]
                        if Tag == "E":
                            elecount = eletongji(oc, currmonth, lastmonth, elecount)
                        elif Tag == "W":
                            watcount = wattongji(oc, currmonth, lastmonth, elecount)
                        elif Tag == "S":
                            stecount = stetongji(oc, currmonth, lastmonth, elecount)
                elif datime == "日":
                    for oc in oclass:
                        Tag = oc.TagClassValue[0:1]
                        if Tag == "E":
                            elecount = eletongji(oc, currday, lastday, elecount)
                        elif Tag == "W":
                            watcount = wattongji(oc, currday, lastday, elecount)
                        elif Tag == "S":
                            stecount = stetongji(oc, currday, lastday, elecount)
                dir["ElectricValue"] = elecount
                dir["WaterValue"] = watcount
                dir["SteamValue"] = stecount
            elif ModelFlag == "成本展示":
                oclass = db_session.query(TagDetail).filter().all()
                if datime == "年":
                    for oc in oclass:
                        Tag = oc.TagClassValue[0:1]
                        if Tag == "E":
                            elecount = eletongji(oc, curryear, lastyear, elecount)
                        elif Tag == "W":
                            watcount = wattongji(oc, curryear, lastyear, elecount)
                        elif Tag == "S":
                            stecount = stetongji(oc, curryear, lastyear, elecount)
                elif datime == "月":
                    for oc in oclass:
                        Tag = oc.TagClassValue[0:1]
                        if Tag == "E":
                            elecount = eletongji(oc, currmonth, lastmonth, elecount)
                        elif Tag == "W":
                            watcount = wattongji(oc, currmonth, lastmonth, elecount)
                        elif Tag == "S":
                            stecount = stetongji(oc, currmonth, lastmonth, elecount)
                elif datime == "日":
                    for oc in oclass:
                        Tag = oc.TagClassValue[0:1]
                        if Tag == "E":
                            elecount = eletongji(oc, currday, lastday, elecount)
                        elif Tag == "W":
                            watcount = wattongji(oc, currday, lastday, elecount)
                        elif Tag == "S":
                            stecount = stetongji(oc, currday, lastday, elecount)
                dir["ElectricValue"] = round(energymoney(elecount, "电"), 2)
                dir["WaterValue"] = round(energymoney(watcount, "水"), 2)
                dir["SteamValue"] = round(energymoney(stecount, "汽"), 2)
                dir["ZCB"] = round(energymoney(elecount, "电") + energymoney(watcount, "水") + energymoney(stecount, "汽"), 2)
                #饼图
                dice = {}
                ztotal = round(energymoney(elecount, "电") + energymoney(watcount, "水") + energymoney(stecount, "汽"), 2)
                dice["name"] = "电"
                dice["y"] = float('{:.2f}'.format(round(energymoney(elecount, "电"), 2)/ztotal*100))
                dicw = {}
                dicw["name"] = "水"
                dicw["y"] = float('{:.2f}'.format(round(energymoney(watcount, "水"), 2)/ztotal*100))
                dics = {}
                dics["name"] = "汽"
                dics["y"] = float('{:.2f}'.format(round(energymoney(stecount, "汽"), 2)/ztotal*100))
                datadic = []
                datadic.append(dice)
                datadic.append(dicw)
                datadic.append(dics)
                dir["data"] = datadic
            elif ModelFlag == "区域成本":
                oclass = db_session.query(TagDetail).filter(TagDetail.AreaName == Area).all()
                if datime == "年":
                    currentyear = CurrentTime[0:4]
                    lastyear = str(int(curryear) - 1)
                    for oc in oclass:
                        Tag = oc.TagClassValue[0:1]
                        if Tag == "E":
                            elecount = eletongji(oc, curryear, lastyear, elecount)
                        elif Tag == "W":
                            watcount = wattongji(oc, curryear, lastyear, elecount)
                        elif Tag == "S":
                            stecount = stetongji(oc, curryear, lastyear, elecount)
                elif datime == "月":
                    currentmonth = CurrentTime[0:7]
                    lastM = strlastMonth(currentmonth)
                    for oc in oclass:
                        Tag = oc.TagClassValue[0:1]
                        if Tag == "E":
                            elecount = eletongji(oc, currmonth, lastmonth, elecount)
                        elif Tag == "W":
                            watcount = wattongji(oc, currmonth, lastmonth, elecount)
                        elif Tag == "S":
                            stecount = stetongji(oc, currmonth, lastmonth, elecount)
                elif datime == "日":
                    currentday = CurrentTime[0:10]
                    vv = datetime.datetime.strptime(currday, "%Y-%m-%d")
                    lastday = str(vv + datetime.timedelta(days=-1))[0:10]
                    for oc in oclass:
                        Tag = oc.TagClassValue[0:1]
                        if Tag == "E":
                            elecount = eletongji(oc, currday, lastday, elecount)
                        elif Tag == "W":
                            watcount = wattongji(oc, currday, lastday, elecount)
                        elif Tag == "S":
                            stecount = stetongji(oc, currday, lastday, elecount)
                chenbY = [round(energymoney(elecount, "电"), 2),round(energymoney(watcount, "水"), 2),round(energymoney(stecount, "汽"), 2)]
                chenbX = ["电","水","汽"]
                dir["X"] = chenbX
                dir["Y"] = chenbY
            elif ModelFlag == "区域成本排名":
                AreaNames = db_session.query(AreaTable.AreaName).filter().all()
                diarea = {}
                for AreaName in AreaNames:
                    oclass = db_session.query(TagDetail).filter(TagDetail.AreaName == AreaName[0]).all()
                    if datime == "年":
                        currentyear = CurrentTime[0:4]
                        lastyear = str(int(curryear) - 1)
                        for oc in oclass:
                            Tag = oc.TagClassValue[0:1]
                            if Tag == "E":
                                elecount = eletongji(oc, curryear, lastyear, elecount)
                            elif Tag == "W":
                                watcount = wattongji(oc, curryear, lastyear, elecount)
                            elif Tag == "S":
                                stecount = stetongji(oc, curryear, lastyear, elecount)
                    elif datime == "月":
                        currentmonth = CurrentTime[0:7]
                        lastM = strlastMonth(currentmonth)
                        for oc in oclass:
                            Tag = oc.TagClassValue[0:1]
                            if Tag == "E":
                                elecount = eletongji(oc, currmonth, lastmonth, elecount)
                            elif Tag == "W":
                                watcount = wattongji(oc, currmonth, lastmonth, elecount)
                            elif Tag == "S":
                                stecount = stetongji(oc, currmonth, lastmonth, elecount)
                    elif datime == "日":
                        currentday = CurrentTime[0:10]
                        vv = datetime.datetime.strptime(currday, "%Y-%m-%d")
                        lastday = str(vv + datetime.timedelta(days=-1))[0:10]
                        for oc in oclass:
                            Tag = oc.TagClassValue[0:1]
                            if Tag == "E":
                                elecount = eletongji(oc, currday, lastday, elecount)
                            elif Tag == "W":
                                watcount = wattongji(oc, currday, lastday, elecount)
                            elif Tag == "S":
                                stecount = stetongji(oc, currday, lastday, elecount)
                    diarea[AreaName[0]] = round((energymoney(elecount, "电") +  energymoney(watcount, "水") + energymoney(stecount, "汽")), 2)
                areavs = sorted(diarea.items(), key=lambda x: float(x[1]), reverse=True)
                areax = []
                areay = []
                for i in areavs:
                    areax.append(i[0])
                    areay.append(float(i[1]))
                dir["X"] = areax
                dir["Y"] = areay
            elif ModelFlag == "电能负荷率":
                dir["a"]=""
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
                    ret = redis_conn.hget("run_status", i.TagClassValue)
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
                data_list.append({"name": "电表", "online": elestatuss, "rate": int(100 * (elestatuss/elestatust))})
                data_list.append({"name": "水表", "online": watstatuss, "rate": int(100 * (watstatuss / watstatust))})
                data_list.append({"name": "汽表", "online": stestatuss, "rate": int(100 * (stestatuss / stestatust))})
                return json.dumps(data_list, cls=AlchemyEncoder, ensure_ascii=False)
            elif ModelFlag == "单位批次能耗":
                curryear = str(currentyear)
                lastyear = str(int(curryear) - 1)
                currmonth = str(currentyear) + "-" + addzero(int(currentmonth))
                wsbs = db_session.query(WaterSteamBatchMaintain).filter().all()
                if TimeClass == "本周":
                    re = getWeekDaysByNum(0, 0)
                    first_week_day = re[0][0]
                    end_week_day = re[0][1]
                    bats = db_session.query(BatchMaintain).filter(BatchMaintain.ProductionDate.between(first_week_day,end_week_day)).all()
                    countw = 0.0
                    counte = 0.0
                    for bat in bats:
                        countw = countw + bat.WaterConsumption
                        counte = counte + bat.ElectricConsumption
                elif TimeClass == "本月":
                    currmonth = str(currentyear) + "-" + addzero(int(currentmonth))
                    BatchMaintain
                    WaterSteamBatchMaintain
                elif TimeClass == "本年":
                    curryear = str(currentyear)
                    BatchMaintain
                    WaterSteamBatchMaintain
            elif ModelFlag == "实时预警":
                oclass = db_session.query(EarlyWarning).filter().order_by(desc("WarningDate")).all()
                dir["data"] = oclass
            elif ModelFlag == "电能负荷率":
                aa = "aa"
                #电能负荷率 = 当前视在功率 / 额定功率
            elif ModelFlag == "系统体检":
                pipe = redis_conn.pipeline(transaction=False)
                pipe.hget("hash_key", "leizhu900516")
                result = pipe.execute()
                conngoods = pipe.hget("run_status","1")
                connbads = pipe.hget("run_status", "0")
                list_bad = []
                for i in connbads:
                    list_bad.append(i.key)
                dir["连接通畅数"] = conngoods
                dir["连接阻塞数"] = connbads
            print(dir)
            print(datetime.datetime.now())
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            insertSyslog("error", "能耗查询报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@energy.route('/energyPreview', methods=['POST', 'GET'])
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
            oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyType).all()
            # if datime == "年":
            zerocurrMonth = str(currentyear) + addzero(currentmonth)
            lastYMonth = str(int(currentyear)-1) + addzero(currentmonth)
            zerolastYMonth = str(int(currentyear) - 1) + "-01"
            for oc in oclass:
                Tag = oc.TagClassValue[0:1]
                if Tag == "E":
                    elecount = eletongji(oc, zerocurrMonth, currmonth, elecount)
                    lastelecount = eletongji(oc, zerolastYMonth, lastYMonth, lastelecount)
                elif Tag == "W":
                    watcount = wattongji(oc, zerocurrMonth, currmonth, watcount)
                    lastwatcount = wattongji(oc, zerolastYMonth, lastYMonth, lastwatcount)
                elif Tag == "S":
                    stecount = stetongji(oc, zerocurrMonth, currmonth, stecount)
                    laststecount = stetongji(oc, zerolastYMonth, lastYMonth, laststecount)
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
                if Tag == "E":
                    thisMonthCon = eletongji(oc, currday, zerocurrday, thisMonthCon)
                    lastMonthCon = eletongji(oc, lastMday, zerolastMday, lastMonthCon)
                elif Tag == "W":
                    thisMonthCon = wattongji(oc, currday, zerocurrday, thisMonthCon)
                    lastMonthCon = wattongji(oc, lastMday, zerolastMday, lastMonthCon)
                elif Tag == "S":
                    thisMonthCon = stetongji(oc, currday, zerocurrday, thisMonthCon)
                    lastMonthCon = stetongji(oc, lastMday, zerolastMday, lastMonthCon)
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
                    if Tag == "E":
                        count = eletongji(oc, currdayxin, lastdayxin, count)
                    elif Tag == "W":
                        count = wattongji(oc, currdayxin, lastdayxin, count)
                    elif Tag == "S":
                        count = stetongji(oc, currdayxin, lastdayxin, count)
                month_data_dir["本月能耗"] = count
                lastcount = 0.0
                lastMondayxin = strlastMonth(currmonth) + "-" + addzero(j)
                mm = datetime.datetime.strptime(currday, "%Y-%m-%d")
                laMondayxin = str(mm + datetime.timedelta(days=-1))[0:10]
                for oc in oclass:
                    Tag = oc.TagClassValue[0:1]
                    if Tag == "E":
                        lastcount = eletongji(oc, lastMondayxin, laMondayxin, lastcount)
                    elif Tag == "W":
                        lastcount = wattongji(oc, lastMondayxin, laMondayxin, lastcount)
                    elif Tag == "S":
                        lastcount = stetongji(oc, lastMondayxin, laMondayxin, lastcount)
                month_data_dir["上月能耗"] = lastcount
                month_data_list.append(month_data_dir)
            dir["lastMonthRow"] = month_data_list
            # elif datime == "日":
            compareday = data.get("CompareDate")
            cv = datetime.datetime.strptime(compareday, "%Y-%m-%d")
            lastcompareday = str(cv + datetime.timedelta(days=-1))[0:10]
            comparedaycount = 0.0
            currdaycounts = 0.0
            for oc in oclass:
                Tag = oc.TagClassValue[0:1]
                if Tag == "E":
                    comparedaycount = eletongji(oc, compareday, lastcompareday, comparedaycount)
                    currdaycounts = eletongji(oc, currday, lastday, currdaycounts)
                elif Tag == "W":
                    comparedaycount = wattongji(oc, compareday, lastcompareday, comparedaycount)
                    currdaycounts = wattongji(oc, currday, lastday, currdaycounts)
                elif Tag == "S":
                    comparedaycount = stetongji(oc, compareday, lastcompareday, comparedaycount)
                    currdaycounts = stetongji(oc, currday, lastday, currdaycounts)
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
                    if Tag == "E":
                        current_countr = eletongji(oc, currhour, lasthour, current_countr)
                        compare_count = eletongji(oc, comparehour, comparelasthour, compare_count)
                    elif Tag == "W":
                        current_countr = wattongji(oc, currhour, lasthour, current_countr)
                        compare_count = wattongji(oc, comparehour, comparelasthour, compare_count)
                    elif Tag == "S":
                        current_countr = stetongji(oc, currhour, lasthour, current_countr)
                        compare_count = stetongji(oc, comparehour, comparelasthour, compare_count)
                compare_dict["今日能耗"] = str(current_countr)
                compare_dict["对比日能耗"] = str(compare_count)
                time_list.append(compare_dict)
            dir["compareTodayRow"] = time_list
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "能耗预览查询报错Error：" + str(e), current_user.Name)

@energy.route('/areaTimeEnergy', methods=['POST', 'GET'])
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
                                                            TagDetail.EnergyClass == EnergyClass).all()
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
                        if Tag == "E":
                            vlaue = eletongji(oc, currhour, lasthour, vlaue)
                        elif Tag == "W":
                            vlaue = wattongji(oc, currhour, lasthour, vlaue)
                        elif Tag == "S":
                            vlaue = stetongji(oc, currhour, lasthour, vlaue)
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

@energy.route('/energyHistory', methods=['POST', 'GET'])
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
            elif Energy == "电":
                CollectionDates = db_session.query(ElectricEnergy.CollectionDate).distinct().filter(ElectricEnergy.CollectionDate.between(StartTime,EndTime)).order_by(("CollectionDate")).all()
                for CollectionDate in CollectionDates:
                    dicss = []
                    timeArray = time.strptime(CollectionDate[0], "%Y-%m-%d %H:%M:%S")
                    timeStamp = int(time.mktime(timeArray))
                    dicss.append(1000 * timeStamp)
                    currhour = CollectionDate[0]
                    vv = datetime.datetime.strptime(currhour, "%Y-%m-%d %H:%M:%S")
                    lasthour = str((vv + datetime.timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M:%S"))[0:13]
                    oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == Energy).all()
                    eletotal = 0.0
                    for oc in oclass:
                        eletotal = eletongji(oc, currhour, lasthour, eletotal)
                    dicss.append(eletotal)
                    diy.append(dicss)
                # 区域能耗排名
                AreaNames = db_session.query(AreaTable.AreaName).filter().all()
                totalflow = 0.0
                for AreaName in AreaNames:
                    TagClassValues = db_session.query(TagDetail.TagClassValue).filter(
                        TagDetail.AreaName == AreaName[0]).all()
                    engsum = 0.0
                    for TagClassValue in TagClassValues:
                        cur = db_session.query(ElectricEnergy.ZGL).filter(
                            ElectricEnergy.TagClassValue == TagClassValue,
                            ElectricEnergy.CollectionDate == StartTime).order_by(desc("CollectionDate")).first()
                        las = db_session.query(ElectricEnergy.ZGL).filter(
                            ElectricEnergy.TagClassValue == TagClassValue,
                            ElectricEnergy.CollectionDate == EndTime).order_by(("CollectionDate")).first()
                        engsum = engsum + appendcur(cur, las)
                    eng[AreaName[0]] = round(engsum, 2)
                    totalflow = totalflow + engsum
                # 累积量
                dir["total"] = round(totalflow, 2)
            elif Energy == "汽":
                CollectionDates = db_session.query(SteamEnergy.CollectionDate).distinct().filter(
                    SteamEnergy.CollectionDate.between(StartTime, EndTime)).order_by(("CollectionDate")).all()
                for CollectionDate in CollectionDates:
                    dicss = []
                    timeArray = time.strptime(CollectionDate[0], "%Y-%m-%d %H:%M:%S")
                    timeStamp = int(time.mktime(timeArray))
                    dicss.append(1000 * timeStamp)
                    steEnergyValues = db_session.query(SteamEnergy.FlowValue).filter(
                        SteamEnergy.CollectionDate == CollectionDate[0]).all()
                    tosteEnergyValue = 0.0
                    for steEnergyValue in steEnergyValues:
                        tosteEnergyValue = tosteEnergyValue + float(steEnergyValue[0])
                    dicss.append(round(float(tosteEnergyValue), 2))
                    diy.append(dicss)
                # 区域能耗排名
                AreaNames = db_session.query(AreaTable.AreaName).filter().all()
                totalflow = 0.0
                for AreaName in AreaNames:
                    TagClassValues = db_session.query(TagDetail.TagClassValue).filter(
                        TagDetail.AreaName == AreaName[0]).all()
                    engsum = 0.0
                    for TagClassValue in TagClassValues:
                        steEnergyValues = db_session.query(SteamEnergy.FlowValue).filter(
                            SteamEnergy.TagClassValue == TagClassValue,
                            SteamEnergy.CollectionDate.between(StartTime, EndTime)).all()
                        engsum = engsum + accumulation(steEnergyValues)
                    eng[AreaName[0]] = str(round(totalflow, 2))
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
        StartTime = data.get("StartTime")[0:15]
        EndTime = data.get("EndTime")[0:15]
        output=exportxstatistic(StartTime,EndTime)
        resp = make_response(output.getvalue())
        resp.headers["Content-Disposition"] ="attachment; filename=consumption.xlsx"
        resp.headers['Content-Type'] = 'application/x-xlsx'
        return resp

def exportxstatistic(StartTime,EndTime):
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
    columns = ['区域', '水累计值', '电总功率', '汽累计值', '统计开始时间', '统计截止时间']
    for item in columns:
        worksheet.write(0, col, item, cell_format)
        col += 1
    AreaNames = db_session.query(AreaTable).filter().all()
    for i in range(0, len(AreaNames)):
        oclass = db_session.query(TagDetail).filter(TagDetail.AreaName == AreaNames[i].AreaName).all()
        elecount = 0.0
        watcount = 0.0
        stecount = 0.0
        for oc in oclass:
            Tag = oc.TagClassValue[0:1]
            if Tag == "E":
                elecount = eletongji(oc, StartTime, EndTime, elecount)
            elif Tag == "W":
                watcount = wattongji(oc, StartTime, EndTime, watcount)
            elif Tag == "S":
                stecount = stetongji(oc, StartTime, EndTime, stecount)
        for cum in columns:
            if cum == '区域':
                worksheet.write(i+1, columns.index(cum), AreaNames[i].AreaName)
            if cum == '水累计值':
                worksheet.write(i+1, columns.index(cum), str(watcount)+"t")
            if cum == '电总功率':
                worksheet.write(i+1, columns.index(cum), str(elecount)+"kW·h")
            if cum == '汽累计值':
                worksheet.write(i+1, columns.index(cum), str(stecount)+"t")
            if cum == '统计开始时间':
                worksheet.write(i+1, columns.index(cum), StartTime+"0:00")
            if cum == '统计截止时间':
                worksheet.write(i+1, columns.index(cum), EndTime+"0:00")
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
        CurrentTime = data.get("CurrentTime")
        output=exportx(Area,EnergyClass,CurrentTime)
        resp = make_response(output.getvalue())
        resp.headers["Content-Disposition"] ="attachment; filename=testing.xlsx"
        resp.headers['Content-Type'] = 'application/x-xlsx'
        return resp


def exportx(Area,EnergyClass,CurrentTime):
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
    tas = db_session.query(TagDetail).filter(TagDetail.AreaName == Area).all()
    for ta in tas:
        tag.append(ta.TagClassValue)
    # 写入列名
    if EnergyClass == "水":
        columns = ['单位', '仪表ID', '价格ID', '采集点', '采集时间', '采集年', '采集月', '采集天', '瞬时流量', '累计流量']
        oclass = db_session.query(WaterEnergy).filter(WaterEnergy.TagClassValue.in_(tag), WaterEnergy.CollectionDate.like("%"+CurrentTime+"%")).all()
    elif EnergyClass == "电":
        columns = ['单位', '仪表ID', '价格ID', '采集点', '采集时间', '采集年', '采集月', '采集天', '总功率', 'A相电压', 'A相电流', 'B相电压', 'B相电流', 'C相电压', 'C相电压']
        oclass = db_session.query(ElectricEnergy).filter(ElectricEnergy.TagClassValue.in_(tag),
                                                         ElectricEnergy.CollectionDate.like("%" + CurrentTime + "%")).all()
    else:
        columns = ['蒸汽值', '单位', '仪表ID', '价格ID', '采集点', '采集时间', '采集年', '采集月', '采集天', '温度', '蒸汽瞬时值', '蒸汽累计值']
        oclass = db_session.query(SteamEnergy).filter(SteamEnergy.TagClassValue.in_(tag),
                                                      SteamEnergy.CollectionDate.like("%" + CurrentTime + "%")).all()
    for item in columns:
        worksheet.write(0, col, item, cell_format)
        col += 1
    # 写入数据
    for i in range(1,len(oclass)):
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
