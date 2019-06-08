from flask import render_template, redirect, current_app

from info import redis_store
from info.modules.index import index_blu
@index_blu.route('/')
def index():
    # redis_store.set('name','laowang')
    return render_template("news/index.html")

@index_blu.route("/favicon.ico")
def favicon():
    # 使用重定向
    # return redirect("/static/news/favicon.ico")
    # 使用静态文件发送的方式
    return current_app.send_static_file("/news/favicon.ico")