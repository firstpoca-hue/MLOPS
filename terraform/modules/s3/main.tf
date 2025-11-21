resource "aws_s3_bucket" "ml_bucket" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_versioning" "ml_bucket_versioning" {
  bucket = aws_s3_bucket.ml_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "pipeline_artifacts" {
  bucket = "${var.bucket_name}-pipeline-artifacts"
}

resource "aws_s3_bucket_versioning" "pipeline_artifacts_versioning" {
  bucket = aws_s3_bucket.pipeline_artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}