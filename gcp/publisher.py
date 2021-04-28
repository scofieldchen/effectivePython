import datetime as dt
import json
import random
import time

from google.cloud import pubsub_v1

project_id = "aqueous-cortex-293313"
topic_id = "test_topic"

publisher = pubsub_v1.PublisherClient()
topic_path = f"projects/{project_id}/topics/{topic_id}"

for i in range(10):
    data = {
        "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "value": random.randint(1, 10) 
    }
    data = json.dumps(data).encode("utf8")
    future = publisher.publish(topic_path, data)
    print(future.result())
    print(f"send message {i}")
    time.sleep(1)
