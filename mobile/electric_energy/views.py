import json
from flask import Blueprint, request

from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.SystemManagement.core import ElectricEnergy, TagDetail

electrics = Blueprint('electrics', __name__)


# @electrics.route('/get_electric_data', methods=['GET', 'POST'])
# def get_electric():
#     start_time = request.values.get('StartTime')
#     end_time = request.values.get('EndTime')
#     # 当前页数
#     current_page = int(request.values.get('offset'))
#     # 每页显示条数
#     pagesize = int(request.values.get('limit'))
#     area_name = request.values.get('AreaName')
#     if area_name:
#         # results = db_session.query(ElectricEnergy).filter(ElectricEnergy.AreaName == area_name).filter(
#         #     ElectricEnergy.CollectionDate.between(start_time, end_time)).order_by(ElectricEnergy.ID.desc()).all()
#         # data = results[(current_page - 1) * pagesize + 1:current_page * pagesize + 1]
#         tag_list = db_session.query(TagDetail).filter(TagDetail.AreaName == area_name, TagDetail.EnergyClass == '电').all()
#         tag_point = [index.TagClassValue for index in tag_list]
#         sql = "select sum(cast(t1.IncremenValue as decimal(9,2)))*1.2*0.8 as count from [DB_MICS].[dbo].[IncrementElectricTable] t1 where t1.TagClassValue in " + (str(tag_point).replace('[', '(')).replace(']', ')') + " and t1.CollectionDate between " + "'" + start_time + "'" + " and" + "'" + end_time + "'" + " group by t1.IncremenType"
#         result = db_session.execute(sql).fetchall()
#
#         return json.dumps({'综合': str(round(result[0]['count'], 2))}, cls=AlchemyEncoder, ensure_ascii=False)
#     else:
#         results = db_session.query(ElectricEnergy).filter(
#             ElectricEnergy.CollectionDate.between(start_time, end_time)).order_by(ElectricEnergy.ID.desc()).all()
#         data = results[(current_page - 1) * pagesize + 1:current_page * pagesize + 1]
#     return json.dumps({'total': len(results), 'rows': data}, cls=AlchemyEncoder, ensure_ascii=False)
#
#
# @electrics.route('/electric_energy', methods=['GET'])
# def get_electric_energy():
#     start_time = request.values.get('StartTime')
#     end_time = request.values.get('EndTime')
#     result = db_session.query(ElectricEnergy).filter().all()
#     # result = db_session.query(ElectricEnergy).filter(ElectricEnergy.CollectionDate.between(start_time, end_time)).all()
#     pass
