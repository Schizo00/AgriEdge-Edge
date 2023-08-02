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

record = {
  "plantInfo": [
    {
      "id": 1,
      "xCoord": 0,
      "yCoord": 1,
      "diseaseName": "Powdery Mildew",
      "severity": 3
    },
    {
      "id": 2,
      "xCoord": 0,
      "yCoord": 2,
      "diseaseName": "Rust",
      "severity": 2
    },
    {
      "id": 3,
      "xCoord": 0,
      "yCoord": 3,
      "diseaseName": "Black Spot",
      "severity": 1
    },
    {
      "id": 4,
      "xCoord": 0,
      "yCoord": 4,
      "diseaseName": "Anthracnose",
      "severity": 4
    },
    {
      "id": 5,
      "xCoord": 1,
      "yCoord": 1,
      "diseaseName": "Leaf Curl",
      "severity": 2
    },
    {
      "id": 6,
      "xCoord": 1,
      "yCoord": 2,
      "diseaseName": "Fusarium Wilt",
      "severity": 5
    },
    {
      "id": 7,
      "xCoord": 1,
      "yCoord": 3,
      "diseaseName": "Blight",
      "severity": 3
    },
    {
      "id": 8,
      "xCoord": 1,
      "yCoord": 4,
      "diseaseName": "Rots",
      "severity": 1
    },
    {
      "id": 9,
      "xCoord": 2,
      "yCoord": 1,
      "diseaseName": "Leaf Spot",
      "severity": 2
    },
    {
      "id": 10,
      "xCoord": 2,
      "yCoord": 2,
      "diseaseName": "Downy Mildew",
      "severity": 4
    },
    {
      "id": 11,
      "xCoord": 2,
      "yCoord": 3,
      "diseaseName": "Root Rot",
      "severity": 5
    },
    {
      "id": 12,
      "xCoord": 2,
      "yCoord": 4,
      "diseaseName": "Yellowing",
      "severity": 1
    },
    {
      "id": 13,
      "xCoord": 3,
      "yCoord": 1,
      "diseaseName": "Wilt",
      "severity": 3
    },
    {
      "id": 14,
      "xCoord": 3,
      "yCoord": 2,
      "diseaseName": "Canker",
      "severity": 4
    },
    {
      "id": 15,
      "xCoord": 3,
      "yCoord": 3,
      "diseaseName": "Bacterial Blight",
      "severity": 2
    },
    {
      "id": 16,
      "xCoord": 3,
      "yCoord": 4,
      "diseaseName": "Anthracnose",
      "severity": 5
    },
    {
      "id": 17,
      "xCoord": 4,
      "yCoord": 1,
      "diseaseName": "Leaf Rust",
      "severity": 3
    },
    {
      "id": 18,
      "xCoord": 4,
      "yCoord": 2,
      "diseaseName": "Scab",
      "severity": 1
    },
    {
      "id": 19,
      "xCoord": 4,
      "yCoord": 3,
      "diseaseName": "Smuts",
      "severity": 2
    },
    {
      "id": 20,
      "xCoord": 4,
      "yCoord": 4,
      "diseaseName": "Leaf Spot",
      "severity": 4
    }
  ]
}


attributes = str(record)
attributes.encode('utf-8')

data= json.dumps(record).encode("utf-8")

print(data)


future = publisher.publish(topic_path,data)
print(f'message id {future.result()}')

