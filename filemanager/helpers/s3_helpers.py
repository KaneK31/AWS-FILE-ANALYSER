import os
import boto3
import botocore.exceptions
import uuid

if not os.path.exists("bucket_name.txt"):
    rand_uuid = str(uuid.uuid4())
    bucket_name = f"awsproject{rand_uuid}"
    with open("bucket_name.txt", "w") as f:
        f.write(bucket_name)
else:
    with open("bucket_name.txt") as f:
        bucket_name = f.read().strip()

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")
bucket = s3_resource.Bucket(bucket_name)


def upload_file(user_id):
    if ensure_bucket_exists():

        files = os.listdir(os.getcwd())

        for i, name in enumerate(files, 1):
            print(i, name)

        while True:
            choice = int(input("Enter number you want"))
            if choice > len(files) or choice < 0:
                print("Invalid File")
                continue
            break
        selected_file = files[choice - 1]
        path = os.path.join(os.getcwd(), selected_file)
        if os.path.exists(path):
            s3_client.upload_file(path, bucket_name, user_id, ExtraArgs={"ContentType": "text/plain"})
            print("file uploaded")
        else:
            print(f"File {path} does not exist")
    else:
        create_bucket(bucket.name)
        print("test1")


def list_versions(user_id):
    if not check_key(user_id):
        print("No key")
        return
    else:
        response = s3_client.list_object_versions(Bucket=bucket_name, Prefix=user_id)
        for versions in response["Versions"]:
            print(versions["VersionId"], versions["LastModified"])
        return response["Versions"]


def download_file(user_id):
    if not check_key(user_id):
        print("No key")
        return
    else:
        output = list_versions(user_id)

        for i, version in enumerate(output, 1):
            print(
                f"Version download number: {i}. VersionID: {version['VersionId']} | Last Modified: {version['LastModified']} | "
                f"{'Latest' if version['IsLatest'] else ''}")

        while True:
            choice = int(input("Enter number you want to download: "))
            if choice > len(output) or choice < 0:
                print("Invalid File")
                continue
            break

        file_key = output[choice - 1]["Key"]
        version_id = output[choice - 1]["VersionId"]
        filename = f"downloaded_{file_key}_V{version_id[:8]}.txt"

        with open(filename, 'wb') as data:
            s3_client.download_fileobj(Bucket=bucket_name,
                                       Key=user_id,
                                       Fileobj=data,
                                       ExtraArgs={"VersionId": version_id}
                                       )
        print(f"✅ Downloaded version {version_id} of {user_id}")


def ensure_bucket_exists():
    if bucket.creation_date:
        print("✅ Bucket exists")
        return True
    print("❌ Bucket not found")
    return False


def create_bucket(bucket_name, region="eu-west-2"):
    s3_client.create_bucket(Bucket=bucket_name,
                            CreateBucketConfiguration={"LocationConstraint": region})
    print("Bucket made")

    # Enable versioning right after creation
    s3_client.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={"Status": "Enabled"}
    )
    print("Versioning enabled")
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
            raise print("Cannot find key")
