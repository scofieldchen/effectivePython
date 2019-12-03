import asyncio
import websockets
import sys


async def connect(uri):
    """简单的客户端应用"""
    async with websockets.connect(uri) as ws:
        
        # await ws.send("this is my API token")
        # print(await ws.recv())

        # await ws.send("subscribe topic")
        # print(await ws.recv())

        # 接收和处理实时数据
        while True:
            resp = await ws.recv()
            print("recvied: %s" % resp)
            # await asyncio.sleep(0.01)


def main():
    uri = "ws://localhost:8080"

    client_id, topic = sys.argv[1], sys.argv[2]
    uri = "/".join([uri, client_id, topic])

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(connect(uri))
    finally:
        loop.close()


if __name__ == "__main__":
    main()