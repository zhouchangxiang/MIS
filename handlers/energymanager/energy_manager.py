import redis
from flask import Blueprint, render_template, request, make_response
import json
import datetime
from sqlalchemy import desc
from dbset.database.db_operate import db_session,pool
from dbset.main.BSFramwork import AlchemyEncoder
from flask_login import login_required, logout_user, login_user,current_user,LoginManager

from models.SystemManagement.core import RedisKey
from tools.common import insert,delete,update
from dbset.database import constant
from dbset.log.BK2TLogger import logger,insertSyslog

pool = redis.ConnectionPool(host=constant.REDIS_HOST, password=constant.REDIS_PASSWORD)  # 实现一个连接池

energy = Blueprint('energy', __name__, template_folder='templates')
@energy.route('/energyRedisData')
def energyRedisData():
    return render_template('./energyRedisData.html')

@energy.route('/energyRedis', methods=['POST', 'GET'])
def energyRedis():
    '''
    Redis实时数据
    :return:
    '''
    if request.method == 'GET':
        data = request.values
        try:
            jsonstr = json.dumps(data.to_dict())
            data_dict = {}
            redis_conn = redis.Redis(connection_pool=pool)
            keys = db_session.query(RedisKey.KEY).filter().all()
            for key in keys:
                data_dict[key] = redis_conn.hget(constant.REDIS_TABLENAME, key[0]).decode('utf-8')
            return json.dumps(data_dict, cls=AlchemyEncoder, ensure_ascii=False)
        except Exception as e:
            print(e)
            logger.error(e)
            insertSyslog("error", "实时数据查询报错Error：" + str(e), current_user.Name)