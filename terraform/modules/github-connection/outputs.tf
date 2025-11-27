output "connection_arn" {
  description = "ARN of the GitHub connection"
  value       = aws_codestarconnections_connection.github.arn
}

output "connection_status" {
  description = "Status of the GitHub connection"
  value       = aws_codestarconnections_connection.github.connection_status
}