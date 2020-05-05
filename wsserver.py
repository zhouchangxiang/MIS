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
from models.SystemManagement.system import ElectricSiteURL
from models.SystemManagement.core import TagDetail, AreaTable
from dbset.log.BK2TLogger import logger,insertSyslog
import ast

pool = redis.ConnectionPool(host=constant.REDIS_HOST)
redis_conn = redis.Redis(connection_pool=pool)

def get_headers(data):
    headers = {}
    data = str(data, encoding="utf-8")

    header, body = data.split("\r\n\r\n", 1)

    header_list = header.split("\r\n")

    for i in header_list:
        i_list = i.split(":", 1)
        if len(i_list) >= 2:
            headers[i_list[0]] = "".join(i_list[1::]).strip()
        else:
            i_list = i.split(" ", 1)
            if i_list and len(i_list) == 2:
                headers["method"] = i_list[0]
                headers["protocol"] = i_list[1]
    return headers


def parse_payload(payload):
    payload_len = payload[1] & 127
    if payload_len == 126:
        extend_payload_len = payload[2:4]
        mask = payload[4:8]
        decoded = payload[8:]

    elif payload_len == 127:
        extend_payload_len = payload[2:10]
        mask = payload[10:14]
        decoded = payload[14:]
    else:
        extend_payload_len = None
        mask = payload[2:6]
        decoded = payload[6:]

    # 这里我们使用字节将数据全部收集，再去字符串编码，这样不会导致中文乱码
    bytes_list = bytearray()

    for i in range(len(decoded)):
        # 解码方式
        chunk = decoded[i] ^ mask[i % 4]
        bytes_list.append(chunk)
    body = str(bytes_list, encoding='utf-8')
    return body


def send_msg(conn, msg_bytes):
    # 接收的第一字节，一般都是x81不变
    first_byte = b"\x81"
    length = len(msg_bytes)
    if length < 126:
        first_byte += struct.pack("B", length)
    elif length <= 0xFFFF:
        first_byte += struct.pack("!BH", 126, length)
    else:
        first_byte += struct.pack("!BQ", 127, length)

    msg = first_byte + msg_bytes
    conn.sendall(msg)
    return True

sock_pool = []


def handler_accept(sock):

    while True:
        conn, addr = sock.accept()

        data = conn.recv(8096)
        headers = get_headers(data)
        # 对请求头中的sec-websocket-key进行加密
        response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                       "Upgrade:websocket\r\n" \
                       "Connection: Upgrade\r\n" \
                       "Sec-WebSocket-Accept: %s\r\n" \
                       "WebSocket-Location: ws://%s\r\n\r\n"

        # 第一次连接发回报文
        magic_string = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        if headers.get('Sec-WebSocket-Key'):
            value = headers['Sec-WebSocket-Key'] + magic_string

        ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
        response_str = response_tpl % (ac.decode('utf-8'), headers.get("Host"))
        conn.sendall(bytes(response_str, encoding="utf-8"))
        t = threading.Thread(target=handler_msg, args=(conn, ))
        t.start()


