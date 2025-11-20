import boto3
import time
import tarfile
import os

# ================== CONFIG ==================
REGION = "ap-south-1"
BUCKET = "REPLACE_WITH_YOUR_S3_BUCKET"
MODEL_KEY = "loan-model/model.tar.gz"

ROLE_ARN = "arn:aws:iam::YOUR_ACCOUNT_ID:role/SageMakerExecutionRole"

MODEL_NAME = "loan-model"
ENDPOINT_NAME = "loan-endpoint"
INSTANCE_TYPE = "ml.t2.medium"

# SageMaker SKLearn built-in image (Mumbai region)
SKLEARN_IMAGE = "683313688378.dkr.ecr.ap-south-1.amazonaws.com/sagemaker-scikit-learn:1.0-1-cpu-py3"
# ============================================


def package_model():
    print("📦 Creating model.tar.gz ...")
    with tarfile.open("model.tar.gz", "w:gz") as tar:
        tar.add("model/model.pkl", arcname="model.pkl")
    print("✅ Model packaged.")


def upload_to_s3():
    print("☁️ Uploading model to S3...")
    s3 = boto3.client("s3", region_name=REGION)
    s3.upload_file("model.tar.gz", BUCKET, MODEL_KEY)
    print(f"✅ Uploaded to s3://{BUCKET}/{MODEL_KEY}")


def deploy_to_sagemaker():
    sm = boto3.client("sagemaker", region_name=REGION)

    model_data_url = f"s3://{BUCKET}/{MODEL_KEY}"
    model_version = f"{MODEL_NAME}-{int(time.time())}"

    print("🚀 Creating SageMaker Model:", model_version)

    sm.create_model(
        ModelName=model_version,
        PrimaryContainer={
            "Image": SKLEARN_IMAGE,
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
    package_model()
    upload_to_s3()
    deploy_to_sagemaker()
