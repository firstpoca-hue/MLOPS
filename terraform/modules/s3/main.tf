terraform {
  required_providers {
    random = {
      source = "hashicorp/random"
      version = "~> 3.1"
    }
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "ml_bucket" {
  bucket        = "${var.bucket_name}-${random_id.bucket_suffix.hex}"
  force_destroy = true
}

resource "aws_s3_bucket" "pipeline_artifacts" {
  bucket        = "${var.bucket_name}-pipeline-${random_id.bucket_suffix.hex}"
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "ml_bucket_versioning" {
  bucket = aws_s3_bucket.ml_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "pipeline_artifacts_versioning" {
  bucket = aws_s3_bucket.pipeline_artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}