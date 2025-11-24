import boto3
import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.workflow.model_step import ModelStep
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo
from sagemaker.workflow.properties import PropertyFile
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.model import Model
from sagemaker.workflow.parameters import ParameterString
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.inputs import TrainingInput

# Configuration
REGION = "eu-central-1"
ROLE_ARN = "arn:aws:iam::361509912577:role/SageMakerExecutionRole"
BUCKET = "teamars"

def create_pipeline():
    # Parameters
    input_data = ParameterString(
        name="InputDataUrl",
        default_value=f"s3://{BUCKET}/data/"
    )
    
    # Processing step
    sklearn_processor = SKLearnProcessor(
        framework_version="1.0-1",
        role=ROLE_ARN,
        instance_type="ml.t3.medium",
        instance_count=1,
    )
    
    processing_step = ProcessingStep(
        name="PreprocessLoanData",
        processor=sklearn_processor,
        inputs=[
            ProcessingInput(
                source=input_data,
                destination="/opt/ml/processing/input"
            )
        ],
        outputs=[
            ProcessingOutput(
                output_name="train",
                source="/opt/ml/processing/train",
                destination=f"s3://{BUCKET}/processed/train"
            ),
            ProcessingOutput(
                output_name="test",
                source="/opt/ml/processing/test",
                destination=f"s3://{BUCKET}/processed/test"
            )
        ],
        code="code/preprocessing.py"
    )
    
    # Training step
    sklearn_estimator = SKLearn(
        entry_point="train.py",
        source_dir="code",
        framework_version="1.0-1",
        instance_type="ml.t3.medium",
        role=ROLE_ARN,
    )
    
    training_step = TrainingStep(
        name="TrainLoanModel",
        estimator=sklearn_estimator,
        inputs={
            "train": TrainingInput(
                s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri
            ),
            "test": TrainingInput(
                s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["test"].S3Output.S3Uri
            )
        }
    )
    
    # Evaluation step
    evaluation_processor = SKLearnProcessor(
        framework_version="1.0-1",
        role=ROLE_ARN,
        instance_type="ml.t3.medium",
        instance_count=1,
    )
    
    evaluation_report = PropertyFile(
        name="EvaluationReport",
        output_name="evaluation",
        path="evaluation.json"
    )
    
    evaluation_step = ProcessingStep(
        name="EvaluateLoanModel",
        processor=evaluation_processor,
        inputs=[
            ProcessingInput(
                source=training_step.properties.ModelArtifacts.S3ModelArtifacts,
                destination="/opt/ml/processing/model"
            ),
            ProcessingInput(
                source=processing_step.properties.ProcessingOutputConfig.Outputs["test"].S3Output.S3Uri,
                destination="/opt/ml/processing/test"
            )
        ],
        outputs=[
            ProcessingOutput(
                output_name="evaluation",
                source="/opt/ml/processing/evaluation",
                destination=f"s3://{BUCKET}/evaluation"
            )
        ],
        code="code/evaluate.py",
        property_files=[evaluation_report]
    )
    
    # Model registration with automatic approval
    model = Model(
        image_uri=f"361509912577.dkr.ecr.{REGION}.amazonaws.com/sagemaker-scikit-learn:1.0-1-cpu-py3",
        model_data=training_step.properties.ModelArtifacts.S3ModelArtifacts,
        role=ROLE_ARN,
    )
    
    model_step_approved = ModelStep(
        name="RegisterApprovedLoanModel",
        step_args=model.register(
            content_types=["application/json"],
            response_types=["application/json"],
            inference_instances=["ml.t2.medium"],
            transform_instances=["ml.t2.medium"],
            model_package_group_name="loan-model-package-group",
            approval_status="Approved",
        ),
    )
    
    model_step_pending = ModelStep(
        name="RegisterPendingLoanModel",
        step_args=model.register(
            content_types=["application/json"],
            response_types=["application/json"],
            inference_instances=["ml.t2.medium"],
            transform_instances=["ml.t2.medium"],
            model_package_group_name="loan-model-package-group",
            approval_status="PendingManualApproval",
        ),
    )
    
    # Condition for automatic approval
    cond_gte = ConditionGreaterThanOrEqualTo(
        left=evaluation_report.get("approved"),
        right=True
    )
    
    condition_step = ConditionStep(
        name="CheckModelApproval",
        conditions=[cond_gte],
        if_steps=[model_step_approved],
        else_steps=[model_step_pending]
    )
    
    # Create pipeline
    sagemaker_session = sagemaker.Session()
    pipeline = Pipeline(
        name="loan-model-pipeline",
        parameters=[input_data],
        steps=[processing_step, training_step, evaluation_step, condition_step],
        sagemaker_session=sagemaker_session
    )
    
    return pipeline

if __name__ == "__main__":
    pipeline = create_pipeline()
    pipeline.upsert(role_arn=ROLE_ARN)
    print("✅ SageMaker Pipeline created successfully!")