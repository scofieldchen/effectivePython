"""
Flask中传递参数有两种方式：1. 表单；2. URL参数。

在URL中传递参数是最常用的方式，这样相同的URL地址，通过不同的参数就可以访问不同的内容。
"""
from flask import Flask, url_for, redirect


app = Flask(__name__)


# 传递参数的形式为'<param_name>'，数据类型默认为字符串
# 视图函数需要接收与URL参数相同的参数名
@app.route("/user/<username>")
def user(username):
    return f"用户名：{username}"


@app.route("/user/<username>/account")
def account(username):
    return f"这是用户{username}的账号"


# 可以定义传递参数的数据类型
@app.route("/news/<int:id>")
def news(id):
    return f"新闻ID：{id}"


# redirect + url_for实现页面跳转
@app.route("/index")
def index():
    # url_for的第一个参数是视图函数名字，如果视图函数接收参数，则必须传递相应值
    # 访问/index自动跳转到/user/kobe页面
    return redirect(url_for("user", username="kobe"))


if __name__ == "__main__":
    app.run(debug=True)