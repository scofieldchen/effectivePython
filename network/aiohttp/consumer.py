import asyncio
from json import loads
import logging

from aiokafka import AIOKafkaConsumer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def consume(loop, topics):
    consumer = AIOKafkaConsumer(
        *topics,
        loop=loop,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="latest",
        group_id="test",
        value_deserializer=lambda x: loads(x.decode("utf-8"))
    )

    await consumer.start()

    try:
        async for msg in consumer:
            logging.info("Consumer: %s:%d:%d: key=%s value=%s" % (
                msg.topic, msg.partition, msg.offset,
                msg.key, msg.value
            ))
    except Exception as e:
        logging.error("Unexpected error %s" % str(e), exc_info=True)
    finally:
        await consumer.stop()


topics = ["BTCUSDT", "ETHUSDT", "LTCUSDT"]

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(consume(loop, topics))
finally:
    loop.close()