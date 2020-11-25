import json
from io import BytesIO
import pandas as pd
from flask import make_response, Blueprint, request

import xlwt

from flask import Blueprint, request

from dbset.database.db_operate import db_session
from dbset.main.BSFramwork import AlchemyEncoder
from models.SystemManagement.core import SteamEnergy, TagDetail
from models.tags_model import Tags

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

@foo.route('/tags', methods=['GET'])
def tags():
    """树形tag点"""
    # factory = db_session.query(AreaMaintain).first()
    sql = "select ChildrenTag from tags"
    parent_tags = db_session.execute(sql).fetchall()
    tags_list = set(str(item[0]) for item in parent_tags)
    children = []
    for item in tags_list:
        # 通过一级节点获取所有对应节点下的值
        children2 = []
        children1 = {"label": item, "children": children2}
        query_data = db_session.query(Tags).filter_by(ChildrenTag=item).all()
        parent_tag2 = set(item.ParentTag for item in query_data)
        for data in query_data:
            rank2_data = {"id": data.TagCode, "label": data.TagName, "ParentTagCode": "1"}
            children2.append(rank2_data)
        children.append(children1)
        # for result in parent_tag2:
        #     # children4 = []
        #     # 通过一级节点获取所有对应的二级节点
        #     if result:
        #         # 二级节点不为空
        #         children3 = []
        #         rank2_data = {"label": result, "children": children3}
        #         # children4.append(rank2_data)
        #         # last_data = db_session.query(Tags).filter_by(ParentTag=result).all()
        #         parent_tag_sql = 'select '
        #         # for data in last_data:
        #         #     # 循环获取最后节点的数据
        #         #
        #         #     rank3_data = {"id": data.TagCode, "label": data.TagName, "ParentTagCode": "1"}
        #         #     children3.append(rank3_data)
        #         # children2.append(rank2_data)
        #         # rank3 = {"label": result.ParentTag, "children": [{"id": result.TagCode, "label": result.TagName}]}
        #     else:
        #         for data in query_data:
        #             rank2_data = {"id": data.TagCode, "label": data.TagName, "ParentTagCode": "1"}
        #             children2.append(rank2_data)
        # children.append(children1)
    tree = [{"label": '辽宁好护士药业', "children": children}]
    return json.dumps({'code': '20001', 'message': '成功', 'data': tree}, cls=AlchemyEncoder, ensure_ascii=False)


@foo.route('/flow', methods=['POST'])
def count():
    tag = "'" + request.values.get('tag') + "'"
    start_time = "'" + request.values.get('start_time') + "'"
    end_time = "'" + request.values.get('end_time') + "'"
    # tag = "'" + 'S_Area_TQR_19_3_502' + "'"
    # start_time = "'" + '2020-11-15 07:00:00' + "'"
    # end_time = "'" + '2020-11-16 07:00:00' + "'"
    print(tag)
    print(start_time)
    print(end_time)
    sql = "select CollectionDate, FlowValue from [DB_MICS].[dbo].[SteamEnergy] where TagClassValue=" + tag + " and CollectionDate between " + start_time + " and " + end_time +" order by CollectionDate"
    results = db_session.execute(sql).fetchall()
    print(results)
    data = []
    for result in results:
        data.append({'time': result[0], 'value': result[1]})
    return json.dumps({'code': '200', 'msg': '操作成功', 'data': data}, cls=AlchemyEncoder, ensure_ascii=False)


@foo.route('/exports')
def excelout():
    '''
    导出原始数据
    :return:
    '''
    data = request.values
    if request.method == 'GET':
        tag = "'" + request.values.get('tag') + "'"
        start_time = "'" + request.values.get('start_time') + "'"
        end_time = "'" + request.values.get('end_time') + "'"
        output = exportx(tag,start_time,end_time)
        resp = make_response(output.getvalue())
        resp.headers["Content-Disposition"] = "attachment; filename=testing.xlsx"
        resp.headers['Content-Type'] = 'application/x-xlsx'
        return resp


def exportx(tag, start_time, end_time):
    # 创建数据流
    output = BytesIO()
    # 创建excel work book
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    # 创建excel sheet
    worksheet = workbook.add_worksheet('sheet1')
    # cell 样式
    cell_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#006633'})

    col = 0
    row = 1

    columns = ['区域', '采集时间', '瞬时流量', '瞬时流量单位', '温度', '累计值', '累计值单位', '体积']
    # if Area != "" and Area != None:
    #     tas = db_session.query(TagDetail).filter(TagDetail.AreaName == Area, TagDetail.EnergyClass == EnergyClass, TagDetail.IsExport == "是").all()
    # else:
    #     tas = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()

    # 写入列名
    # columns = ['区域', '采集点', '增量值', '单位', '开始时间', '结束时间']
    # if EnergyClass == "电":
    #     columns = ['区域', '采集点', '用电设备', '增量值', '单位', '开始时间', '结束时间']
    for item in columns:
        worksheet.write(0, col, item, cell_format)
        col += 1
    # UnitValue = db_session.query(Unit.UnitValue).filter(Unit.UnitName == EnergyClass).first()
    # if UnitValue:
    #     unit = UnitValue[0]
    # else:
    #     unit = ""
    # if EnergyClass == "汽":
    #     # totaltag = db_session.query(TagDetail).filter(TagDetail.TagClassValue == "S_AllArea_Value").first()
    #     totalm = energyStatisticsteamtotal(StartTime, EndTime)
    #     for cum in columns:
    #         if cum == '采集点':
    #             worksheet.write(1, columns.index(cum), totaltag.FEFportIP)
    #         if cum == '增量值':
    #             worksheet.write(1, columns.index(cum), totalm)
    #         if cum == '区域':
    #             worksheet.write(1, columns.index(cum), totaltag.AreaName)
    #         if cum == '单位':
    #             worksheet.write(1, columns.index(cum), unit)
    #         if cum == '开始时间':
    #             worksheet.write(1, columns.index(cum), StartTime)
    #         if cum == '结束时间':
    #             worksheet.write(1, columns.index(cum), EndTime)
    # 写入数据
    sql = "select AreaName, CollectionDate, FlowValue, FlowUnit, WD, SumValue, SumUnit, Volume from [DB_MICS].[dbo].[SteamEnergy] where TagClassValue=" + tag + " and CollectionDate between " + start_time + " and " + end_time + " order by CollectionDate"
    # sql = "select AreaName, CollectionDate, FlowValue, FlowUnit, WD, SumValue, SumUnit, Volume from [DB_MICS].[dbo].[SteamEnergy] where CollectionDate between '2020-11-24 07:00:00' and '2020-11-24 18:00:00'"
    all_data = db_session.execute(sql).fetchall()
    i = 1
    for ta in all_data:
        # reclass = tongjibaobiaosql(EnergyClass, ta.TagClassValue, StartTime, EndTime)
        for cum in columns:
            if cum == '区域':
                worksheet.write(i, columns.index(cum), ta[0])
            if cum == '采集时间':
                worksheet.write(i, columns.index(cum), ta[1])
            if cum == '瞬时流量':
                worksheet.write(i, columns.index(cum), ta[2])
            if cum == '瞬时流量单位':
                worksheet.write(i, columns.index(cum), ta[3])
            if cum == '温度':
                worksheet.write(i, columns.index(cum), ta[4])
            if cum == '累计值':
                worksheet.write(i, columns.index(cum), ta[5])
            if cum == '累计值单位':
                worksheet.write(i, columns.index(cum), ta[6])
            if cum == '体积':
                worksheet.write(i, columns.index(cum), ta[7])
        i += 1
    writer.close()
    output.seek(0)
    return output