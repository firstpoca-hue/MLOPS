# MLOps Loan Prediction Pipeline

Automated ML pipeline for loan approval prediction using AWS SageMaker, CodePipeline, and Terraform.

## 🏗️ Architecture

```
GitHub → CodePipeline → CodeBuild → SageMaker Pipeline → Model Registry → Endpoint
```

## 🚀 Quick Start

### 1. Infrastructure Deployment
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your GitHub details
./deploy.sh
```

### 2. Push Code
```bash
git add .
git commit -m "Initial MLOps setup"
git push origin main
```

### 3. Monitor Pipeline
- AWS CodePipeline Console
- SageMaker Pipelines Console
- Model Registry for approvals

## 📁 Project Structure

```
├── code/                   # ML scripts
│   ├── preprocessing.py    # Data preprocessing
│   ├── train.py           # Model training
│   ├── evaluate.py        # Model evaluation
│   └── inference.py       # Endpoint inference
├── deploy/                # Deployment scripts
│   └── deploy_model.py    # Model deployment
├── pipeline/              # SageMaker Pipeline
│   └── sagemaker_pipeline.py
├── terraform/             # Infrastructure as Code
│   ├── main.tf           # Main configuration
│   ├── variables.tf      # Variables
│   └── deploy.sh         # Deployment script
├── Pipeline/              # CI/CD configuration
│   └── buildspec.yml     # CodeBuild specification
├── data.csv              # Training data
└── requirements.txt      # Python dependencies
```

## 🤖 Automated Workflow

1. **Data Update**: Modify `data.csv` and push to GitHub
2. **Pipeline Trigger**: CodePipeline automatically starts
3. **Data Processing**: Feature engineering and train/test split
4. **Model Training**: LogisticRegression training
5. **Model Evaluation**: Performance metrics calculation
6. **Auto Approval**: Models with Accuracy ≥ 0.7 and F1 ≥ 0.7
7. **Model Registration**: Approved models registered
8. **Deployment**: Automatic endpoint deployment

## 🎯 Model Approval Criteria

- **Accuracy**: ≥ 70%
- **F1 Score**: ≥ 70%

## 🧹 Cleanup

```bash
cd terraform
./destroy.sh
```

## 📊 Monitoring

- **CodePipeline**: Build status and logs
- **SageMaker**: Pipeline execution and model metrics
- **CloudWatch**: Logs and monitoring
- **Model Registry**: Model versions and approvals# MLOps Pipeline Ready - Thu Nov 27 14:11:59 IST 2025
# Force pipeline trigger
