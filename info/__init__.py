import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_wtf import CSRFProtect
from config import config_dict
# 这里是一个非常有意思的步骤
# 如果一开始定义为None值，那么会出现迁移错误，
# 是由于None会使得models中db的操作失败，init app可以等待调用create_app时候执行
db = SQLAlchemy() # type:SQLAlchemy
# db = SQLAlchemy()，那么下面使用global时候的内存地址是相同的
redis_store = None
# redis_store = None，那么下面使用global时候的内存地址是不同的 140728032259296、2376997811144
def create_app(config_name):

    app = Flask(__name__) #type:Flask
    Config = config_dict.get(config_name)
    app.config.from_object(Config)

    # 配置日志文件
    log_file(Config.LEVEL_NAME)

    # 创建SQLAlchemy
    global db
    # print(id(db))
    # db.SQLAlchemy(app)
    db.init_app(app)
    # 创建redis对象
    global redis_store
    redis_store = StrictRedis(host=Config.REDIS_HSOT,port=Config.REDIS_PORT,decode_responses=True)

    # 配置session信息，通过Session读取App中的session
    Session(app)

    # CSRF保护
    # CSRFProtect(app)

    # 注册蓝图
    from .modules.index import index_blue
    app.register_blueprint(index_blue)
    from .modules.passport import passport_blue
    app.register_blueprint(passport_blue)
    return app

def log_file(level_name):
    #设置日志的记录等级，常见的有四种，大小关系如下：DEBUG< INFO<WARNING < ERROR
    logging.basicConfig(level=level_name)#调试debug级
    #创建日志记录器，指明日志保存的路径、每个日志件的最大大小、保存的日志文件个数上限
    # file_log_handler
    file_log_handler = RotatingFileHandler("logs/log",maxBytes=1024*1024*100,backupCount=10)
    #创建日志记录的格式白等级输入日志信息的文件名行数日志信息
    formatter=logging.Formatter('%(levelname)s %(filename)s:%(lineno)d%(message)s')
    #为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    #为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)