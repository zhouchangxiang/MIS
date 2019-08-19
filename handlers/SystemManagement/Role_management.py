import json
import re, string, datetime
from collections import Counter
from flask import render_template,request,Blueprint
from sqlalchemy import func
from tools.common import insert,delete,update
from dbset.database.db_operate import db_session
from flask_login import current_user
from dbset.log.BK2TLogger import logger,insertSyslog
from dbset.main.BSFramwork import AlchemyEncoder

role_management = Blueprint('role_management', __name__, template_folder='templates')

# 工作台菜单role
@role_management.route('/sysrole')
def sysrole():

    # dataRoleInfo = []
    # roleNames = db_session.query(Role.ID, Role.RoleName).all()
    # for role in roleNames:
    #     li = list(role)
    #     id = li[0]
    #     name = li[1]
    #     roleName = {'RoleID': id, 'RoleName': name}
    #     dataRoleInfo.append(roleName)
    return render_template('./sysRole.html') #RoleInfos=dataRoleInfo