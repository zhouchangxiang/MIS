from flask import Blueprint, jsonify
from flask import Blueprint, render_template, request, make_response, send_file
import json

from flask_login import current_user
from sqlalchemy import desc

from dbset.database.db_operate import db_session, pool
from dbset.log.BK2TLogger import logger, insertSyslog
from dbset.main.BSFramwork import AlchemyEncoder
from models.SystemManagement.core import BrandAreaTable
from models.SystemManagement.system import BatchInfo

mobilemanager = Blueprint('mobile', __name__, template_folder='templates')


@mobilemanager.route('/', methods=['POST', 'GET'])
def index():
    data = {'name': 'huangxiongjin', 'age': 25}
    return jsonify(data)


@mobilemanager.route('/energyPreview', methods=['POST', 'GET'])
def BatchMaterialTracing():
    if request.method == 'GET':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            if len(jsonstr) > 10:
                pages = int(data.get("offset"))
                rowsnumber = int(data.get("limit"))
                inipage = pages * rowsnumber + 0
                endpage = pages * rowsnumber + rowsnumber
                begin = data.get('begin')
                end = data.get('end')
                BatchNum = data.get('BatchNum')
                if BatchNum == "" or BatchNum == None:
                    BrandAreaTable
                    total = db_session.query(BatchInfo).filter(BatchInfo.CreateDate.between(begin, end)).order_by(
                        desc("CreateDate")).count()
                    oclass = db_session.query(BatchInfo).filter(BatchInfo.CreateDate.between(begin, end)).order_by(
                        desc("CreateDate")).all()[inipage:endpage]
                else:
                    total = db_session.query(BatchInfo).filter(BatchInfo.BatchNum.like("%" + BatchNum + "%"),
                                                               BatchInfo.CreateDate.between(begin, end)).order_by(
                        desc("CreateDate")).count()
                    oclass = db_session.query(BatchInfo).filter(BatchInfo.BatchNum.like("%" + BatchNum + "%"),
                                                                BatchInfo.CreateDate.between(begin, end)).order_by(
                        desc("CreateDate")).all()[inipage:endpage]
                jsonoclass = json.dumps(oclass, cls=AlchemyEncoder, ensure_ascii=False)
                return '{"total"' + ":" + str(total) + ',"rows"' + ":\n" + jsonoclass + "}"
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "/BatchInfoSearch查询报错Error：" + str(e), current_user.Name)
