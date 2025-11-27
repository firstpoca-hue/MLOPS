# MLOps Pipeline with AWS CodeBuild CI/CD

Complete Terraform configuration for deploying MLOps pipeline using AWS CodeBuild and CodePipeline.

## 🏗️ Architecture

```
GitHub → CodePipeline → CodeBuild → SageMaker → Model Registry → Endpoint
```

## 📋 Prerequisites

1. **AWS CLI configured** with appropriate permissions
2. **Terraform installed** (v1.0+)
3. **GitHub Personal Access Token** with repo permissions
4. **jq installed** (for output formatting)

## 🚀 Quick Deployment

### 1. Configure Variables
```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
```

### 2. Deploy Infrastructure
```bash
./deploy-codebuild.sh
```

### 3. Configure GitHub Webhook (Optional)
The webhook URL will be provided in the output. Add it to your GitHub repository settings.

## 📁 Terraform Modules

### Core Infrastructure
- **S3**: ML artifacts and pipeline artifacts storage
- **IAM**: Service roles for CodeBuild, CodePipeline, SageMaker
- **CodeBuild**: Build project with MLOps environment
- **CodePipeline**: CI/CD pipeline with GitHub integration

### ML Infrastructure  
- **API Gateway**: REST API for model inference
- **Lambda**: Proxy function for SageMaker endpoints

## 🔧 Configuration Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `aws_region` | AWS region | `eu-central-1` |
| `project_name` | Project identifier | `mlops-loan-model` |
| `bucket_name` | S3 bucket name | `your-unique-bucket` |
| `github_owner` | GitHub username | `your-username` |
| `github_repo` | Repository name | `mlops-pipeline` |
| `github_token` | Personal access token | `ghp_xxxxx` |

## 🔐 Required Permissions

The deployment requires these AWS permissions:
- `IAMFullAccess`
- `S3FullAccess` 
- `CodeBuildAdminAccess`
- `CodePipelineFullAccess`
- `SageMakerFullAccess`
- `APIGatewayAdminAccess`
- `LambdaFullAccess`
- `CloudWatchEventsFullAccess`

## 📊 Monitoring

After deployment, monitor your pipeline:

1. **CodePipeline Console**: Pipeline execution status
2. **CodeBuild Console**: Build logs and metrics
3. **SageMaker Console**: Training jobs and models
4. **CloudWatch**: Logs and monitoring

## 🧹 Cleanup

```bash
terraform destroy -auto-approve
```

## 🔄 Pipeline Workflow

1. **Source**: GitHub repository changes trigger pipeline
2. **Build**: CodeBuild runs buildspec.yml
   - Install dependencies
   - Run SageMaker pipeline
   - Upload artifacts
3. **Deploy**: Artifacts deployed to S3

## 🛠️ Customization

### Environment Variables (CodeBuild)
- `AWS_DEFAULT_REGION`: AWS region
- `SAGEMAKER_ROLE_ARN`: SageMaker execution role
- `S3_BUCKET`: ML artifacts bucket
- `MODEL_PACKAGE_GROUP_NAME`: Model registry group

### Build Specification
Edit `buildspec.yml` to customize the build process:
- Add testing phases
- Modify deployment steps
- Include additional tools

## 🚨 Troubleshooting

### Common Issues

1. **GitHub Token**: Ensure token has `repo` permissions
2. **S3 Bucket**: Must be globally unique
3. **IAM Permissions**: Check service roles have required policies
4. **Region**: Ensure all resources in same region

### Debug Commands
```bash
# Check Terraform state
terraform show

# Validate configuration
terraform validate

# View detailed plan
terraform plan -detailed-exitcode
```

## 📈 Scaling

For production environments:
- Use separate environments (dev/staging/prod)
- Implement approval gates in CodePipeline
- Add automated testing stages
- Configure monitoring and alerting
- Use Terraform workspaces for multi-environment

## 🔗 Useful Links

- [AWS CodeBuild Documentation](https://docs.aws.amazon.com/codebuild/)
- [AWS CodePipeline Documentation](https://docs.aws.amazon.com/codepipeline/)
- [SageMaker Pipelines](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)