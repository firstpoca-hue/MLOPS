import json
import boto3

def lambda_handler(event, context):
    """Lambda function to serve HTML UI and handle predictions via SageMaker Endpoint"""
    # Updated: 2025-11-28-14:30 - Add debug logging
    
    try:
        print(f"Event received: {json.dumps(event)}")
        print(f"Lambda invoked with method: {event.get('httpMethod')}")
        # Handle GET request - serve HTML UI
        if event.get('httpMethod') == 'GET':
            html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Loan Prediction System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        .header {
            background: linear-gradient(135deg, #ff6b6b, #feca57);
            padding: 40px;
            text-align: center;
            color: white;
        }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        .form-container {
            padding: 40px;
        }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        .form-group {
            position: relative;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
            font-size: 0.95rem;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e8ed;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            transform: translateY(-2px);
        }
        .submit-btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.2rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        .submit-btn:active {
            transform: translateY(-1px);
        }
        .result {
            margin-top: 30px;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            animation: slideIn 0.5s ease;
        }
        .approved {
            background: linear-gradient(135deg, #56ab2f, #a8e6cf);
            color: white;
            box-shadow: 0 10px 25px rgba(86, 171, 47, 0.3);
        }
        .rejected {
            background: linear-gradient(135deg, #ff416c, #ff4757);
            color: white;
            box-shadow: 0 10px 25px rgba(255, 65, 108, 0.3);
        }
        .result h3 {
            font-size: 1.8rem;
            margin-bottom: 10px;
        }
        .result p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 768px) {
            .form-grid { grid-template-columns: 1fr; }
            .header h1 { font-size: 2rem; }
            .container { margin: 10px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Loan Prediction System</h1>
            <p>Get instant loan approval decisions powered by machine learning</p>
        </div>
        <div class="form-container">
            <form id="loanForm">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="no_of_dependents">👨‍👩‍👧‍👦 Number of Dependents</label>
                        <input type="number" id="no_of_dependents" name="no_of_dependents" min="0" max="10" placeholder="e.g., 2" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="education">🎓 Education Level</label>
                        <select id="education" name="education" required>
                            <option value="">Select Education Level</option>
                            <option value="Graduate">Graduate</option>
                            <option value="Not Graduate">Not Graduate</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="self_employed">💼 Employment Status</label>
                        <select id="self_employed" name="self_employed" required>
                            <option value="">Select Employment Status</option>
                            <option value="Yes">Self Employed</option>
                            <option value="No">Employed</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="income_annum">💰 Annual Income (₹)</label>
                        <input type="number" id="income_annum" name="income_annum" min="100000" max="50000000" placeholder="e.g., 5000000" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="loan_amount">🏦 Loan Amount (₹)</label>
                        <input type="number" id="loan_amount" name="loan_amount" min="100000" max="50000000" placeholder="e.g., 2000000" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="loan_term">📅 Loan Term (Years)</label>
                        <input type="number" id="loan_term" name="loan_term" min="1" max="30" placeholder="e.g., 15" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="credit_score">📊 Credit Score</label>
                        <input type="number" id="credit_score" name="credit_score" min="300" max="900" placeholder="e.g., 750" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="residential_assets_value">🏠 Residential Assets (₹)</label>
                        <input type="number" id="residential_assets_value" name="residential_assets_value" min="0" max="100000000" placeholder="e.g., 8000000" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="commercial_assets_value">🏢 Commercial Assets (₹)</label>
                        <input type="number" id="commercial_assets_value" name="commercial_assets_value" min="0" max="100000000" placeholder="e.g., 1000000" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="luxury_assets_value">💎 Luxury Assets (₹)</label>
                        <input type="number" id="luxury_assets_value" name="luxury_assets_value" min="0" max="100000000" placeholder="e.g., 500000" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="bank_asset_value">🏛️ Bank Assets (₹)</label>
                        <input type="number" id="bank_asset_value" name="bank_asset_value" min="0" max="100000000" placeholder="e.g., 2000000" required>
                    </div>
                </div>
                
                <button type="submit" class="submit-btn">🚀 Get AI Prediction</button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>AI is analyzing your application...</p>
            </div>
            
            <div id="result"></div>
        </div>
    </div>
    
    <script>
        document.getElementById('loanForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            
            ['no_of_dependents', 'income_annum', 'loan_amount', 'loan_term', 'credit_score', 
             'residential_assets_value', 'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value'].forEach(field => {
                data[field] = parseInt(data[field]);
            });
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').innerHTML = '';
            
            try {
                const response = await fetch(window.location.href, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                // Hide loading
                document.getElementById('loading').style.display = 'none';
                
                const resultDiv = document.getElementById('result');
                if (result.prediction === 'Approved') {
                    resultDiv.innerHTML = '<div class="result approved"><h3>🎉 Congratulations! Loan Approved!</h3><p>AI Confidence: ' + (result.confidence * 100).toFixed(1) + '%</p><p>Your application has been successfully processed.</p></div>';
                } else {
                    resultDiv.innerHTML = '<div class="result rejected"><h3>😔 Loan Application Declined</h3><p>AI Confidence: ' + (result.confidence * 100).toFixed(1) + '%</p><p>Please review your financial profile and try again.</p></div>';
                }
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('result').innerHTML = '<div class="result rejected"><h3>⚠️ System Error</h3><p>' + error.message + '</p><p>Please try again later.</p></div>';
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
        print(f"Lambda error: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }