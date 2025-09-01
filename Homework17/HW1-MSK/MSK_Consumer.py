from kafka import KafkaConsumer
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider
from kafka.sasl.oauth import AbstractTokenProvider

BROKERS = "b-1-public.mimskpart1.8k48gi.c4.kafka.us-east-1.amazonaws.com:9198, b-2-public.mimskpart1.8k48gi.c4.kafka.us-east-1.amazonaws.com:9198"
region='us-east-1'
topic_name = 'Part1'

# Class to provide MSK authentication token
class MSKTokenProvider(AbstractTokenProvider):
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token(region)
        return token

tp = MSKTokenProvider()

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers = BROKERS,
    group_id = "part1_consumer",
    auto_offset_reset = "earliest",
    enable_auto_commit = True,
    security_protocol = 'SASL_SSL',
    sasl_mechanism = 'OAUTHBEARER',
    sasl_oauth_token_provider = tp,
    value_deserializer=lambda v: v.decode("utf-8", errors="ignore"),)

for data in consumer:
    print(data.value)
