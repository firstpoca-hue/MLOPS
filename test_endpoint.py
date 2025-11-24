import boto3
import json
import numpy as np

# Configuration
REGION = "eu-central-1"
ENDPOINT_NAME = "loan-endpoint"

def test_endpoint():
    """Test the deployed SageMaker endpoint"""
    runtime = boto3.client('sagemaker-runtime', region_name=REGION)
    
    # Sample test data (same format as training data after preprocessing)
    test_data = {
        "no_of_dependents": 2,
        "education": 0,  # Graduate
        "self_employed": 0,  # No
        "income_annum": np.log(5000000 + 1),  # Log transformed
        "loan_amount": np.log(10000000 + 1),  # Log transformed
        "loan_term": 12,
        "credit_score": 750,
        "total_asset": np.log(15000000 + 1)   # Log transformed
    }
    
    try:
        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType='application/json',
            Body=json.dumps(test_data)
        )
        
        result = json.loads(response['Body'].read().decode())
        print(f"✅ Prediction successful: {result}")
        
        # Interpret result
        prediction = result['prediction']
        status = "Approved" if prediction == 1 else "Rejected"
        print(f"🏦 Loan Status: {status}")
        
    except Exception as e:
        print(f"❌ Endpoint test failed: {e}")

if __name__ == "__main__":
    test_endpoint()