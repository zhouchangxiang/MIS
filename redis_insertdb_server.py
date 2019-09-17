#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import base64
import hashlib
import time
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

pool = redis.ConnectionPool(host=constant.REDIS_HOST, password=constant.REDIS_PASSWORD)
def run():
    while True:
        # bytes_list = ""
        # icount = icount + 1
        # strtmp = "My Websocket中文测试" + str(icount)
        # # str(bytes_list.encode('utf-8').strip() + b"\n")
        # # body = str(bytes_list, encoding='utf-8')
        # bytemsg = bytes(strtmp, encoding="utf8")

        data_dict = {}
        redis_conn = redis.Redis(connection_pool=pool)
        keys = db_session.query(RedisKey.KEY).filter().all()
        for key in keys:
            data_dict[key[0]] = redis_conn.hget(constant.REDIS_TABLENAME, key[0]).decode('utf-8')
        time.sleep(1)

    sock.close()


if __name__ == '__main__':
    run()