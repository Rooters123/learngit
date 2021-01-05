from flask import Response
import json
def err_rsp(errcode,errmsg):
    json_string = json.dumps({"errcode": errcode, "errmsg": errmsg}, ensure_ascii=False)
    response = Response(json_string, content_type="application/json; charset=utf-8")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response