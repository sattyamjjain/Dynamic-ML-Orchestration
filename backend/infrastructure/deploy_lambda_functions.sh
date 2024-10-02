#!/bin/bash

# Define directories and Lambda function names
LAMBDA_FUNCTIONS=("data_ingestion" "data_processing" "data_retrieval")
LAMBDA_FUNCTION_NAMES=("DataIngestionFunction" "DataProcessingFunction" "DataRetrievalFunction")
LAMBDA_PACKAGE_DIR="./backend/lambda_functions"
REQUIREMENTS_FILE="./backend/requirements.txt"
S3_BUCKET="pyverseai"  # Set your S3 bucket name here
S3_PATH="dynamic-ml-orchestration/lambdas"  # Set the desired S3 path for your packages
AWS_PROFILE="root"  # Set your AWS CLI profile here

# Capture the base directory
BASE_DIR="$(pwd)"

# Function to package and deploy a Lambda function using S3
package_and_deploy_lambda_s3() {
    FUNCTION_NAME=$1
    LAMBDA_NAME=$2
    FUNCTION_DIR="$LAMBDA_PACKAGE_DIR/${FUNCTION_NAME}_package"
    ZIP_FILE="${BASE_DIR}/backend/${FUNCTION_NAME}_package.zip"  # Absolute path
    S3_KEY="$S3_PATH/${FUNCTION_NAME}_package.zip"

    echo "-----------------------------"
    echo "Packaging and deploying Lambda function: $LAMBDA_NAME"
    echo "Lambda function file path: $LAMBDA_PACKAGE_DIR/$FUNCTION_NAME.py"

    # Check if the Lambda function file exists
    if [ ! -f "$LAMBDA_PACKAGE_DIR/$FUNCTION_NAME.py" ]; then
        echo "Error: Lambda function file $FUNCTION_NAME.py not found in $LAMBDA_PACKAGE_DIR"
        echo "Directory listing of $LAMBDA_PACKAGE_DIR:"
        ls -l "$LAMBDA_PACKAGE_DIR"
        exit 1
    else
        echo "Lambda function file $FUNCTION_NAME.py found."
    fi

    # Check if the utils directory exists
    if [ ! -d "$LAMBDA_PACKAGE_DIR/utils" ]; then
        echo "Error: utils directory not found in $LAMBDA_PACKAGE_DIR"
        exit 1
    else
        echo "utils directory found."
    fi

    # Check if requirements.txt exists
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        echo "Error: requirements.txt not found in $REQUIREMENTS_FILE"
        exit 1
    else
        echo "requirements.txt found."
    fi

    # Create a new directory for the Lambda function package
    echo "Creating package directory: $FUNCTION_DIR"
    mkdir -p "$FUNCTION_DIR"

    # Copy Lambda function code and utils directory to the package directory
    echo "Copying Lambda function code and utils to package directory..."
    cp "$LAMBDA_PACKAGE_DIR/${FUNCTION_NAME}.py" "$FUNCTION_DIR"/
    cp -r "$LAMBDA_PACKAGE_DIR/utils" "$FUNCTION_DIR"/
    echo "Files copied to package directory."

    # Install dependencies in the package directory
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE" -t "$FUNCTION_DIR"
    if [ $? -ne 0 ]; then
        echo "Error installing dependencies."
        exit 1
    fi
    echo "Dependencies installed successfully."

    # Zip the package directory
    echo "Creating zip file: $ZIP_FILE"
    (cd "$FUNCTION_DIR" && zip -r "$ZIP_FILE" .)  # Use quotes for safety
    if [ $? -ne 0 ]; then
        echo "Error creating zip file."
        exit 1
    fi

    echo "Zip file created successfully."

    # Check the size of the zip file
    echo "Zip file size:"
    ls -lh "$ZIP_FILE"

    # Upload the zip file to S3
    echo "Uploading zip file to S3: s3://$S3_BUCKET/$S3_KEY"
    aws s3 cp "$ZIP_FILE" "s3://$S3_BUCKET/$S3_KEY" --profile "$AWS_PROFILE"
    if [ $? -ne 0 ]; then
        echo "Error uploading zip file to S3."
        exit 1
    fi
    echo "Zip file uploaded to S3 successfully."

    # Update the Lambda function code with the S3 object
    echo "Updating Lambda function $LAMBDA_NAME with the S3 package..."
    aws lambda update-function-code \
        --function-name "$LAMBDA_NAME" \
        --s3-bucket "$S3_BUCKET" \
        --s3-key "$S3_KEY" \
        --profile "$AWS_PROFILE"
    if [ $? -ne 0 ]; then
        echo "Error updating Lambda function $LAMBDA_NAME."
        exit 1
    fi
    echo "Lambda function $LAMBDA_NAME updated successfully."

    # Cleanup: Remove package directory and zip file after deployment
    echo "Cleaning up..."
    rm -rf "$FUNCTION_DIR"
    rm "$ZIP_FILE"
    echo "Cleanup completed."
    echo "Lambda function $LAMBDA_NAME deployed successfully!"
    echo "-----------------------------"
}

# Iterate over each Lambda function and deploy
for i in "${!LAMBDA_FUNCTIONS[@]}"; do
    package_and_deploy_lambda_s3 "${LAMBDA_FUNCTIONS[$i]}" "${LAMBDA_FUNCTION_NAMES[$i]}"
done

echo "All Lambda functions deployed successfully!"
