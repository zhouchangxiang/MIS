from flask import Flask
from flask_cors import CORS
from flask_script import Manager
from common.electric_energy.views import electrics
from common.accounts.views import accounts
from common.steam_energy.views import steams
from common.warter_energy.views import waters

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
manage = Manager(app)


# 手机管理
app.register_blueprint(accounts, url_prefix='/v2/accounts')
app.register_blueprint(electrics, url_prefix='/v2/electrics')
app.register_blueprint(steams, url_prefix='/v2/steams')
app.register_blueprint(waters, url_prefix='/v2/waters')


@app.route('/')
def hello_world():
    return 'Hello 2020!'


if __name__ == '__main__':
    manage.run()
