from datetime import timedelta
from flask import Flask,request,session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
app = Flask(__name__) #type:Flask

# 设置配置信息
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

app.config.from_object(Config)

# 创建SQLAlchemy
db = SQLAlchemy(app)

# 配置session信息，通过Session读取App中的session
Session(app)
# 创建redis对象
redis_store = StrictRedis(host=Config.REDIS_HSOT,port=Config.REDIS_PORT,decode_responses=True)
@app.route("/")
def index():
    redis_store.set("name","zbr")
    print(redis_store.get("name"))
    session["name"] = "zbr"
    return "index"

if __name__ == '__main__':
    app.run()