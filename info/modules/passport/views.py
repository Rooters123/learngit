from flask import request,current_app,make_response,Response

from info import redis_store,constants
from . import passport_blue
from info.utils.captcha.captcha import captcha
from info.utils.jsonrsp.jsonrsp import err_rsp
from info.libs.yuntongxun.sms import CCP
import json
import re
@passport_blue.route('/image_code')
def image_code():
    pre_id = request.args.get("pre_id")
    cur_id = request.args.get("cur_id")
    name, text, image_file = captcha.generate_captcha()
    try:
        if pre_id:
            redis_store.delete("image_code:%s"%pre_id)
        redis_store.set("image_code:%s"%cur_id,text,constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)

    # 如何直接return回去的话是返回一个text文本，因为没指定类型，浏览器不认识它是图片
    # return image_file
    # 方法一：使用image的src属性来接收
    # 方法二：直接告诉浏览器返回的是什么类型
    response = make_response(image_file)
    response.headers["Content-type"] = "image/jpg"
    return response

@passport_blue.route('/sms_code', methods=['POST'])
def sms_code():
    req_data = request.data
    json_data = json.loads(req_data,encoding="utf-8")
    mobile = json_data["mobile"]
    image_code = json_data["image_code"]
    image_code_id = json_data["image_code_id"]
    if not re.match('1[3-9]\d{9}',mobile):

        return err_rsp(100,"号码不正确！")
    if image_code!=redis_store.get("image_code:%s"%image_code_id):
        return err_rsp(200, "验证码不正确！")
    ccp = CCP()
    statue_code = ccp.send_template_sms('18332672733', ['1234', 5], 1)
    if statue_code == -1:
        return err_rsp(300, "短信发送失败！")
    return err_rsp(0, "短信发送成功！")