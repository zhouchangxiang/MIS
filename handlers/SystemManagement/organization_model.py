import string
from flask import Blueprint, render_template, request, make_response
from sqlalchemy.orm import Session, relationship, sessionmaker
from sqlalchemy import create_engine, func
import json
import socket
import datetime
from flask_login import login_required, logout_user, login_user,current_user,LoginManager
import re
from dbset.database import db_operate
from dbset.log.BK2TLogger import insertSyslog, MESLogger
from dbset.main.BSFramwork import AlchemyEncoder
from models.SystemManagement.system import Organization
from collections import Counter
from dbset.log.BK2TLogger import logger,insertSyslog
from tools.common import insert,delete,update
from dbset.database.db_operate import db_session

organiza = Blueprint('organiza', __name__, template_folder='templates')

# 组织机构建模
@organiza.route('/organization')
def organization():
    return render_template('./SystemManagement/sysOrganization.html')

@organiza.route('/organizationMap')
def organizationMap():
    return render_template('./SystemManagement/index_organization.html')

@organiza.route('/organizationMap/selectAll')#组织结构
def selectAll():
    if request.method == 'GET':
        try:
            return json.dumps(getMyOrganizationChildrenMap(id=0), cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            insertSyslog("error", "查询组织结构报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
def getMyOrganizationChildrenMap(id):
    sz = []
    try:
        orgs = db_session.query(Organization).filter().all()
        for obj in orgs:
            if obj.ParentNode == id:
                sz.append(
                    {"name": obj.OrganizationName, "value": obj.ID, "children": getMyOrganizationChildrenMap(obj.ID)})
        return sz
    except Exception as e:
        print(e)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@organiza.route('/Myorganization')
def myorganization():
    return render_template('./SystemManagement/Myorganization.html')
def getMyOrganizationChildren(id=0):
    sz = []
    try:
        orgs = db_session.query(Organization).filter().all()
        for obj in orgs:
            if obj.ParentNode == id:
                sz.append({"id": obj.ID, "text": obj.OrganizationName, "nodes": getMyOrganizationChildren(obj.ID)})
        srep = ',' + 'items' + ':' + '[]'
        # data = string(sz)
        # data.replace(srep, '')
        return sz
    except Exception as e:
        print(e)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
def getMyEnterprise(id=0):
    sz = []
    try:
        orgs = db_session.query(Organization).filter().all()
        for obj in orgs:
            sz.append({"id": obj.ID, "text": obj.OrganizationName, "group": obj.ParentNode})
        return sz
    except Exception as e:
        print(e)
        logger.error(e)
        insertSyslog("error", "获取树形结构报错Error：" + str(e), current_user.Name)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
@organiza.route('/MyOp')
def MyOpFind():
    if request.method == 'GET':
        try:
            data = getMyOP(id=0)
            return json.dumps(data, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
def getMyOP(id):
    sz = []
    try:
        orgs = db_session.query(Organization).filter().all()
        for obj in orgs:
            if obj.ParentNode == id:
                sz.append(
                    {"text": obj.OrganizationName, "value": obj.ID, "nodes": getMyOP(obj.ID)})
        return sz
    except Exception as e:
        print(e)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@organiza.route('/Myenterprise')
def myenterprise():
    if request.method == 'GET':
        try:
            return json.dumps(getMyEnterprise(id=0), cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)