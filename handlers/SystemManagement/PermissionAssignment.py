import json
import re
from flask import render_template,request,Blueprint,redirect,url_for
from flask_restful import reqparse

from dbset.database.db_operate import db_session
from models.SystemManagement.system import Permission, ResourceMenus, ModulMenus
from flask_login import current_user
from dbset.log.BK2TLogger import logger,insertSyslog
from dbset.main.BSFramwork import AlchemyEncoder

permission_distribution = Blueprint('permission_distribution', __name__, template_folder='templates')

# 权限分配
@permission_distribution.route('/permission')
def permission():
    return render_template('./permission.html')

# 角色列表树形图
def getRoleList(id=0):
    sz = []
    try:
        roles = db_session.query(Role).filter().all()
        for obj in roles:
            if obj.ParentNode == id:
                sz.append({"id": obj.ID,
                           "text": obj.RoleName,
                           "children": getRoleList(obj.ID)})
        srep = ',' + 'items' + ':' + '[]'
        return sz
    except Exception as e:
        print(e)
        logger.error(e)
        insertSyslog("error", "查询角色报错Error：" + str(e), current_user.Name)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

# 权限分配下的角色列表
@permission_distribution.route('/Permission/SelectRoles')
def SelectRoles():
    if request.method == 'GET':
        try:
            data = getRoleList(id=0)
            jsondata = json.dumps(data, cls=AlchemyEncoder, ensure_ascii=False)
            return jsondata.encode("utf8")
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "查询权限分配下的角色列表报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)


# 权限分配下的用户列表
@permission_distribution.route('/permission/userlist')
def userList():
    # 获取用户列表
    if request.method == 'GET':
        data = request.values  # 返回请求中的参数和form
        # 默认返回所有用户
        ID = data['ID']
        if ID == '':
            try:
                json_str = json.dumps(data.to_dict())
                if len(json_str) > 10:
                    pages = int(data.get("offset"))  # 页数
                    rowsnumber = int(data.get("limit"))  # 行数
                    inipage = pages * rowsnumber + 0  # 起始页
                    endpage = pages * rowsnumber + rowsnumber  # 截止页
                    total = db_session.query(User).count()
                    users_data = db_session.query(User)[inipage:endpage]
                    # ORM模型转换json格式
                    jsonusers = json.dumps(users_data, cls=AlchemyEncoder, ensure_ascii=False)
                    jsonusers = '{"total"' + ":" + str(total) + ',"rows"' + ":\n" + jsonusers + "}"
                    return jsonusers.encode("utf8")
            except Exception as e:
                print(e)
                logger.error(e)
                insertSyslog("error", "查询权限分配下的用户列表报错Error：" + str(e), current_user.Name)
                return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
        if ID != '':
            data = request.values  # 返回请求中的参数和form
            try:
                json_str = json.dumps(data.to_dict())
                if len(json_str) > 10:
                    pages = int(data['page'])  # 页数
                    rowsnumber = int(data['rows'])  # 行数
                    inipage = (pages - 1) * rowsnumber + 0  # 起始页
                    endpage = (pages - 1) * rowsnumber + rowsnumber  # 截止页
                    # 通过角色ID获取当前角色对应的用户
                    role_id = data['ID']
                    role_name= db_session.query(Role.RoleName).filter_by(ID=role_id).first()
                    if role_name is None:  # 判断当前角色是否存在
                        return
                    total = db_session.query(User).filter_by(RoleName=role_name).count()
                    users_data = db_session.query(User).filter_by(RoleName=role_name).all()[
                                 inipage:endpage]
                    # ORM模型转换json格式
                    jsonusers = json.dumps(users_data, cls=AlchemyEncoder, ensure_ascii=False)
                    jsonusers = '{"total"' + ":" + str(total) + ',"rows"' + ":\n" + jsonusers + "}"
                    return jsonusers
            except Exception as e:
                print(e)
                logger.error(e)
                insertSyslog("error", "通过点击角色查询用户报错Error：" + str(e), current_user.Name)
                return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

def trueOrFalse(obj,user_menus):
    dic = {}
    if str(obj.ModulMenuName) in user_menus:
        dic["checked"] = True
        return dic
    else:
        dic["checked"] = False
    return dic

