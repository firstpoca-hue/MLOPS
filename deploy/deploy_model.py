import boto3
import time

# ================== CONFIG ==================
REGION = "eu-central-1"
ROLE_ARN = "arn:aws:iam::361509912577:role/SageMakerExecutionRole"
BUCKET = "teamars"
MODEL_PACKAGE_GROUP_NAME = "loan-model-package-group"
ENDPOINT_NAME = "loan-endpoint"
INSTANCE_TYPE = "ml.t2.medium"
# ============================================

def get_latest_model():
    """Get the latest trained model from S3"""
    s3 = boto3.client("s3", region_name=REGION)
    
    try:
        response = s3.list_objects_v2(
            Bucket=BUCKET.replace('s3://', '').replace('/', ''),
            Prefix='model-output/',
            Delimiter='/'
        )
        
        if 'CommonPrefixes' in response:
            # Get the latest training job folder
            folders = [obj['Prefix'] for obj in response['CommonPrefixes']]
            latest_folder = sorted(folders)[-1]
            model_data_url = f"s3://{BUCKET}/{latest_folder}output/model.tar.gz"
            print(f"✅ Found trained model: {model_data_url}")
            return model_data_url
        else:
            print("❌ No trained models found in S3")
            return None
            
    except Exception as e:
        print(f"❌ Error finding model: {e}")
        return None

def deploy_to_sagemaker():
    sm = boto3.client("sagemaker", region_name=REGION)
    
    # Get trained model
    model_data_url = get_latest_model()
    if not model_data_url:
        return
    
    model_version = f"loan-model-{int(time.time())}"
    print(f"🚀 Creating SageMaker Model from: {model_data_url}")
    
    # Create model from S3 artifacts
    sm.create_model(
        ModelName=model_version,
        PrimaryContainer={
            "Image": f"492215442770.dkr.ecr.{REGION}.amazonaws.com/sagemaker-scikit-learn:1.0-1-cpu-py3",
            "ModelDataUrl": model_data_url,
        },
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
