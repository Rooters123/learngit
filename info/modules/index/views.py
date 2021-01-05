from . import index_blue
from flask import render_template,current_app
@index_blue.route("/")
def index():
    # redis_store.set("name","zbr")
    # print(redis_store)
    return render_template("news/index.html")


@index_blue.route('/favicon.ico')
def get_web_logo():
    # 内部使用的函数将静态文件从静态文件夹发送到浏览器。
    return current_app.send_static_file("new/favicon.ico")
