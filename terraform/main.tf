module "s3" {
  source      = "./modules/s3"
  bucket_name = var.bucket_name
}

module "iam" {
  source                        = "./modules/iam"
  project_name                  = var.project_name
  ml_bucket_arn                 = module.s3.ml_bucket_arn
  pipeline_artifacts_bucket_arn = module.s3.pipeline_artifacts_bucket_arn
}

module "codebuild" {
  source              = "./modules/codebuild"
  project_name        = var.project_name
  codebuild_role_arn  = module.iam.codebuild_role_arn
  sagemaker_role_arn  = module.iam.sagemaker_role_arn
  s3_bucket_name      = module.s3.ml_bucket_name
}

# Endpoint deployment CodeBuild project
module "endpoint_codebuild" {
  source              = "./modules/codebuild"
  project_name        = "${var.project_name}-endpoint"
  codebuild_role_arn  = module.iam.codebuild_role_arn
  sagemaker_role_arn  = module.iam.sagemaker_role_arn
  s3_bucket_name      = module.s3.ml_bucket_name
  buildspec_file      = "endpoint-buildspec.yml"
}

# GitHub Connection
module "github_connection" {
  source       = "./modules/github-connection"
  project_name = var.project_name
}

# CodePipeline module - Native AWS CI/CD
module "codepipeline" {
  source                          = "./modules/codepipeline"
  project_name                    = var.project_name
  codepipeline_role_arn           = module.iam.codepipeline_role_arn
  pipeline_artifacts_bucket_name  = module.s3.pipeline_artifacts_bucket_name
  codebuild_project_name          = module.codebuild.project_name
  endpoint_deploy_project_name    = module.endpoint_codebuild.project_name
  github_owner                    = var.github_owner
  github_repo                     = var.github_repo
  github_branch                   = var.github_branch
  github_connection_arn           = module.github_connection.connection_arn
}

# API Gateway for web interface
module "api_gateway" {
  source            = "./modules/api-gateway"
  api_name          = "${var.project_name}-api"
  stage_name        = "prod"
  lambda_invoke_arn = module.lambda.lambda_invoke_arn
}

# Lambda function for SageMaker proxy
module "lambda" {
  source                    = "./modules/lambda"
  function_name            = "${var.project_name}-proxy"
  lambda_zip_path          = data.archive_file.lambda_zip.output_path
  api_gateway_execution_arn = module.api_gateway.api_gateway_execution_arn
}