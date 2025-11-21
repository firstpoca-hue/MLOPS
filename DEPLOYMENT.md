# MLOps Deployment Guide

## Prerequisites
- GitHub repository with your code
- AWS Account with appropriate permissions
- Training data: `data.csv` in your Git repository

## Setup

### 1. Configure GitHub Secrets
Add these secrets to your GitHub repository:
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

### 2. Deploy Infrastructure
1. Go to **Actions** tab in your GitHub repository
2. Select **Deploy Infrastructure** workflow
3. Click **Run workflow**
4. Choose **apply** to deploy infrastructure

### 3. Trigger ML Pipeline
- **Automatic**: Push changes to `data.csv`
- **Manual**: Run **Trigger ML Pipeline** workflow

### 2. Manual Pipeline Execution
```bash
# Install dependencies
pip install -r requirements.txt

# Run complete workflow
python run_pipeline.py

# Or run individual steps:
# 1. Create SageMaker Pipeline
python pipeline/sagemaker_pipeline.py

# 2. Execute pipeline (trains and evaluates model)
aws sagemaker start-pipeline-execution --pipeline-name loan-model-pipeline

# 3. Deploy approved model (automatic if criteria met)
python deploy/deploy_model.py
```

### 3. Automatic Approval Criteria
- **Accuracy**: >= 0.7 (70%)
- **F1 Score**: >= 0.7 (70%)
- Models meeting both criteria are automatically approved
- Models below criteria require manual approval

### 3. Workflow
1. **Code Push**: Push updated `data.csv` to Git repository
2. **Pipeline Trigger**: CodePipeline automatically triggers
3. **Data Upload**: BuildSpec uploads `data.csv` to `s3://teamars/data/data.csv`
4. **Pipeline Execution**: SageMaker Pipeline starts automatically
5. **Data Processing**: Reads from S3, applies feature engineering
6. **Model Training**: Trains LogisticRegression on processed data
7. **Model Evaluation**: Evaluates model performance (Accuracy, F1 Score)
8. **Automatic Approval**: Models with Accuracy >= 0.7 AND F1 >= 0.7 are auto-approved
9. **Model Registration**: Registers model with appropriate approval status
10. **Deployment**: Deploy approved model to endpoint

### 4. Test Endpoint
```python
import boto3
import json

runtime = boto3.client('sagemaker-runtime', region_name='eu-central-1')

payload = {
    "no_of_dependents": 2,
    "education": 0,
    "self_employed": 0,
    "income_annum": 13.3,  # log(600000)
    "loan_amount": 15.4,   # log(5000000)
    "loan_term": 12,
    "credit_score": 750,
    "total_asset": 15.9    # log(8000000)
}

response = runtime.invoke_endpoint(
    EndpointName='loan-endpoint',
    ContentType='application/json',
    Body=json.dumps(payload)
)

result = json.loads(response['Body'].read().decode())
print(f"Prediction: {result['prediction']}")
```

## Architecture
- **Source**: GitHub repository + S3 data
- **CI/CD**: CodePipeline + CodeBuild
- **ML Pipeline**: SageMaker Pipelines (Preprocessing → Training → Registration)
- **Model Registry**: SageMaker Model Registry
- **Deployment**: SageMaker Endpoint
- **Storage**: S3 bucket