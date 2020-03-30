from flask import Blueprint
from handlers.energymanager.energy_manager import energyStatistics

steams = Blueprint('steams', __name__)


@steams.route('/steam_energy', methods=['GET'])
def get_steam_energy():

    energyStatistics
    pass

