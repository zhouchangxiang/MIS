import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
import struct
import time, datetime
import redis

from dbset.database import constant
from dbset.database.db_operate import db_session, conn
from models.SystemManagement.core import TagDetail
from test_model import TestIncrementStream

pool = redis.ConnectionPool(host=constant.REDIS_HOST, decode_responses=True)
redis_conn = redis.Redis(connection_pool=pool, password=constant.REDIS_PASSWORD)


while True:
    print("Test数据:计算增量数据")

    for item in ['S_Area_TQR_19_3_502', 'S_Area_TQR_19_1_502', 'S_Area_TQR_19_2_502', 'S_Area_ZH_46_3_502', 'S_Area_ZH_21_3_502', 'S_Area_ZH_21_1_502']:
        try:
            tag = db_session.query(TagDetail).filter(TagDetail.TagClassValue == item).first()
            print(tag.TagClassValue)
            # d-温度 c-瞬时流量 e-体积 f-累积量
            d = redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue+"WD")

            c = redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "F")

            e = redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "V")

            f = redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "S")
            old_value = redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "_old_S")
            print(f)
            save_time = redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "_Samptime")
            print(save_time)
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            redis_conn.hset(constant.REDIS_TABLENAME, tag.TagClassValue + "_old_WD", d)
            redis_conn.hset(constant.REDIS_TABLENAME, tag.TagClassValue + "_old_F", c)
            redis_conn.hset(constant.REDIS_TABLENAME, tag.TagClassValue + "_old_V", e)
            redis_conn.hset(constant.REDIS_TABLENAME, tag.TagClassValue + "_old_S", f)
            value = float(f) - float(old_value)
            cursor = conn.cursor()
            sql = "insert into TestIncrementStream(TagClassValue, CollectionDate, IncremenValue, HistoryDate, NewValue, OldValue) values " + f"('{tag.TagClassValue}', '{now_time}', '{value}', '{save_time}', '{f}', '{old_value}')"
            cursor.execute(sql)
            conn.commit()
            print('增量写入完成')
        except Exception as e:
            print(str(e))
    time.sleep(300)
