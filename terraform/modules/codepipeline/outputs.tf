output "pipeline_name" {
  description = "Name of the CodePipeline"
  value       = aws_codepipeline.mlops_pipeline.name
}

output "pipeline_arn" {
  description = "ARN of the CodePipeline"
  value       = aws_codepipeline.mlops_pipeline.arn
}

output "pipeline_url" {
  description = "URL to view the CodePipeline in AWS Console"
  value       = "https://${data.aws_region.current.name}.console.aws.amazon.com/codesuite/codepipeline/pipelines/${aws_codepipeline.mlops_pipeline.name}/view"
}

data "aws_region" "current" {}