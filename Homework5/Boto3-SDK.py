import logging
import boto3 
from botocore.exceptions import ClientError 
import requests

# This function is to generate the presigned url to download
def create_presigned_url(bucket_name, object_name, expiration=3600):

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': 'assignment-git', 'Key': 'sample2.jpg'},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

if __name__ == '__main__':
    url = create_presigned_url('assignment-git', 'sample2.jpg')
    if url:
        print("Presigned URL generated successfully:")
        print(url)
    else:
        print("Failed to generate presigned URL.")

# This function is to generate the presigned url to upload
def create_presigned_post(bucket_name, object_name, fields=None, conditions=None, expiration=3600):
    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(
            bucket_name,
            object_name,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response 

local_path = r'H:\DE\DE Lecture\Homework5\sample4.jpg'
object_name = 'sample4.jpg'
response = create_presigned_post('assignment-git', object_name)
if response is None:
    exit(1)

# how python use url to upload
with open(local_path, 'rb') as f:
    files = {'file': (object_name, f)}
    http_response = requests.post(response['url'], data = response['fields'], files = files)

logging.info(f'File upload HTTP status code: {http_response.status_code}')
