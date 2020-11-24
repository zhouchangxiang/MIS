from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, ForeignKey, Table, DateTime, Integer, String
from sqlalchemy import Column, DateTime, Float, Integer, String, Unicode, BigInteger
from sqlalchemy.dialects.mssql.base import BIT
from dbset.database.db_operate import GLOBAL_DATABASE_CONNECT_STRING
from datetime import datetime
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

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


class Tags(Base):
    """tags表"""
    __tablename__ = 'tags'
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # tag编号
    TagCode = Column(Unicode(100), nullable=True)
    # tag名称
    TagName = Column(Unicode(100), nullable=True)
    # 上级tag点
    ChildrenTag = Column(Unicode(100), nullable=True)
    # 父节点
    ParenTag = Column(Unicode(100), nullable=True)


Base.metadata.create_all(engine)

