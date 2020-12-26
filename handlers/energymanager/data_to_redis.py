# import redis
# from flask import Blueprint, render_template, request, make_response, send_file, jsonify
# import json
# import datetime
# from sqlalchemy import desc
# from dbset.database.db_operate import db_session, pool
# from dbset.main.BSFramwork import AlchemyEncoder
# from flask_login import login_required, logout_user, login_user, current_user, LoginManager
# import calendar
#
# from handlers.energymanager.energy_manager import energyStatistics, energyStatisticsCost, energyStatisticshour
# from models.SystemManagement.core import RedisKey, ElectricEnergy, WaterEnergy, SteamEnergy, LimitTable, Equipment, \
#     AreaTable, Unit, TagClassType, TagDetail, BatchMaintain
# from models.SystemManagement.system import EarlyWarning, EarlyWarningLimitMaintain, WaterSteamBatchMaintain, \
#     AreaTimeEnergyColour, ElectricProportion, IncrementElectricTable, ElectricPrice, RatedPowerMaintain, ElectricSiteURL
# from tools.common import insert, delete, update
# from dbset.database import constant
# from dbset.log.BK2TLogger import logger, insertSyslog
# import datetime
# import arrow
# import time
#
#
# def today_electric(start_time, end_time):
#     tags = db_session.query(TagDetail).filter(TagDetail.EnergyClass == '电').all()
#     tag_list = []
#     for tag in tags:
#         if tag.TagClassValue not in ['E_Area_ZH_50_1_41_3', 'E_Area_YTQ_38_2_29_3', 'E_Area_GT_30_2_19_2',
#                                      'E_Area_TQR_18_2_36_4']:
#             tag_list.append(tag.TagClassValue)
#         else:
#             pass
#     if len(tag_list) > 0:
#         electric_count = energyStatistics(tag_list, start_time, end_time, '电')
#     else:
#         electric_count = 0.0
#
#     if request.method == 'GET':
#         try:
#             dir = {}
#             data = request.values
#             Area = data.get("Area")
#             StartTime = data.get("StartTime")
#             EndTime = data.get("EndTime")
#             energy = "电"
#             elecount = 0.0
#             if Area is not None and Area != "":
#                 oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == energy,
#                                                             TagDetail.AreaName == Area).all()
#             else:
#                 oclass = db_session.query(TagDetail).filter(TagDetail.EnergyClass == energy).all()
#             oc_list = []
#             for oc in oclass:
#                 if oc.TagClassValue not in ['E_Area_ZH_50_1_41_3', 'E_Area_YTQ_38_2_29_3', 'E_Area_GT_30_2_19_2',
#                                             'E_Area_TQR_18_2_36_4']:
#                     oc_list.append(oc.TagClassValue)
#                 else:
#                     pass
#             if len(oc_list) > 0:
#                 elecount = energyStatistics(oc_list, StartTime, EndTime, energy)
#             else:
#                 elecount = 0.0
#             dir["value"] = elecount
#             dir["type"] = "电"
#             unit = db_session.query(Unit.UnitValue).filter(Unit.UnitName == energy).first()[0]
#             dir["unit"] = unit
#             # 成本
#             if len(oc_list) > 0:
#                 cost = energyStatisticsCost(oc_list, StartTime, EndTime, energy)
#             else:
#                 cost = 0.0
#             dir["cost"] = cost
#             return json.dumps(dir, cls=AlchemyEncoder, ensure_ascii=False)
#         except Exception as e:
#             print(e)
#             insertSyslog("error", "能耗查询报错Error：" + str(e), current_user.Name)
#             return json.dumps([{"status": "Error：" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
