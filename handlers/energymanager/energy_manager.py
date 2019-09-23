import redis
from flask import Blueprint, render_template, request, make_response
import json
import datetime
from sqlalchemy import desc
from dbset.database.db_operate import db_session,pool
from dbset.main.BSFramwork import AlchemyEncoder
from flask_login import login_required, logout_user, login_user,current_user,LoginManager
import calendar
from models.SystemManagement.core import RedisKey, ElectricEnergy, WaterEnergy, SteamEnergy
from tools.common import insert,delete,update
from dbset.database import constant
from dbset.log.BK2TLogger import logger,insertSyslog
import datetime

energy = Blueprint('energy', __name__, template_folder='templates')
@energy.route('/energyRedisData')
def energyRedisData():
    return render_template('./energyRedisData.html')

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
@energy.route('/energyTrend', methods=['POST', 'GET'])
def energyTrend():
    '''
    能耗趋势
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            currenttime = data.get("currenttime")
            classparam = data.get("classparam")
            currentyear = datetime.datetime.now().year
            currentmonth = datetime.datetime.now().month
            currentday = datetime.datetime.now().day
            currenthour = datetime.datetime.now().hour
            dir = {}
            dix = []
            diy = []
            diyr = {}
            diyz = []
            if currenttime == "年":
                for j in range(1,currentmonth+1):
                    mon = str(currentyear) + "-" + addzero(j)
                    dix.append(str(j))
                    if classparam == "电":
                        EnergyValues = db_session.query(ElectricEnergy.ElectricEnergyValue).filter(ElectricEnergy.CollectionMonth == mon).all()
                    elif classparam == "水":
                        EnergyValues = db_session.query(WaterEnergy.WaterMeterValue).filter(
                            WaterEnergy.CollectionMonth == mon).all()
                    elif classparam == "汽":
                        EnergyValues = db_session.query(SteamEnergy.SteamValue).filter(
                            SteamEnergy.CollectionMonth == mon).all()
                    diyz.append(accumulation(EnergyValues))
            elif currenttime == "月":#2019-9-22
                for j in range(1, currentday+1):
                    day = str(currentyear) + "-" + addzero(currentmonth) + "-" + addzero(j)
                    dix.append(str(j))
                    if classparam == "电":
                        EnergyValues = db_session.query(ElectricEnergy.ElectricEnergyValue).filter(
                            ElectricEnergy.CollectionDay == day).all()

                    elif classparam == "水":
                        EnergyValues = db_session.query(WaterEnergy.WaterMeterValue).filter(
                            WaterEnergy.CollectionDay == day).all()
                    elif classparam == "汽":
                        EnergyValues = db_session.query(SteamEnergy.SteamValue).filter(
                            SteamEnergy.CollectionDay == day).all()
                    diyz.append(accumulation(EnergyValues))
            elif currenttime == "日":
                for j in range(0, currenthour):
                    hour = str(currentyear) + "-" + addzero(currentmonth) + "-" + addzero(currentday) + " " + addzero(j)
                    dix.append(str(j))
                    if classparam == "电":
                        EnergyValues = db_session.query(ElectricEnergy.ElectricEnergyValue).filter(
                            ElectricEnergy.CollectionDate.like("%"+hour+"%")).all()
                    elif classparam == "水":
                        EnergyValues = db_session.query(WaterEnergy.WaterMeterValue).filter(
                            WaterEnergy.CollectionDate.like("%"+hour+"%")).all()
                    elif classparam == "汽":
                        EnergyValues = db_session.query(SteamEnergy.SteamValue).filter(
                            SteamEnergy.CollectionDate.like("%"+hour+"%")).all()
                    diyz.append(accumulation(EnergyValues))
            diyr["name"] = classparam
            diyr["data"] = diyz
            dir["X"] = dix
            diy.append(diyr)
            dir["Y"] = diy
            print(dir)
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "能耗趋势查询报错Error：" + str(e), current_user.Name)