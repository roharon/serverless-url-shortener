import boto3
import os
import random
import string
import botocore
from botocore import exceptions
from botocore.client import Config

AWS_REGION = os.environ['AWS_REGION']

DEBUG = True


def generate_random(n):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase +
                                                string.digits)
                   for _ in range(n))


def is_key_available(s3_client, bucket, key):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return False
    except botocore.exceptions.ClientError as e:
        code = e.response['Error']['Code']
        if code == '403' or code == '404':
            return True
        raise e


def lambda_handler(event, context):
    BUCKET_NAME = os.environ['S3_BUCKET']

    native_url = event.get("native_url")
    s3 = boto3.client('s3', config=Config(signature_version='s3v4'))

    while (True):
        key_size = int(os.environ["SHORT_KEY_SIZE"])
        short_id = generate_random(key_size)
        short_key = "url/" + short_id
        if is_key_available(s3, BUCKET_NAME, short_key):
            break
        else:
            print("short_key collision: " + short_key + ". Retrying.")

    try:
        s3.put_object(Bucket=BUCKET_NAME,
                      Key=short_key,
                      Body=b'',
                      WebsiteRedirectLocation=native_url,
                      ContentType="text/plain")
    except Exception as e:
        print("Error: ", e)
        short_id = None

    return {
        "short_id": short_id,
        "forward_url": os.environ['FOWARD_HOST'],
        "native_url": native_url
    }
