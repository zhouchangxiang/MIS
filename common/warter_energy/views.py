from flask import Blueprint
from handlers.energymanager.energy_manager import energyStatistics

waters = Blueprint('waters', __name__)


@waters.route('/water_energy', methods=['GET'])
def get_water_energy():

    energyStatistics
    pass

