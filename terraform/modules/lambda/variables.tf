variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "loan-prediction-proxy"
}

variable "lambda_zip_path" {
  description = "Path to the Lambda deployment package"
  type        = string
}

variable "api_gateway_execution_arn" {
  description = "API Gateway execution ARN for Lambda permissions"
  type        = string
}