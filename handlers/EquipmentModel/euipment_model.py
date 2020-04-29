import redis
import xlwt
from flask import Blueprint, render_template
from sqlalchemy.orm import Session, relationship, sessionmaker
from sqlalchemy import create_engine
from flask import render_template, request, make_response
from dbset.main.BSFramwork import AlchemyEncoder
import json
import socket
import datetime
from flask_login import login_required, logout_user, login_user,current_user,LoginManager
import re
from sqlalchemy import create_engine, Column, ForeignKey, Table, Integer, String, and_, or_, desc,extract
from io import StringIO
import calendar
from dbset.main.BSFramwork import AlchemyEncoder
from dbset.database import db_operate
from dbset.log.BK2TLogger import logger,insertSyslog
from handlers.energymanager.energy_manager import energyStatistics, energyStatisticsFlowSumWD
from models.SystemManagement.system import EarlyWarning
from tools.common import insert,delete,update
from dbset.database.db_operate import db_session
from models.SystemManagement.core import Equipment, Instrumentation, TagDetail
from dbset.database import constant

# 创建蓝图 第一个参数为蓝图的名字
equip = Blueprint('equip', __name__, template_folder='templates')

pool = redis.ConnectionPool(host=constant.REDIS_HOST)
redis_conn = redis.Redis(connection_pool=pool)

# 设备建模
@equip.route('/Equipment')
def equipment():
    return render_template('./Equipment/sysEquipment.html')

# 器仪仪表周期诊定功能
@equip.route('/InstrumentationReminderTimeSelect', methods=['GET', 'POST'])
def InstrumentationReminderTimeSelect():
    if request.method == 'GET':
        data = request.values
        try:
            # pages = int(data.get("offset"))  # 页数
            # rowsnumber = int(data.get("limit"))  # 行数
            # inipage = pages * rowsnumber + 0  # 起始页
            # endpage = pages * rowsnumber + rowsnumber  # 截止页
            oclass = db_session.query(Instrumentation).all()
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
            dic = []
            for oc in oclass:
                if oc != None:
                    # aa = (datetime.datetime.now() - datetime.datetime.strptime(oc.CreateTime[0:10],"%Y-%m-%d")).days
                    # bb = aa/int(oc.NumberVerification)
                    # cc = int(oc.VerificationCycle) - int(oc.ReminderTime)
                    if (datetime.datetime.now() - datetime.datetime.strptime(oc.CreateTime[0:10],"%Y-%m-%d")).days / int(oc.NumberVerification) >= (int(oc.VerificationCycle) - int(oc.ReminderTime)):
                        dic.append(oc)
            jsonoclass = json.dumps(dic, cls=AlchemyEncoder, ensure_ascii=False)
            return '{"total"' + ":" + str(len(dic)) + ',"rows"' + ":\n" + jsonoclass + "}"
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "仪器仪表查询报错Error：" + str(e), current_user.Name)
            return json.dumps("仪器仪表查询报错")



@equip.route('/EquipmentDetail', methods=['POST', 'GET'])
def EquipmentDetail():
    '''
    设备详情
    return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            TagClassValue = data.get("TagClassValue")
            EnergyClass = data.get("EnergyClass")
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            if EnergyClass == "电":
                dir["ZGL"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_ZGL"))
                dir["AU"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_AU"))
                dir["AI"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_AI"))
                dir["BU"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_BU"))
                dir["BI"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_BI"))
                dir["CU"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_CU"))
                dir["CI"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_CI"))
            elif EnergyClass == "水":
                dir["WaterS"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "S"))  # 水的累计流量
                dir["WaterF"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "F"))  # 水的瞬时流量
            elif EnergyClass == "汽":
                dir["SteamF"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "F"))  # 蒸汽瞬时流量
                dir["SteamS"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "S"))  # 蒸汽累计流量
                dir["SteamV"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "V"))  # 蒸汽体积
                dir["SteamWD"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "WD"))  # 蒸汽体积
            oc_list = []
            dir_list = []
            oc_list.append(TagClassValue)
            for i in range(int(StartTime[11:13]), int(EndTime[11:13]) + 1):
                staeH = StartTime[0:11] + addzero(i) + ":00:00"
                endeH = StartTime[0:11] + addzero(i) + ":59:59"
                dir_list_i = {}
                dir_list_i["时间"] = StartTime[0:11] + addzero(i)
                if EnergyClass == "电":
                    elecs = energyStatistics(oc_list, staeH, endeH, EnergyClass)
                    dir_list_i["功率"] = elecs
                elif EnergyClass == "水":
                    rews = energyStatisticsFlowSumWD(oc_list, staeH, endeH, EnergyClass)
                    wats = energyStatistics(oc_list, staeH, endeH, EnergyClass)
                    dir_list_i["累计量"] = wats
                    dir_list_i["瞬时量"] = roundtwo(rews[0][0])
                elif EnergyClass == "汽":
                    stes = energyStatistics(oc_list, staeH, endeH, EnergyClass)
                    steams = energyStatisticsFlowSumWD(oc_list, staeH, endeH, EnergyClass)
                    dir_list_i["瞬时量"] = roundtwo(steams[0][0])
                    dir_list_i["累计量"] = stes
                    dir_list_i["体积"] = roundtwo(steams[0][1])
                    dir_list_i["温度"] = roundtwo(steams[0][2])
                dir_list.append(dir_list_i)
            DeviceNum = db_session.query(TagDetail.DeviceNum).filter(TagDetail.TagClassValue == TagClassValue).first()
            if DeviceNum:
                earlywarn = db_session.query(EarlyWarning).filter(EarlyWarning.EQPName == DeviceNum).order_by(desc("WarningDate")).first()
                if earlywarn:
                    dir["Situation"] = earlywarn.WarningType
                    dir["SituationTime"] = earlywarn.WarningDate
                else:
                    dir["Situation"] = "未发现异常"
                    dir["SituationTime"] = ""
            else:
                dir["Situation"] = "未发现异常"
                dir["SituationTime"] = ""
            energys = energyStatisticsFlowSumWD(oc_list, StartTime, EndTime, EnergyClass)
            if EnergyClass == "电":
                dir["MaxValue"] = roundtwo(energys[0][0])
                dir["MinValue"] = roundtwo(energys[0][1])
            elif EnergyClass == "水":
                dir["MaxValue"] = roundtwo(energys[0][1])
                dir["MinValue"] = roundtwo(energys[0][2])
            elif EnergyClass == "汽":
                dir["MaxValue"] = roundtwo(energys[0][3])
                dir["MinValue"] = roundtwo(energys[0][4])
            # print(dir_list)
            # if EnergyClass == "汽":
            #     objects = sorted(dir_list_i, key=lambda obj: obj["volum"])
            #     print(objects[0].volum)
            #     dir["max"] = objects[0].volum
            #     dir["min"] = objects[-1].volum
            dir["row"] = dir_list
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "设备详情查询报错Error：" + str(e), current_user.Name)

def roundtwo(rod):
    if rod == None or rod == "" or rod == b'':
        return 0.0
    else:
        if float(rod) < 0:
            return 0.0
        return round(float(rod), 2)
def returnb(rod):
    if rod == None or rod == "" or rod == b'':
        return ""
    else:
        return rod.decode()
def addzero(j):
    if j < 10:
        return "0" + str(j)
    else:
        return str(j)