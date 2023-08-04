import json
import os
import pandas as pd
from google.cloud import pubsub_v1

cred_path = 'edge-device-account.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
avsc_file = 'schema.avsc'

publisher = pubsub_v1.PublisherClient(publisher_options = pubsub_v1.types.PublisherOptions(
        enable_message_ordering=True,
    ))
topic_path = 'projects/shining-rush-392311/topics/edge-device-weather'
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
humidity = liveWeatherToday['Humidity3pm'].iloc[0]
windSpeed = liveWeatherToday['WindSpeed3pm'].iloc[0]
temperature = liveWeatherToday['Temp'].iloc[0]
precipitation = liveWeatherToday['Rainfall'].iloc[0]



record = {
    "humidity" : humidity,
    "windSpeed": windSpeed,
    "temperature": temperature,
    "precipitation": precipitation,
}

attributes = str(record)
attributes.encode('utf-8')

data= json.dumps(record).encode("utf-8")

print(data)


future = publisher.publish(topic_path,data)
print(f'message id {future.result()}')

