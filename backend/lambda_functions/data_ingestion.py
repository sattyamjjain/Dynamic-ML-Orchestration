import boto3
import json
import os
from dotenv import load_dotenv
import jwt
from jwt import PyJWKClient

# Load environment variables from .env file
load_dotenv()

# Retrieve configuration from environment variables
s3_bucket = os.getenv("S3_BUCKET_NAME")
dynamodb_table = os.getenv("DYNAMODB_TABLE_NAME")
user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
client_id = os.getenv("COGNITO_USER_POOL_CLIENT_ID")
region = os.getenv("DMO_AWS_REGION")


def lambda_handler(event, context):
    # Check if the request has 'Authorization' header and decode the JWT token
    # try:
    #     token = event['headers']['Authorization'].split(' ')[1]
    #     jwks_url = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json'
    #     jwk_client = PyJWKClient(jwks_url)
    #     signing_key = jwk_client.get_signing_key_from_jwt(token)
    #     decoded_token = jwt.decode(token, signing_key.key, algorithms=["RS256"], audience=client_id)
    #     user_email = decoded_token.get('email')
    # except KeyError:
    #     return {
    #         'statusCode': 403,
    #         'body': json.dumps({'error': 'Authorization header missing or invalid'})
    #     }

    # Check if 'Records' is in the event
    if "Records" not in event:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "error": "Invalid event structure. Expected S3 event with Records key."
                }
            ),
        }

    # Extract bucket name and key from the event
    try:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = event["Records"][0]["s3"]["object"]["key"]
    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Missing key in event: {str(e)}"}),
        }

    # Initialize S3 and DynamoDB clients
    s3 = boto3.client("s3")
    dynamodb = boto3.client("dynamodb")

    # Get the uploaded file
    response = s3.get_object(Bucket=bucket, Key=key)
    file_content = response["Body"].read().decode("utf-8")

    # Extract metadata from the file content (e.g., title, author)
    metadata = extract_metadata(file_content)

    # Log metadata to DynamoDB
    dynamodb.put_item(
        TableName=dynamodb_table,
        Item={
            "DocumentID": {"S": key},
            "Title": {"S": metadata["title"]},
            "Author": {"S": metadata["author"]},
            "UploadedBy": {"S": user_email},  # Add user email who uploaded the document
            "Status": {"S": "Uploaded"},
        },
    )
    return {
        "statusCode": 200,
        "body": json.dumps("Document uploaded and metadata logged."),
    }


def extract_metadata(file_content):
    # Placeholder function for extracting metadata
    # Replace with actual metadata extraction logic
    return {"title": "Sample Title", "author": "Sample Author"}
