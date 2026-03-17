terraform {
  required_version = ">= 1.0.0"
}

provider "aws" {
  # region left unset; use AWS_REGION env var or profile
}

# Example resource: S3 bucket for demo (name variable)
resource "aws_s3_bucket" "demo" {
  bucket = var.bucket_name
  acl    = "private"
}
