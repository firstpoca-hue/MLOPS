import boto3
import json
import time
import os

# Configuration from environment variables
REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
ROLE_ARN = os.environ.get('SAGEMAKER_ROLE_ARN')
BUCKET = os.environ.get('S3_BUCKET')

def upload_code_to_s3():
    """Upload training code to S3"""
    import tarfile
    import tempfile
    
    s3 = boto3.client('s3')
    
    # Create tar.gz of code directory
    with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as tmp:
        with tarfile.open(tmp.name, 'w:gz') as tar:
            tar.add('code/', arcname='.')
        
        # Upload to S3
        s3.upload_file(tmp.name, BUCKET, 'code/source.tar.gz')
        print("✅ Code uploaded to S3")
    
    # Upload data
    s3.upload_file('data.csv', BUCKET, 'data/data.csv')
    print("✅ Data uploaded to S3")

def create_training_job():
    """Create SageMaker Training Job with CodeBuild integration"""
    if not all([REGION, ROLE_ARN, BUCKET]):
        print("❌ Missing required environment variables")
        return None
        
    # Upload code and data first
    upload_code_to_s3()
    
    sagemaker = boto3.client('sagemaker', region_name=REGION)
    training_job_name = f"loan-model-{int(time.time())}"
    
    try:
        response = sagemaker.create_training_job(
            TrainingJobName=training_job_name,
            RoleArn=ROLE_ARN,
            AlgorithmSpecification={
                'TrainingImage': f'492215442770.dkr.ecr.{REGION}.amazonaws.com/sagemaker-scikit-learn:1.0-1-cpu-py3',
                'TrainingInputMode': 'File'
            },
            HyperParameters={
                'sagemaker_program': 'train.py',
                'sagemaker_submit_directory': f's3://{BUCKET}/code/source.tar.gz'
            },
            InputDataConfig=[
                {
                    'ChannelName': 'training',
                    'DataSource': {
                        'S3DataSource': {
                            'S3DataType': 'S3Prefix',
                            'S3Uri': f's3://{BUCKET}/data/',
                            'S3DataDistributionType': 'FullyReplicated'
                        }
                    },
                    'ContentType': 'text/csv'
                }
            ],
            OutputDataConfig={
                'S3OutputPath': f's3://{BUCKET}/model-output/'
            },
            ResourceConfig={
                'InstanceType': 'ml.m5.large',
                'InstanceCount': 1,
                'VolumeSizeInGB': 10
            },
            StoppingCondition={
                'MaxRuntimeInSeconds': 3600
            }
        )
        
        print(f"✅ Training job created: {training_job_name}")
        print(f"📊 Monitor at: https://{REGION}.console.aws.amazon.com/sagemaker/home?region={REGION}#/jobs/{training_job_name}")
        return training_job_name
        
    except Exception as e:
        print(f"❌ Training job failed: {e}")
        return None

def wait_for_training_completion(job_name):
    """Wait for training job to complete"""
    sagemaker = boto3.client('sagemaker', region_name=REGION)
    
    while True:
        response = sagemaker.describe_training_job(TrainingJobName=job_name)
        status = response['TrainingJobStatus']
        
        print(f"Training status: {status}")
        
        if status in ['Completed', 'Failed', 'Stopped']:
            return status == 'Completed'
            
        time.sleep(30)

if __name__ == "__main__":
    print("🚀 Starting MLOps pipeline with CodeBuild...")
    job_name = create_training_job()
    
    if job_name:
        print("✅ Training job started, waiting for completion...")
        success = wait_for_training_completion(job_name)
        
        if success:
            print("🎉 Training completed successfully!")
            
            # Download model for deployment
            s3 = boto3.client('s3')
            try:
                # Create artifacts directory
                os.makedirs('artifacts', exist_ok=True)
                
                # Download model from S3
                s3.download_file(BUCKET, f'model-output/{job_name}/output/model.tar.gz', 'artifacts/model.tar.gz')
                
                # Extract model.pkl
                import tarfile
                with tarfile.open('artifacts/model.tar.gz', 'r:gz') as tar:
                    tar.extractall('artifacts/')
                
                print("✅ Model downloaded for deployment")
            except Exception as e:
                print(f"⚠️ Could not download model: {e}")
        else:
            print("❌ Training failed")
            exit(1)
    else:
        print("❌ Failed to start training")
        exit(1)