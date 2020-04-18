import json

from flask import Blueprint

from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.SystemManagement.core import Role, DepartmentManager
from models.SystemManagement.system import User

user_manager = Blueprint('user_manager', __name__)


@user_manager.route('/system_tree', methods=['GET'])
def get_user():
    departments = db_session.query(DepartmentManager).all()
    queryset = []
    for department in departments:
        role_query = db_session.query(Role).filter(Role.ParentNode == department.DepartCode).all()
        # role_name = [data.RoleName for data in role_query]
        role_list = []
        for data in role_query:
            user_list = {'name': data.RoleName, 'code': data.RoleCode,  'children': []}
            user_query = db_session.query(User).filter(User.RoleName == data.RoleName).all()
            for user in user_query:
                user_data = {'name': user.Name, 'value': user.WorkNumber}
                user_list['children'] = user_data
            if user_list:
                role_list.append(user_list)
        department_data = {'name': department.DepartName, 'code': department.DepartCode,  'children': role_list}
        queryset.append(department_data)
    data = {'name': '好护士药业桓仁厂区', 'children': queryset}
    return json.dumps(data, cls=AlchemyEncoder, ensure_ascii=False)
