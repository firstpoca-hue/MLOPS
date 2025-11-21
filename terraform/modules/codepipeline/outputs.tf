output "pipeline_name" {
  value = aws_codepipeline.mlops_pipeline.name
}

output "pipeline_arn" {
  value = aws_codepipeline.mlops_pipeline.arn
}