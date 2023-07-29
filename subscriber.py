from google.cloud import pubsub_v1
import os
from concurrent.futures import TimeoutError

cred_path = 'edge-device-account.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path

timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/shining-rush-392311/subscriptions/edge-device-sub'

def callback(message):
    print(f'Received Message: {message}')
    print(f'Data: {message.data}')
    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'Listening On {subscription_path}')


with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()