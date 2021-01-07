import random

from flask import request,current_app,make_response,Response

from info import redis_store,constants
from . import passport_blue
from info.utils.captcha.captcha import captcha
from info.utils.jsonrsp.jsonrsp import err_rsp
from info.libs.yuntongxun.sms import CCP
from info.utils.response_code import RET
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
    # 1.获取参数
    req_data = request.data
    json_data = json.loads(req_data, encoding="utf-8")
    mobile = json_data["mobile"]
    image_code = json_data["image_code"]
    image_code_id = json_data["image_code_id"]

    # 2.参数的为空校验
    if not all([mobile,image_code,image_code_id]):
        err_rsp(RET.PARAMERR,"参数错误！")

    # 3.校验手机的格式
    if not re.match('1[3-9]\d{9}',mobile):
        err_rsp(RET.DATAERR, "手机号格式错误！")

    # 4.通过图片验证码编号获取，图片验证码
    try:
        pic_code = redis_store.get("image_code:%s"%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        err_rsp(RET.DBERR, "操作redis失败")

    # 5.判断图片验证码是否过期
    if not pic_code:
        err_rsp(RET.NODATA, "验证码过期")

    # 6.判断图片验证码是否正确
    if pic_code.upper() != image_code.upper():
        err_rsp(RET.DATAERR,"图片验证码不正确")

    # 7.核验成功，删除redis中的图片验证码，短信验证码的层级更高，就不需要图片验证码对用户注册进行验证
    try:
        redis_store.delete("image_code:%s"%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        err_rsp(RET.DBERR, "操作redis失败")

    # 8.生成一个随机的短信验证码，调用cCp发送短信，判断是否成功
    rd_sms_code = "%06d"%random.randint(0,999999)
    ccp = CCP()
    statue_code = ccp.send_template_sms('18332672733', [rd_sms_code, 5], 1)
    if statue_code == -1:
        err_rsp(RET.DBERR, "验证码发送失败")

    # 9.将短信保存到redis中
    try:
        redis_store.set("rd_sms_code:%s"%mobile,rd_sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        err_rsp(RET.DBERR, "操作redis失败")

    # 10.返回
    return err_rsp(RET.OK,"短信发送成功！")





