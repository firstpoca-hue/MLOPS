# Create Lambda deployment package
data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/lambda_function.zip"
  
  source {
    content = file("${path.module}/../lambda_function.py")
    filename = "lambda_function.py"
  }
  
  # Force recreation when file changes
  depends_on = [null_resource.lambda_trigger]
}

# Trigger to force Lambda update
resource "null_resource" "lambda_trigger" {
  triggers = {
    lambda_hash = filebase64sha256("${path.module}/../lambda_function.py")
    timestamp = timestamp()
  }
}