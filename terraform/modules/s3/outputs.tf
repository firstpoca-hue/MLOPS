output "ml_bucket_name" {
  value = aws_s3_bucket.ml_bucket.bucket
}

output "ml_bucket_arn" {
  value = aws_s3_bucket.ml_bucket.arn
}

output "pipeline_artifacts_bucket_name" {
  value = aws_s3_bucket.pipeline_artifacts.bucket
}

output "pipeline_artifacts_bucket_arn" {
  value = aws_s3_bucket.pipeline_artifacts.arn
}