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
liveWeatherToday = pd.read_csv('liveWeatherToday.csv')
rainfall = liveWeatherToday['Rainfall'].iloc[0]
sunshine = liveWeatherToday['Sunshine'].iloc[0]
windGustSpeed = liveWeatherToday['WindGustSpeed'].iloc[0]
humidity9am = liveWeatherToday['Humidity9am'].iloc[0]
humidity3pm = liveWeatherToday['Humidity3pm'].iloc[0]
cloud9am = liveWeatherToday['Cloud9am'].iloc[0]
cloud3pm = liveWeatherToday['Cloud3pm'].iloc[0]
temp3pm = liveWeatherToday['Temp3pm'].iloc[0]
rainToday = liveWeatherToday['RainToday'].iloc[0]



record = {
    "Rainfall": rainfall,
    "Sunshine": sunshine,
    "WindGustSpeed": windGustSpeed,
    "Humidity9am": humidity9am,
    "Humidity3pm": humidity3pm,
    "Cloud9am": cloud9am,
    "Cloud3pm": cloud3pm,
    "Temp3pm": temp3pm,
    "RainToday": float(rainToday)
}

attributes = str(record)
attributes.encode('utf-8')

data= json.dumps(record).encode("utf-8")

print(data)


future = publisher.publish(topic_path,data)
print(f'message id {future.result()}')

