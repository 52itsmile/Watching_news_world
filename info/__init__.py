import logging
from logging.handlers import RotatingFileHandler
from urllib import response

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import generate_csrf
from redis import StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session
from flask import session
import redis
from config import config
from info.utils.common import do_index_class

db = SQLAlchemy()

def set_log(config_name):
    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
# 声明这个变量属于哪一个对象
redis_store = None # type:StrictRedis
def create_app(config_name):
    set_log(config_name)
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    # db = SQLAlchemy(app)
    db.init_app(app)
    # 存储容易变化的值
    global redis_store
    # redis_store = StrictRedis(host=config[config_name].REDIS_HOST,port=config[config_name].REDIS_PORT)
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST,port=config[config_name].REDIS_PORT, decode_responses=True)

    StrictRedis(app)
    # 开启csrf
    CSRFProtect(app)
    @app.after_request
    def after_request(response):
        csrf_token = generate_csrf()
        response.set_cookie("csrf_token", csrf_token)
        return response
    # 设置session
    Session(app)
    # 添加自定义过滤器
    app.add_template_filter(do_index_class,"index_class")
    # 注册蓝图
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)
    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)
    return app