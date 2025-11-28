import json
import boto3
import numpy as np

def lambda_handler(event, context):
    """Lambda function to serve HTML UI and handle predictions via SageMaker Endpoint"""
    # Updated: 2025-11-28 - Endpoint integration
    
    try:
        # Handle GET request - serve HTML UI
        if event.get('httpMethod') == 'GET':
            html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loan Prediction System</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .result { margin-top: 20px; padding: 15px; border-radius: 4px; }
        .approved { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .rejected { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <h1>🏦 Loan Prediction System</h1>
    <p>Enter loan application details to get an instant prediction:</p>
    
    <form id="loanForm">
        <div class="form-group">
            <label for="no_of_dependents">Number of Dependents:</label>
            <input type="number" id="no_of_dependents" name="no_of_dependents" min="0" max="10" required>
        </div>
        
        <div class="form-group">
            <label for="education">Education:</label>
            <select id="education" name="education" required>
                <option value="">Select Education</option>
                <option value="Graduate">Graduate</option>
                <option value="Not Graduate">Not Graduate</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="self_employed">Self Employed:</label>
            <select id="self_employed" name="self_employed" required>
                <option value="">Select Employment</option>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="income_annum">Annual Income:</label>
            <input type="number" id="income_annum" name="income_annum" min="100000" max="50000000" required>
        </div>
        
        <div class="form-group">
            <label for="loan_amount">Loan Amount:</label>
            <input type="number" id="loan_amount" name="loan_amount" min="100000" max="50000000" required>
        </div>
        
        <div class="form-group">
            <label for="loan_term">Loan Term (years):</label>
            <input type="number" id="loan_term" name="loan_term" min="1" max="30" required>
        </div>
        
        <div class="form-group">
            <label for="credit_score">Credit Score:</label>
            <input type="number" id="credit_score" name="credit_score" min="300" max="900" required>
        </div>
        
        <div class="form-group">
            <label for="residential_assets_value">Residential Assets Value:</label>
            <input type="number" id="residential_assets_value" name="residential_assets_value" min="0" max="100000000" required>
        </div>
        
        <div class="form-group">
            <label for="commercial_assets_value">Commercial Assets Value:</label>
            <input type="number" id="commercial_assets_value" name="commercial_assets_value" min="0" max="100000000" required>
        </div>
        
        <div class="form-group">
            <label for="luxury_assets_value">Luxury Assets Value:</label>
            <input type="number" id="luxury_assets_value" name="luxury_assets_value" min="0" max="100000000" required>
        </div>
        
        <div class="form-group">
            <label for="bank_asset_value">Bank Asset Value:</label>
            <input type="number" id="bank_asset_value" name="bank_asset_value" min="0" max="100000000" required>
        </div>
        
        <button type="submit">🔮 Predict Loan Status</button>
    </form>
    
    <div id="result"></div>
    
    <script>
        document.getElementById('loanForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            
            ['no_of_dependents', 'income_annum', 'loan_amount', 'loan_term', 'credit_score', 
             'residential_assets_value', 'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value'].forEach(field => {
                data[field] = parseInt(data[field]);
            });
            
            try {
                const response = await fetch(window.location.href, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                const resultDiv = document.getElementById('result');
                if (result.prediction === 'Approved') {
                    resultDiv.innerHTML = '<div class="result approved"><h3>✅ Loan Approved!</h3><p>Confidence: ' + (result.confidence * 100).toFixed(1) + '%</p></div>';
                } else {
                    resultDiv.innerHTML = '<div class="result rejected"><h3>❌ Loan Rejected</h3><p>Confidence: ' + (result.confidence * 100).toFixed(1) + '%</p></div>';
                }
            } catch (error) {
                document.getElementById('result').innerHTML = '<div class="result rejected"><h3>Error</h3><p>' + error.message + '</p></div>';
            }
        });
    </script>
</body>
</html>"""
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': html_content
            }
        
        elif event.get('httpMethod') == 'POST':
            if not event.get('body'):
                return {
                    'statusCode': 400,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'error': 'Request body is required'})
                }
            
            body = json.loads(event['body'])
            
            # Call SageMaker endpoint
            sagemaker_runtime = boto3.client('sagemaker-runtime')
            endpoint_name = 'loan-endpoint'  # Matches deploy_model.py
            
            try:
                response = sagemaker_runtime.invoke_endpoint(
                    EndpointName=endpoint_name,
                    ContentType='application/json',
                    Body=json.dumps(body)
                )
                
                result_body = response['Body'].read().decode('utf-8')
                sagemaker_result = json.loads(result_body)
                
                result = {
                    'prediction': sagemaker_result['loan_status'],
                    'confidence': sagemaker_result['confidence']
                }
                
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps(result)
                }
                
            except Exception as endpoint_error:
                return {
                    'statusCode': 500,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'error': f'SageMaker endpoint error: {str(endpoint_error)}'})
                }
        
        else:
            return {
                'statusCode': 405,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Method not allowed'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }