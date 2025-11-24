terraform {
  backend "s3" {
    bucket = "statears"
    key    = "mlops/terraform.tfstate"
    region = "eu-central-1"
  }
}