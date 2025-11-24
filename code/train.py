import pandas as pd
import joblib
import os
import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import numpy as np

def train():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    
    args = parser.parse_args()
    
    # Read training data
    input_path = '/opt/ml/input/data/training'
    files = os.listdir(input_path)
    data_file = [f for f in files if f.endswith('.csv')][0]
    
    df = pd.read_csv(os.path.join(input_path, data_file))
    
    # Feature engineering
    df['education'] = df['education'].map({'Graduate': 0, 'Not Graduate': 1})
    df['self_employed'] = df['self_employed'].map({'No': 0, 'Yes': 1})
    
    # Log transform numerical features
    df['income_annum'] = np.log(df['income_annum'] + 1)
    df['loan_amount'] = np.log(df['loan_amount'] + 1)
    df['total_asset'] = np.log(df['total_asset'] + 1)
    
    # Split features and target
    X = df.drop('loan_status', axis=1)
    y = df['loan_status']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    # Save model
    joblib.dump(model, os.path.join(args.model_dir, 'model.pkl'))
    
    # Copy inference script to model directory
    import shutil
    inference_source = '/opt/ml/input/data/training/inference.py'
    if os.path.exists(inference_source):
        shutil.copy(inference_source, os.path.join(args.model_dir, 'inference.py'))
        print("Inference script included")
    else:
        # Create basic inference script if not found
        inference_code = '''import joblib
import pandas as pd
import json
import os

def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "model.pkl"))
    return model

def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        input_data = json.loads(request_body)
        return pd.DataFrame([input_data])
    else:
        raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    prediction = model.predict(input_data)
    return prediction

def output_fn(prediction, content_type):
    if content_type == 'application/json':
        result = {"prediction": int(prediction[0])}
        return json.dumps(result)
    else:
        raise ValueError(f"Unsupported content type: {content_type}")
'''
        with open(os.path.join(args.model_dir, 'inference.py'), 'w') as f:
            f.write(inference_code)
        print("Basic inference script created")
    
    print("Model saved successfully")

if __name__ == '__main__':
    train()