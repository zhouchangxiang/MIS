import json

import redis
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from flask_login import current_user
import pymssql
from dbset.database import constant

GLOBAL_DATABASE_CONNECT_STRING= "mssql+pymssql://sa:Qcsw@758@192.168.2.123:1433/DB_MICS?charset=utf8"
engine = create_engine(GLOBAL_DATABASE_CONNECT_STRING, deprecate_large_types=True)
Session = sessionmaker(bind=engine)
db_session = Session()
pool = redis.ConnectionPool(host=constant.REDIS_HOST, password=constant.REDIS_PASSWORD)


