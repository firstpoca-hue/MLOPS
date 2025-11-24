resource "aws_s3_bucket" "ml_bucket" {
  bucket        = var.bucket_name
  force_destroy = true
}

resource "aws_s3_bucket" "pipeline_artifacts" {
  bucket        = "${var.bucket_name}-pipeline-artifacts"
  force_destroy = true
}