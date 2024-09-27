import boto3


def create_lambda_function(function_name, role_arn, handler, zip_file):
    lambda_client = boto3.client("lambda", region_name="us-east-1")
    try:
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime="python3.12",
            Role=role_arn,
            Handler=handler,
            Code={"ZipFile": zip_file},
            Timeout=300,
            MemorySize=128,
        )
        print(
            f"Lambda function '{function_name}' created successfully with response {response}"
        )
    except lambda_client.exceptions.ResourceConflictException:
        print(
            f"Lambda function '{function_name}' already exists. Consider updating instead."
        )
    except Exception as e:
        print(f"Failed to create Lambda function '{function_name}': {str(e)}")
