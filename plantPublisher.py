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
result_df = pd.read_csv('PlantInfo.csv')

##result_df["diseaseName"] = result_df["diseaseName"].astype(str)
##dict_data = result_df.to_dict(orient='records')
##record = {'plantInfo': dict_data}
##print(lt_df["diseaseName"].iloc[0].tolist())

result_df = result_df[:20]
print(result_df.head())
plant_info_list = []
for index, row in result_df.iterrows():
    plant_info = {
        "id": row["id"],
        "xCoord": row["xCoord"],
        "yCoord": row["yCoord"],
        "diseaseName": row["diseaseName"],
        "severity": row["severity"]
    }
    plant_info_list.append(plant_info)

record = {"plantInfo": plant_info_list}

attributes = str(record)
attributes.encode('utf-8')

data= json.dumps(record).encode("utf-8")

print(data)


future = publisher.publish(topic_path,data)
print(f'message id {future.result()}')

