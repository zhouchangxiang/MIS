import json, string, re, datetime
from flask import Blueprint, render_template, request
from dbset.database.db_operate import db_session
from models.SystemManagement.system import Organization
from sqlalchemy import and_,desc
from dbset.main.BSFramwork import AlchemyEncoder
from dbset.log.BK2TLogger import logger,insertSyslog
from flask_login import current_user
from models.SystemManagement.system import User

user_manage = Blueprint('user_manage', __name__, template_folder='templates')

# 用户管理
@user_manage.route('/user_manage/userpage')
def userpage():
    # departments = db_session.query(Organization.ID, Organization.OrganizationName).all()
    # # print(departments)
    # # departments = json.dumps(departments, cls=AlchemyEncoder, ensure_ascii=False)
    # data = []
    # for tu in departments:
    #     li = list(tu)
    #     id = li[0]
    #     name = li[1]
    #     department = {'OrganizationID':id,'OrganizationName':name}
    #     data.append(department)
    #
    # dataRoleName = []
    # roleNames = db_session.query(Role.ID, Role.RoleName).all()
    # for role in roleNames:
    #     li = list(role)
    #     id = li[0]
    #     name = li[1]
    #     roleName = {'RoleID': id, 'RoleName': name}
    #     dataRoleName.append(roleName)
    return render_template('./user.html')#, departments=data, roleNames=dataRoleName
