import boto3
import time

# ================== CONFIG ==================
REGION = "eu-central-1"
ROLE_ARN = "arn:aws:iam::361509912577:role/SageMakerExecutionRole"
MODEL_PACKAGE_GROUP_NAME = "loan-model-package-group"
ENDPOINT_NAME = "loan-endpoint"
INSTANCE_TYPE = "ml.t2.medium"
# ============================================

def get_approved_model():
    """Get the latest approved model from Model Registry"""
    sm = boto3.client("sagemaker", region_name=REGION)
    
    response = sm.list_model_packages(
        ModelPackageGroupName=MODEL_PACKAGE_GROUP_NAME,
        ModelApprovalStatus="Approved",
        SortBy="CreationTime",
        SortOrder="Descending"
    )
    
    if not response["ModelPackageSummaryList"]:
        print("❌ No approved models found. Model may not meet approval criteria.")
        print("Check evaluation metrics: Accuracy >= 0.7 and F1 Score >= 0.7")
        return None
        
    latest_model = response["ModelPackageSummaryList"][0]
    print(f"✅ Found approved model: {latest_model['ModelPackageArn']}")
    return latest_model["ModelPackageArn"]

def deploy_to_sagemaker():
    sm = boto3.client("sagemaker", region_name=REGION)
    
    # Get approved model
    model_package_arn = get_approved_model()
    if not model_package_arn:
        return
    
    model_version = f"loan-model-{int(time.time())}"
    print(f"🚀 Creating SageMaker Model from: {model_package_arn}")
    
    # Create model from model package
    sm.create_model(
        ModelName=model_version,
        Containers=[
            {
                "ModelPackageName": model_package_arn
            }
        ],
        ExecutionRoleArn=ROLE_ARN,
    )
    
    config_name = model_version + "-config"
    print("📄 Creating Endpoint Config:", config_name)
    
    sm.create_endpoint_config(
        EndpointConfigName=config_name,
        ProductionVariants=[
            {
                "VariantName": "AllTraffic",
                "ModelName": model_version,
                "InitialInstanceCount": 1,
                "InstanceType": INSTANCE_TYPE,
            }
        ],
    )
    
    print("🌐 Deploying Endpoint:", ENDPOINT_NAME)
    
    try:
        sm.describe_endpoint(EndpointName=ENDPOINT_NAME)
        print("🔁 Updating existing endpoint...")
        sm.update_endpoint(
            EndpointName=ENDPOINT_NAME,
            EndpointConfigName=config_name,
        )
    except:
        print("🆕 Creating new endpoint...")
        sm.create_endpoint(
            EndpointName=ENDPOINT_NAME,
            EndpointConfigName=config_name,
        )
    
    print("✅ Deployment triggered successfully!")

if __name__ == "__main__":
    deploy_to_sagemaker()
