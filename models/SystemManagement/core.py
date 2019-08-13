
#/******************************************************************************************
# ************* STK make model usage:
# ************* version: print python3.6.3  version
# ************* make: make Python file
# ************* STK makemodel.py 1.0.0
# ************* @author Xujin
# ************* @date 2019-08-09 15:58:36
# ************* @Model 
# ******************************************************************************************/

#引入必要的类库
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column,ForeignKey, Table, DateTime, Integer, String
from sqlalchemy import Column, DateTime, Float, Integer, String, Unicode,BigInteger
from sqlalchemy.dialects.mssql.base import BIT
from dbset.database.db_operate import GLOBAL_DATABASE_CONNECT_STRING
from datetime import datetime
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

#引入mssql数据库引擎
import pymssql

# 创建对象的基类
engine = create_engine(
		GLOBAL_DATABASE_CONNECT_STRING, deprecate_large_types=True,
		max_overflow=0,  # 超过连接池大小外最多创建的连接
		pool_size=100,  # 连接池大小
		pool_timeout=50,  # 池中没有线程最多等待的时间，否则报错
		pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
		 # echo = True   #输出SQL
)
SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()
Base = declarative_base(bind=engine)

# AA_START:
class AA(Base):
	__tablename__ = "AA"

	# 用户名:
	name = Column(Unicode, primary_key=False, autoincrement=False, nullable=True)

	# 密码:
	password = Column(Unicode, primary_key=False, autoincrement=False, nullable=True)

	# ID:
	ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)


# AA_END:

# 生成表单的执行语句_START
def init_db():
	try:
		Base.metadata.create_all(engine)
	except Exception as err:
		raise Exception('创建数据库出错！错误信息为：' + str(err))

def drop_db():
	Base.metadata.drop_all(engine)
init_db()
# 生成表单的执行语句_END
