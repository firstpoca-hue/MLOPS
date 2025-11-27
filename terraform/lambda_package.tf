# Create Lambda deployment package
data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/lambda_function.zip"
  
  source {
    content = file("${path.module}/../lambda_function.py")
    filename = "lambda_function.py"
  }
}