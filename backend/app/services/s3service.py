import boto3
import os
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")



s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION,
)

def upload_to_s3(file_data: bytes, filename: str, folder: str, content_type="image/jpeg") -> str:
    key = f"{folder}/{uuid4().hex}_{filename}"
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=file_data, ContentType=content_type)
    return key


def delete_from_s3(key: str):
    """Deleta arquivo do bucket"""
    s3.delete_object(Bucket=S3_BUCKET, Key=key)
