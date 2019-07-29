#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import base64
import hashlib
import time

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource


def get_headers(data):
    """
    将请求头格式化成字典
    :param data:
    :return:
    """
    header_dict = {}
    data = str(data, encoding='utf-8')
    # data = str(data)

    header, body = data.split('\r\n\r\n', 1)
    header_list = header.split('\r\n')
    for i in range(0, len(header_list)):
        if i == 0:
            if len(header_list[i].split(' ')) == 3:
                header_dict['method'], header_dict['url'], header_dict['protocol'] = header_list[i].split(' ')
        else:
            k, v = header_list[i].split(':', 1)
            header_dict[k] = v.strip()
    return header_dict


def send_msg(conn, msg_bytes):
    """
    WebSocket服务端向客户端发送消息
    :param conn: 客户端连接到服务器端的socket对象,即： conn,address = socket.accept()
    :param msg_bytes: 向客户端发送的字节
    :return:
    """
    import struct

    token = b"\x81"
    length = len(msg_bytes)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)
    msg = token + msg_bytes
    conn.send(msg)
    return True

def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 9200))
    sock.listen(5)

    conn, address = sock.accept()
    data = conn.recv(1024)
    print(data)
    headers = get_headers(data)
    response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade:websocket\r\n" \
                   "Connection:Upgrade\r\n" \
                   "Sec-WebSocket-Accept:%s\r\n" \
                   "WebSocket-Location:ws://%s%s\r\n\r\n"

    value = headers['Sec-WebSocket-Key'] + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
    response_str = response_tpl % (ac.decode('utf-8'), headers['Host'], headers['url'])
    # response_str = response_tpl % (str(ac, encoding='utf-8'), headers['Host'], headers['url'])

    print(response_str)
    conn.send(bytes(response_str, encoding='utf-8'))

    # while True:
    try:
        info = conn.recv(1024)
    except Exception as e:
        info = None
    if not info:
        # break
        return
    payload_len = info[1] & 127
    if payload_len == 126:
        extend_payload_len = info[2:4]
        mask = info[4:8]
        decoded = info[8:]
    elif payload_len == 127:
        extend_payload_len = info[2:10]
        mask = info[10:14]
        decoded = info[14:]
    else:
        extend_payload_len = None
        mask = info[2:6]
        decoded = info[6:]

    # bytes_list = bytearray()
    # for i in range(len(decoded)):
    #     chunk = decoded[i] ^ mask[i % 4]
    #     bytes_list.append(chunk)
    # body = str(bytes_list, encoding='utf-8')
    icount = 0
    while True:
        bytes_list = ""
        icount = icount + 1
        strtmp = "My Websocket中文测试" + str(icount)
        # str(bytes_list.encode('utf-8').strip() + b"\n")
        # body = str(bytes_list, encoding='utf-8')
        bytemsg = bytes(strtmp, encoding="utf8")
        send_msg(conn, bytemsg)
        time.sleep(1)

    sock.close()

app = Flask(__name__)
api = Api(app)
class REDIS(Resource):
    def get(self):
        return run()
api.add_resource(REDIS, '/redis')



if __name__ == '__main__':
    run()