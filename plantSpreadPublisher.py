import json
import os

from google.cloud import pubsub_v1

cred_path = 'edge-device-account.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
avsc_file = 'schema.avsc'

publisher = pubsub_v1.PublisherClient(publisher_options = pubsub_v1.types.PublisherOptions(
        enable_message_ordering=True,
    ))
topic_path = 'projects/shining-rush-392311/topics/edge-device-plant'
topic_id = 'shining-rush-392311'


data= "Trigger message!!!"


future = publisher.publish(topic_path,data)
print(f'message id {future.result()}')

