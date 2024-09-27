import boto3


def create_dynamodb_table(table_name):
    dynamodb = boto3.client("dynamodb", region_name="us-east-1")
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "DocumentID", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "DocumentID", "AttributeType": "S"}
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        print(
            f"DynamoDB table '{table_name}' created successfully with table response {table}"
        )
    except dynamodb.exceptions.ResourceInUseException:
        print(f"DynamoDB table '{table_name}' already exists.")
    except Exception as e:
        print(f"Error creating DynamoDB table: {str(e)}")
