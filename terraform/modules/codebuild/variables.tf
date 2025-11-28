variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "codebuild_role_arn" {
  description = "ARN of the CodeBuild service role"
  type        = string
}

variable "sagemaker_role_arn" {
  description = "ARN of the SageMaker execution role"
  type        = string
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket for ML artifacts"
  type        = string
}

variable "buildspec_file" {
  description = "Path to the buildspec file"
  type        = string
  default     = "buildspec.yml"
}