variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "mlops-loan-model"
}

variable "bucket_name" {
  description = "S3 bucket name for ML artifacts"
  type        = string
  default     = "teamars"
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
  default     = "main"
}

# GitHub token not needed for infrastructure deployment
# CodePipeline will be configured without GitHub integration