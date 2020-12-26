from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, ForeignKey, Table, DateTime, Integer, String
from sqlalchemy import Column, DateTime, Float, Integer, String, Unicode, BigInteger
from dbset.database.db_operate import GLOBAL_DATABASE_CONNECT_STRING

# 引入mssql数据库引擎
import pymssql

# 创建对象的基类
engine = create_engine(GLOBAL_DATABASE_CONNECT_STRING, deprecate_large_types=True,
                       max_overflow=0,  # 超过连接池大小外最多创建的连接
                       pool_size=100,  # 连接池大小
                       pool_timeout=50,  # 池中没有线程最多等待的时间，否则报错
                       pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
                       # echo = True   #输出SQL
                       )
SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()
Base = declarative_base(engine)


class TestSteamEnergy(Base):
    """蒸汽能量"""
    __tablename__ = "TestSteamEnergy"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 瞬时流量单位:
    FlowUnit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 仪表ID:
    EquipmnetID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 价格ID:
    PriceID = Column(Float(53), primary_key=False, autoincrement=False, nullable=True)

    # 采集点:
    TagClassValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集时间:
    CollectionDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集年:
    CollectionYear = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集月:
    CollectionMonth = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集天:
    CollectionDay = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 温度:
    WD = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 蒸汽瞬时值（单位：kg/h）:
    FlowValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 蒸汽重量累计值（单位：kg）:
    SumValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 累计量体积单位:
    SumUnit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 体积（单位：m3:
    Volume = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 计算增量更新标识:
    IncrementFlag = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 两个相邻采集点上一个采集点ID:
    PrevID = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 区域:
    AreaName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 增量库体积插入标识
    insertVolumeFlag = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# 汽增量表
class TestIncrementStream(Base):
    __tablename__ = "TestIncrementStream"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 增量值:
    IncremenValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 增量类型:
    IncremenType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 计算原始数据表ID:
    CalculationID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 价格表ID:
    NewValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 单位:
    OldValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 仪表ID:
    EquipmnetID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 采集点:
    TagClassValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集时间:
    CollectionDate = Column(DateTime, primary_key=False, autoincrement=False, nullable=True)

    # 历史数据采集时间
    HistoryDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集月:
    CollectionMonth = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集天:
    CollectionDay = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集时:
    CollectionHour = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 区域:
    AreaName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 增量库插入标识
    insertFlag = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


Base.metadata.create_all(engine)
