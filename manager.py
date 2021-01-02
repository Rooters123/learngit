from datetime import timedelta
from flask import Flask,request,session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_wtf import CSRFProtect
from config import Config
app = Flask(__name__) #type:Flask


app.config.from_object(Config)

# 创建SQLAlchemy
db = SQLAlchemy(app)

# 创建redis对象
redis_store = StrictRedis(host=Config.REDIS_HSOT,port=Config.REDIS_PORT,decode_responses=True)

# 配置session信息，通过Session读取App中的session
Session(app)

# CSRF保护
CSRFProtect(app)

@app.route("/")
def index():
    redis_store.set("name","zbr")
    print(redis_store.get("name"))
    session["name"] = "zbr"
    return "index"

if __name__ == '__main__':
    app.run()