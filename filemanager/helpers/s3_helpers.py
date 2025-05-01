import os
import boto3
import botocore.exceptions
from dotenv import load_dotenv

load_dotenv()

bucket_name = os.getenv("AWS_BUCKET_NAME")
if not bucket_name:
    raise RuntimeError("AWS_BUCKET_NAME not set in .env")

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")


def ensure_bucket_exists():
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        if error_code == 404:
            print("❌ Bucket does not exist.")
            return False
        elif error_code == 403:
            print("🚫 Access forbidden to the bucket.")
            return False
        else:
            raise


def create_bucket(bucket_name, region="eu-west-2"):
    s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": region}
    )
    s3_client.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={"Status": "Enabled"}
    )
    return True


def check_key(key, user=None):
    try:
        if user:
            key = f"{user}/{key}"
        s3_client.head_object(Bucket=bucket_name, Key=key)
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            raise
