variable "project_name" {
  description = "Project name"
  type        = string
}

variable "codebuild_role_arn" {
  description = "ARN of the CodeBuild IAM role"
  type        = string
}

variable "buildspec_path" {
  description = "Path to buildspec file"
  type        = string
  default     = "Pipeline/buildspec.yml"
}