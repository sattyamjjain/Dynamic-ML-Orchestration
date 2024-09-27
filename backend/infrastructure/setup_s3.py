import boto3


def create_s3_bucket(bucket_name):
    s3 = boto3.client("s3")
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "us-east-1"},
        )
        print(f"S3 bucket '{bucket_name}' created successfully.")
    except s3.exceptions.BucketAlreadyExists:
        print(f"S3 bucket '{bucket_name}' already exists.")
    except Exception as e:
        print(f"Error creating S3 bucket: {str(e)}")
