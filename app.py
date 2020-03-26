from flask import Flask
from flask_cors import CORS
from flask_script import Manager
from mobile.users.views import mobile

app = Flask(__name__)
# CORS(app, supports_credentials=True)
CORS(app, resources={r'/*': {'origins': '*'}})
manage = Manager(app)

# 手机管理
app.register_blueprint(mobile, url_prefix='/v2/accounts')


@app.route('/')
def hello_world():
    return 'Hello 2020!'


if __name__ == '__main__':
    manage.run()
