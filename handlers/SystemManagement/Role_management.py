import json
import re, string, datetime
from collections import Counter
from flask import render_template,request,Blueprint
from sqlalchemy import func
from tools.common import insert,delete,update
from dbset.database.db_operate import db_session
from models.SystemManagement.system import Role
from flask_login import current_user
from dbset.log.BK2TLogger import logger,insertSyslog
from dbset.main.BSFramwork import AlchemyEncoder

role_management = Blueprint('role_management', __name__, template_folder='templates')

# 工作台菜单role
@role_management.route('/sysrole')
def sysrole():
    dataRoleInfo = []
    roleNames = db_session.query(Role.ID, Role.RoleName).all()
    for role in roleNames:
        li = list(role)
        id = li[0]
        name = li[1]
        roleName = {'RoleID': id, 'RoleName': name}
        dataRoleInfo.append(roleName)
    return render_template('./SystemManagement/sysRole.html', RoleInfos=dataRoleInfo)


# role更新数据，通过传入的json数据，解析之后进行相应更新
@role_management.route('/allroles/Update', methods=['POST', 'GET'])
def allrolesUpdate():
    if request.method == 'POST':
        data = request.values
        return update(Role, data)


# role删除数据
@role_management.route('/allroles/Delete', methods=['POST', 'GET'])
def allrolesDelete():
    if request.method == 'POST':
        data = request.values
        return delete(Role, data)


# role创建数据
@role_management.route('/allroles/Create', methods=['POST', 'GET'])
def allrolesCreate():
    if request.method == 'POST':
        data = request.values
        return insert(Role, data)
