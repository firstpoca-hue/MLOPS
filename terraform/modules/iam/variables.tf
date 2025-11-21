variable "project_name" {
  description = "Project name"
  type        = string
}

variable "ml_bucket_arn" {
  description = "ARN of the ML bucket"
  type        = string
}

variable "pipeline_artifacts_bucket_arn" {
  description = "ARN of the pipeline artifacts bucket"
  type        = string
}