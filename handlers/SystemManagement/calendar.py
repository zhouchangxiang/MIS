import string
from flask import Blueprint, render_template, request, make_response
from sqlalchemy.orm import Session, relationship, sessionmaker
from sqlalchemy import create_engine, func
import json
import socket
import datetime
from flask_login import login_required, logout_user, login_user,current_user,LoginManager
import re
from dbset.database import db_operate
from dbset.log.BK2TLogger import insertSyslog, MESLogger
from dbset.main.BSFramwork import AlchemyEncoder
from models.SystemManagement.system import Organization
from collections import Counter
from dbset.log.BK2TLogger import logger,insertSyslog
from tools.common import insert,delete,update
from dbset.database.db_operate import db_session

calender = Blueprint('calender', __name__, template_folder='templates')

# 日历
@calender.route('/calender')
def calender():
    return render_template('./calender.html')