output "project_name" {
  value = aws_codebuild_project.mlops_build.name
}

output "project_arn" {
  value = aws_codebuild_project.mlops_build.arn
}