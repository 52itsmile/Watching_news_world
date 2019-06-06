from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session
from flask import session
import redis
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from config import Config
app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
# 存储容易变化的值
redis_store = StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)

StrictRedis(app)
# 开启csrf
CSRFProtect(app)
# 设置session
Session(app)
# 设置flask_script
manager = Manager(app)
# 设置数据库迁移
manager.add_command('db',MigrateCommand)
Manager(app,db)

@app.route('/')
def index():
    # redis_store.set(('name_test'),'sdgewgsfgwe')
    # session['qwe'] = 'sfsdfwrwfsdgwfwgf'
    return 'index'


if __name__ == "__main__":
    app.run()