import json
import boto3
import random
import time
from faker import Faker
from datetime import datetime, timedelta, timezone

region='us-east-1'
stream_name = 'mi-ks-homework12'

clientkinesis = boto3.client('kinesis', region_name = region)
fake = Faker()
actions = ['login', 'view_item', 'add_to_cart', 'checkout']

def generate_event():
    user_id = fake.uuid4()
    action = random.choices(actions, weights=[0.2, 0.3, 0.4, 0.1])[0]
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    item_id = fake.random_int(min = 100, max = 999) if action != 'login' else None
    price = round(random.uniform(10, 100), 2) if action in ['view_item', 'add_to_cart', 'checkout'] else None
    return {
        'timestamp': timestamp,
        'user_id': user_id,
        'session_id': fake.uuid4(),
        'action': action,
        'item_id': item_id,
        'price': price
    }

def stream_data():
    while True:
        event = generate_event()
        response = clientkinesis.put_record(StreamName = stream_name, Data = json.dumps(event), PartitionKey = event['user_id'])
        print(f"Sent event: {event['action']} by {event['user_id']} at {event['timestamp']}")
        time.sleep(1)

if __name__ == '__main__':
    stream_data()