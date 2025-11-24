output "s3_bucket_name" {
  description = "Name of the S3 bucket for ML artifacts"
  value       = module.s3.ml_bucket_name
}

output "pipeline_artifacts_bucket" {
  description = "Name of the S3 bucket for pipeline artifacts"
  value       = module.s3.pipeline_artifacts_bucket_name
}

output "sagemaker_role_arn" {
  description = "ARN of the SageMaker execution role"
  value       = module.iam.sagemaker_role_arn
}

# CodePipeline replaced by GitHub Actions
# output "codepipeline_name" {
#   description = "Name of the CodePipeline"
#   value       = module.codepipeline.pipeline_name
# }

output "codebuild_project_name" {
  description = "Name of the CodeBuild project"
  value       = module.codebuild.project_name
}