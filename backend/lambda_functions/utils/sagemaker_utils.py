import boto3
import json


def invoke_sagemaker_endpoint(endpoint_name, payload):
    sagemaker = boto3.client("runtime.sagemaker")
    try:
        response = sagemaker.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="application/json",
            Body=json.dumps(payload),
        )
        result = json.loads(response["Body"].read().decode())
        return result
    except Exception as e:
        print(f"Error invoking SageMaker endpoint: {str(e)}")
        return None
