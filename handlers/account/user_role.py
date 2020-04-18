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
            user_list = {'name': data.RoleName, 'value': data.RoleCode, 'type': 'role', 'children': []}
            user_query = db_session.query(User).filter(User.RoleName == data.RoleName).all()
            for user in user_query:
                user_data = {'name': user.Name, 'value': user.WorkNumber, 'type': 'user'}
                user_list['children'].append(user_data)
            role_list.append(user_list)
        department_data = {'name': department.DepartName, 'value': department.DepartCode, 'type': 'department', 'children': role_list}
        queryset.append(department_data)
    data = {'name': factory.FactoryName, 'value': factory.AreaCode, 'type': 'factory', 'children': queryset}
    return json.dumps(data, cls=AlchemyEncoder, ensure_ascii=False)


@user_manager.route('/system_tree/add_department', methods=['POST'])
def add_department():
    did = request.json.get('department_code')
    dname = request.json.get('department_name')
    fname = request.json.get('factory_name')
    depart = DepartmentManager(DepartCode=did, DepartName=dname, DepartLoad=fname)
    db_session.add(depart)
    db_session.commit()
    return json.dumps({'code': 10000, 'msg': '新增成功', 'data': {'Did': depart.ID}})


@user_manager.route('/system_tree/delete_department', methods=['DELETE'])
def delete_department():
    code = request.headers.get('department_code')
    department = db_session.query(DepartmentManager).filter(DepartmentManager.DepartCode == code).first()
    role_query = db_session.query(Role).filter(Role.ParentNode == department.DepartCode).all()
    for item in role_query:
        item.ParentNode = ''
    db_session.commit()
    user_query = db_session.query(User).filter(User.OrganizationName == department.DepartName).all()
    for item in user_query:
        item.OrganizationName = ''
    db_session.commit()
    db_session.delete(department)
    db_session.commit()
    return json.dumps({'code': 10001, 'msg': '删除成功'})


@user_manager.route('/system_tree/update_department', methods=['PATCH'])
def update_department():
    code = request.json.get('department_code')
    department_name = request.json.get('department_name')
    department = db_session.query(DepartmentManager).filter(DepartmentManager.ID == code).first()
    department.DepartCode = code
    department.DepartName = department_name
    db_session.commit()
    return json.dumps({'code': 10002, 'msg': '更新成功'})


@user_manager.route('/system_tree/add_role', methods=['POST'])
def add_role():
    rid = request.json.get('role_code')
    rname = request.json.get('role_name')
    fname = request.json.get('factory_name')
    role = Role(DepartCode=rid, DepartName=rname, DepartLoad=fname)
    db_session.add(role)
    db_session.commit()
    return json.dumps({'code': 10003, 'msg': '新增成功', 'data': {'Did': role.ID}})


@user_manager.route('/system_tree/delete_role', methods=['DELETE'])
def delete_role():
    code = request.headers.get('role_code')
    role = db_session.query(Role).filter(Role.DepartCode == code).first()
    # role_query = db_session.query(Role).filter(Role.ParentNode == department.DepartCode).all()
    # for item in role_query:
    #     item.ParentNode = ''
    db_session.commit()
    user_query = db_session.query(User).filter(User.RoleName == role.DepartName).all()
    for item in user_query:
        item.OrganizationName = ''
    db_session.commit()
    db_session.delete(role)
    db_session.commit()
    return json.dumps({'code': 10004, 'msg': '删除成功'})


@user_manager.route('/system_tree/update_role', methods=['PATCH'])
def update_role():
    code = request.headers.get('role_code')
    role_name = request.headers.get('role_name')
    role = db_session.query(Role).filter(Role.DepartCode == code).first()
    role.DepartCode = code
    role.DepartName = role_name
    db_session.commit()
    return json.dumps({'code': 10005, 'msg': '更新成功'})


