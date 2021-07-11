import os
import boto3
from botocore.client import Config

S3_BUCKET = os.environ['S3_BUCKET']

def handler(event, context):
  short_url = "url/" + event.get("Key")
  
  s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
  resp = s3.head_object(Bucket=S3_BUCKET, Key=short_url)
  
  redirect_url = resp.get('WebsiteRedirectLocation')
  if redirect_url:
    return { "redirect_url": redirect_url }
  else:
    return { "Error": "Unable to load redirect url for object: s3://" + S3_BUCKET + "/" + short_url }
