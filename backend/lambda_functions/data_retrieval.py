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

    # Get document ID from query parameters
    document_id = event["queryStringParameters"]["document_id"]

    # Retrieve the processed file from S3
    try:
        response = boto3.client("s3").get_object(
            Bucket=s3_bucket,
            Key=f"dynamic-ml-orchestration/processed/{document_id}.json",
        )
        result = json.loads(response["Body"].read().decode())
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error retrieving document: {str(e)}"),
        }

    return {"statusCode": 200, "body": json.dumps({"data": result, "user": user_email})}
