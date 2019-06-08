from flask import request, abort, current_app, make_response

from info import redis_store, constants
from info.modules.passport import passport_blu
from info.utils.captcha.captcha import captcha

@passport_blu.route("/image_code")
def passport():
    # 1.接收参数
    image_code = request.args.get("imageCodeId")
    # 2.判断参数是否存在
    if not image_code:
        abort(404)

    name, text, image = captcha.generate_captcha()
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