# 权限分配下的功能模块列表
def getMenuList(user_menus, id=0):
    sz = []
    try:
        menus = db_session.query(ModulMenus).filter_by(ParentNode=id).all()
        for obj in menus:
            if obj.ParentNode == id:
                    sz.append({"id": obj.ID,
                               "text": obj.ModulMenuName,
                               "ModulMenuName":obj.ModulMenuName,
                               "MenuType":obj.MenuType,
                               "ModulMenuCode":obj.ModulMenuCode,
                               "state":trueOrFalse(obj, user_menus),
                               "nodes": getMenuList(user_menus, obj.ID)})
        return sz
    except Exception as e:
        print(e)
        insertSyslog("error", "查询权限分配下的功能模块列表Error：" + str(e), current_user.Name)
        return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)


# 加载菜单列表
@permission_distribution.route('/permission/menulist')
def menulist():
    if request.method == 'GET':
        role_data = request.values
        if 'id' not in role_data.keys():
            try:
                data = getMenuList(role_menus=[],id=0)
                jsondata = json.dumps(data, cls=AlchemyEncoder, ensure_ascii=False)
                return jsondata.encode("utf8")
            except Exception as e:
                print(e)
                logger.error(e)
                insertSyslog("error", "加载菜单列表Error：" + str(e), current_user.Name)
                return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
        id = role_data['id']
        try:
            role_menus = db_session.query(Menu.ModuleName).join(Role_Menu, isouter=True).filter_by(Role_ID=id).all()
            r_menus = []
            for menu in role_menus:
                r_menus.append(menu[0])
            menus_data = getMenuList(r_menus, id=0)
            jsondata = json.dumps(menus_data, cls=AlchemyEncoder, ensure_ascii=False)
            return jsondata.encode("utf8")
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "加载菜单列表Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

# 权限分配下为角色添加权限
@permission_distribution.route('/permission/MenuToRole')
def menuToUser():
    if request.method == 'GET':
        data = request.values  # 返回请求中的参数和form
        try:
            # 获取菜单和用户并存入数据库
            role_id = data['role_id']  # 获取角色ID
            if role_id is None:
                return
            menus = db_session.query(Menu).join(Role_Menu, isouter=True).filter_by(Role_ID=id).all()
            if menus:
                db_session.delete(menus)
                db_session.commit()
            menu_id = data['menu_id'] # 获取菜单ID
            if menu_id is None:
                return
            menu_id = re.findall(r'\d+\.?\d*', menu_id)
            for r in menu_id:
                role = db_session.query(Role).filter_by(ID=role_id).first()
                menu = db_session.query(Menu).filter_by(ID=r).first()
                # 将菜单ID和角色ID存入User_Role
                menu.roles.append(role)
                db_session.add(menu)
                db_session.commit()
            # 存入数据库后跳转到权限分配页面
            return redirect(url_for("roleright"))
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "权限分配下为角色添加权限Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

# 菜单权限控制
@permission_distribution.route('/ZYPlanGuid/menuRedirect', methods=['POST', 'GET'])
def menuRedirect():
    if request.method == 'POST':
        data = request.values  # 返回请求中的参数和form
        try:
            menuName = data['menuName']
            RoleNames = db_session.query(User.RoleName).filter(User.Name == current_user.Name).all()
            flag = 'OK'
            for rN in RoleNames:
                roleID = db_session.query(Role.ID).filter(Role.RoleName == rN[0]).first()
                menus = db_session.query(Menu.ModuleName).join(Role_Menu, isouter=True).filter_by(Role_ID=roleID).all()
                for menu in menus:
                    if (menu[0] == menuName):
                        return 'OK'
                    else:
                        flag = '当前用户没有此操作权限！'
            return flag
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "计划向导生成计划报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

