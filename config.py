from redis import StrictRedis
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
    SESSION_REDIS = StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 86400