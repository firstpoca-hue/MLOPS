# S3 Outputs
output "s3_bucket_name" {
  description = "Name of the S3 bucket for ML artifacts"
  value       = module.s3.ml_bucket_name
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket for ML artifacts"
  value       = module.s3.ml_bucket_arn
}

# IAM Outputs
output "sagemaker_role_arn" {
  description = "ARN of the SageMaker execution role"
  value       = module.iam.sagemaker_role_arn
}

output "codebuild_role_arn" {
  description = "ARN of the CodeBuild service role"
  value       = module.iam.codebuild_role_arn
}

output "codepipeline_role_arn" {
  description = "ARN of the CodePipeline service role"
  value       = module.iam.codepipeline_role_arn
}

# CodeBuild Outputs
output "codebuild_project_name" {
  description = "Name of the CodeBuild project"
  value       = module.codebuild.project_name
}

output "codebuild_webhook_url" {
  description = "GitHub webhook URL for CodeBuild"
  value       = module.codebuild.webhook_url
}

# CodePipeline Outputs
output "codepipeline_name" {
  description = "Name of the CodePipeline"
  value       = module.codepipeline.pipeline_name
}

output "codepipeline_url" {
  description = "URL to view the CodePipeline in AWS Console"
  value       = module.codepipeline.pipeline_url
}

# API Gateway Outputs
output "api_gateway_url" {
  description = "URL of the API Gateway endpoint"
  value       = module.api_gateway.api_url
}

# Instructions
output "next_steps" {
  description = "Next steps after deployment"
  value = <<-EOT
    🎉 MLOps Pipeline deployed successfully!
    
    📋 Next Steps:
    1. Configure GitHub webhook: ${module.codebuild.webhook_url}
    2. Push code to trigger pipeline: git push origin main
    3. Monitor pipeline: ${module.codepipeline.pipeline_url}
    4. Test API endpoint: ${module.api_gateway.api_url}
    
    📊 AWS Console Links:
    - CodePipeline: https://console.aws.amazon.com/codesuite/codepipeline/home
    - CodeBuild: https://console.aws.amazon.com/codesuite/codebuild/home
    - SageMaker: https://console.aws.amazon.com/sagemaker/home
    - S3: https://s3.console.aws.amazon.com/s3/buckets/${module.s3.ml_bucket_name}
  EOT
}