#----------------------------------------------------------------------------------------%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# 菜单权限查询
@permission_distribution.route('/Permission/SelectMenus', methods=['POST', 'GET'])
def SelectMenus():
    if request.method == 'GET':
        data = request.values
        try:
            MenuType = data.get("MenuType")
            Name = current_user.Name
            if Name == "系统管理员":
                oclass = db_session.query(ModulMenus).all()
                return json.dumps(oclass, cls=AlchemyEncoder, ensure_ascii=False)
            periss = db_session.query(Permission).filter(Permission.Name == current_user.Name, Permission.MenuType == MenuType).all()
            flag = 'OK'
            dic = []
            for i in periss:
                oclass = db_session.query(ModulMenus).filter(
                    ModulMenus.ResourceMenuName.like("%" + i.MenuName + "%")).first()
                dic.append(oclass)
                # if MenuType == "资源级":
                #     oclass = db_session.query(ResourceMenus).filter(ResourceMenus.ModulMenuName.like("%"+i.MenuName+"%")).first()
                #     dic.append(oclass)
                # else:
                #     oclass = db_session.query(ModulMenus).filter(
                #         ModulMenus.ResourceMenuName.like("%" + i.MenuName + "%")).first()
                #     dic.append(oclass)
            return json.dumps(dic, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "菜单权限查询报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

# 增加菜单父节点查询
@permission_distribution.route('/Permission/SelectParentMenus', methods=['POST', 'GET'])
def SelectParentMenus():
    if request.method == 'GET':
        data = request.values
        try:
            pages = int(data.get("offset"))  # 页数
            rowsnumber = int(data.get("limit"))  # 行数
            inipage = pages * rowsnumber + 0  # 起始页
            endpage = pages * rowsnumber + rowsnumber  # 截止页
            total = db_session.query(ModulMenus).filter(ModulMenus.MenuType.in_(("系统级", "模块级"))).count()
            oclass = db_session.query(ModulMenus).filter(ModulMenus.MenuType.in_(("系统级", "模块级"))).all()[inipage:endpage]
            jsonoclass = json.dumps(oclass, cls=AlchemyEncoder, ensure_ascii=False)
            return '{"total"' + ":" + str(total) + ',"rows"' + ":\n" + jsonoclass + "}"
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "增加菜单父节点查询报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

# 加载菜单列表
@permission_distribution.route('/permission/menulisttree', methods=['POST', 'GET'])
def menulisttree():
    if request.method == 'GET':
        data = request.values
        try:
            WorkNumber = data.get("WorkNumber")
            user_menus = []
            usermenus = db_session.query(Permission.MenuName).filter(Permission.WorkNumber == WorkNumber).all()
            for menu in usermenus:
                user_menus.append(menu[0])
            data = getMenuList(user_menus, id=0)
            jsondata = json.dumps(data, cls=AlchemyEncoder, ensure_ascii=False)
            return jsondata.encode("utf8")
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "加载菜单列表Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

# 加载菜单列表
@permission_distribution.route('/permission/PermissionsSave', methods=['POST', 'GET'])
def PermissionsSave():
    if request.method == 'POST':
        data = request.values
        try:
            datastr = json.loads(data.get("data"))
            #删除之前的权限
            perss = db_session.query(Permission).filter(Permission.WorkNumber == datastr[0].get("WorkNumber")).all()
            for pe in perss:
                db_session.delete(pe)
            db_session.commit()
            for i in datastr:
                per = Permission()
                per.MenuName = i.get("MenuName")
                per.MenuType = i.get("MenuType")
                per.MenuCode = i.get("MenuCode")
                per.Name = i.get("Name")
                per.WorkNumber = i.get("WorkNumber")
                db_session.add(per)
            db_session.commit()
            return 'OK'
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "添加用户报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)

# 加载菜单列表
@permission_distribution.route('/permission/PermissionsMenus', methods=['POST', 'GET'])
def PermissionsMenus():
    if request.method == 'GET':
        data = request.values
        try:
            MenuNames = db_session.query(Permission.MenuName).filter(Permission.WorkNumber == current_user.WorkNumber).all()
            dir = []
            for menuName in MenuNames:
                meu = db_session.query(ModulMenus).filter(ModulMenus.ModulMenuName == menuName).first()
                dir.append(meu)
            return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            db_session.rollback()
            print(e)
            logger.error(e)
            insertSyslog("error", "添加用户报错Error：" + str(e), current_user.Name)
            return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)