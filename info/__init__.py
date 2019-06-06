from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session
from flask import session
import redis
from config import config
app = Flask(__name__)

app.config.from_object(config['develop'])
db = SQLAlchemy(app)
# 存储容易变化的值
redis_store = StrictRedis(host=config['develop'].REDIS_HOST,port=config['develop'].REDIS_PORT)

StrictRedis(app)
# 开启csrf
CSRFProtect(app)
# 设置session
Session(app)