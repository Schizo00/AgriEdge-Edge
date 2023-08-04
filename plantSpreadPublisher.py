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

# data = ""
# data = data.encode('utf-8')
# record = {
#     "id": 1,
#     "xCoord": 10,
#     "yCoord": 20,
#     "diseaseName": "Leaf Spot",
#     "severity": 3
# }
file_path = 'plantsPerDisease.json'

with open(file_path, 'r') as file:
    loaded_data = json.load(file)
    
record = loaded_data


attributes = str(record)
attributes.encode('utf-8')

data= json.dumps(record).encode("utf-8")

print(data)


future = publisher.publish(topic_path,data)
print(f'message id {future.result()}')

