import pandas as pd
import joblib
import os
import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import numpy as np

def format_raw_data(raw_file):
    """Format messy CSV data into clean structure"""
    formatted_data = []
    
    with open(raw_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        parts = [part.strip() for part in line.strip().split(',')]
        
        if len(parts) < 12:
            continue
            
        try:
            formatted_data.append({
                'loan_id': int(parts[0]),
                'no_of_dependents': int(parts[1]),
                'education': parts[2].strip(),
                'self_employed': parts[3].strip(),
                'income_annum': int(parts[4]),
                'loan_amount': int(parts[5]),
                'loan_term': int(parts[6]),
                'credit_score': int(parts[7]),
                'residential_assets_value': int(parts[8]),
                'commercial_assets_value': int(parts[9]),
                'luxury_assets_value': int(parts[10]),
                'bank_asset_value': int(parts[11]),
                'loan_status': parts[12].strip()
            })
        except (ValueError, IndexError):
            continue
    
    return pd.DataFrame(formatted_data)

def train():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    
    args = parser.parse_args()
    
    # Read training data
    input_path = '/opt/ml/input/data/training'
    files = os.listdir(input_path)
    data_file = [f for f in files if f.endswith('.csv')][0]
    
    # Try to format raw data if needed
    file_path = os.path.join(input_path, data_file)
    try:
        df = pd.read_csv(file_path)
        # Check if data needs formatting
        if 'loan_id' not in df.columns:
            df = format_raw_data(file_path)
    except:
        df = format_raw_data(file_path)
    
    print(f"Training with {len(df)} records")
    
    # Feature engineering
    df['education'] = df['education'].map({'Graduate': 0, 'Not Graduate': 1})
    df['self_employed'] = df['self_employed'].map({'No': 0, 'Yes': 1})
    df['loan_status'] = df['loan_status'].map({'Approved': 1, 'Rejected': 0})
    
    # Calculate total assets
    df['total_assets'] = (df['residential_assets_value'] + 
                         df['commercial_assets_value'] + 
                         df['luxury_assets_value'] + 
                         df['bank_asset_value'])
    
    # Log transform numerical features
    numerical_cols = ['income_annum', 'loan_amount', 'total_assets']
    for col in numerical_cols:
        df[col] = np.log(np.abs(df[col]) + 1)
    
    # Select features
    feature_cols = ['no_of_dependents', 'education', 'self_employed', 'income_annum', 
                   'loan_amount', 'loan_term', 'credit_score', 'total_assets']
    
    X = df[feature_cols]
    y = df['loan_status']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = LogisticRegression(random_state=42, max_iter=1000)
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