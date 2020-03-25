from flask import Flask
from flask_script import Manager

from handlers.mobile.views import mobilemanager

app = Flask(__name__)
manage = Manager(app)

# 手机管理
app.register_blueprint(mobilemanager, url_prefix='/mobile')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    manage.run()
