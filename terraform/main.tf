terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

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
  source             = "./modules/codebuild"
  project_name       = var.project_name
  codebuild_role_arn = module.iam.codebuild_role_arn
}

module "codepipeline" {
  source                          = "./modules/codepipeline"
  project_name                    = var.project_name
  codepipeline_role_arn           = module.iam.codepipeline_role_arn
  pipeline_artifacts_bucket_name  = module.s3.pipeline_artifacts_bucket_name
  codebuild_project_name          = module.codebuild.project_name
  github_owner                    = var.github_owner
  github_repo                     = var.github_repo
  github_branch                   = var.github_branch
  github_token                    = var.github_token
}