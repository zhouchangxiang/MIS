from flask import Blueprint, request

from dbset.database.db_operate import db_session
from models.SystemManagement.core import ElectricEnergy

electrics = Blueprint('electrics', __name__)


@electrics.route('/electric_energy', methods=['GET'])
def get_electric_energy():
    start_time = request.values.get('StartTime')
    end_time = request.values.get('EndTime')
    result = db_session.query(ElectricEnergy).filter().all()
    # result = db_session.query(ElectricEnergy).filter(ElectricEnergy.CollectionDate.between(start_time, end_time)).all()
    pass