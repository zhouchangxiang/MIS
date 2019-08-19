
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


#Factory_START:
class Factory(Base):
	__tablename__ = "Factory" 
	
	#ID:
	ID = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
	
	#所在地区:
	Region = Column(Unicode(65), primary_key = False, autoincrement = False, nullable = True)
	
	#厂名:
	FactoryName = Column(Unicode(65), primary_key = False, autoincrement = False, nullable = True)
	
#Factory_END:




#DepartmentManager_START:
class DepartmentManager(Base):
	__tablename__ = "DepartmentManager" 
	
	#ID:
	ID = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
	
	#部门名称:
	DepartName = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
	#部门编码:
	DepartCode = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
	#所属厂区:
	DepartLoad = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
#DepartmentManager_END:

#MenuType_START:
class MenuType(Base):
	__tablename__ = "MenuType"
	
	#ID:
	ID = Column(Integer, primary_key = True, autoincrement = True, nullable = False)

	#类型名称:
	TypeName = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
	#类型编码:
	TypeCode = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)

#MenuType_END:

# Role_START:
class Role(Base):
	__tablename__ = "Role"

	# ID:
	ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

	#角色编码:
	RoleCode = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
	#RoleName:
	RoleName = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
	#Description:
	Description = Column(Unicode(50), primary_key = False, autoincrement = False, nullable = True)
	
	#所属部门:
	ParentNode = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
#Role_END:


#User_START:
class User(Base):
	__tablename__ = "User" 
	
	#ID:
	id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
	
	#用户名:
	Name = Column(Unicode(64), primary_key = False, autoincrement = False, nullable = True)
	
	#密码:
	Password = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
	#工号:
	WorkNumber = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
	#登录状态:
	Status = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
	#创建用户:
	Creater = Column(Unicode(65), primary_key = False, autoincrement = False, nullable = True)
	
	#创建时间:
	CreateTime = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
	#上次登录时间:
	LastLoginTime = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
	#是否锁定:
	IsLock = Column(BIT, primary_key = False, autoincrement = False, nullable = True)
	
	#所属厂区:
	FactoryName = Column(Unicode(65), primary_key = False, autoincrement = False, nullable = True)
	
	#所属部门:
	OrganizationName = Column(Unicode(50), primary_key = False, autoincrement = False, nullable = True)
	
	#角色名称:
	RoleName = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)
	
	#角色编码:
	RoleCode = Column(Unicode(32), primary_key = False, autoincrement = False, nullable = True)

	# session_ID:
	session_id = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

	# @property
	# def password(self):
	#     raise AttributeError('password is not a readable attribute')

	# 定义password字段的写方法，我们调用generate_password_hash将明文密码password转成密文Shadow
	# @password.setter
	def password(self, password):
		self.Password = generate_password_hash(password)
		return self.Password

	# 定义验证密码的函数confirm_password
	def confirm_password(self, password):
		return check_password_hash(self.Password, password)

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)  # python 3
	
#User_END:

# 生成表单的执行语句_START
Base.metadata.create_all(engine)

# 生成表单的执行语句_END
