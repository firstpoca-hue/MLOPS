# Eraser.io Prompts for MLOps Architecture Diagrams

## Prompt 1: High-Level Architecture Diagram

```
Create a cloud architecture diagram for an MLOps loan prediction pipeline with the following components:

**GitHub Repository** (top-left):
- Contains: data.csv, ML code, Terraform modules, GitHub Actions workflows
- Icon: GitHub logo
- Color: Black/Gray

**GitHub Actions** (connected to GitHub):
- Two workflows: "Deploy Infrastructure" and "Trigger ML Pipeline"
- Icon: GitHub Actions logo
- Color: Blue
- Arrows: Bidirectional to GitHub repo

**AWS Cloud** (large container encompassing AWS services):
- Background: Light blue/AWS orange

**Inside AWS Cloud:**

**S3 Buckets** (left side):
- "teamars" bucket for ML artifacts
- "teamars-pipeline-artifacts" for CI/CD
- Icon: S3 bucket
- Color: Green

**IAM Roles** (top-right):
- SageMakerExecutionRole
- CodeBuildRole  
- CodePipelineRole
- Icon: IAM shield
- Color: Red

**CodePipeline** (center):
- Source → Build stages
- Icon: CodePipeline
- Color: Purple
- Arrow from GitHub Actions

**CodeBuild** (connected to CodePipeline):
- Executes buildspec.yml
- Icon: CodeBuild
- Color: Orange
- Arrow to SageMaker

**SageMaker Pipeline** (right side):
- Steps: Preprocess → Train → Evaluate → Register
- Icon: SageMaker
- Color: Orange
- Connected to S3 and Model Registry

**Model Registry** (bottom-right):
- Approved/Pending models
- Icon: Database
- Color: Purple

**SageMaker Endpoint** (bottom):
- Real-time inference
- Icon: Endpoint
- Color: Green
- Arrow from Model Registry

**Data Flow Arrows:**
- GitHub → GitHub Actions → CodePipeline → CodeBuild → SageMaker Pipeline
- S3 ↔ SageMaker Pipeline
- SageMaker Pipeline → Model Registry → Endpoint
- data.csv flow: GitHub → S3 → SageMaker

**Labels:**
- Add service names under each component
- Include "Terraform Managed" label for AWS resources
- Add "Automated" labels on workflow arrows
```

## Prompt 2: Detailed Workflow Diagram

```
Create a detailed workflow diagram for MLOps pipeline execution with the following process:

**Trigger Event** (top):
- "Developer pushes data.csv to GitHub"
- Shape: Oval
- Color: Light blue

**GitHub Actions Workflow** (sequential steps):
1. "Detect data.csv changes"
2. "Upload data to S3"
3. "Create/Update SageMaker Pipeline"
4. "Execute SageMaker Pipeline"
- Shape: Rectangles
- Color: Blue
- Arrows: Downward flow

**SageMaker Pipeline Steps** (parallel/sequential):
1. **Preprocessing Step**:
   - Input: S3 data
   - Process: Feature engineering, train/test split
   - Output: Processed data to S3
   - Shape: Rectangle
   - Color: Orange

2. **Training Step**:
   - Input: Processed training data
   - Process: LogisticRegression training
   - Output: Model artifacts
   - Shape: Rectangle
   - Color: Orange

3. **Evaluation Step**:
   - Input: Model + test data
   - Process: Calculate accuracy, F1 score
   - Output: Evaluation metrics
   - Shape: Rectangle
   - Color: Orange

**Decision Point** (diamond shape):
- "Accuracy ≥ 0.7 AND F1 ≥ 0.7?"
- Color: Yellow
- Two paths: Yes/No

**Approval Paths**:
- **Yes Path**: "Auto-approve model" → "Register as Approved"
- **No Path**: "Pending manual approval" → "Register as Pending"
- Shapes: Rectangles
- Colors: Green (approved), Red (pending)

**Deployment Step**:
- "Deploy approved model to endpoint"
- Shape: Rectangle
- Color: Green
- Arrow from approved models only

**End States**:
- "Model deployed and ready for inference"
- "Model pending manual review"
- Shape: Ovals
- Colors: Green/Orange

**Additional Elements:**
- Time indicators (e.g., "~5 minutes", "~10 minutes")
- Data flow arrows with labels
- Error handling paths (dotted lines)
- Monitoring/logging connections (dashed lines)
- Legend explaining shapes and colors
```

## Prompt 3: Infrastructure Components Diagram

```
Create a Terraform infrastructure diagram showing modular components:

**Terraform Modules** (organized in grid layout):

**S3 Module** (top-left):
- Components: ML bucket, Pipeline artifacts bucket
- Versioning enabled
- Icon: S3
- Color: Green

**IAM Module** (top-right):
- Components: SageMaker role, CodeBuild role, CodePipeline role
- Policies attached
- Icon: IAM shield
- Color: Red

**CodeBuild Module** (bottom-left):
- Components: Build project, Environment config
- Buildspec.yml reference
- Icon: CodeBuild
- Color: Orange

**CodePipeline Module** (bottom-right):
- Components: Pipeline, Source/Build stages
- GitHub integration
- Icon: CodePipeline
- Color: Purple

**Connections:**
- IAM → All other modules (permissions)
- S3 → CodeBuild (artifact storage)
- S3 → CodePipeline (artifact storage)
- CodePipeline → CodeBuild (trigger)

**External Dependencies:**
- GitHub repository (outside Terraform)
- SageMaker services (managed separately)

**Labels:**
- Module names
- Resource types
- Dependency arrows
- "Terraform Managed" boundary
```

## Usage Instructions for Eraser.io

1. **Copy any prompt above**
2. **Go to eraser.io**
3. **Paste the prompt in the AI diagram generator**
4. **Customize colors, shapes, and layout as needed**
5. **Export as PNG/SVG for documentation**

## Customization Tips

- **Colors**: Use AWS brand colors (orange, blue, gray)
- **Icons**: Use official AWS service icons when available
- **Layout**: Left-to-right or top-to-bottom flow
- **Labels**: Keep text concise and readable
- **Arrows**: Use different styles for different data types (solid, dashed, dotted)