# -*- coding: utf-8 -*-
import json
from datetime import datetime
import time
import os
import random
import tornado
from tornado.options import define, options
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from dbset.database import constant
import redis
from dbset.database.db_operate import db_session
from models.SystemManagement.system import ElectricSiteURL
from models.SystemManagement.core import TagDetail
from dbset.log.BK2TLogger import logger,insertSyslog

# 设置服务器端口
define("port", default=2223, type=int)


class IndexHandler(RequestHandler):
    def get(self):
        self.render("chat-client.html")

def strtofloat(f):
    if f == None or f == "" or f == b'':
        return 0.0
    else:
        return round(float(f), 2)
class ChatHandler(WebSocketHandler):
    users = set()  # 用来存放在线用户的容器

    def open(self):
        # 建立连接后添加用户到容器中
        self.users.add(self)

        # 向已在线用户发送消息
        for user in self.users:
            remote_ip, port = self.request.connection.context.address
            now = datetime.now().strftime("%H:%M:%S")
            user.write_message("[{}][{}:{}]-进入聊天室".format(now, remote_ip, port))

    def on_message(self, parameter):
        # 向在线用户广播消息
        now = datetime.now().strftime("%H:%M:%S")
        remote_ip, port = self.request.connection.context.address
        t = random.randint(1, 100)
        for user in self.users:
            data_dict = {}
            dir = []
            dis = []
            diw = []
            die = []
            pool = redis.ConnectionPool(host=constant.REDIS_HOST)
            redis_conn = redis.Redis(connection_pool=pool)
            Tags = db_session.query(TagDetail).filter(TagDetail.AreaName == parameter).all()
            i = 0
            for tag in Tags:
                try:
                    S = str(tag.TagClassValue)[0:1]
                    if S == "S":
                        tis_i = {}
                        tis_i["title"] = tag.FEFportIP
                        tis_i["WD"] = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                 tag.TagClassValue + "WD"))
                        tis_i["Flow"] = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                   tag.TagClassValue + "F"))
                        tis_i["Sum"] = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                  tag.TagClassValue + "S"))
                        dis.append(tis_i)
                    elif S == "W":
                        tiw_i = {}
                        tiw_i["title"] = tag.FEFportIP
                        tiw_i["Flow"] = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                   tag.TagClassValue + "F"))
                        tiw_i["Sum"] = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                  tag.TagClassValue + "S"))
                        diw.append(tiw_i)
                    elif S == "E":
                        tie_i = {}
                        tie_i["title"] = tag.FEFportIP
                        tie_i["ZGL"] = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                  tag.TagClassValue + "_ZGL"))
                        tie_i["AU"] = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                 tag.TagClassValue + "_AU"))
                        tie_i["AI"] = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                 tag.TagClassValue + "_AI"))
                        tie_i["BU"] = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                 tag.TagClassValue + "_BU"))
                        tie_i["BI"] = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                 tag.TagClassValue + "_BI"))
                        tie_i["CU"] = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                 tag.TagClassValue + "_CU"))
                        tie_i["CI"] = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                 tag.TagClassValue + "_CI"))
                        die.append(tie_i)
                except Exception as ee:
                    print("报错tag：" + tag.TagClassValue + " |报错IP：" + tag.IP + "  |报错端口：" + tag.COMNum + "  |错误：" + str(
                        ee))
                finally:
                    i = i + 1
                    pass
            data_dict["E"] = die
            data_dict["S"] = dis
            data_dict["W"] = diw
            dir.append(data_dict)
            print(dir)
            json_data = json.dumps(data_dict)
            bytemsg = bytes(json_data, encoding="utf-8")
            user.write_message("[{}][{}:{}] {}".format(now, remote_ip, port, bytemsg))

    def on_close(self):
        # 用户关闭连接后从容器中移除用户
        now = datetime.now().strftime("%H:%M:%S")
        remote_ip, port = self.request.connection.context.address
        self.users.remove(self)
        for user in self.users:
            user.write_message("[{}][{}:{}]-离开聊天室".format(now, remote_ip, port))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/chat", ChatHandler),
    ],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        debug=True
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
