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
    print("Model saved successfully")

if __name__ == '__main__':
    train()