import boto3


def upload_file_to_s3(bucket_name, file_content, key):
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket_name, Key=key, Body=file_content)


def download_file_from_s3(bucket_name, key):
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket_name, Key=key)
    return response["Body"].read()


def store_results_in_s3(bucket_name, key, result):
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(result))
