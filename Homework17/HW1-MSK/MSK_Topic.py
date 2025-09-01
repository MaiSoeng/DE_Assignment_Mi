from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from kafka.sasl.oauth import AbstractTokenProvider
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider
import certifi

# AWS region where MSK cluster is located
region= 'us-east-1'

BOOTSTRAPS = ["b-2-public.mimskpart1.8k48gi.c4.kafka.us-east-1.amazonaws.com:9198","b-1-public.mimskpart1.8k48gi.c4.kafka.us-east-1.amazonaws.com:9198",] 

# Class to provide MSK authentication token
class MSKTokenProvider(AbstractTokenProvider):
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token(region)
        return token


# Initialize KafkaAdminClient with required configurations
admin_client = KafkaAdminClient(
    bootstrap_servers=BOOTSTRAPS,
    security_protocol='SASL_SSL',
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=MSKTokenProvider(),
    client_id='client1',
)

# create topic
topic_name="Part1"
topic_list =[NewTopic(name=topic_name, num_partitions=1, replication_factor=2)]
existing_topics = admin_client.list_topics()
if(topic_name not in existing_topics):
    admin_client.create_topics(topic_list)
    print("Topic has been created")
else:
    print("topic already exists!. List of topics are:" + str(existing_topics))