from fastapi import FastAPI
import joblib
import pandas as pd
from feature_engineering import generate_features

# Load pipeline
model = joblib.load("../models/xgb_pipeline.pkl")

app = FastAPI()

@app.post("/predict/")
def predict_customer(data: dict):
    input_df = pd.DataFrame([data]) 
    
    processed_df = generate_features(input_df)

    prediction = model.predict(processed_df)[0]
    probability = model.predict_proba(processed_df)[0,1]

    return {
        "prediction": int(prediction),
        "probability": float(probability)
    }
