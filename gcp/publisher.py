import datetime as dt
import json
import random
import time

from google.cloud.pubsublite.cloudpubsub import PublisherClient
from google.cloud.pubsublite.types import (CloudRegion, CloudZone,
                                           MessageMetadata, TopicPath)

project_number = 533637743951
cloud_region = "asia-east1"
zone_id = "a"
topic_id = "test_topic"

location = CloudZone(CloudRegion(cloud_region), zone_id)
topic_path = TopicPath(project_number, location, topic_id)

with PublisherClient() as publisher:
    for i in range(200):
        data = {
            "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "value": random.randint(1, 10) 
        }
        data_encoded = json.dumps(data).encode("utf8")
        future = publisher.publish(topic_path, data_encoded)
        print(future.result())
        time.sleep(1)
