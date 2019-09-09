from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import desc
from flask_login import current_user
from sqlalchemy.ext.automap import automap_base
from dbset.main.BSFramwork import AlchemyEncoder
from models.SystemManagement.system import FieldSet
from tools import autocode
from tools.MESLogger import MESLogger
from dbset.log.BK2TLogger import logger,insertSyslog
from dbset.database.db_operate import db_session
import json
from tools.common import engine
logger = MESLogger('../logs', 'log')
from sqlalchemy import MetaData, create_engine
metadata = MetaData()
from sqlalchemy import Table
Base = automap_base()
Base.prepare(engine, reflect=True)

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





