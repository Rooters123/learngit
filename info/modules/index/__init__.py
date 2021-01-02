from flask import Blueprint
# 1.定义蓝图对象
index_blue = Blueprint("index",__name__)
# 2.导入views装饰视图函数
from info.modules.index import views


