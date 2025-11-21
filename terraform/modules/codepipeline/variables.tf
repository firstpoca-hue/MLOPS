variable "project_name" {
  description = "Project name"
  type        = string
}

variable "codepipeline_role_arn" {
  description = "ARN of the CodePipeline IAM role"
  type        = string
}

variable "pipeline_artifacts_bucket_name" {
  description = "Name of the pipeline artifacts bucket"
  type        = string
}

variable "codebuild_project_name" {
  description = "Name of the CodeBuild project"
  type        = string
}

variable "github_owner" {
  description = "GitHub repository owner"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
}

variable "github_branch" {
  description = "GitHub branch"
  type        = string
}

variable "github_token" {
  description = "GitHub personal access token"
  type        = string
  sensitive   = true
}