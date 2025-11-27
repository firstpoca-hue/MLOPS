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
    buildspec = "version: 0.2\nphases:\n  install:\n    runtime-versions:\n      python: 3.8\n    commands:\n      - pip install boto3 sagemaker pandas scikit-learn joblib numpy\n  build:\n    commands:\n      - echo 'MLOps Pipeline Starting'\n      - ls -la\n      - python Pipeline/sagemaker_pipeline.py\n      - echo 'Pipeline Completed'"
  }

  tags = {
    Name        = "${var.project_name}-codebuild"
    Environment = "production"
    Project     = var.project_name
  }
}

# Note: Webhook not needed when using CodePipeline
# CodePipeline handles GitHub integration via CodeStar Connections

data "aws_region" "current" {}