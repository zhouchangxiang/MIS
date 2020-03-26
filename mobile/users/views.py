import json
import uuid
import pickle
import redis

from flask import jsonify
from flask import Blueprint, request
from datetime import datetime
from werkzeug.security import check_password_hash

from dbset.database.db_operate import db_session
from dbset.log.BK2TLogger import logger
from dbset.main.BSFramwork import AlchemyEncoder
from models.SystemManagement.system import User

mobile = Blueprint('mobile', __name__, template_folder='templates')


class Redis:

    @staticmethod
    def connect():
        return redis.StrictRedis(host='localhost', port=6379)

    @staticmethod
    def set_data(red, key, data):
        return red.set(key, pickle.dumps(data), ex=604800)

    @staticmethod
    def get_data(red, key):
        return pickle.loads(red.get(key)) if red.get(key) else '身份验证失败'


@mobile.route('/login', methods=['POST'])
def login():
    try:
        json_data = request.get_json()
        user = db_session.query(User).filter_by(WorkNumber=json_data['worknumber']).first()
        if user and check_password_hash(user.Password, json_data['password']):
            token = uuid.uuid4().hex
            user.LastLoginTime = datetime.now()
            Redis.set_data(Redis.connect(), token, user.id)
            db_session.add(user)
            db_session.commit()
            return jsonify({'code': 1001, 'msg': '登录成功', 'data': {'token': token, 'user': user.WorkNumber}})
        else:
            return jsonify({'code': 2001, 'msg': '账号或密码错误'})
    except Exception as e:
        print(e)
        db_session.rollback()
        logger.error(e)
        return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)


@mobile.route('/', methods=['GET'])
def index():
    token = request.headers.get('token')
    result = Redis.get_data(Redis.connect(), token)
    return jsonify({'code': 1003, 'msg': '获取数据成功', 'data': result})
