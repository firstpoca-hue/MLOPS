# GitHub Connection using CodeStar Connections (Recommended)
resource "aws_codestarconnections_connection" "github" {
  name          = "${var.project_name}-github-connection"
  provider_type = "GitHub"

  tags = {
    Name    = "${var.project_name}-github"
    Project = var.project_name
  }
}