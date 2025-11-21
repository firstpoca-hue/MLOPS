import joblib
import pandas as pd
import numpy as np
import json
import os

def model_fn(model_dir):
    """Load model from the model_dir"""
    model = joblib.load(os.path.join(model_dir, "model.pkl"))
    return model

def input_fn(request_body, request_content_type):
    """Parse input data for predictions"""
    if request_content_type == 'application/json':
        input_data = json.loads(request_body)
        return pd.DataFrame([input_data])
    else:
        raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    """Make predictions using the loaded model"""
    prediction = model.predict(input_data)
    return prediction

def output_fn(prediction, content_type):
    """Format the output"""
    if content_type == 'application/json':
        result = {"prediction": int(prediction[0])}
        return json.dumps(result)
    else:
        raise ValueError(f"Unsupported content type: {content_type}")