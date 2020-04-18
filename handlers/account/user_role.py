import json

from flask import Blueprint, request

from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.SystemManagement.core import Role, DepartmentManager, AreaMaintain
from models.SystemManagement.system import User

user_manager = Blueprint('user_manager', __name__)


@user_manager.route('/system_tree', methods=['GET'])
def get_user():
    departments = db_session.query(DepartmentManager).all()
    factory = db_session.query(AreaMaintain).first()
    queryset = []
    for department in departments:
        role_query = db_session.query(Role).filter(Role.ParentNode == department.DepartCode).all()
        role_list = []
        for data in role_query:
            user_list = {'name': data.RoleName, 'value': data.RoleCode, 'children': []}
            user_query = db_session.query(User).filter(User.RoleName == data.RoleName).all()
            for user in user_query:
                user_data = {'name': user.Name, 'value': user.WorkNumber}
                user_list['children'] = user_data
            if user_list:
                role_list.append(user_list)
        department_data = {'name': department.DepartName, 'value': department.DepartCode, 'children': role_list}
        queryset.append(department_data)
    data = {'name': factory.FactoryName, 'value': factory.AreaCode, 'children': queryset}
    return json.dumps(data, cls=AlchemyEncoder, ensure_ascii=False)


@user_manager.route('/system_tree/add_department', methods=['POST'])
def add_department():
    did = request.json.get('department_id')
    dname = request.json.get('department_name')
    fname = request.json.get('factory_name')
    depart = DepartmentManager(DepartCode=did, DepartName=dname, DepartLoad=fname)
    db_session.add(depart)
    db_session.commit()
    return json.dumps({'code': 10000, 'msg': '新增成功', 'data': {'Did': depart.ID}})


