from google.cloud import pubsub_v1
import os
import json

cred_path = 'edge-device-account.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path

publisher = pubsub_v1.PublisherClient(publisher_options = pubsub_v1.types.PublisherOptions(
        enable_message_ordering=True,
    ))
topic_path = 'projects/airy-charge-384205/topics/edge-device'

data = "Hello World"
data = data.encode('utf-8')
record = {
    'Key1': 'Value1',
    'Key2': 'Value2',
    'Key3': 'Value3',
    'Key4': 'Value4'
}

attributes = str(record)
attributes.encode('utf-8')
# attributes = json.dumps(record).encode("utf-8")


future = publisher.publish(topic_path, data, messages=attributes)
print(f'message id {future.result()}')