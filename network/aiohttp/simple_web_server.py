"""
用aiohttp搭建简单的web server
"""

from aiohttp import web


routes = web.RouteTableDef()

# 定义request handler，处理客户端请求
# request handler必须是协程，接收唯一参数'request'，返回Response对象
@routes.get("/index")  # 定义路由和请求方法，flask-style
async def index(request):
    return web.Response(text="this is main page")

@routes.get("/hello")
async def hello(request):
    return web.Response(text="this is hello page")

@routes.get("/user/{name}")
async def user(request):
    # 获取url参数
    name = request.match_info["name"]
    return web.Response(text="hello %s" % name)


# 创建app实例，添加所有路由规则
app = web.Application()
app.add_routes(routes)

# 运行app
web.run_app(app, host="127.0.0.1", port=8000)