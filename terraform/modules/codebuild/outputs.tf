output "project_name" {
  description = "Name of the CodeBuild project"
  value       = aws_codebuild_project.mlops_build.name
}

output "project_arn" {
  description = "ARN of the CodeBuild project"
  value       = aws_codebuild_project.mlops_build.arn
}

output "webhook_url" {
  description = "GitHub webhook URL (handled by CodePipeline)"
  value       = "Not applicable - CodePipeline handles GitHub integration"
}