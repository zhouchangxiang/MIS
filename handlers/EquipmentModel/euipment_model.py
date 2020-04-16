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
            dir["ZGL"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_ZGL"))
            ZGLSamptime = returnb(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_ZGL_Samptime"))
            dir["AU"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_AU"))
            dir["AI"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_AI"))
            dir["BU"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_BU"))
            dir["BI"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_BI"))
            dir["CU"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_CU"))
            dir["CI"] = roundtwo(redis_conn.hget(constant.REDIS_TABLENAME, TagClassValue + "_CI"))
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