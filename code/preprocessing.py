import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import argparse
import os
import boto3

def preprocess_data():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-data', type=str, default='/opt/ml/processing/input')
    parser.add_argument('--output-train', type=str, default='/opt/ml/processing/train')
    parser.add_argument('--output-test', type=str, default='/opt/ml/processing/test')
    
    args = parser.parse_args()
    
    # Read data from S3 input
    df = pd.read_csv(f"{args.input_data}/data.csv")
    
    # Feature engineering
    df['education'] = df['education'].map({'Graduate': 0, 'Not Graduate': 1})
    df['self_employed'] = df['self_employed'].map({'No': 0, 'Yes': 1})
    
    # Log transform
    df['income_annum'] = np.log(df['income_annum'])
    df['loan_amount'] = np.log(df['loan_amount'])
    df['total_asset'] = np.log(df['total_asset'])
    
    # Split features and target
    X = df.drop('loan_status', axis=1)
    y = df['loan_status']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Save processed data
    train_data = pd.concat([X_train, y_train], axis=1)
    test_data = pd.concat([X_test, y_test], axis=1)
    
    train_data.to_csv(f"{args.output_train}/train.csv", index=False)
    test_data.to_csv(f"{args.output_test}/test.csv", index=False)
    
    print("✅ Data preprocessing completed")

if __name__ == "__main__":
    preprocess_data()