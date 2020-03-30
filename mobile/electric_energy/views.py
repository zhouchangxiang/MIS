from flask import Blueprint, request
from dbset.database.db_operate import db_session
from handlers.energymanager.energy_manager import energyStatistics
from models.SystemManagement.core import AreaTable, TagDetail

electrics = Blueprint('electrics', __name__)


@electrics.route('/electric_energy', methods=['GET'])
def get_electric_energy():
    data = request.values.get('area')
    if data:
        areas = db_session.query(AreaTable).filter(AreaTable.AreaName).all()
    pass
    # re = request.values.get('area')
    # if re:
    #     re.get()
    # areas = db_session.query(AreaTable).filter(AreaTable.AreaName).all()
    # oc_list = []
    # dir = {}
    # for area in areas:
    #     data = db_session.query(TagDetail).filter_by(AreaName=area.AreaName).all()
    #     for tag in data:
    #         oc_list.append(tag.TagClassValue)
    #     dir["dian"] = energyStatistics(oc_list, '', '', 'µç')
    # return 'nihao'
