output "bucket_arn" {
  description = "ARN of the demo S3 bucket"
  value       = aws_s3_bucket.demo.arn
}
