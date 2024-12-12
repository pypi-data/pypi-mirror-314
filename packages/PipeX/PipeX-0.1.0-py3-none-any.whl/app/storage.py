'''
this module will be used to save data to a file and upload it to an S3 bucket.
proposed approach:
1. Create a function save_to_file(data, file_path, format='csv') that saves the data to a file in the specified format (csv or json).
2. Create a function upload_to_s3(file_path, bucket_name, key) that uploads the file to the specified S3 bucket.
3. Create a function save_and_upload(data, file_path, bucket_name, key, format='
csv') that combines the above two functions to save the data to a file and upload it to an S3 bucket.

'''

import boto3
import os
import logging
from botocore.exceptions import ClientError
import pandas as pd
from dotenv import load_dotenv


load_dotenv() 
logger = logging.getLogger(__name__)

def save_to_file(data, file_path, format = 'csv'):
    try:
        if format == 'csv':
            data.to_csv(file_path, index=False)
        elif format == 'json':
            data.to_json(file_path, orient='records', lines=True)
        else:
            raise ValueError(f"File format not supported: {format}")
    except Exception as e:
        logger.error(f"Failed to save data to file '{file_path}': {str(e)}")
        raise
    
def upload_to_s3(file_path, bucket_name, key):
    s3 = boto3.client(
        "s3",
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name = os.getenv("AWS_REGION")
    )
    
    try:
        s3.upload_file(file_path, bucket_name, key)
        logger.info(f"{file_path} uploaded to S3 bucket: {bucket_name}")
    except ClientError as e:
        logger.error(f"Failed to upload {file_path} to S3 bucket '{bucket_name}': {str(e)}")
        raise 
def download_from_s3(bucket_name, key, file_path):
    s3 = boto3.client(
        "s3",
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name = os.getenv("AWS_REGION")
    )
    try:
        s3.download_file(bucket_name,key,file_path)
        logger.info(f"{key} downloaded from S3 bucket: {bucket_name} to {file_path}")
    except ClientError as e:
        logger.error(f"Failed to download {key} from S3 bucket '{bucket_name}': {str(e)}")
        raise
    
def file_exists_in_s3(bucket_name, key):
    s3 = boto3.client(
        "s3",
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name = os.getenv("AWS_REGION")
        )
    
    try:
        s3.head_object(Bucket=bucket_name, Key=key)
        logger.info(f"File {key} exists in S3 bucket: {bucket_name}")
    except ClientError as e:
        logger.error(f"File {key} does not exist in S3 bucket: {bucket_name}")
        raise
    
def save_data(data, file_path, format="csv", bucket_name=None, key=None):
    save_to_file(data, file_path, format)
    
    if bucket_name and key:
        upload_to_s3(file_path, bucket_name, key)
        
