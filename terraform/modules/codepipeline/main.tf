# CodeStar connection for GitHub
resource "aws_codestar_connections_connection" "github" {
  name          = "${var.project_name}-github-connection"
  provider_type = "GitHub"
}

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
        ConnectionArn    = aws_codestar_connections_connection.github.arn
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
      version          = "1"

      configuration = {
        ProjectName = var.codebuild_project_name
      }
    }
  }
}