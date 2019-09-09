from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import desc
from flask_login import current_user
from dbset.main.BSFramwork import AlchemyEncoder
from models.SystemManagement.system import FieldSet
from tools import autocode
from tools.MESLogger import MESLogger
from dbset.log.BK2TLogger import logger,insertSyslog
from dbset.database.db_operate import db_session
import json
logger = MESLogger('../logs', 'log')

system_set = Blueprint('system_set', __name__, template_folder='templates')


# 加载工作台
@system_set.route('/home/workbench')
def workbenck():
    return render_template('./main/workbench.html')

# 加载工作台
@system_set.route('/system_set/make_model', methods=['POST', 'GET'])
def make_model():
    if request.method == 'POST':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            return autocode.make_model_main(data)
        except Exception as e:
            print(e)
            logger.error(e)

# 加载工作台
@system_set.route('/FieldSetSelect', methods=['POST', 'GET'])
def FieldSetSelect(data):
    try:
        pages = int(data.get("offset"))
        rowsnumber = int(data.get("limit"))
        param = data.get("field")
        tableName = data.get("tableName")
        paramvalue = data.get("fieldvalue")
        inipage = pages * rowsnumber + 0  # 起始页
        endpage = pages * rowsnumber + rowsnumber  # 截止页
        if (param == "" or param == None):
            total = db_session.query(FieldSet).count()
            oclass = db_session.query(FieldSet).order_by(desc("ID")).all()[inipage:endpage]
        else:
            total = db_session.query(FieldSet).filter(FieldSet.columns._data[param] == paramvalue).count()
            oclass = db_session.query(FieldSet).filter(FieldSet.columns._data[param] == paramvalue).order_by(desc("ID")).all()[
                     inipage:endpage]
        jsonoclass = json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
        jsonoclass = '{"total"' + ":" + str(total) + ',"rows"' + ":\n" + jsonoclass + "}"
        return jsonoclass
    except Exception as e:
        print(e)
        logger.error(e)
        insertSyslog("error", "查询报错Error：" + str(e), current_user.Name)


