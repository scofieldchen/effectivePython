import asyncio
from ssl import Purpose, create_default_context

import yaml
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


def load_config(filepath):
    with open(filepath) as f:
        return yaml.full_load(f)


async def produce(topic, config):
    ssl_context = create_default_context(Purpose.SERVER_AUTH, cafile=config["ssl_cafile"])
    producer = AIOKafkaProducer(
        bootstrap_servers=config["bootstrap_servers"],
        security_protocol=config["security_protocol"],
        ssl_context=ssl_context,
        sasl_mechanism=config["sasl_mechanism"],
        sasl_plain_username=config["sasl_username"],
        sasl_plain_password=config["sasl_password"]
    )
    await producer.start()

    try:
        for _ in range(100):
            await producer.send_and_wait(topic, b"hello kafka")
            await asyncio.sleep(1)
    finally:
        await producer.stop()


async def consume(topic, config):
    ssl_context = create_default_context(Purpose.SERVER_AUTH, cafile=config["ssl_cafile"])
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=config["bootstrap_servers"],
        security_protocol=config["security_protocol"],
        ssl_context=ssl_context,
        sasl_mechanism=config["sasl_mechanism"],
        sasl_plain_username=config["sasl_username"],
        sasl_plain_password=config["sasl_password"]
    )
    await consumer.start()

    try:
        async for msg in consumer:
            print("Message: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
    finally:
        await consumer.stop()


async def main(topic, config):
    await asyncio.gather(
        produce(topic, config),
        consume(topic, config)
    )


if __name__ == "__main__":
    config = load_config("./kafka.yaml")
    topic = "test"
    asyncio.run(main(topic, config))
