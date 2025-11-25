variable "api_name" {
  description = "Name of the API Gateway"
  type        = string
  default     = "loan-prediction-api"
}

variable "stage_name" {
  description = "Stage name for API Gateway deployment"
  type        = string
  default     = "prod"
}

variable "lambda_invoke_arn" {
  description = "Lambda function invoke ARN"
  type        = string
}