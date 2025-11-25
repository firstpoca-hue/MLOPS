import boto3
import time
from datetime import datetime, timedelta

# Configuration
REGION = "eu-central-1"
ENDPOINT_NAME = "loan-endpoint"

def check_endpoint_logs():
    """Check CloudWatch logs for endpoint issues"""
    logs_client = boto3.client('logs', region_name=REGION)
    sm_client = boto3.client('sagemaker', region_name=REGION)
    
    try:
        # Get endpoint info
        endpoint_info = sm_client.describe_endpoint(EndpointName=ENDPOINT_NAME)
        print(f"📊 Endpoint Status: {endpoint_info['EndpointStatus']}")
        
        if endpoint_info['EndpointStatus'] == 'Failed':
            print(f"❌ Failure Reason: {endpoint_info.get('FailureReason', 'Unknown')}")
        
        # Check CloudWatch logs
        log_group_name = f"/aws/sagemaker/Endpoints/{ENDPOINT_NAME}"
        
        try:
            # Get recent log events
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=1)
            
            response = logs_client.filter_log_events(
                logGroupName=log_group_name,
                startTime=int(start_time.timestamp() * 1000),
                endTime=int(end_time.timestamp() * 1000)
            )
            
            print(f"\n📋 Recent CloudWatch Logs for {ENDPOINT_NAME}:")
            print("-" * 60)
            
            for event in response.get('events', [])[-20:]:  # Last 20 events
                timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
                print(f"[{timestamp}] {event['message']}")
                
        except Exception as e:
            print(f"⚠️ Could not retrieve logs: {e}")
            
    except Exception as e:
        print(f"❌ Error checking endpoint: {e}")

def check_model_artifacts():
    """Check if model artifacts exist in S3"""
    s3_client = boto3.client('s3', region_name=REGION)
    
    try:
        # List model artifacts
        response = s3_client.list_objects_v2(
            Bucket='teamars-1ee00834',
            Prefix='model-output/'
        )
        
        print("\n📦 Available Model Artifacts:")
        print("-" * 40)
        
        for obj in response.get('Contents', []):
            print(f"📄 {obj['Key']} ({obj['Size']} bytes)")
            
        # Check source code
        response = s3_client.list_objects_v2(
            Bucket='teamars-1ee00834',
            Prefix='code/'
        )
        
        print("\n💻 Available Source Code:")
        print("-" * 30)
        
        for obj in response.get('Contents', []):
            print(f"📄 {obj['Key']} ({obj['Size']} bytes)")
            
    except Exception as e:
        print(f"❌ Error checking S3: {e}")

if __name__ == "__main__":
    print("🔍 Debugging SageMaker Endpoint Issues")
    print("=" * 50)
    
    check_endpoint_logs()
    check_model_artifacts()