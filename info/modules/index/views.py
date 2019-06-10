from flask import render_template, redirect, current_app, session, jsonify

from info import redis_store, constants
from info.models import User, News, Category
from info.modules.index import index_blu
from info.utils.response_code import RET


@index_blu.route('/')
def index():
    user_id = session.get("user_id")
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)  # user 是一个obj
        except Exception as e:
            current_app.logger.error(e)


    # 显示新闻点击排行
    click_news = []
    try:
        click_news = News.query.order_by(News.title.desc()).limit(6).all()
    except Exception as e:
        current_app.logger.error(e)
    click_news_li = []
    for new_obj in click_news:
        click_news_dict = new_obj.to_basic_dict()
        click_news_li.append(click_news_dict)
    print(click_news_li)

    # 显示新闻分类
    categorys = []
    try:
        categorys = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)

    categorys_li = []
    for categorys_obj in categorys:
        categorys_dict = categorys_obj.to_dict()
        categorys_li.append(categorys_dict)
    print(categorys_li)


    # data = {
    #     "user_info": {
    #         "nick_name": "laozhang",
    #         "mobile": "aaaaa"
    #     }
    # }
    # 如果user为空，那么传一个None，如果不为空 user.to_dict()
    data = {
        "user_info": user.to_dict() if user else None,
        "click_news_li":click_news_li,
        "categorys_li":categorys_li
    }
    # data.user_info.avatar_url

    return render_template("news/index.html", data=data)

@index_blu.route("/favicon.ico")
def favicon():
    # 使用重定向
    # return redirect("/static/news/favicon.ico")
    # 使用静态文件发送的方式
    return current_app.send_static_file("info/news/favicon.ico")