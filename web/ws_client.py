"""
Websockets Client

websocket是双向通信机制，客户端程序连接服务器后，订阅相关主题，一旦数据有更新，
服务器会自动推送数据。ws特别适用于实时数据处理。

websockets是python搭建服务端和客户端WS应用的库，基于asyncio，支持高并发。

python客户端程序使用websockets的几个步骤：

1. 连接服务器。
2. 验签(如果服务器不要求可忽略)。
3. 订阅相关主题。
4. 接收和处理实时数据。
5. 实现断开重连。
"""


import asyncio
import websockets


async def test():
    """简单的客户端应用"""
    uri = "wss://echo.websocket.org"
    async with websockets.connect(uri) as ws:  # 连接服务器
        
        # 验签
        # await ws.send("this is my API token")
        # print(await ws.recv())

        # 订阅数据
        # await ws.send("subscribe topic")
        # print(await ws.recv())

        # 接收和处理实时数据
        while True:
            # 测试uri会返回我们传送的消息
            msg = "hello websocket"
            await ws.send(msg)
            resp = await ws.recv()
            print("recvied: %s" % resp)
            await asyncio.sleep(1)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(test())
finally:
    loop.close()