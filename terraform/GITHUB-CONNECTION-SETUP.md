# GitHub Connection Setup Guide

## 🔗 How GitHub Connects to AWS

The Terraform configuration uses **AWS CodeStar Connections** to securely connect to your GitHub account without storing tokens.

## 📋 Connection Methods

### Method 1: CodeStar Connections (Recommended) ✅
- **Secure**: No tokens stored in Terraform
- **Managed**: AWS handles authentication
- **Easy**: One-time setup through AWS Console

### Method 2: Personal Access Token (Legacy) ❌
- **Less Secure**: Token stored in Terraform state
- **Manual**: Requires token management
- **Deprecated**: AWS recommends CodeStar Connections

## 🚀 Setup Steps

### 1. Deploy Infrastructure
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars (no GitHub token needed)
./deploy-codebuild.sh
```

### 2. Complete GitHub Connection (One-time)
After Terraform deployment, you'll see:
```
⚠️  GitHub connection created but PENDING
📝 Complete setup in AWS Console
```

### 3. Authorize Connection in AWS Console
1. **Go to AWS CodePipeline Console**
2. **Navigate to Settings → Connections**
3. **Find your connection**: `mlops-loan-model-github-connection`
4. **Click "Update pending connection"**
5. **Authorize with GitHub**:
   - Login to GitHub
   - Grant permissions to AWS
   - Select repositories

### 4. Verify Connection
```bash
# Check connection status
aws codestar-connections get-connection \
  --connection-arn $(terraform output -raw github_connection_arn)
```

Status should show: `AVAILABLE`

## 🔧 Connection Details

### What Gets Created:
```hcl
resource "aws_codestarconnections_connection" "github" {
  name          = "mlops-loan-model-github-connection"
  provider_type = "GitHub"
}
```

### How CodePipeline Uses It:
```hcl
configuration = {
  ConnectionArn    = "arn:aws:codestar-connections:region:account:connection/xxx"
  FullRepositoryId = "your-username/your-repo"
  BranchName       = "main"
}
```

## 🔐 Security Benefits

### CodeStar Connections:
- ✅ **No tokens in Terraform state**
- ✅ **AWS manages authentication**
- ✅ **Automatic token rotation**
- ✅ **Fine-grained permissions**
- ✅ **Audit logging**

### vs Personal Access Tokens:
- ❌ **Tokens stored in state files**
- ❌ **Manual token rotation**
- ❌ **Broad permissions required**
- ❌ **Token expiration issues**

## 🚨 Troubleshooting

### Connection Status: PENDING
```bash
# Check connection in AWS Console
# Complete authorization flow
```

### Pipeline Fails: "Connection not available"
```bash
# Verify connection status
aws codestar-connections get-connection --connection-arn <arn>

# Re-authorize if needed
```

### Repository Access Issues
```bash
# Ensure GitHub App has access to your repository
# Check repository permissions in GitHub settings
```

## 📊 Monitoring

### Connection Health:
- **AWS Console**: CodePipeline → Settings → Connections
- **CloudWatch**: Connection events and metrics
- **CloudTrail**: API calls and changes

### Pipeline Triggers:
- **Automatic**: Push to main branch
- **Manual**: Start execution in console
- **Webhook**: GitHub webhook events

## 🔄 Alternative: GitHub Webhooks

If you prefer webhooks over polling:

```hcl
resource "aws_codebuild_webhook" "github" {
  project_name = aws_codebuild_project.mlops_build.name
  
  filter_group {
    filter {
      type    = "EVENT"
      pattern = "PUSH"
    }
    filter {
      type    = "HEAD_REF"
      pattern = "refs/heads/main"
    }
  }
}
```

## 📝 Summary

1. **Deploy**: Terraform creates connection (PENDING state)
2. **Authorize**: Complete setup in AWS Console
3. **Verify**: Connection status becomes AVAILABLE
4. **Use**: CodePipeline automatically triggers on pushes

No GitHub tokens needed in your Terraform configuration! 🎉