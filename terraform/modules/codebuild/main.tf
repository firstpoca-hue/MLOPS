# CodeBuild Project for MLOps Pipeline
resource "aws_codebuild_project" "mlops_build" {
  name          = "${var.project_name}-build"
  description   = "MLOps pipeline build project"
  service_role  = var.codebuild_role_arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_MEDIUM"
    image                      = "aws/codebuild/amazonlinux2-x86_64-standard:3.0"
    type                       = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"
    privileged_mode            = true

    environment_variable {
      name  = "AWS_DEFAULT_REGION"
      value = data.aws_region.current.name
    }

    environment_variable {
      name  = "SAGEMAKER_ROLE_ARN"
      value = var.sagemaker_role_arn
    }

    environment_variable {
      name  = "S3_BUCKET"
      value = var.s3_bucket_name
    }

    environment_variable {
      name  = "MODEL_PACKAGE_GROUP_NAME"
      value = "loan-prediction-models"
    }
  }

  source {
    type = "CODEPIPELINE"
    buildspec = "buildspec.yml"
  }

  tags = {
    Name        = "${var.project_name}-codebuild"
    Environment = "production"
    Project     = var.project_name
  }
}

# GitHub webhook for automatic builds
resource "aws_codebuild_webhook" "mlops_webhook" {
  project_name = aws_codebuild_project.mlops_build.name
  build_type   = "BUILD"

  filter_group {
    filter {
      type    = "EVENT"
      pattern = "PUSH"
    }

    filter {
      type    = "HEAD_REF"
      pattern = "refs/heads/main"
    }
  }
}

data "aws_region" "current" {}