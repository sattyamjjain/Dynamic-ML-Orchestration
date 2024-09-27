#!/bin/bash

# Set your AWS region and profile
AWS_REGION="us-east-1"
AWS_PROFILE="root"  # Replace 'root' with your AWS CLI profile name if different

# Cognito User Pool and Client settings
USER_POOL_NAME="DynamicMLUserPool"
USER_POOL_CLIENT_NAME="DynamicMLUserPoolClient"

# Function to create Cognito User Pool
create_user_pool() {
    echo "Creating Cognito User Pool: $USER_POOL_NAME ..."
    USER_POOL_ID=$(aws cognito-idp create-user-pool \
        --pool-name "$USER_POOL_NAME" \
        --auto-verified-attributes email \
        --policies '{
            "PasswordPolicy": {
                "MinimumLength": 8,
                "RequireUppercase": true,
                "RequireLowercase": true,
                "RequireNumbers": true,
                "RequireSymbols": false
            }
        }' \
        --region "$AWS_REGION" \
        --profile "$AWS_PROFILE" \
        --query 'UserPool.Id' \
        --output text)

    if [ -z "$USER_POOL_ID" ]; then
        echo "Failed to create User Pool."
        exit 1
    else
        echo "User Pool created successfully. User Pool ID: $USER_POOL_ID"
    fi
}

# Function to create Cognito User Pool Client
create_user_pool_client() {
    echo "Creating Cognito User Pool Client: $USER_POOL_CLIENT_NAME ..."
    USER_POOL_CLIENT_ID=$(aws cognito-idp create-user-pool-client \
        --user-pool-id "$USER_POOL_ID" \
        --client-name "$USER_POOL_CLIENT_NAME" \
        --no-generate-secret \
        --explicit-auth-flows "ALLOW_USER_PASSWORD_AUTH" "ALLOW_REFRESH_TOKEN_AUTH" "ALLOW_ADMIN_USER_PASSWORD_AUTH" \
        --region "$AWS_REGION" \
        --profile "$AWS_PROFILE" \
        --query 'UserPoolClient.ClientId' \
        --output text)

    if [ -z "$USER_POOL_CLIENT_ID" ]; then
        echo "Failed to create User Pool Client."
        exit 1
    else
        echo "User Pool Client created successfully. User Pool Client ID: $USER_POOL_CLIENT_ID"
    fi
}

# Main script execution
create_user_pool
create_user_pool_client

echo "Cognito User Pool and Client setup completed."
echo "User Pool ID: $USER_POOL_ID"
echo "User Pool Client ID: $USER_POOL_CLIENT_ID"

# Exporting the variables for future use (optional)
export COGNITO_USER_POOL_ID="$USER_POOL_ID"
export COGNITO_USER_POOL_CLIENT_ID="$USER_POOL_CLIENT_ID"
export AWS_REGION="$AWS_REGION"
