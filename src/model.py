import pandas as pd
import joblib
import numpy as np
from feature_engineering import generate_features   # relative import (if inside same package)

model = joblib.load("../models/lr_pipeline.pkl")

def get_customer_factors(input_df, pipeline):
    clf = pipeline.named_steps['classifier']
    pre = pipeline.named_steps['preprocessor']
    X_proc = pre.transform(input_df)
    coefs = clf.coef_[0]
    feature_names = pre.get_feature_names_out()

    contributions = X_proc[0] * coefs
    top_idx = np.argsort(np.abs(contributions))[::-1][:5]
    return [(feature_names[i], contributions[i]) for i in top_idx]

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

    factors = get_customer_factors(input_df, model)
    customer_id = input_df["customerID"].iloc[0]
    input_df = input_df.drop(columns=["customerID"])
    input_df = input_df.replace({None: np.nan})
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0, 1]
    reasons = [
        f"{feat} {'↑' if val > 0 else '↓'} (impact={round(val, 3)})"
        for feat, val in factors
    ]
    


    return {
        "Customer_ID": str(customer_id) ,
        "prediction": int(prediction),
        "Reasons": reasons
    }