def handler_msg(conn):
    with conn as c:
        data_recv = c.recv(1024)
        runcount = 0
        failcount = 0
        while True:
            try:
                redis_conn.hset(constant.REDIS_TABLENAME, "websocket_start",
                                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                AreaName = ""
                time.sleep(2)
                if data_recv[0:1] == b"\x81":
                    data_parse = parse_payload(data_recv)
                    AreaName = str(data_parse)
                area_list = []
                areaSFlow = 0.0
                areaSSum = 0.0
                areaWFlow = 0.0
                areaWSum = 0.0
                areaEZGL = 0.0
                areaEAI = 0.0
                areaEAU = 0.0
                areaEBI = 0.0
                areaEBU = 0.0
                areaECI = 0.0
                areaECU = 0.0
                area_dir = {}
                if AreaName == "":
                    all_tags = returnb(redis_conn.hget(constant.REDIS_TABLENAME, "all_tags"))
                    if all_tags:
                        all_tags = ast.literal_eval(all_tags)
                    for tag in all_tags:
                        try:
                            S = tag[0:1]
                            if S == "S":
                                areaSFlow = areaSFlow + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                     tag + "F"))
                                areaSSum = areaSSum + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                   tag + "S"))
                            elif S == "W":
                                areaWFlow = areaWFlow + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                     tag + "F"))
                                areaWSum = areaWSum + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                   tag + "S"))
                            elif S == "E":
                                areaEZGL = areaEZGL + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                   tag + "_ZGL"))
                                areaEAU = areaEAU + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                 tag + "_AU"))
                                areaEAI = areaEAI + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                 tag + "_AI"))
                                areaEBI = areaEBI + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                 tag + "_BU"))
                                areaEBU = areaEBU + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                 tag + "_BI"))
                                areaECI = areaECI + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                 tag + "_CU"))
                                areaECU = areaECU + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                 tag + "_CI"))
                        except Exception as ee:
                            print(
                                "报错tag：" + tag.TagClassValue + " |报错IP：" + tag.IP + "  |报错端口：" + tag.COMNum + "  |错误：" + str(
                                    ee))
                        finally:
                            pass
                    area_dir["AreaName"] = ""
                    area_dir["areaSFlow"] = strtofloat(areaSFlow)
                    area_dir["areaSSum"] = strtofloat(areaSSum)
                    area_dir["areaWFlow"] = strtofloat(areaWFlow)
                    area_dir["areaWSum"] = strtofloat(areaWSum)
                    area_dir["areaEZGL"] = strtofloat(areaEZGL)
                    area_dir["areaEAI"] = strtofloat(areaEAI)
                    area_dir["areaEAU"] = strtofloat(areaEAU)
                    area_dir["areaEBI"] = strtofloat(areaEBI)
                    area_dir["areaEBU"] = strtofloat(areaEBU)
                    area_dir["areaECI"] = strtofloat(areaEBI)
                    area_dir["areaECU"] = strtofloat(areaEBU)
                else:
                    all_area_tags = returnb(redis_conn.hget(constant.REDIS_TABLENAME, AreaName))
                    if all_area_tags:
                        all_area_tags = ast.literal_eval(all_area_tags)
                    for tag_area in all_area_tags:
                        try:
                            S = tag_area[0:1]
                            if S == "S":
                                areaSFlow = areaSFlow + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                   tag_area + "F"))
                                areaSSum = areaSSum + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                 tag_area + "S"))
                            elif S == "W":
                                areaWFlow = areaWFlow + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                   tag_area + "F"))
                                areaWSum = areaWSum + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                 tag_area + "S"))
                            elif S == "E":
                                areaEZGL = areaEZGL + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                 tag_area + "_ZGL"))
                                areaEAU = areaEAU + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                               tag_area + "_AU"))
                                areaEAI = areaEAI + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                               tag_area + "_AI"))
                                areaEBI = areaEBI + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                               tag_area + "_BU"))
                                areaEBU = areaEBU + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                               tag_area + "_BI"))
                                areaECI = areaECI + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                               tag_area + "_CU"))
                                areaECU = areaECU + strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                               tag_area + "_CI"))
                        except Exception as ee:
                            print("报错tag：" + tag.TagClassValue + " |报错IP：" + tag.IP + "  |报错端口：" + tag.COMNum + "  |错误：" + str(ee))
                        finally:
                            pass
                    area_dir["AreaName"] = AreaName
                    area_dir["areaSFlow"] = strtofloat(areaSFlow)
                    area_dir["areaSSum"] = strtofloat(areaSSum)
                    area_dir["areaWFlow"] = strtofloat(areaWFlow)
                    area_dir["areaWSum"] = strtofloat(areaWSum)
                    area_dir["areaEZGL"] = strtofloat(areaEZGL)
                    area_dir["areaEAI"] = strtofloat(areaEAI)
                    area_dir["areaEAU"] = strtofloat(areaEAU)
                    area_dir["areaEBI"] = strtofloat(areaEBI)
                    area_dir["areaEBU"] = strtofloat(areaEBU)
                    area_dir["areaECI"] = strtofloat(areaEBI)
                    area_dir["areaECU"] = strtofloat(areaEBU)
                oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == "汽").all()
                dir_list = []
                for oc in oclass:
                    oc_dict_i_tag = {}
                    oc_dict_i = {}
                    oc_dict_i["flowValue"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc.TagClassValue + "F"))  # 蒸汽瞬时流量
                    oc_dict_i["sumValue"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc.TagClassValue + "S"))  # 蒸汽累计流量
                    oc_dict_i["SteamWD"] = strtofloat(
                        redis_conn.hget(constant.REDIS_TABLENAME, oc.TagClassValue + "WD"))  # 蒸汽体积
                    oc_dict_i_tag[oc.TagClassValue] = oc_dict_i
                    dir_list.append(oc_dict_i_tag)
                oc_dict = {}
                oc_dict["steam"] = dir_list
                area_list.append(oc_dict)
                area_list.append(area_dir)
                json_data = json.dumps(area_list)
                # bytemsg = bytes(json_data, encoding="utf8")
                # send_msg(c, bytes("recv: {}".format(data_parse), encoding="utf-8"))
                bytemsg = bytes(json_data,encoding="utf-8")
                send_msg(conn, bytemsg)
                runcount = runcount + 1
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


def server_socket():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 5002))
        sock.listen(2)
        #将所有的tag写入redis
        Tags = db_session.query(TagDetail).all()
        tag_all_list = []
        for tag in Tags:
            tag_all_list.append(tag.TagClassValue)
        redis_conn.hset(constant.REDIS_TABLENAME,"all_tags",str(tag_all_list))
        areas = db_session.query(AreaTable).all()
        for area in areas:
            tagareas = db_session.query(TagDetail).filter(TagDetail.AreaName == area.AreaName).all()
            area_tag_list = []
            for ta in tagareas:
                area_tag_list.append(ta.TagClassValue)
            redis_conn.hset(constant.REDIS_TABLENAME, area.AreaName, str(area_tag_list))
        t = threading.Thread(target=handler_accept(sock))
        t.start()
    except Exception as e:
        print(e)
        redis_conn.hset(constant.REDIS_TABLENAME, "websocket_status", "执行失败")


if __name__ == "__main__":
    server_socket()
