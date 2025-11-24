# Secure Token Management for MLOps Deployment

## Problem
GitHub tokens should not be hardcoded in `terraform.tfvars` files as they can be accidentally committed to version control.

## Solutions

### Option 1: Environment Variables (Recommended)

1. **Set up environment variables:**
```bash
cd terraform

# Copy example files
cp terraform.tfvars.example terraform.tfvars
cp .env.example .env

# Edit .env file with your token
echo 'export TF_VAR_github_token="your-github-token-here"' > .env
```

2. **Deploy securely:**
```bash
# Load environment variables and deploy
./deploy-secure.sh

# Or manually:
source .env
terraform init
terraform plan
terraform apply
```

### Option 2: Export Variables Directly

```bash
# Export token before running Terraform
export TF_VAR_github_token="your-github-token-here"

# Run Terraform commands
terraform init
terraform plan
terraform apply
```

### Option 3: Terraform Cloud/Enterprise

```bash
# Set as environment variable in Terraform Cloud
TF_VAR_github_token = "your-github-token-here"
```

### Option 4: AWS Systems Manager Parameter Store

```bash
# Store token in AWS Parameter Store
aws ssm put-parameter \
  --name "/mlops/github-token" \
  --value "your-github-token-here" \
  --type "SecureString"

# Reference in Terraform
data "aws_ssm_parameter" "github_token" {
  name = "/mlops/github-token"
}
```

## Security Best Practices

### Files to Never Commit:
- `terraform.tfvars` (contains sensitive values)
- `.env` (contains tokens)
- `*.tfstate` (may contain sensitive data)

### .gitignore Configuration:
```
# Terraform
*.tfstate
*.tfstate.*
*.tfvars
.terraform/
.terraform.lock.hcl

# Environment variables
.env

# OS
.DS_Store
Thumbs.db
```

### GitHub Token Permissions:
Minimum required permissions:
- `repo` (Full control of private repositories)
- `admin:repo_hook` (Read and write repository hooks)

## Recommended Approach

Use **Option 1 (Environment Variables)** with the provided `deploy-secure.sh` script:

1. Never commit sensitive files
2. Use environment variables for tokens
3. Use the secure deployment script
4. Regularly rotate GitHub tokens
5. Use least-privilege token permissions