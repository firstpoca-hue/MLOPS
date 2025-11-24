import json
import boto3

def lambda_handler(event, context):
    """Simple CORS proxy for SageMaker endpoint"""
    
    # Handle CORS preflight
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': ''
        }
    
    try:
        # Parse request
        body = json.loads(event['body'])
        
        # Call SageMaker
        runtime = boto3.client('sagemaker-runtime', region_name='eu-central-1')
        response = runtime.invoke_endpoint(
            EndpointName='loan-endpoint',
            ContentType='application/json',
            Body=json.dumps(body)
        )
        
        result = json.loads(response['Body'].read().decode())
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }