from flask import Blueprint, render_template, request
from flask_login import login_required
from tools import autocode
from tools.MESLogger import MESLogger
logger = MESLogger('../logs', 'log')

system_set = Blueprint('system_set', __name__, template_folder='templates')


# 加载工作台
@system_set.route('/home/workbench')
def workbenck():
    return render_template('./main/workbench.html')

# 加载工作台
@system_set.route('/system_set/make_model', methods=['POST', 'GET'])
def make_model():
    if request.method == 'POST':
        data = request.values
        try:
            autocode.make_model_main(data)
        except Exception as e:
            print(e)
            logger.error(e)


