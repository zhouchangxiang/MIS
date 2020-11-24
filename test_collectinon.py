import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
import struct
import time, datetime
import redis

from dbset.database import constant
from dbset.database.db_operate import db_session, conn
from models.SystemManagement.core import TagDetail
from test_model import TestSteamEnergy

pool = redis.ConnectionPool(host=constant.REDIS_HOST, decode_responses=True)
redis_conn = redis.Redis(connection_pool=pool, password=constant.REDIS_PASSWORD)


while True:
    print("Test数据开始存入历表")
    # tags = db_session.query(TagDetail).filter(TagDetail.TagClassValue == 'S_Area_TQR_19_3_502').all()
    for item in ['S_Area_TQR_19_3_502', 'S_Area_TQR_19_1_502', 'S_Area_TQR_19_2_502', 'S_Area_ZH_46_3_502', 'S_Area_ZH_21_3_502', 'S_Area_ZH_21_1_502']:
        try:
            # d-温度 c-瞬时流量 e-体积 f-累积量
            tag = db_session.query(TagDetail).filter(TagDetail.TagClassValue == item).first()
            print(tag.TagClassValue)
            d = redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue+"WD")
            print(d)

            c = redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "F")

            e = redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "V")

            f = redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "S")
            print(f)
            save_time = redis_conn.hget(constant.REDIS_TABLENAME, tag.TagClassValue + "_Samptime")
            data = [tag.TagClassValue, save_time, d, c, e, f]
            # data.TagClassValue = tag
            # data.CollectionDate = save_time
            # data.WD = d
            # data.FlowValue = c
            # data.Volume = e
            # data.SumValue = f
            cursor = conn.cursor()
            sql = "insert into TestSteamEnergy(TagClassValue, CollectionDate, WD, FlowValue, Volume, SumValue) values " + f"('{tag.TagClassValue}', '{save_time}', '{d}', '{c}', '{e}', '{f}')"
            cursor.execute(sql)
            conn.commit()
            # db_session.add(data)
            # db_session.commit()
            print('写入完成')
        except Exception as e:
            print(str(e))
    time.sleep(300)
