# Terraform AWS Demo (local state)

This directory contains a minimal Terraform project configured to use a local backend (state saved to `terraform.tfstate`).

Files:
- `main.tf` - provider and example S3 bucket resource
- `variables.tf` - variable for bucket name
- `outputs.tf` - outputs the bucket ARN
- `backend.tf` - configures local backend
- `.gitignore` - ignores state and local files

Usage:

```bash
cd /Users/duckhue01/code/lab/aws
terraform init
terraform plan
terraform apply
```

Notes:
- AWS credentials must be available in your environment (e.g., `AWS_PROFILE` or environment variables).
- This example creates an S3 bucket; change/remove resources for your needs.
