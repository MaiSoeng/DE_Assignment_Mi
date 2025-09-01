import json
import random
from uuid import uuid4
from kafka import KafkaProducer
from datetime import datetime, timezone
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider
from kafka.sasl.oauth import AbstractTokenProvider

topic_name = 'Part1'
BROKERS = "b-1-public.mimskpart1.8k48gi.c4.kafka.us-east-1.amazonaws.com:9198, b-2-public.mimskpart1.8k48gi.c4.kafka.us-east-1.amazonaws.com:9198"
region='us-east-1'

# Class to provide MSK authentication token
class MSKTokenProvider(AbstractTokenProvider):
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token(region)
        return token

tp = MSKTokenProvider()

# generate the events for MSK streaming
actions = ['login', 'view_item', 'add_to_cart', 'checkout']

def generate_event():
    user_id = str(uuid4())
    session_id = str(uuid4())
    action = random.choices(actions, weights=[0.2, 0.3, 0.4, 0.1])[0]
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    item_id = random.randint(100, 999) if action != 'login' else None
    price = round(random.uniform(10, 100), 2) if action in ['view_item', 'add_to_cart', 'checkout'] else None
    return {
        'timestamp': timestamp,
        'user_id': user_id,
        'session_id': session_id,
        'action': action,
        'item_id': item_id,
        'price': price
    }

producer = KafkaProducer(
    bootstrap_servers = BROKERS,
    value_serializer = lambda v: json.dumps(v).encode('utf-8'),
    retry_backoff_ms = 500,
    request_timeout_ms = 20000,
    security_protocol = 'SASL_SSL',
    sasl_mechanism = 'OAUTHBEARER',
    sasl_oauth_token_provider = tp,)

if __name__ == '__main__':
    while True:
        data = generate_event()
        print(data)
        try:
            future = producer.send(topic_name, data)
            producer.flush()
            record_metadata = future.get(timeout = 10)

        except Exception as e:
            print(e.with_traceback())
