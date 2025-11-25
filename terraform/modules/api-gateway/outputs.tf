output "api_gateway_url" {
  description = "URL of the API Gateway"
  value       = "https://${aws_api_gateway_rest_api.loan_prediction_api.id}.execute-api.${data.aws_region.current.name}.amazonaws.com/${var.stage_name}"
}

output "api_gateway_execution_arn" {
  description = "Execution ARN of the API Gateway"
  value       = aws_api_gateway_rest_api.loan_prediction_api.execution_arn
}

data "aws_region" "current" {}