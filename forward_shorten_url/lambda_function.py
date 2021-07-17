import os
import boto3
from botocore.client import Config

S3_BUCKET = os.environ['S3_BUCKET']


def lambda_handler(event, context):
    print(event)
    shorten_key = "url/" + event.get("pathParameters").get("key")

    s3 = boto3.client('s3', config=Config(signature_version='s3v4'))

    try:
        resp = s3.head_object(Bucket=S3_BUCKET, Key=shorten_key)
        redirect_url = resp.get('WebsiteRedirectLocation')
    except Exception as e:
        print(e)
        redirect_url = os.environ["HOST"]

    return {
        "statusCode": 301,
        "headers": {
            "Location": redirect_url
        },
        "isBase64Encoded": False,
    }
