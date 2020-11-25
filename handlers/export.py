# from io import BytesIO
# import pandas as pd
# from flask import make_response, Blueprint, request
#
# import xlwt
#
# from dbset.database.db_operate import db_session, conn
# from test_model import TestIncrementStream
#
#
# t = Blueprint('ex', __name__)
#
#
# def e():
#     fields = ['采集点', '采集时间', '增量']
#     sql = "select TagClassValue, CollectionDate, IncremenValue, HistoryDate, NewValue, OldValue from [DB_MICS].[dbo].[TestIncrementStream] where CollectionDate between '2020-11-24 07:00:00' and '2020-11-24 18:00:00'"
#     all_data = db_session.execute(sql).fetchall()
#     book = xlwt.Workbook()
#     sheet = book.add_sheet('sheet1')
#     for col, field in enumerate(fields):
#         sheet.write(0, col, field)
#     row = 1
#     for data in all_data:
#         for col, field in enumerate(data):
#             sheet.write(row, col, field)
#         row += 1
#     book.save('t.xls')
#
#
# e()
#
#
# @t.route('/ex')
# def excelout():
#     '''
#     导出原始数据
#     :return:
#     '''
#     data = request.values
#     if request.method == 'GET':
#         # Area = data.get("Area")
#         # EnergyClass = data.get("EnergyClass")
#         # StartTime = data.get("StartTime")
#         # EndTime = data.get("EndTime")
#         output = exportx()
#         resp = make_response(output.getvalue())
#         resp.headers["Content-Disposition"] = "attachment; filename=testing.xlsx"
#         resp.headers['Content-Type'] = 'application/x-xlsx'
#         return resp
#
#
# def exportx():
#     # 创建数据流
#     output = BytesIO()
#     # 创建excel work book
#     writer = pd.ExcelWriter(output, engine='xlsxwriter')
#     workbook = writer.book
#     # 创建excel sheet
#     worksheet = workbook.add_worksheet('sheet1')
#     # cell 样式
#     cell_format = workbook.add_format({
#         'bold': 1,
#         'border': 1,
#         'align': 'center',
#         'valign': 'vcenter',
#         'fg_color': '#006633'})
#
#     col = 0
#     row = 1
#
#     columns = ['区域', '采集时间', '瞬时流量', '瞬时流量单位', '温度', '累计值', '累计值单位', '体积']
#     # if Area != "" and Area != None:
#     #     tas = db_session.query(TagDetail).filter(TagDetail.AreaName == Area, TagDetail.EnergyClass == EnergyClass, TagDetail.IsExport == "是").all()
#     # else:
#     #     tas = db_session.query(TagDetail).filter(TagDetail.EnergyClass == EnergyClass).all()
#
#     # 写入列名
#     # columns = ['区域', '采集点', '增量值', '单位', '开始时间', '结束时间']
#     # if EnergyClass == "电":
#     #     columns = ['区域', '采集点', '用电设备', '增量值', '单位', '开始时间', '结束时间']
#     for item in columns:
#         worksheet.write(0, col, item, cell_format)
#         col += 1
#     # UnitValue = db_session.query(Unit.UnitValue).filter(Unit.UnitName == EnergyClass).first()
#     # if UnitValue:
#     #     unit = UnitValue[0]
#     # else:
#     #     unit = ""
#     # if EnergyClass == "汽":
#     #     # totaltag = db_session.query(TagDetail).filter(TagDetail.TagClassValue == "S_AllArea_Value").first()
#     #     totalm = energyStatisticsteamtotal(StartTime, EndTime)
#     #     for cum in columns:
#     #         if cum == '采集点':
#     #             worksheet.write(1, columns.index(cum), totaltag.FEFportIP)
#     #         if cum == '增量值':
#     #             worksheet.write(1, columns.index(cum), totalm)
#     #         if cum == '区域':
#     #             worksheet.write(1, columns.index(cum), totaltag.AreaName)
#     #         if cum == '单位':
#     #             worksheet.write(1, columns.index(cum), unit)
#     #         if cum == '开始时间':
#     #             worksheet.write(1, columns.index(cum), StartTime)
#     #         if cum == '结束时间':
#     #             worksheet.write(1, columns.index(cum), EndTime)
#     # 写入数据
#
#     sql = "select AreaName, CollectionDate, FlowValue, FlowUnit, WD, SumValue, SumUnit, Volume from [DB_MICS].[dbo].[SteamEnergy] where CollectionDate between '2020-11-24 07:00:00' and '2020-11-24 18:00:00'"
#     all_data = db_session.execute(sql).fetchall()
#     i = 1
#     for ta in all_data:
#         # reclass = tongjibaobiaosql(EnergyClass, ta.TagClassValue, StartTime, EndTime)
#         for cum in columns:
#             if cum == '采集点':
#                 worksheet.write(i, columns.index(cum), ta[0])
#             if cum == '采集时间':
#                 worksheet.write(i, columns.index(cum), ta[1])
#             if cum == '增量':
#                 worksheet.write(i, columns.index(cum), ta[2])
#             # if cum == '区域':
#             #     worksheet.write(i, columns.index(cum), ta.AreaName)
#             # if cum == '单位':
#             #     worksheet.write(i, columns.index(cum), unit)
#             # if cum == '开始时间':
#             #     worksheet.write(i, columns.index(cum), StartTime)
#             # if cum == '结束时间':
#             #     worksheet.write(i, columns.index(cum), EndTime)
#             # if cum == '用电设备':
#             #     worksheet.write(i, columns.index(cum), ta.Equipment)
#         i += 1
#     writer.close()
#     output.seek(0)
#     return output
