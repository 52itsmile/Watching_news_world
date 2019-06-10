from datetime import datetime
import random
import re

from flask import request, abort, current_app, make_response, request, jsonify, session

from info import redis_store, constants, db
from info.libs.yuntongxun.sms import CCP
from info.models import User
from info.modules.passport import passport_blu
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET


@passport_blu.route("/logout")
def logout():
    session.pop("user_id", None)
    return jsonify(errno=RET.OK,errmsg="退出成功")


@passport_blu.route("/login", methods=["POST"])
def login():
    data_dict = request.json
    mobile = data_dict["mobile"]
    passport = data_dict["passport"]

    if not all([mobile,passport]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数错误")

    if not re.match(r"1[35678]\d{9}",mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")

    try:
        user = User.query.filter_by(mobile = mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="数据库查询错误")

    if not user:
        return jsonify(errno=RET.NODATA, errmsg="用户不存在")

    if not user.check_passowrd(passport):
        return jsonify(errno=RET.PWDERR, errmsg="密码错误")

    user.last_login = datetime.now()
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg="添加最后登录时间失败")

    session["user_id"] = user.id
    return jsonify(errno=RET.OK, errmsg="登录成功")




@passport_blu.route("/register", methods=["POST"])
def register():
    """
    1.接收参数
    2.整体校验  参数的完整性
    3.手机号格式是否正确
    4.从redis中通过手机号取出真是的短信验证码
    5.和用户输入的验证码进行校验
    6.初始化user()添加数据
    7.session保持用户登录状态
    8.返回响应
    :return:
    """
    # return jsonify(errno=RET.OK, errmsg="成功发送短信验证码")
    dict_data = request.json
    mobile = dict_data["mobile"]
    smscode = dict_data["smscode"]
    password = dict_data["password"]

    # 整体校验参数的完整性
    if not all([mobile,smscode,password]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不全")
    # 正则
    if not re.match(r"1[35678]\d{9}",mobile):
        return jsonify(errno=RET.PARAMERR,errmsg="手机号格式不正确")
    # 判断是否已经注册过
    try:
        user_mobile = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg="数据库查询失败")
    if user_mobile:
        return jsonify(errno=RET.PARAMERR,errmsg="用户已存在,请重新输入")

    try:
        redis_sms_code = redis_store.get("SMS_" + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据库查询失败")
    if not redis_sms_code:
        return jsonify(errno=RET.NODATA,errmsg="短信验证码过期")
    if redis_sms_code != smscode:
        return jsonify(errno=RET.NODATA,errmsg="验证码过期了")

    user = User()
    user.nick_name = mobile
    user.password_hash = password
    user.password = password
    user.mobile = mobile

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库保存失败")

    session["user_id"] = user.id
    return jsonify(errno=RET.OK, errmsg="注册成功")


# 1.获取到前端发送的数据 json格式
# mobile
# image_code
# image_code_id
# 2.处理获取到的数据


@passport_blu.route("/sms_code",methods=["POST"])
def get_sms_code():
    # return jsonify(errno=RET.OK, errmsg="OK")
    dict_data = request.json

    mobile = dict_data["mobile"]
    image_code = dict_data["image_code"]
    image_code_id = dict_data["image_code_id"]


    # 1.
    # 接收参数并判断是否有值
    if not all([mobile,image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不全")
    # 2.
    # 校验手机号是正确
    if not re.match(r"1[35678]\d{9}",mobile):
        return jsonify(errno=RET.PARAMERR,errmsg="手机号格式不正确")
    # 3.
    # 通过传入的图片编码去redis中查询真实的图片验证码内容
    try:
        redis_image_code = redis_store.get("ImageCode_"+ image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据库查询失败")
    if not redis_image_code:
        return jsonify(errno=RET.NODATA,errmsg="验证码过期了")

    # 4.
    # 进行验证码内容的比对
    if redis_image_code.upper() != image_code.upper():
        return jsonify(errno=RET.DATAERR,errmsg="验证码不一致")

    # 5.
    # 生成发送短信的内容并发送短信
    sms_code = "%06d" %random.randint(0,999999)
    current_app.logger.info("短信验证码%" + sms_code)
    # result = CCP().send_template_sms(mobile,[sms_code,5],1)
    # if result != 0:
    #     return jsonify(errno=RET.DBERR, errmsg="手机验证码发送失败")
    try:
        redis_store.setex("SMS_" +mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
    except Exception as e:
        current_app.logger.error(e)
        return  jsonify(errno=RET.DBERR, errmsg="手机验证码发送失败")
    # 7.给前端一个响应
    return jsonify(errno=RET.OK, errmsg="成功发送短信验证码")










@passport_blu.route("/image_code")
def passport():
    # 1.接收参数
    image_code = request.args.get("imageCodeId")
    # 2.判断参数是否存在
    if not image_code:
        abort(404)

    name, text, image = captcha.generate_captcha()
    current_app.logger.info("图片验证码%" + text)
    # 3.添加到后台redis
    try:
        redis_store.setex("ImageCode_" + image_code, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.logger.error(e)
        return abort(500)
    # 4.返回验证码
    # 设置验证码请求格式
    response = make_response(image)
    response.headers["Content-Type"] = "image/jpg"
    return response
