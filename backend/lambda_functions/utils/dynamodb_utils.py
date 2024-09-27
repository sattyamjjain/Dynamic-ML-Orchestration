import boto3


def put_item_to_dynamodb(table_name, item):
    dynamodb = boto3.client("dynamodb")
    dynamodb.put_item(TableName=table_name, Item=item)


def get_item_from_dynamodb(table_name, key):
    dynamodb = boto3.client("dynamodb")
    response = dynamodb.get_item(TableName=table_name, Key=key)
    return response.get("Item")
