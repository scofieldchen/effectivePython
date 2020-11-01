"""
用aiohttp创建websocket client

1. 创建ClientSession实例
2. 调用session.ws_connect()创建ClientWebSocketResponse实例
3. 调用response对象的方法接受和发送消息
"""


import asyncio
import aiohttp
import random
import json
from pprint import pprint


async def main(url):
    """连接ws server，不断发送消息"""
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            # while True:
                # msg = {"symbol": "BTC/USDT", "price": random.randint(1, 100)}
                # await ws.send_bytes(json.dumps(msg).encode("utf8"))
                # await asyncio.sleep(1)
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.ERROR:
                    break
                data = json.loads(msg.data.decode("utf8"))
                # pprint(data)
                print(data)


if __name__ == "__main__":
    url = "ws://127.0.0.1:8000/ws"
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(url))
    finally:
        loop.close()