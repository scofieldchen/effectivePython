import asyncio
from json import dumps, loads
import logging

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def consume(loop):
    consumer = AIOKafkaConsumer(
        "test",
        loop=loop,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="latest",
        group_id="myGroup",
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


async def produce(loop):
    producer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers="localhost:9092",
        value_serializer=lambda x: dumps(x).encode("utf-8")
    )

    await producer.start()

    try:
        for i in range(10):
            msg = {"number": i}
            await producer.send_and_wait("test", msg)
            logging.info("Producer: publish message %s" % msg)
            await asyncio.sleep(2)
    except Exception as e:
        logging.error("Unexpected error %s" % str(e), exc_info=True)
    finally:
        await producer.stop()


async def main(loop):
    await asyncio.gather(*(
        consume(loop),
        produce(loop)
    ))


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main(loop))
finally:
    loop.close()