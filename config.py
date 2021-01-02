# 设置配置信息
import logging
from datetime import timedelta

from redis import StrictRedis
# 基本配置信息
class Config(object):
    # app的调试信息
    DEBUG = True
    SECRET_KEY = "wdqzbr"
    # 数据库配置信息
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres@localhost/BlogProj"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 5

    # redis的配置信息
    REDIS_HSOT = "127.0.0.1"
    REDIS_PORT = 6379

    # session配置
    SESSION_TYPE = "redis" # 设置session的存储类型
    SESSION_REDIS = StrictRedis(host=REDIS_HSOT,port=REDIS_PORT) # 配置存储环境
    SESSION_USE_SIGNER = True # 设置使用用户签名存储
    PERMANENT_SESSION_LIFETIME = timedelta(days=2) # 设置session的可用时长

    # 配置日志文件
    LEVEL_NAME = logging.DEBUG

# 开发环境配置
class DevelopConfig(Config):
    pass

# 生产（线上）环境配置
class ProductConfig(Config):
    # 配置日志文件
    LEVEL_NAME = logging.ERROR
    pass

# 测试环境配置
class TestConfig(Config):
    pass

# 定义一个访问字典使用
config_dict = {
    "develop":DevelopConfig,
    "product":ProductConfig,
    "test":TestConfig
}