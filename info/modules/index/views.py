from info import redis_store
from info.models import User
from . import index_blue
from flask import render_template,current_app,session
@index_blue.route("/")
def index():
    # redis_store.set("name","zbr")
    # print(redis_store)
    try:
        user_id = session.get("user_id")
    except Exception as e:
        current_app.logger.error(e)
    if user_id:
        user = User.query.get(user_id)
        user_info = user.to_dict()
    else:
        user_info = None
    data = {
        "user_info":user_info
    }
    return render_template("news/index.html",data = data)


@index_blue.route('/favicon.ico')
def get_web_logo():
    # 内部使用的函数将静态文件从静态文件夹发送到浏览器。
    return current_app.send_static_file("new/favicon.ico")
