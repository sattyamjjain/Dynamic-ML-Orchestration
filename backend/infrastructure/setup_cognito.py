import boto3


def create_cognito_user_pool(pool_name):
    cognito = boto3.client("cognito-idp", region_name="us-east-1")
    response = cognito.create_user_pool(
        PoolName=pool_name,
        AutoVerifiedAttributes=["email"],
        Policies={
            "PasswordPolicy": {
                "MinimumLength": 8,
                "RequireUppercase": True,
                "RequireLowercase": True,
                "RequireNumbers": True,
                "RequireSymbols": False,
            }
        },
    )
    print(f"User pool '{pool_name}' created successfully.")
    return response["UserPool"]["Id"]


def create_cognito_user_pool_client(user_pool_id, client_name):
    cognito = boto3.client("cognito-idp", region_name="us-east-1")
    response = cognito.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName=client_name,
        GenerateSecret=False,
        ExplicitAuthFlows=[
            "ALLOW_REFRESH_TOKEN_AUTH",
            "ALLOW_USER_PASSWORD_AUTH",
            "ALLOW_ADMIN_USER_PASSWORD_AUTH",
        ],
    )
    print(f"User pool client '{client_name}' created successfully.")
    return response["UserPoolClient"]["ClientId"]
