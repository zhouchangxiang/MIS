import time
import datetime
from sqlalchemy import desc
from dbset.database.db_operate import db_session
from models.SystemManagement.core import RedisKey, TagClassType, ElectricEnergy, Unit, WaterEnergy, \
    WaterEnergy, TagDetail
from dbset.log.BK2TLogger import logger, insertSyslog
from dbset.database.db_operate import engine,conn


def run():
    while True:
        # time.sleep(60)
        print("数据开始写入增量数据库")
        try:
            start = time.time()
            steamInitial= list()
            # stekeys = db_session.query(TagDetail).filter(TagDetail.insertFlag == "0").order_by(("ID")).all()
            Tags = db_session.query(TagDetail).filter(TagDetail.EnergyClass == '汽').order_by(("ID")).all()
            print(time.time() - start)
            start = time.time()
            for tag in Tags:
                Inikeys = db_session.query(WaterEnergy).filter(WaterEnergy.TagClassValue == tag.TagClassValue).order_by(desc("ID")).all()
                currID = 0
                preID = 0
                icount = 0
                for key in Inikeys:
                    if (preID == currID) and (preID == 0):
                        currID = key.ID
                        continue
                    elif (preID != currID) and (preID == 0):
                        preID = key.ID
                        ss = (preID,currID)
                        print(ss)
                        steamInitial.append(ss)
                        currID = key.ID
                        preID = 0
                    else:
                        pass
                    icount = icount + 1
                    if icount == len(Inikeys)-1:
                        currID = key.ID
                        currCollectionDate = key.CollectionDate
                        prekey = db_session.query(WaterEnergy).filter(
                            WaterEnergy.TagClassValue == tag.TagClassValue,
                            WaterEnergy.CollectionDate < currCollectionDate).order_by(desc("ID")).first()
                        if prekey != None:
                            preID = prekey.ID
                            ss = (preID,currID)
                            steamInitial.append(ss)
                        else:
                            preID = currID
                            ss = (preID,currID)
                            steamInitial.append(ss)

                    print(str(icount) + ":" + str(key.ID))

                print("一个TagOK的")

            print(datetime.datetime.now())
            print(time.time() - start)
            if len(steamInitial) > 0:
                try:
                    cursor = conn.cursor()
                    print(datetime.datetime.now())
                    cursor.executemany(
                        "update WaterEnergy SET prevID=(%d) where id=(%d)", steamInitial)
                    conn.commit()
                    print(datetime.datetime.now())
                except Exception as e:
                    print(e)
        except Exception as e:
            print("写入增量库报错：" + str(e))
            logger.errro(e)
            insertSyslog("error", "写入增量库报错Error：" + str(e), "")
        finally:
            pass
        print("数据开始写入增量库结束")
if __name__ == '__main__':
    run()