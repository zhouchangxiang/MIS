import redis
from flask import Blueprint, render_template, request, make_response
import json
import datetime
from sqlalchemy import desc
from dbset.database.db_operate import db_session,pool
from dbset.main.BSFramwork import AlchemyEncoder
from flask_login import login_required, logout_user, login_user,current_user,LoginManager
import calendar
from models.SystemManagement.core import RedisKey, ElectricEnergy, WaterEnergy, SteamEnergy, LimitTable, Equipment, \
    PriceList, AreaTable, Unit, TagClassType, TagDetail
from tools.common import insert,delete,update
from dbset.database import constant
from dbset.log.BK2TLogger import logger,insertSyslog
import datetime
import arrow
import time

energy = Blueprint('energy', __name__, template_folder='templates')

arro = arrow.now()
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
        diff = float(cur) - float(las)
        if diff < 0:
            return 0.0
        else:
            return round(diff, 2)

def curcutlas(cur, las, count):
    if cur is None:
        return count
    else:
        cur = cur[0]
        if las is None:
            las = 0.0
        else:
            las = las[0]
        diff = round(float(cur) - float(las), 2)
        if diff < 0:
            return count
        else:
             return round(count + diff, 2)
def eletongji(oc, currtime, lasttime, elecount):
    cur = \
        db_session.query(ElectricEnergy.ZGL).filter(
            ElectricEnergy.TagClassValue == oc.TagClassValue,
            ElectricEnergy.CollectionDate.like("%"+currtime+"%")).order_by(
            desc("CollectionDate")).first()
    las = db_session.query(ElectricEnergy.ZGL).filter(
        ElectricEnergy.TagClassValue == oc.TagClassValue,
        ElectricEnergy.CollectionDate.like("%"+lasttime+"%")).order_by(desc("CollectionDate")).first()
    return curcutlas(cur, las, elecount)
def wattongji(oc, currtime, lasttime, elecount):
    cur = \
        db_session.query(WaterEnergy.WaterSum).filter(
            WaterEnergy.TagClassValue == oc.TagClassValue,
            WaterEnergy.CollectionDate.like("%"+currtime+"%")).order_by(
            desc("CollectionDate")).first()
    las = db_session.query(WaterEnergy.WaterSum).filter(
        WaterEnergy.TagClassValue == oc.TagClassValue,
        WaterEnergy.CollectionDate.like("%"+lasttime+"%")).order_by(desc("CollectionDate")).first()
    return curcutlas(cur, las, elecount)
def stetongji(oc, currtime, lasttime, elecount):
    cur = \
        db_session.query(SteamEnergy.SumValue).filter(
            SteamEnergy.TagClassValue == oc.TagClassValue,
            SteamEnergy.CollectionDate.like("%"+currtime+"%")).order_by(
            desc("CollectionDate")).first()
    las = db_session.query(SteamEnergy.SumValue).filter(
        SteamEnergy.TagClassValue == oc.TagClassValue,
        SteamEnergy.CollectionDate.like("%"+lasttime+"%")).order_by(desc("CollectionDate")).first()
    return curcutlas(cur, las, elecount)
