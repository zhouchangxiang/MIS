import json

from flask import Blueprint, request

from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.SystemManagement.core import SteamEnergy, TagDetail

foo = Blueprint('foo', __name__)

#
# @opc.route('/energy_trend', methods=['GET'])
# def energy_trends():
#     """趋势图"""
#     try:
#         if request.values.get('TagFlag') == 'first':
#             # 多个tag点查询一天
#             TagCodes = request.values.get('TagCodes').split(",")
#             Begin = request.values.get('begin')
#             End = request.values.get('end')
#             data = []
#             count = 0
#             for item in TagCodes:
#                 count += 1
#                 sql = "select " + "`SampleTime` as time, " + "`" + item + "`" + " as value" + " from datahistory where" \
#                                                                                               " SampleTime between " + "'" + Begin + "'" + " and " + "'" + End + "'"
#                 results = db_session.execute(sql).fetchall()
#                 list1 = []
#                 for result in results[::30]:
#                     list1.append({f'time{count}': datetime.strftime(result['time'], "%Y-%m-%d %H:%M:%S"),
#                                   f'value{count}': result['value']})
#                 # data.append({item: list1})
#                 data.append(list1)
#             return json.dumps({'code': '20001', 'message': '成功', 'data': data}, cls=AlchemyEncoder, ensure_ascii=False)
#         else:
#             # 一个tag查询多天
#             start_date = datetime.strptime(request.values.get('start_date'), "%Y-%m-%d")
#             end_date = datetime.strptime(request.values.get('end_date'), "%Y-%m-%d")
#             if start_date != end_date:
#                 date_list = [request.values.get('start_date')]
#                 while True:
#                     start_date += timedelta(days=1)
#                     if start_date == end_date:
#                         date_list.append(datetime.strftime(end_date, "%Y-%m-%d"))
#                         break
#                     else:
#                         date_list.append(datetime.strftime(start_date, "%Y-%m-%d"))
#                 Begin = request.values.get("start_time")
#                 End = request.values.get("end_time")
#                 data = []
#                 count = 0
#                 for item in date_list:
#                     count += 1
#                     start_time = item + " " + Begin
#                     end_time = item + " " + End
#                     sql = "select `SampleTime` as time, " + "`" + request.values.get(
#                         'TagCode') + "`" + "as value from " \
#                                            "datahistory where SampleTime between " + "'" + start_time + "'" + " and " + "'" + end_time + "'"
#                     results = db_session.execute(sql).fetchall()
#                     list1 = []
#                     for result in results[::30]:
#                         list1.append({f'time{count}': datetime.strftime(result['time'], "%Y-%m-%d %H:%M:%S"),
#                                       f'value{count}': result['value']})
#                     # data.append({item: list1})
#                     data.append(list1)
#                 return json.dumps({'code': '20001', 'message': '成功', 'data': data, 'date': date_list},
#                                   cls=AlchemyEncoder, ensure_ascii=False)
#             else:
#                 Begin = request.values.get("start_time")
#                 End = request.values.get("end_time")
#                 data = []
#                 count = 0
#                 for item in [request.values.get('start_date')]:
#                     count += 1
#                     start_time = item + " " + Begin
#                     end_time = item + " " + End
#                     sql = "select `SampleTime` as time, " + "`" + request.values.get('TagCode') + "`" + "as value from " \
#                           "datahistory where SampleTime between " + "'" + start_time + "'" + " and " + "'" + end_time + "'"
#                     results = db_session.execute(sql).fetchall()
#                     list1 = []
#                     for result in results[::30]:
#                         list1.append({f'time{count}': datetime.strftime(result['time'], "%Y-%m-%d %H:%M:%S"),
#                                       f'value{count}': result['value']})
#                     # data.append({item: list1})
#                     data.append(list1)
#                 return json.dumps({'code': '20001', 'message': '成功', 'data': data}, cls=AlchemyEncoder,
#                                   ensure_ascii=False)
#
#     except Exception as e:
#         logger.error(e)
#         insertSyslog("error", "energy_trend错误：" + str(e), current_user.Name)
#         return json.dumps({'code': '20002', 'message': 'energy_trend错误： ' + str(e)},
#                           cls=AlchemyEncoder, ensure_ascii=False)
#
#
# @opc.route('/tags', methods=['GET'])
# def tags():
#     """树形tag点"""
#     factory = db_session.query(AreaMaintain).first()
#     sql = "select ChildrenTag from tags"
#     parent_tags = db_session.execute(sql).fetchall()
#     tags_list = set(str(item[0]) for item in parent_tags)
#     children = []
#     for item in tags_list:
#         # 通过一级节点获取所有对应节点下的值
#         children2 = []
#         children1 = {"label": item, "children": children2}
#         query_data = db_session.query(Tags).filter_by(ChildrenTag=item).all()
#         parent_tag2 = set(item.ParentTag for item in query_data)
#         for result in parent_tag2:
#             # children4 = []
#             # 通过一级节点获取所有对应的二级节点
#             if result:
#                 # 二级节点不为空
#                 children3 = []
#                 rank2_data = {"label": result, "children": children3}
#                 # children4.append(rank2_data)
#                 last_data = db_session.query(Tags).filter_by(ParentTag=result).all()
#                 parent_tag_sql = 'select '
#                 for data in last_data:
#                     # 循环获取最后节点的数据
#
#                     rank3_data = {"id": data.TagCode, "label": data.TagName, "ParentTagCode": "1"}
#                     children3.append(rank3_data)
#                 children2.append(rank2_data)
#                 # rank3 = {"label": result.ParentTag, "children": [{"id": result.TagCode, "label": result.TagName}]}
#             else:
#                 for data in query_data:
#                     rank2_data = {"id": data.TagCode, "label": data.TagName, "ParentTagCode": "1"}
#                     children2.append(rank2_data)
#         children.append(children1)
#     tree = [{"label": factory.AreaName, "children": children}]
#     return json.dumps({'code': '20001', 'message': '成功', 'data': tree}, cls=AlchemyEncoder, ensure_ascii=False)





@foo.route('/flow', methods=["GET", 'POST'])
def count():
    if request.method == 'GET':

        data = [{'原提取车间': ['原提取蒸气表']}, {'前处理车间': ['前处理蒸气表']}, {'提取二车间': ['灭菌柜蒸气表', '喷雾车间蒸气表',
                '管式灭菌蒸气表', '单号提取罐蒸气表', '双号提取罐蒸气表', '单/双效浓缩蒸气表']},{'综合制剂车间': ['综合制剂蒸气表']},
                {'综合车间': ['120带干蒸汽表','单号提取蒸汽表', '双号提取蒸气表', '双效浓缩蒸汽表', '二次浓缩（刮板浓缩）蒸汽表',
               '醇提车间（醇提+浓缩）蒸汽表','流化床制粒蒸汽表	']}, {'固体制剂车间': ['固体制剂蒸气表']}, {'办公楼\食堂': ['办公楼\食堂蒸气表']}, {'GMP车间': ['GMP蒸气表']}]
        return json.dumps({'code': '200', 'msg': '操作成功', 'data': data}, cls=AlchemyEncoder, ensure_ascii=False)

    if request.method == 'POST':
        data = request.values.get('name')
        start_time = request.values.get('start_time')
        end_time = request.values.get('end_time')
        print('data')
        tag = db_session.query(TagDetail).filter(TagDetail.FEFportIP == data).first()
         # = db_session.query(TagDetail).filter(TagDetail.FEFportIP == data).first()

        pass