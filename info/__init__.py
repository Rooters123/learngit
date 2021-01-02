from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_wtf import CSRFProtect
from config import config_dict
from .modules.index import index_blue
def create_app(Config_name):

    app = Flask(__name__) #type:Flask
    Config = config_dict.get(Config_name)
    app.config.from_object(Config)

    # 创建SQLAlchemy
    db = SQLAlchemy(app)

    # 创建redis对象
    redis_store = StrictRedis(host=Config.REDIS_HSOT,port=Config.REDIS_PORT,decode_responses=True)

    # 配置session信息，通过Session读取App中的session
    Session(app)

    # CSRF保护
    CSRFProtect(app)

    # 注册蓝图
    app.register_blueprint(index_blue)
    return app