import pandas as pd
import joblib
from feature_engineering import generate_features   # relative import (if inside same package)

model = joblib.load("../models/lr_pipeline.pkl")

def classify_customer(raw_data: dict):
    """
    Entry function for customer churn classification.

    Parameters
    ----------
    raw_data : dict
        Dictionary containing raw customer data.

    Returns
    -------
    dict : prediction results
    """
    input_df = pd.DataFrame([raw_data])

    input_df = generate_features(input_df)

    customer_id = input_df["customerID"].iloc[0]
    input_df = input_df.drop(columns=["customerID"])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0, 1]

    return {
        "Customer_ID": str(customer_id) ,
        "prediction": int(prediction),
        "probability": float(probability)
    }
