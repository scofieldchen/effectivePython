import asyncio
import logging
import random
from datetime import datetime
from json import dumps

from aiokafka import AIOKafkaProducer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def produce(loop, topic):
    producer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers="localhost:9092",
        value_serializer=lambda x: dumps(x).encode("utf-8")
    )

    await producer.start()

    try:
        while True:
            msg = {
                "timestamp": str(datetime.now()),
                "symbol": topic,
                "price": random.randrange(1, 100)
            }
            await producer.send_and_wait(topic, msg)
            await asyncio.sleep(random.randint(1, 3))
    except Exception as e:
        logging.error("Unexpected error %s" % str(e), exc_info=True)
    finally:
        await producer.stop()


loop = asyncio.get_event_loop()

topics = ["BTCUSDT", "ETHUSDT", "LTCUSDT"]
for topic in topics:
    loop.create_task(produce(loop, topic))

try:
    loop.run_forever()
finally:
    loop.close()