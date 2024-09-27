import boto3
import json
import os
from dotenv import load_dotenv
import jwt
from jwt import PyJWKClient

# Load environment variables from .env file
load_dotenv()

# Retrieve configuration from environment variables
sagemaker_endpoint = os.getenv("SAGEMAKER_ENDPOINT_NAME")
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

    # Get the document ID from the event
    document_id = event.get("DocumentID")
    if not document_id:
        return {
            "statusCode": 400,
            "body": json.dumps("DocumentID is required in the event."),
        }

    # Preprocess the document (e.g., extract text)
    processed_text = preprocess_document(document_id)

    # Invoke the SageMaker endpoint
    try:
        response = boto3.client("runtime.sagemaker").invoke_endpoint(
            EndpointName=sagemaker_endpoint,
            ContentType="application/json",
            Body=json.dumps({"text": processed_text}),
        )
        result = json.loads(response["Body"].read().decode())
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error invoking SageMaker endpoint: {str(e)}"),
        }

    # Store the results in S3
    store_results_in_s3(document_id, result)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"message": "Document processed and results stored.", "user": user_email}
        ),
    }


def preprocess_document(document_id):
    # Placeholder function for document preprocessing
    return "Sample preprocessed text"


def store_results_in_s3(document_id, result):
    s3 = boto3.client("s3")
    key = f"dynamic-ml-orchestration/processed/{document_id}.json"
    s3.put_object(Bucket=s3_bucket, Key=key, Body=json.dumps(result))
