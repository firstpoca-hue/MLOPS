#!/bin/bash

echo "🚀 Deploying MLOps Pipeline with CodeBuild CI/CD..."

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    echo "❌ terraform.tfvars not found!"
    echo "📝 Please copy terraform.tfvars.example to terraform.tfvars and fill in your values"
    exit 1
fi

# Initialize Terraform
echo "🔧 Initializing Terraform..."
terraform init

# Plan the deployment
echo "📋 Planning deployment..."
terraform plan

# Ask for confirmation
read -p "🤔 Do you want to proceed with deployment? (y/N): " confirm
if [[ $confirm != [yY] ]]; then
    echo "❌ Deployment cancelled"
    exit 0
fi

# Apply the configuration
echo "🚀 Deploying infrastructure..."
terraform apply -auto-approve

# Get outputs
echo "📊 Deployment completed! Here are the important URLs:"
echo ""
terraform output -json | jq -r '
  "🔗 CodePipeline: " + (.codepipeline_url.value // "Not available"),
  "🔗 CodeBuild: https://console.aws.amazon.com/codesuite/codebuild/projects",
  "🔗 SageMaker: https://console.aws.amazon.com/sagemaker/home#/jobs",
  "🔗 S3 Bucket: https://s3.console.aws.amazon.com/s3/buckets/" + (.s3_bucket_name.value // "")
'

echo ""
echo "✅ MLOps Pipeline deployed successfully!"
echo "📝 Next steps:"
echo "   1. Push your code to trigger the pipeline"
echo "   2. Monitor progress in AWS CodePipeline console"
echo "   3. Check SageMaker for training job status"