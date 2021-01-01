from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__) #type:Flask

# 设置配置信息
class Config(object):
    # app的调试信息
    DEBUG = True
    # 数据库配置信息
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres@39.105.169.249:5432/Tongji"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 5
app.config.from_object(Config)
db = SQLAlchemy(app)
@app.route("/")
def index():
    return "index"

if __name__ == '__main__':
    app.run()