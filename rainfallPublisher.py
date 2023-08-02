from google.cloud import pubsub_v1
import avro.schema as schema
from google.api_core.exceptions import NotFound
from google.pubsub_v1.types import Encoding
from avro.io import BinaryEncoder, DatumWriter
import io
import os
import json

cred_path = 'edge-device-account.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
avsc_file = 'schema.avsc'

publisher = pubsub_v1.PublisherClient(publisher_options = pubsub_v1.types.PublisherOptions(
        enable_message_ordering=True,
    ))
topic_path = 'projects/shining-rush-392311/topics/edge-device-rainfall'
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
rainfall = 15.6
sunshine = 10.0
windGustSpeed = 41.747501
humidity9am = 92.0
humidity3pm = 84.0
cloud9am = 8.0
cloud3pm = 8.0
temp3pm = 20.9
rainToday = 1



record = {
    "Rainfall": rainfall,
    "Sunshine": sunshine,
    "WindGustSpeed": windGustSpeed,
    "Humidity9am": humidity9am,
    "Humidity3pm": humidity3pm,
    "Cloud9am": cloud9am,
    "Cloud3pm": cloud3pm,
    "Temp3pm": temp3pm,
    "RainToday":rainToday
}

attributes = str(record)
attributes.encode('utf-8')

data= json.dumps(record).encode("utf-8")

print(data)


future = publisher.publish(topic_path,data)
print(f'message id {future.result()}')

