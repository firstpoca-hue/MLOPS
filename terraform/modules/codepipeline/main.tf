# CodePipeline for MLOps CI/CD
resource "aws_codepipeline" "mlops_pipeline" {
  name     = "${var.project_name}-pipeline"
  role_arn = var.codepipeline_role_arn

  artifact_store {
    location = var.pipeline_artifacts_bucket_name
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "AWS"
      provider         = "CodeStarSourceConnection"
      version          = "1"
      output_artifacts = ["source_output"]

      configuration = {
        ConnectionArn    = var.github_connection_arn
        FullRepositoryId = "${var.github_owner}/${var.github_repo}"
        BranchName       = var.github_branch
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_output"]
      version          = "1"

      configuration = {
        ProjectName = var.codebuild_project_name
      }
    }
  }

  stage {
    name = "Deploy"

    action {
      name            = "Deploy"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "S3"
      input_artifacts = ["build_output"]
      version         = "1"

      configuration = {
        BucketName = var.pipeline_artifacts_bucket_name
        Extract    = "true"
        ObjectKey  = "deployments/"
      }
    }
  }

  tags = {
    Name        = "${var.project_name}-pipeline"
    Environment = "production"
    Project     = var.project_name
  }
}

# CloudWatch Event Rule for automatic pipeline triggers
resource "aws_cloudwatch_event_rule" "codepipeline_trigger" {
  name        = "${var.project_name}-pipeline-trigger"
  description = "Trigger CodePipeline on repository changes"

  event_pattern = jsonencode({
    source      = ["aws.codecommit"]
    detail-type = ["CodeCommit Repository State Change"]
    resources   = [var.codecommit_repo_arn]
    detail = {
      event = ["referenceCreated", "referenceUpdated"]
      referenceType = ["branch"]
      referenceName = [var.github_branch]
    }
  })
}

resource "aws_cloudwatch_event_target" "codepipeline" {
  rule      = aws_cloudwatch_event_rule.codepipeline_trigger.name
  target_id = "TriggerCodePipeline"
  arn       = aws_codepipeline.mlops_pipeline.arn
  role_arn  = var.codepipeline_role_arn
}