"""
flask app基础程序

1. 初始化Flask对象
2. 定义路由和试图函数
3. app.run()
"""
from flask import Flask

# 创建app实例
app = Flask(__name__)

# 路由定义客户端访问的URL，视图函数是对应的后端逻辑
@app.route("/")
@app.route("/index")
def index():
    return "hello flask"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)