def energyselect(data):
    if request.method == 'GET':
        try:
            dir = {}
            currentyear = datetime.datetime.now().year
            currentmonth = datetime.datetime.now().month
            currentday = datetime.datetime.now().day
            currenthour = datetime.datetime.now().hour
            curryear = str(currentyear)
            lastyear = str(int(curryear) - 1)
            currmonth = str(currentyear) + "-" + addzero(str(currentmonth))
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
            elecount = 0.0
            watcount = 0.0
            stecount = 0.0
            if ModelFlag == "能耗趋势" or  ModelFlag == "数据报表":
                dix = []
                diy = []
                diyr = {}
                diyz = []
                if ModelFlag == "数据报表":
                    oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass, TagDetail.AreaName == Area).all()
                    currentyear = CurrentTime[0:4]
                    currentmonth = CurrentTime[0:7]
                    currentday = CurrentTime[0:10]
                elif ModelFlag == "能耗趋势":
                    oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()
                if datime == "年":
                    for j in range(1, currentmonth + 1):
                        currM = str(currentyear) + "-" + addzero(j)
                        lastM = strlastMonth(currM)
                        dix.append(str(j))
                        count = 0.0
                        for oc in oclass:
                            Tag = oc.TagClassValue[0:1]
                            if Tag == "E":
                                count = eletongji(oc, currM, lastM, count)
                            elif Tag == "W":
                                count = wattongji(oc, currM, lastM, count)
                            elif Tag == "S":
                                count = stetongji(oc, currM, lastM, count)
                        diyz.append(count)
                elif datime == "月":
                    for j in range(1, currentday + 1):
                        currday = str(currentyear) + "-" + addzero(currentmonth) + "-" + addzero(j)
                        vv = datetime.datetime.strptime(currday, "%Y-%m-%d")
                        lastday = str(vv + datetime.timedelta(days=-1))[0:10]
                        dix.append(str(j))
                        count = 0.0
                        for oc in oclass:
                            Tag = oc.TagClassValue[0:1]
                            if Tag == "E":
                                count = eletongji(oc, currday, lastday, count)
                            elif Tag == "W":
                                count = wattongji(oc, currday, lastday, count)
                            elif Tag == "S":
                                count = stetongji(oc, currday, lastday, count)
                        diyz.append(count)
                elif datime == "日":
                    for j in range(0, currenthour):
                        currhour = str(currentyear) + "-" + addzero(currentmonth) + "-" + addzero(
                            currentday) + " " + addzero(j)
                        if ModelFlag == "数据报表":
                            currhour = CurrentTime[0:10]
                        vv = datetime.datetime.strptime(currhour, "%Y-%m-%d %H")
                        lasthour = str((vv + datetime.timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M:%S"))[0:13]
                        dix.append(str(j))
                        count = 0.0
                        for oc in oclass:
                            Tag = oc.TagClassValue[0:1]
                            if Tag == "E":
                                count = eletongji(oc, currhour, lasthour, count)
                            elif Tag == "W":
                                count = wattongji(oc, currhour, lasthour, count)
                            elif Tag == "S":
                                count = stetongji(oc, currhour, lasthour, count)
                        diyz.append(count)
                diyr["name"] = EnergyClass
                diyr["data"] = diyz
                dir["X"] = dix
                diy.append(diyr)
                dir["Y"] = diy
                unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == EnergyClass).first()[0]
                dir["unit"] = unit
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
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            insertSyslog("error", "能耗查询报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
def energymoney(count, name):
    prices = db_session.query(PriceList).filter(PriceList.IsEnabled == "是").all()
    for pr in prices:
        if pr.PriceName == name:
            return float(count)*float(pr.PriceValue)
def getO(sum):
    if sum is not None:
        return float(sum[0])
    else:
        return 0

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
            if Energy == "水":
                #能耗历史数据
                watEnergyValues = db_session.query(WaterEnergy).filter(WaterEnergy.CollectionDate.between(StartTime,EndTime)).order_by(("CollectionDate")).all()
                Unit = ""
                for wa in watEnergyValues:
                    Unit = wa.Unit
                    dicss = []
                    if wa.CollectionDate != None:
                        timeArray = time.strptime(wa.CollectionDate, "%Y-%m-%d %H:%M:%S")
                        timeStamp = int(time.mktime(timeArray))
                        dicss.append(1000*timeStamp)
                    else:
                        dicss.append(0)
                    dicss.append(float(wa.WaterSum))
                    diy.append(dicss)
                dir["Unit"] = Unit
                #区域能耗排名
                AreaNames = db_session.query(AreaTable.AreaName).filter().all()
                for AreaName in AreaNames:
                    TagClassValues = db_session.query(TagDetail.TagClassValue).filter(TagDetail.AreaName == AreaName[0]).all()
                    engsum = 0.0
                    for TagClassValue in TagClassValues:
                        watEnergyValues = db_session.query(WaterEnergy.WaterSum).filter(WaterEnergy.TagClassValue == TagClassValue,
                            WaterEnergy.CollectionDate.between(StartTime, EndTime)).all()
                        engsum = engsum + accumulation(watEnergyValues)
                    eng[AreaName[0]] = str(engsum)
                # 累积量
                dir["total"] = accumulation(watEnergyValues)
            elif Energy == "电":
                eleEnergyValues = db_session.query(ElectricEnergy).filter(ElectricEnergy.CollectionDate.between(StartTime,EndTime)).order_by(("CollectionDate")).all()
                Unit = ""
                for el in eleEnergyValues:
                    Unit = el.Unit
                    dicss = []
                    if el.CollectionDate != None:
                        timeArray = time.strptime(el.CollectionDate, "%Y-%m-%d %H:%M:%S")
                        timeStamp = int(time.mktime(timeArray))
                        dicss.append(1000*timeStamp)
                    else:
                        dicss.append(0)
                    dicss.append(float(el.ZGL))
                    diy.append(dicss)
                dir["Unit"] = Unit
                # 区域能耗排名
                AreaNames = db_session.query(AreaTable.AreaName).filter().all()
                for AreaName in AreaNames:
                    TagClassValues = db_session.query(TagDetail.TagClassValue).filter(
                        TagDetail.AreaName == AreaName[0]).all()
                    engsum = 0.0
                    for TagClassValue in TagClassValues:
                        eleEnergyValues = db_session.query(ElectricEnergy.ZGL).filter(
                            ElectricEnergy.TagClassValue == TagClassValue,
                            ElectricEnergy.CollectionDate.between(StartTime, EndTime)).all()
                        engsum = engsum + accumulation(eleEnergyValues)
                    eng[AreaName[0]] = str(engsum)
                # 累积量
                dir["total"] = accumulation(eleEnergyValues)
            elif Energy == "汽":
                steEnergyValues = db_session.query(SteamEnergy).filter(SteamEnergy.CollectionDate.between(StartTime,EndTime)).order_by(("CollectionDate")).all()
                Unit = ""
                for st in steEnergyValues:
                    Unit = st.Unit
                    dicss = []
                    if st.CollectionDate != None:
                        timeArray = time.strptime(st.CollectionDate, "%Y-%m-%d %H:%M:%S")
                        timeStamp = int(1000*time.mktime(timeArray))
                        dicss.append(timeStamp)
                    else:
                        dicss.append(0)
                    dicss.append(st.SumValue)
                    diy.append(dicss)
                dir["Unit"] = Unit
                # 区域能耗排名
                AreaNames = db_session.query(AreaTable.AreaName).filter().all()
                for AreaName in AreaNames:
                    TagClassValues = db_session.query(TagDetail.TagClassValue).filter(
                        TagDetail.AreaName == AreaName[0]).all()
                    engsum = 0.0
                    for TagClassValue in TagClassValues:
                        steEnergyValues = db_session.query(SteamEnergy.SumValue).filter(
                            SteamEnergy.TagClassValue == TagClassValue,
                            SteamEnergy.CollectionDate.between(StartTime, EndTime)).all()
                        engsum = engsum + accumulation(steEnergyValues)
                    eng[AreaName[0]] = str(engsum)
                # 累积量
                dir["total"] = accumulation(steEnergyValues)
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