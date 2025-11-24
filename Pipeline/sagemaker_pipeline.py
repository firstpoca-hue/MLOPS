import boto3
import json

# Configuration
REGION = "eu-central-1"
ROLE_ARN = "arn:aws:iam::361509912577:role/SageMakerExecutionRole"
BUCKET = "teamars"

def create_sagemaker_pipeline():
    """Create SageMaker Pipeline using boto3 API directly"""
    sagemaker = boto3.client('sagemaker', region_name=REGION)
    
    pipeline_definition = {
        "Version": "2020-12-01",
        "Metadata": {},
        "Parameters": [
            {
                "Name": "InputDataUrl",
                "Type": "String",
                "DefaultValue": f"s3://{BUCKET}/data/"
            }
        ],
        "Steps": [
            {
                "Name": "PreprocessLoanData",
                "Type": "Processing",
                "Arguments": {
                    "ProcessingResources": {
                        "ClusterConfig": {
                            "InstanceType": "ml.t3.medium",
                            "InstanceCount": 1,
                            "VolumeSizeInGB": 10
                        }
                    },
                    "AppSpecification": {
                        "ImageUri": f"683313688378.dkr.ecr.{REGION}.amazonaws.com/sagemaker-scikit-learn:1.0-1-cpu-py3",
                        "ContainerEntrypoint": ["python3", "/opt/ml/processing/input/code/preprocessing.py"]
                    },
                    "ProcessingInputs": [
                        {
                            "InputName": "input-1",
                            "AppManaged": False,
                            "S3Input": {
                                "S3Uri": {"Get": "Parameters.InputDataUrl"},
                                "LocalPath": "/opt/ml/processing/input",
                                "S3DataType": "S3Prefix",
                                "S3InputMode": "File"
                            }
                        },
                        {
                            "InputName": "code",
                            "AppManaged": False,
                            "S3Input": {
                                "S3Uri": f"s3://{BUCKET}/code/",
                                "LocalPath": "/opt/ml/processing/input/code",
                                "S3DataType": "S3Prefix",
                                "S3InputMode": "File"
                            }
                        }
                    ],
                    "ProcessingOutputs": [
                        {
                            "OutputName": "train",
                            "AppManaged": False,
                            "S3Output": {
                                "S3Uri": f"s3://{BUCKET}/processed/train",
                                "LocalPath": "/opt/ml/processing/train",
                                "S3UploadMode": "EndOfJob"
                            }
                        },
                        {
                            "OutputName": "test",
                            "AppManaged": False,
                            "S3Output": {
                                "S3Uri": f"s3://{BUCKET}/processed/test",
                                "LocalPath": "/opt/ml/processing/test",
                                "S3UploadMode": "EndOfJob"
                            }
                        }
                    ],
                    "RoleArn": ROLE_ARN
                }
            },
            {
                "Name": "TrainLoanModel",
                "Type": "Training",
                "Arguments": {
                    "AlgorithmSpecification": {
                        "TrainingImage": f"683313688378.dkr.ecr.{REGION}.amazonaws.com/sagemaker-scikit-learn:1.0-1-cpu-py3",
                        "TrainingInputMode": "File"
                    },
                    "InputDataConfig": [
                        {
                            "ChannelName": "train",
                            "DataSource": {
                                "S3DataSource": {
                                    "S3DataType": "S3Prefix",
                                    "S3Uri": f"s3://{BUCKET}/processed/train",
                                    "S3DataDistributionType": "FullyReplicated"
                                }
                            }
                        }
                    ],
                    "OutputDataConfig": {
                        "S3OutputPath": f"s3://{BUCKET}/model-output/"
                    },
                    "ResourceConfig": {
                        "InstanceType": "ml.t3.medium",
                        "InstanceCount": 1,
                        "VolumeSizeInGB": 10
                    },
                    "RoleArn": ROLE_ARN,
                    "StoppingCondition": {
                        "MaxRuntimeInSeconds": 3600
                    }
                }
            },
            {
                "Name": "EvaluateLoanModel",
                "Type": "Processing",
                "Arguments": {
                    "ProcessingResources": {
                        "ClusterConfig": {
                            "InstanceType": "ml.t3.medium",
                            "InstanceCount": 1,
                            "VolumeSizeInGB": 10
                        }
                    },
                    "AppSpecification": {
                        "ImageUri": f"683313688378.dkr.ecr.{REGION}.amazonaws.com/sagemaker-scikit-learn:1.0-1-cpu-py3",
                        "ContainerEntrypoint": ["python3", "/opt/ml/processing/input/code/evaluate.py"]
                    },
                    "ProcessingInputs": [
                        {
                            "InputName": "model",
                            "AppManaged": False,
                            "S3Input": {
                                "S3Uri": f"s3://{BUCKET}/model-output/",
                                "LocalPath": "/opt/ml/processing/model",
                                "S3DataType": "S3Prefix",
                                "S3InputMode": "File"
                            }
                        },
                        {
                            "InputName": "test",
                            "AppManaged": False,
                            "S3Input": {
                                "S3Uri": f"s3://{BUCKET}/processed/test",
                                "LocalPath": "/opt/ml/processing/test",
                                "S3DataType": "S3Prefix",
                                "S3InputMode": "File"
                            }
                        },
                        {
                            "InputName": "code",
                            "AppManaged": False,
                            "S3Input": {
                                "S3Uri": f"s3://{BUCKET}/code/",
                                "LocalPath": "/opt/ml/processing/input/code",
                                "S3DataType": "S3Prefix",
                                "S3InputMode": "File"
                            }
                        }
                    ],
                    "ProcessingOutputs": [
                        {
                            "OutputName": "evaluation",
                            "AppManaged": False,
                            "S3Output": {
                                "S3Uri": f"s3://{BUCKET}/evaluation",
                                "LocalPath": "/opt/ml/processing/evaluation",
                                "S3UploadMode": "EndOfJob"
                            }
                        }
                    ],
                    "RoleArn": ROLE_ARN
                }
            }
        ]
    }
    
    try:
        # Create or update pipeline
        pipeline_name = "loan-model-pipeline"
        
        try:
            # Try to update existing pipeline
            response = sagemaker.update_pipeline(
                PipelineName=pipeline_name,
                PipelineDefinition=json.dumps(pipeline_definition),
                RoleArn=ROLE_ARN
            )
            print(f"✅ Pipeline updated: {pipeline_name}")
        except sagemaker.exceptions.ResourceNotFound:
            # Create new pipeline if it doesn't exist
            response = sagemaker.create_pipeline(
                PipelineName=pipeline_name,
                PipelineDefinition=json.dumps(pipeline_definition),
                RoleArn=ROLE_ARN
            )
            print(f"✅ Pipeline created: {pipeline_name}")
        
        return pipeline_name
        
    except Exception as e:
        print(f"❌ Error creating pipeline: {e}")
        return None

if __name__ == "__main__":
    pipeline_name = create_sagemaker_pipeline()
    if pipeline_name:
        print("✅ SageMaker Pipeline created successfully!")
    else:
        print("❌ Failed to create SageMaker Pipeline")