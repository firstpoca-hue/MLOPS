resource "aws_codebuild_project" "mlops_build" {
  name         = "${var.project_name}-build"
  service_role = var.codebuild_role_arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type = "BUILD_GENERAL1_MEDIUM"
    image        = "aws/codebuild/amazonlinux2-x86_64-standard:3.0"
    type         = "LINUX_CONTAINER"
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = var.buildspec_path
  }
}