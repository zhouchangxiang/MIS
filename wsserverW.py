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
from models.SystemManagement.core import TagDetail
from dbset.log.BK2TLogger import logger,insertSyslog


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
        # data_recv = c.recv(1024)
        while True:
            try:
                time.sleep(2)
                # if data_recv[0:1] == b"\x81":
                #     data_parse = parse_payload(data_recv)
                data_dict = {}
                pool = redis.ConnectionPool(host=constant.REDIS_HOST)
                redis_conn = redis.Redis(connection_pool=pool)
                Tags = db_session.query(TagDetail).filter().all()
                EtotalZGL = 0.0
                StotalF = 0.0
                StotalS = 0.0
                WtotalF = 0.0
                WtotalS = 0.0
                for tag in Tags:
                    try:
                        S = str(tag.TagClassValue)[0:1]
                        if S == "S":
                            data_dict[tag.TagClassValue + "WD"] = str(strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                  tag.TagClassValue + "WD")))
                            data_dict[tag.TagClassValue + "F"] = str(strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                 tag.TagClassValue + "F")))
                            data_dict[tag.TagClassValue + "S"] = str(strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                 tag.TagClassValue + "S")))
                            Sflow = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "F"))
                            Ssum = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "S"))
                            StotalF = StotalF +Sflow
                            StotalS = StotalS + Ssum
                        elif S == "W":
                            data_dict[tag.TagClassValue + "F"] = str(strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                 tag.TagClassValue + "F")))
                            data_dict[tag.TagClassValue + "S"] = str(strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                 tag.TagClassValue + "S")))
                            Wsum = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "S"))  # 水的累计流量
                            Wflow = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "F"))  # 水的瞬时流量
                            WtotalF = WtotalF + Wflow
                            WtotalS = WtotalS + Wsum
                        elif S == "E":
                            data_dict[tag.TagClassValue + "ZGL"] = str(strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                   tag.TagClassValue + "ZGL")))
                            data_dict[tag.TagClassValue + "AU"] = str(strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                  tag.TagClassValue + "AU")))
                            data_dict[tag.TagClassValue + "AI"] = str(strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                  tag.TagClassValue + "AI")))
                            data_dict[tag.TagClassValue + "BU"] = str(strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                  tag.TagClassValue + "BU")))
                            data_dict[tag.TagClassValue + "BI"] = str(strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                  tag.TagClassValue + "BI")))
                            data_dict[tag.TagClassValue + "CU"] = str(strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                  tag.TagClassValue + "CU")))
                            data_dict[tag.TagClassValue + "CI"] = str(strtofloat(redis_conn.hget(constant.REDIS_TABLENAME,
                                                                                  tag.TagClassValue + "CI")))
                            ZGL = strtofloat(redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "ZGL"))
                            EtotalZGL = EtotalZGL + ZGL
                    except Exception as ee:
                        print("报错tag：" + tag.TagClassValue + " |报错IP：" + tag.IP + "  |报错端口：" + tag.COMNum + "  |错误：" + str(ee))
                    finally:
                        pass
                data_dict["EtotalZGL"] = str(EtotalZGL)
                data_dict["StotalF"] = str(StotalF)
                data_dict["StotalS"] = str(StotalS)
                data_dict["WtotalF"] = str(WtotalF)
                data_dict["WtotalS"] = str(WtotalS)
                data_dict['currentTime'] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                json_data = json.dumps(data_dict)
                # bytemsg = bytes(json_data, encoding="utf8")
                # send_msg(c, bytes("recv: {}".format(data_parse), encoding="utf-8"))
                bytemsg = bytes(json_data,encoding="utf-8")
                send_msg(conn, bytemsg)
            except Exception as e:
                print(e)
            finally:
                pass
def strtofloat(f):
    if f == None or f == "" or f == "0.0":
        return 0.0
    else:
        return float(f)


def server_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 5005))
    sock.listen(2)
    t = threading.Thread(target=handler_accept(sock))
    t.start()


if __name__ == "__main__":
    server_socket()