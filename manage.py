from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session
from flask import session
import redis


app = Flask(__name__)

class Config(object):
    # 设置项目配置项
    SECRET_KEY = 'DSFSFdgrgsdfsef'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/Watching_news_world'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 配置flask_session
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    # 存储session到redis
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 86400

app.config.from_object(Config)
db = SQLAlchemy(app)
# 存储容易变化的值
redis_store = StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
StrictRedis(app)
# 开启csrf
CSRFProtect(app)
Session(app)

@app.route('/')
def index():
    # redis_store.set(('name_test'),'sdgewgsfgwe')
    session['qwe'] = 'sfsdfwrwfsdgwfwgf'
    return 'index'


if __name__ == "__main__":
    app.run()