from concurrent.futures._base import TimeoutError
from google.cloud.pubsublite.cloudpubsub import SubscriberClient
from google.cloud.pubsublite.types import (
    CloudRegion,
    CloudZone,
    FlowControlSettings,
    SubscriptionPath,
    MessageMetadata
)

project_number = 533637743951
cloud_region = "asia-east1"
zone_id = "a"
subscription_id = "test_sub_one"
timeout = 90

location = CloudZone(CloudRegion(cloud_region), zone_id)
subscription_path = SubscriptionPath(project_number, location, subscription_id)
# Configure when to pause the message stream for more incoming messages based on the
# maximum size or number of messages that a single-partition subscriber has received,
# whichever condition is met first.
per_partition_flow_control_settings = FlowControlSettings(
    # 1,000 outstanding messages. Must be >0.
    messages_outstanding=1000,
    # 10 MiB. Must be greater than the allowed size of the largest message (1 MiB).
    bytes_outstanding=10 * 1024 * 1024,
)

def callback(message):
    message_data = message.data.decode("utf-8")
    print(message_data)
    # metadata = MessageMetadata.decode(message.message_id)
    message.ack()

# SubscriberClient() must be used in a `with` block or have __enter__() called before use.
with SubscriberClient() as subscriber:
    streaming_pull_future = subscriber.subscribe(
        subscription_path,
        callback=callback,
        per_partition_flow_control_settings=per_partition_flow_control_settings,
    )

    try:
        streaming_pull_future.result(timeout=timeout)
    except (TimeoutError, KeyboardInterrupt):
        streaming_pull_future.cancel()
        assert streaming_pull_future.done()
