"""
用aiohttp创建websocket server

1. 定义ws请求处理器(request handler)
    1.1 request handler必须是协程
    1.2 接受request参数
    1.3 创建WebSocketResponse实例
    1.4 调用response方法接受和发送消息
    1.5 request handler最终返回response
2. 创建app实例
3. 定义路由
4. 运行app
"""


import asyncio
import aiohttp
from aiohttp import web


# 定义WS请求处理器(request handler)
async def websocket_handler(request):
    # 创建WebSocketResponse实例
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # 服务端逻辑
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.ERROR:
            print(f"ws connection closed with exception {ws.exception()}")
        else:
            print(msg.data)

    # 返回response对象
    print("websocket connection closed")
    return ws


if __name__ == "__main__":
    # 创建app实例
    app = web.Application()

    # 添加路由，将请求url和请求处理器绑定在一起
    app.add_routes([web.get("/ws", websocket_handler)])

    # 运行app
    web.run_app(app, host="127.0.0.1", port=8000)