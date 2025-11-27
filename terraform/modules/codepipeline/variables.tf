variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "codepipeline_role_arn" {
  description = "ARN of the CodePipeline service role"
  type        = string
}

variable "pipeline_artifacts_bucket_name" {
  description = "Name of the S3 bucket for pipeline artifacts"
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
  description = "GitHub branch to track"
  type        = string
  default     = "main"
}

variable "github_connection_arn" {
  description = "ARN of the GitHub CodeStar connection"
  type        = string
}

variable "codecommit_repo_arn" {
  description = "ARN of CodeCommit repository (if using CodeCommit instead of GitHub)"
  type        = string
  default     = ""
}