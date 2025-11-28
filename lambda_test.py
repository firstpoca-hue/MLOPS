import json

def lambda_handler(event, context):
    """Simple test Lambda function"""
    
    try:
        if event.get('httpMethod') == 'GET':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': '<h1>Lambda Test Working!</h1><p>SageMaker integration coming soon...</p>'
            }
        else:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'message': 'POST test working'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }