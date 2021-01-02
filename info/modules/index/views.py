from . import index_blue
from info import db
from info import redis_store
@index_blue.route("/")
def index():
    redis_store.set("name","zbr")
    print(redis_store["name"])
    return "index"
