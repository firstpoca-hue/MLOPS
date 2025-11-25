# API Gateway REST API
resource "aws_api_gateway_rest_api" "loan_prediction_api" {
  name        = var.api_name
  description = "API for Loan Prediction ML Model"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# API Gateway Resource
resource "aws_api_gateway_resource" "predict" {
  rest_api_id = aws_api_gateway_rest_api.loan_prediction_api.id
  parent_id   = aws_api_gateway_rest_api.loan_prediction_api.root_resource_id
  path_part   = "predict"
}

# POST Method
resource "aws_api_gateway_method" "predict_post" {
  rest_api_id   = aws_api_gateway_rest_api.loan_prediction_api.id
  resource_id   = aws_api_gateway_resource.predict.id
  http_method   = "POST"
  authorization = "NONE"
}

# OPTIONS Method for CORS
resource "aws_api_gateway_method" "predict_options" {
  rest_api_id   = aws_api_gateway_rest_api.loan_prediction_api.id
  resource_id   = aws_api_gateway_resource.predict.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

# Lambda Integration for POST
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.loan_prediction_api.id
  resource_id = aws_api_gateway_resource.predict.id
  http_method = aws_api_gateway_method.predict_post.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = var.lambda_invoke_arn
}

# Mock Integration for OPTIONS (CORS)
resource "aws_api_gateway_integration" "options_integration" {
  rest_api_id = aws_api_gateway_rest_api.loan_prediction_api.id
  resource_id = aws_api_gateway_resource.predict.id
  http_method = aws_api_gateway_method.predict_options.http_method

  type = "MOCK"
  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

# Method Response for OPTIONS
resource "aws_api_gateway_method_response" "options_response" {
  rest_api_id = aws_api_gateway_rest_api.loan_prediction_api.id
  resource_id = aws_api_gateway_resource.predict.id
  http_method = aws_api_gateway_method.predict_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

# Integration Response for OPTIONS
resource "aws_api_gateway_integration_response" "options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.loan_prediction_api.id
  resource_id = aws_api_gateway_resource.predict.id
  http_method = aws_api_gateway_method.predict_options.http_method
  status_code = aws_api_gateway_method_response.options_response.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

# API Gateway Deployment
resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda_integration,
    aws_api_gateway_integration.options_integration,
  ]

  rest_api_id = aws_api_gateway_rest_api.loan_prediction_api.id
  stage_name  = var.stage_name
}