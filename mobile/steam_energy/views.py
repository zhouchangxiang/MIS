import json
from flask import Blueprint, request, jsonify
from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.SystemManagement.core import TagDetail
from models.SystemManagement.system import IncrementStreamTable

steams = Blueprint('steams', __name__)


@steams.route('/steam_energy', methods=['GET'])
def get_steam_energy():
    pass


@steams.route('/get_steam_energy', methods=['GET'])
def get_electric():
    start_time = request.values.get('StartTime')
    end_time = request.values.get('EndTime')
    # 当前页数
    current_page = int(request.values.get('offset'))
    # 每页显示条数
    pagesize = int(request.values.get('limit'))
    area_name = request.values.get('AreaName')
    if area_name:
        # data = results[(current_page - 1) * pagesize + 1:current_page * pagesize + 1]
        rows = db_session.query(IncrementStreamTable).filter(IncrementStreamTable.AreaName == area_name).filter(IncrementStreamTable.CollectionDate.between(start_time, end_time)).all()[(current_page - 1) * pagesize + 1:current_page * pagesize + 1]
        total = len(db_session.query(IncrementStreamTable).filter(IncrementStreamTable.AreaName == area_name).filter(IncrementStreamTable.CollectionDate.between(start_time, end_time)).all())
        # data = rows[(current_page - 1) * pagesize + 1:current_page * pagesize + 1]
        tag_list = db_session.query(TagDetail).filter(TagDetail.AreaName == area_name, TagDetail.EnergyClass == '汽').all()
        tag_point = [index.TagClassValue for index in tag_list]
        sql = "select sum(cast(t1.IncremenValue as decimal(9,2)))*0.0001*50 as count from [DB_MICS].[dbo].[IncrementStreamTable] t1 where t1.TagClassValue in " + (str(tag_point).replace('[', '(')).replace(']', ')') + " and t1.CollectionDate between " + "'" + start_time + "'" + " and" + "'" + end_time + "'" + " group by t1.IncremenType"
        result = db_session.execute(sql).fetchall()
        return json.dumps({'rows': rows, 'total_column': total, 'price': str(round(result[0]['count'], 2))}, cls=AlchemyEncoder, ensure_ascii=False)
    else:
        tag_list = db_session.query(TagDetail).filter(TagDetail.EnergyClass == '汽').all()
        tag_point = [index.TagClassValue for index in tag_list]
        sql = "select t1.AreaName, sum(cast(t1.IncremenValue as decimal(9,2)))*0.0001*50 as count from [DB_MICS].[dbo].[IncrementStreamTable] t1 where t1.TagClassValue in " + (str(tag_point).replace('[', '(')).replace(']', ')') + "and t1.CollectionDate between " + "'" + start_time + "'" + " and" + "'" + end_time + "'" + " group by t1.AreaName"
        rows = db_session.query(IncrementStreamTable).filter(IncrementStreamTable.CollectionDate.between(start_time, end_time)).all()[(current_page - 1) * pagesize + 1:current_page * pagesize + 1]
        total = len(db_session.query(IncrementStreamTable).filter(IncrementStreamTable.CollectionDate.between(start_time, end_time)).all())
        # sql = "select t1.AreaName, sum(cast(t1.IncremenValue as decimal(9,2)))*0.0001*50 as count from [DB_MICS].[dbo].[IncrementStreamTable] t1 where "  + "t1.CollectionDate between " + "'" + start_time + "'" + " and" + "'" + end_time + "'" + " group by t1.AreaName"
        result = db_session.execute(sql).fetchall()
        return json.dumps({'rows': rows, 'total_column': total, 'price': str(round(result[0]['count'], 2))}, cls=AlchemyEncoder, ensure_ascii=False)

