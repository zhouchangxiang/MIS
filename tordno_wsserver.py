import redis
import json
from dbset.database import constant
import time
from tools.MESLogger import MESLogger
logger = MESLogger('../logs', 'log')
import socket
import struct
import hashlib
import base64
import threading
import random
import datetime
from dbset.database.db_operate import db_session
from models.SystemManagement.system import ElectricSiteURL, ElectricProportion
from models.SystemManagement.core import TagDetail, AreaTable
from dbset.log.BK2TLogger import logger,insertSyslog
import ast
from __future__ import unicode_literals, print_function
from datetime import datetime
import time
import os
import random
import tornado
from tornado import gen
from tornado.options import define, options
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.options import define, options, parse_command_line
from tornado.ioloop import IOLoop
import asyncio
import threading
import time
import gc
import datetime
import sys
from sys import getrefcount

pool = redis.ConnectionPool(host=constant.REDIS_HOST)
redis_conn = redis.Redis(connection_pool=pool)

clients = dict()  # 客户端Session字典
# loop = asyncio.new_event_loop()

# 设置服务器端口
define("port", default=5002, type=int)
# users = set()

class IndexHandler(RequestHandler):
    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    def get(self):
        self.render("chat-client.html")

class SendThread(threading.Thread):

    # 启动单独的线程运行此函数，每隔1秒向所有的客户端推送当前时间

    def run(self):
        runcount = 0
        failcount = 0
        asyncio.set_event_loop(asyncio.new_event_loop())
        msg = ''
        # asyncio.set_event_loop(loop)
        while True:

            try:
                area_list = []
                oclass = ast.literal_eval(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "all_steam_tags")))
                oc_dict_i_tag = {}
                for oc in oclass:
                    oc_dict_i = {}
                    oc_dict_i["flowValue"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "F"))  # 蒸汽瞬时流量
                    oc_dict_i["sumValue"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "S"))  # 蒸汽累计流量
                    oc_dict_i["SteamWD"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "WD"))  # 蒸汽体积
                    oc_dict_i_tag[oc] = oc_dict_i
                water_oclass = ast.literal_eval(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "all_water_tags")))
                oc_dict_i_water_tag = {}
                for oc in water_oclass:
                    oc_water_dict_i = {}
                    oc_water_dict_i["flowValue"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "F"))
                    oc_water_dict_i["sumValue"] = abs(strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "S")))
                    oc_dict_i_water_tag[oc] = oc_water_dict_i
                electric_oclass = ast.literal_eval(returnb(redis_conn.hget(constant.REDIS_TABLENAME, "all_water_tags")))
                oc_dict_i_electric_tag = {}
                for oc in electric_oclass:
                    oc_electric_dict_i = {}
                    oc_electric_dict_i["ZGL"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_ZGL"))
                    oc_electric_dict_i["AU"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_AU"))
                    oc_electric_dict_i["AI"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_AI"))
                    oc_electric_dict_i["BU"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_BU"))
                    oc_electric_dict_i["BI"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_BI"))
                    oc_electric_dict_i["CU"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_CU"))
                    oc_electric_dict_i["CI"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc + "_CI"))
                    oc_dict_i_electric_tag[oc] = oc_electric_dict_i
                oc_dict = {}
                oc_dict["steam"] = oc_dict_i_tag
                oc_dict["water"] = oc_dict_i_water_tag
                oc_dict["electric"] = oc_dict_i_electric_tag
                area_list.append(oc_dict)
                json_data = json.dumps(area_list)
                # bytemsg = bytes(json_data, encoding="utf8")
                # send_msg(c, bytes("recv: {}".format(data_parse), encoding="utf-8"))
                bytemsg = bytes(json_data,encoding="utf-8")
                for key in clients.keys():
                    clients[key]["object"].write_message(bytemsg)
                runcount = runcount + 1
                time.sleep(2)
            except Exception as e:
                print(e)
                failcount = failcount + 1
                break
            finally:
                pass
            redis_conn.hset(constant.REDIS_TABLENAME, "websocket_end",
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            redis_conn.hset(constant.REDIS_TABLENAME, "websocket_runcount", str(runcount))
            redis_conn.hset(constant.REDIS_TABLENAME, "websocket_failcount", str(failcount))
            redis_conn.hset(constant.REDIS_TABLENAME, "websocket_status", "执行成功")


class ChatHandler(WebSocketHandler):
    # users = set()  # 用来存放在线用户的容器
    # clients = dict()

    def open(self):
        # 建立连接后添加用户到容器中

        # # 向已在线用户发送消息
        # for user in self.users:
        #     remote_ip, port = self.request.connection.context.address
        #     now = datetime.now().strftime("%H:%M:%S")
        #     user.write_message("[{}][{}:{}]-进入聊天室".format(now, remote_ip, port))
        remote_ip, port = self.request.connection.context.address
        self.id = remote_ip + ":" + str(port)

        # self.stream.set_nodelay(True)
        # self.set_nodelay(True)

        clients[self.id] = {"id": self.id, "object": self}  # 保存Session到clients字典中

    def on_message(self, message):
        # 向在线用户广播消息
        # now = datetime.now().strftime("%H:%M:%S")
        # remote_ip, port = self.request.connection.context.address
        # t = random.randint(1, 100)
        # for user in users:
        #     # user.write_message("[{}][{}:{}] {}".format(now, remote_ip, port, t))
        #     user.write_message("[{}][{}:{}] {}".format(now, remote_ip, port, t))
        print("Client %s received a message:%s" % (self.id, message))

    def on_close(self):
        # 用户关闭连接后从容器中移除用户
        # now = datetime.now().strftime("%H:%M:%S")
        remote_ip, port = self.request.connection.context.address
        # self.users.remove(self)
        # for user in self.users:
        #     user.write_message("[{}][{}:{}]-离开聊天室".format(now, remote_ip, port))
        if self.id in clients:
            print(clients[self.id])
            del clients[self.id]
        gc.collect()

            # print("Client %s is closed" % (self.id))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求

def strtofloat(f):
    if f == None or f == "" or f == b'':
        return 0.0
    else:
        return round(float(f), 2)
def returnb(rod):
    if rod == None or rod == "" or rod == b'':
        return ""
    else:
        return rod.decode()


if __name__ == "__main__":
    # tornado.options.parse_command_line()
    # 将所有的tag写入redis
    Tags = db_session.query(TagDetail).filter().all()
    tag_steam_list = []
    tag_water_list = []
    for tag in Tags:
        EnergyClass = str(tag.TagClassValue)[0:1]
        if EnergyClass == "S":
            tag_steam_list.append(tag.TagClassValue)
        elif EnergyClass == "W":
            tag_water_list.append(tag.TagClassValue)
    redis_conn.hset(constant.REDIS_TABLENAME, "all_steam_tags", str(tag_steam_list))
    redis_conn.hset(constant.REDIS_TABLENAME, "all_water_tags", str(tag_water_list))
    areas = db_session.query(AreaTable).all()
    for area in areas:
        tagareas = db_session.query(TagDetail).filter(TagDetail.AreaName == area.AreaName).all()
        area_tag_list = []
        for ta in tagareas:
            area_tag_list.append(ta.TagClassValue)
        redis_conn.hset(constant.REDIS_TABLENAME, area.AreaName, str(area_tag_list))

    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/chat", ChatHandler),
    ],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        # debug=True
    )

    # http_server = tornado.httpserver.HTTPServer(app)
    # http_server.listen(options.port)
    # tornado.ioloop.IOLoop.current().start()

    # http_server = tornado.httpserver.HTTPServer(app)
    SendThread().start()

    parse_command_line()

    app.listen(options.port)
    # 挂起运行
    tornado.ioloop.IOLoop.instance().start()
    # tornado.ioloop.IOLoop.current().start()
