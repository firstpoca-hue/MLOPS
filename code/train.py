import pandas as pd
import joblib
import os
import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

def train_model():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))
    parser.add_argument('--test', type=str, default=os.environ.get('SM_CHANNEL_TEST'))
    
    args = parser.parse_args()
    
    # Load training data
    train_df = pd.read_csv(f"{args.train}/train.csv")
    test_df = pd.read_csv(f"{args.test}/test.csv")
    
    # Prepare features and target
    X_train = train_df.drop('loan_status', axis=1)
    y_train = train_df['loan_status']
    X_test = test_df.drop('loan_status', axis=1)
    y_test = test_df['loan_status']
    
    # Train model
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    # Save model
    joblib.dump(model, f"{args.model_dir}/model.pkl")
    print("✅ Model training completed")

if __name__ == "__main__":
    train_model()