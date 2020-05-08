import redis
import arrow
from flask import Blueprint
from flask import render_template, request
import json
import datetime
from flask_login import login_required, logout_user, login_user,current_user
from sqlalchemy import create_engine, Column, ForeignKey, Table, Integer, String, and_, or_, desc,extract
from dbset.main.BSFramwork import AlchemyEncoder
from dbset.log.BK2TLogger import logger,insertSyslog
from models.SystemManagement.system import EarlyWarning, SteamTotalMaintain, ElectricProportion
from dbset.database.db_operate import db_session
from models.SystemManagement.core import Instrumentation, TagDetail, ElectricEnergy
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


def energyhistory(TagClassValue, StartTime, EndTime, energy):
    '''
    :param oc_list: tag点的List
    :param StartTime:
    :param EndTime:
    :param energy: 水，电 ，气
    :return:历史表的瞬时值、温度、体积
    '''
    if energy == "水":
        sql = "SELECT t.CollectionDate as CollectionDate, t.WaterFlow as WaterFlow, t.WaterSum as WaterSum FROM [DB_MICS].[dbo].[WaterEnergy] t with (INDEX =IX_WaterEnergy)  WHERE t.TagClassValue = '" + TagClassValue + "' AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    elif energy == "电":
        sql = "SELECT t.CollectionDate as CollectionDate, t.ZGL FROM [DB_MICS].[dbo].[ElectricEnergy] t with (INDEX =IX_ElectricEnergy) WHERE t.TagClassValue = '" + TagClassValue + "' AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    elif energy == "汽":
        if TagClassValue == 'S_AllArea_Value':
            sql = "SELECT t.CollectionDate as CollectionDate, t.FlowValue as FlowValue, t.SumValue as SumValue,t.Volume as Volume, t.WD as WD FROM [DB_MICS].[dbo].[SteamTotalMaintain] t with (INDEX =IX_SteamTotalMaintain) WHERE t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
        else:
            sql = "SELECT t.CollectionDate as CollectionDate, t.FlowValue as FlowValue, t.SumValue as SumValue,t.Volume as Volume, t.WD as WD FROM [DB_MICS].[dbo].[SteamEnergy] t with (INDEX =IX_SteamEnergy) WHERE t.TagClassValue = '" + TagClassValue + "' AND t.CollectionDate BETWEEN " + "'" + StartTime + "'" + " AND " + "'" + EndTime + "'"
    re = db_session.execute(sql).fetchall()
    db_session.close()
    return re
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
            Proportion = db_session.query(ElectricProportion.Proportion).filter(ElectricProportion.ProportionType == EnergyClass).first()
            if Proportion:
                Proportion = float(Proportion[0])
            else:
                Proportion = 1
            if EnergyClass == "电":
                dir["ZGL"] = round((roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_ZGL")))*Proportion, 2)
                dir["AU"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_AU"))
                dir["AI"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_AI"))
                dir["BU"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_BU"))
                dir["BI"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_BI"))
                dir["CU"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_CU"))
                dir["CI"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_CI"))
            elif EnergyClass == "水":
                dir["WaterS"] = round((roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "S")))*Proportion, 2)  # 水的累计流量
                dir["WaterF"] = round((roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "F")))*Proportion, 2)  # 水的瞬时流量
            elif EnergyClass == "汽":
                if TagClassValue == "S_AllArea_Value":
                    stm = db_session.query(SteamTotalMaintain).filter().order_by(desc("CollectionDate")).first()
                    dir["SteamF"] = roundtwo(stm.FlowValue)  # 蒸汽瞬时流量
                    dir["SteamS"] = roundtwo(stm.SumValue) # 蒸汽累计流量
                    dir["SteamV"] = roundtwo(stm.Volume)  # 蒸汽体积
                    dir["SteamWD"] = roundtwo(stm.WD)  # 蒸汽体积
                else:
                    dir["SteamF"] = round((roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "F")))*Proportion, 2)  # 蒸汽瞬时流量
                    dir["SteamS"] = round((roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "S")))*Proportion, 2)  # 蒸汽累计流量
                    dir["SteamV"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "V"))  # 蒸汽体积
                    dir["SteamWD"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "WD"))  # 蒸汽体积
            dir_list = []
            res = energyhistory(TagClassValue, StartTime, EndTime, EnergyClass)
            for re in res:
                dir_list_i = {}
                dir_list_i["时间"] = re['CollectionDate']
                if EnergyClass == "电":
                    dir_list_i["功率"] = round(((0 if re['ZGL'] is None else float(re['ZGL'])))*Proportion, 2)
                elif EnergyClass == "水":
                    dir_list_i["累计量"] = round(((0 if re['WaterSum'] is None else float(re['WaterSum'])))*Proportion, 2)
                    dir_list_i["瞬时量"] = round(((0 if re['WaterFlow'] is None else float(re['WaterFlow'])))*Proportion, 2)
                elif EnergyClass == "汽":
                    if TagClassValue == "S_AllArea_Value":
                        dir_list_i["瞬时量"] = round((0 if re['FlowValue'] is None else float(re['FlowValue'])), 2)
                        dir_list_i["累计量"] = round((0 if re['SumValue'] is None else float(re['SumValue'])), 2)
                        dir_list_i["体积"] = round((0 if re['Volume'] is None else float(re['Volume'])), 2)
                        dir_list_i["温度"] = round((0 if re['WD'] is None else float(re['WD'])), 2)
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


@equip.route('/powerquality', methods=['POST', 'GET'])
def powerquality():
    '''
    电能质量
    return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            dir = {}
            StartTime = data.get("StartTime")
            EndTime = data.get("EndTime")
            TagClassValue = data.get("TagClassValue")
            a = arrow.now()
            warfirst = db_session.query(EarlyWarning).filter(EarlyWarning.TagClassValue == TagClassValue).order_by(desc("WarningDate")).first()
            thredaycount = db_session.query(EarlyWarning).filter(EarlyWarning.TagClassValue == TagClassValue, EarlyWarning.WarningDate.between(str(a.shift(days=-30)), str(a.shift(days=0)))).order_by(desc("WarningDate")).count()
            dir["thredaycount"] = thredaycount
            dir["row"] = thredaycount
            if warfirst:
                dir["WarningType"] = warfirst.WarningType
                dir["WarningDate"] = warfirst.WarningDate
            else:
                dir["WarningType"] = ""
                dir["WarningDate"] = ""
            dir_list = []
            oclass = db_session.query(ElectricEnergy).filter(ElectricEnergy.CollectionDate.between(StartTime,EndTime)).all()
            for oc in oclass:
                oc_dict = {}
                oc_dict["时间"] = oc.CollectionDate
                oc_dict["A项电流"] = oc.AI
                oc_dict["A项电压"] = oc.AU
                oc_dict["B项电流"] = oc.BI
                oc_dict["B项电压"] = oc.BU
                oc_dict["C项电流"] = oc.CI
                oc_dict["C项电压"] = oc.CU
                dir_list.append(oc_dict)
            dir["dir_list"] = dir_list
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "电能质量查询报错Error：" + str(e), current_user.Name)