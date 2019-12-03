import asyncio
import random
import logging
from json import loads, dumps

import aiohttp
from aiohttp import web
from aiokafka import AIOKafkaConsumer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

routes = web.RouteTableDef()


# 定义request handler，flask-style
# 用户请求提交两个参数：client_id, topic
@routes.get("/{client_id}/{topic}")
async def websocket_handler(request):
    
    # 为每个连接的客户创建WS实例
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    client_id = request.match_info["client_id"]
    topic = request.match_info["topic"]
    logging.info("client connected: %s" % client_id)

    try:
        await asyncio.gather(
            listen_to_websocket(ws),
            push_data(ws, topic)
        )
    finally:
        logging.info("connection closed: %s" % client_id)

    return ws


async def listen_to_websocket(ws):
    """处理客户发送消息的逻辑"""
    try:
        async for msg in ws:
            print(msg)
    finally:
        return ws


async def push_data(ws, topic):
    """向客户推送数据"""
    try:
        loop = asyncio.get_running_loop()
        consumer = AIOKafkaConsumer(
            topic, loop=loop,
            bootstrap_servers="localhost:9092",
            auto_offset_reset="latest",
            value_deserializer=lambda x: loads(x.decode("utf-8"))
        )

        await consumer.start()

        try:
            async for msg in consumer:
                msg = dumps(msg.value).encode("utf-8")
                # await ws.send_bytes(msg)
                asyncio.create_task(ws.send_bytes(msg))
        except Exception as e:
            logging.error("Unexpected error %s" % str(e), exc_info=True)
        finally:
            await consumer.stop()

    except (asyncio.CancelledError, asyncio.TimeoutError):
        pass


app = web.Application()
app.add_routes(routes)
web.run_app(app, host="localhost", port=8080)
