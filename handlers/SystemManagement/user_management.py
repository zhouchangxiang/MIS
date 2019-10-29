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

@user_manage.route('/user/addUser', methods=['POST', 'GET'])
def addUser():
    if request.method == 'POST':
        data = request.values
        str = request.get_json()
        try:
            json_str = json.dumps(data.to_dict())
            if len(json_str) > 10:
                user = User()
                user.WorkNumber=data['WorkNumber']
                ocal = db_session.query(User).filter(User.WorkNumber == user.WorkNumber).first()
                if ocal != None:
                    return "工号重复，请重新录入！"
                user.Name=data['Name']
                user.Password=user.password(data['Password'])
                user.StationName = data['StationName']
                user.session_id = data['session_id']
                user.FactoryName = data['FactoryName']
                user.Status="1" # 登录状态先设置一个默认值1：已登录，0：未登录
                user.Creater=current_user.Name
                user.CreateTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                user.LastLoginTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                user.IsLock='false'
                user.OrganizationName=data['OrganizationName']
                user.RoleName=data['RoleName']
                db_session.add(user)
                db_session.commit()
                return 'OK'
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "添加用户报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

@user_manage.route('/user/updateUser', methods=['POST', 'GET'])
def UpdateUser():
    if request.method == 'POST':
        data = request.values
        str = request.get_json()
        try:
            json_str = json.dumps(data.to_dict())
            if len(json_str) > 10:
                id = int(data['ID'])
                user = db_session.query(User).filter_by(id=id).first()
                ocal = db_session.query(User).filter(User.WorkNumber == user.WorkNumber).first()
                if ocal != None:
                    return "工号重复，请重新修改！"
                user.WorkNumber = data['WorkNumber']
                user.Name = data['Name']
                user.Password = user.password(data['Password'])
                user.StationName = data['StationName']
                user.session_id = data['session_id']
                user.FactoryName = data['FactoryName']
                user.OrganizationName = data['OrganizationName']
                user.RoleName = data['RoleName']
                db_session.add(user)
                db_session.commit()
                return 'OK'
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "更新用户报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
