output "pipeline_name" {
  value = aws_codepipeline.mlops_pipeline.name
}

output "pipeline_arn" {
  value = aws_codepipeline.mlops_pipeline.arn
}

output "github_connection_arn" {
  description = "ARN of the GitHub CodeStar connection"
  value       = aws_codestar_connections_connection.github.arn
}