terraform {
  backend "s3" {
    bucket = "statear"
    key    = "mlops/terraform.tfstate"
    region = "eu-central-1"
  }
}