# GitHub Actions Workflows

## Workflows

### 1. Deploy Infrastructure (`deploy-infrastructure.yml`)
- **Trigger**: Manual workflow dispatch
- **Purpose**: Deploy/destroy AWS infrastructure using Terraform
- **Actions**: plan, apply, destroy
- **Requirements**: AWS credentials in GitHub secrets

### 2. Trigger ML Pipeline (`trigger-ml-pipeline.yml`)
- **Trigger**: 
  - Push to `data.csv` file
  - Manual workflow dispatch
- **Purpose**: Execute ML pipeline when training data changes
- **Steps**:
  1. Upload `data.csv` to S3
  2. Create/update SageMaker Pipeline
  3. Execute pipeline
  4. Deploy approved models

## Required GitHub Secrets

```
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
```

## Usage

1. **First Time Setup**:
   - Add AWS credentials to GitHub secrets
   - Run "Deploy Infrastructure" workflow with "apply"

2. **Update Training Data**:
   - Modify `data.csv`
   - Push changes → ML pipeline automatically triggers

3. **Manual Pipeline Execution**:
   - Run "Trigger ML Pipeline" workflow manually

4. **Cleanup**:
   - Run "Deploy Infrastructure" workflow with "destroy"