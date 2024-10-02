# Dynamic-ML-Orchestration

Dynamic-ML-Orchestration is an AI-driven platform designed for sentiment analysis, leveraging a serverless architecture for scalability, efficiency, and cost-effectiveness. The project is divided into two main parts: Frontend and Backend, both of which work in harmony to deliver real-time sentiment analysis.

## Project Overview

### Frontend Features:
- Seamless integration with AWS S3 for data storage.
- Real-time processing and analysis of large datasets.
- Intuitive UI built using React, Next.js, and Tailwind CSS.
- Serverless architecture to ensure scalability.

### Backend Features:
- Built on AWS Lambda, API Gateway, S3, and DynamoDB.
- Supports data ingestion, processing, and retrieval using machine learning.
- Integration with AWS SageMaker for sentiment model inference.

```plaintext
dynamic-ml-orchestration/
├── frontend/
│   ├── app/
│   │   └── page.tsx
│   ├── components/
│   │   └── ui/
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       ├── input.tsx
│   │       ├── label.tsx
│   │       ├── progress.tsx
│   │       ├── tabs.tsx
│   │       ├── toast.tsx
│   │       ├── toaster.tsx
│   │       └── use-toast.ts
│   ├── public/
│   ├── styles/
│   │   └── globals.css
│   ├── .env.local
│   ├── next.config.js
│   ├── package.json
│   ├── README.md
│   └── tsconfig.json
├── backend/
│   ├── api_gateway/
│   │   ├── api_routes.py
│   │   ├── __init__.py
│   │   └── request_handlers.py
│   ├── deploy_lambda_functions.sh
│   ├── infrastructure/
│   │   ├── deploy_lambda.py
│   │   ├── setup_cognito.py
│   │   ├── setup_dynamodb.py
│   │   └── setup_s3.py
│   ├── lambda_functions/
│   │   ├── data_ingestion.py
│   │   ├── data_processing.py
│   │   ├── data_retrieval.py
│   │   ├── __init__.py
│   │   └── utils/
│   │       ├── dynamodb_utils.py
│   │       ├── s3_utils.py
│   │       └── sagemaker_utils.py
│   ├── notebook/
│   │   └── Dynamic-ml-orchestration.ipynb
│   ├── README.md
│   └── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Prerequisites

Before starting, ensure the following:

- Node.js >= 14.0.0 (for frontend)
- npm >= 6.0.0 (for frontend)
- Python >= 3.8 (for backend)
- An AWS account with proper permissions

## Frontend Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sattyamjjain/dynamic-ml-orchestration.git
   cd dynamic-ml-orchestration
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Set Up Environment Variables**:
   Create a `.env.local` file and add:
   ```plaintext
   NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com
   ```

4. **Run Development Server**:
   ```bash
   npm run dev
   ```

5. **Production Build**:
   ```bash
   npm run build
   ```

## Backend Setup Instructions

1. **Clone Backend**:
   ```bash
   git clone https://github.com/yourusername/dynamic-ml-orchestration.git
   cd dynamic-ml-orchestration/backend
   ```

2. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Backend Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the `backend/` directory and add:
   ```plaintext
   DMO_AWS_REGION=us-east-1
   S3_BUCKET_NAME=<your-s3-table>
   DYNAMODB_TABLE_NAME=<your-dynamodb-table>
   SAGEMAKER_ENDPOINT_NAME=<your-sagemaker-ml-endpoint>
   COGNITO_USER_POOL_ID=<your-user-pool>
   COGNITO_USER_POOL_CLIENT_ID=<your-user-pool-secret>
   ```

5. **Set Up AWS Infrastructure**:
   - Setup S3 Bucket:
     ```bash
     python3 infrastructure/setup_s3.py
     ```
   - Setup DynamoDB:
     ```bash
     python3 infrastructure/setup_dynamodb.py
     ```
   - Deploy Lambda Functions:
     ```bash
     bash deploy_lambda_functions.sh
     ```

   - Setup Cognito:
     ```bash
     bash setup_cognito.sh
     ```

## API Endpoints

- **Ingest**: POST to `/ingest` to store data.
- **Process**: POST to `/process` to analyze data using SageMaker.
- **Retrieve**: GET from `/retrieve` to get processed data.

## Troubleshooting

- **Lambda Deployment Issues:** Ensure that the Lambda functions have the correct IAM roles with permissions to access S3, DynamoDB, and SageMaker.
- **Cognito Authentication:** If you encounter issues with authentication, ensure that the Cognito User Pool and App Client are correctly configured and that the API Gateway is using the Cognito authorizer.

## Testing

- **Frontend**: Unit tests using `npm test`.
- **Backend**: Unit tests using `unittest`.
  ```bash
  python3 -m unittest discover -s tests/backend_tests
  ```

## Contributing

We welcome contributions to improve the project. Please submit a pull request or open an issue for any changes or suggestions.