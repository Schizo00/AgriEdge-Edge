from google.cloud import pubsub_v1
import avro.schema as schema
from google.api_core.exceptions import NotFound
from google.pubsub_v1.types import Encoding
from avro.io import BinaryEncoder, DatumWriter
import io
import os
import json
import pandas as pd

cred_path = 'edge-device-account.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
avsc_file = 'schema.avsc'

publisher = pubsub_v1.PublisherClient(publisher_options = pubsub_v1.types.PublisherOptions(
        enable_message_ordering=True,
    ))
topic_path = 'projects/shining-rush-392311/topics/edge-device-temp'
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

liveWeatherToday = pd.read_csv('liveWeatherToday.csv')
rainfall = liveWeatherToday['Rainfall'].iloc[0]
evaporation = liveWeatherToday['Evaporation'].iloc[0]
sunshine = liveWeatherToday['Sunshine'].iloc[0]
windSpeed9am = liveWeatherToday['WindSpeed9am'].iloc[0]
humidity3pm = liveWeatherToday['Humidity3pm'].iloc[0]
pressure3pm = liveWeatherToday['Pressure3pm'].iloc[0]
temp = liveWeatherToday['Temp'].iloc[0]



record = {
  "Rainfall": rainfall,
  "Evaporation":evaporation,
  "Sunshine": sunshine,
  "WindSpeed9am": windSpeed9am,
  "Humidity3pm": humidity3pm,
  "Pressure3pm": pressure3pm,
  "Temp":temp
}

attributes = str(record)
attributes.encode('utf-8')

data= json.dumps(record).encode("utf-8")

print(data)


future = publisher.publish(topic_path,data)
print(f'message id {future.result()}')

