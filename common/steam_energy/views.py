import json
from flask import Blueprint, request
from numpy import unicode
from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.SystemManagement.core import TagDetail

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
        # results = db_session.query(ElectricEnergy).filter(ElectricEnergy.AreaName == area_name).filter(
        #     ElectricEnergy.CollectionDate.between(start_time, end_time)).order_by(ElectricEnergy.ID.desc()).all()
        # data = results[(current_page - 1) * pagesize + 1:current_page * pagesize + 1]
        # tag_list = db_session.query(TagDetail).filter(TagDetail.AreaName == unicode(area_name, 'utf-8'), TagDetail.EnergyClass == unicode('电'), 'utf-8').all()
        tag_list = db_session.query(TagDetail).filter(TagDetail.AreaName == area_name, TagDetail.EnergyClass == '电').all()
        tag_point = [index.TagClassValue for index in tag_list]
        sql = "select sum(cast(t1.IncremenValue as decimal(9,2)))*1.2*0.8 as count from [DB_MICS].[dbo].[IncrementElectricTable] t1 where t1.TagClassValue in " + (str(tag_point).replace('[', '(')).replace(']', ')') + " and t1.CollectionDate between " + "'" + start_time + "'" + " and" + "'" + end_time + "'" + " group by t1.IncremenType"
        result = db_session.execute(sql).fetchall()
        pass
        # return json.dumps({'综合': str(round(result[0]['count'], 2))}, cls=AlchemyEncoder, ensure_ascii=False)
    else:
        pass
    #     # results = db_session.query(ElectricEnergy).filter(
    #     #     ElectricEnergy.CollectionDate.between(start_time, end_time)).order_by(ElectricEnergy.ID.desc()).all()
    #     data = results[(current_page - 1) * pagesize + 1:current_page * pagesize + 1]
    # return json.dumps({'total': len(results), 'rows': data}, cls=AlchemyEncoder, ensure_ascii=False)
