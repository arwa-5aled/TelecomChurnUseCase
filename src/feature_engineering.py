import pandas as pd

def generate_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate features for a DataFrame of customer data.
    Works for single-row or multi-row DataFrames.

    """
    ''' 
    def fill_tenure(row):
        if 'tenure' in row and pd.notna(row['tenure']):
            return row['tenure']
        elif 'Monthly_Charges' in row and 'Total_Charges' in row and \
            pd.notna(row['Monthly_Charges']) and pd.notna(row['Total_Charges']) and \
            row['Monthly_Charges'] != 0:
            return row['Total_Charges'] / row['Monthly_Charges']
        else:
            return None  # can't compute tenure

    if {'tenure', 'Monthly_Charges', 'Total_Charges'}.issubset(df.columns):
     df['tenure'] = df.apply(fill_tenure, axis=1)

    def fill_service_dependencies(row):
    # Internet-dependent features
        internet_features = [
            "Streaming_TV",
            "Streaming_Movies",
            "Online_Backup",
            "Device_Protection",
            "Tech_Support",
            "Online_Security"
        ]
        if row.get("Internet_Service") == "No":
            for feature in internet_features:
                if pd.isna(row.get(feature)):
                    row[feature] = "No internet service"
        
        # Phone-dependent feature
        if row.get("Phone_Service") == "No":
            if pd.isna(row.get("Dual")):
                row["Dual"] = "No phone service"
    df = df.apply(fill_service_dependencies, axis=1)
    ''' 
    if {'Total_Charges', 'Monthly_Charges', 'tenure'}.issubset(df.columns):
    # Only fill tenure where it's missing
        missing_tenure_mask = df['tenure'].isna()  # True where tenure is NaN
        df.loc[missing_tenure_mask & df['Monthly_Charges'].notna() & df['Total_Charges'].notna() & (df['Monthly_Charges'] != 0), 'tenure'] = \
            df['Total_Charges'] / df['Monthly_Charges']
    # Internet- and Phone-dependent features logic
    def fill_service_dependencies(row):
        # Internet-dependent features
        internet_features = [
            "Streaming_TV",
            "Streaming_Movies",
            "Online_Backup",
            "Device_Protection",
            "Tech_Support",
            "Online_Security"
        ]
        # If Internet_Service is "No" OR any internet-dependent feature is missing, set all to "No internet service"
        if row.get("Internet_Service") == "No" or any(pd.isna(row.get(f)) for f in internet_features):
            row["Internet_Service"] = "No"
            for feature in internet_features:
                row[feature] = "No internet service"
        
        # Phone-dependent feature
        if row.get("Phone_Service") == "No" or pd.isna(row.get("Dual")):
            row["Dual"] = "No phone service"
        
        return row

    # Apply this row-wise to the dataframe
    df = df.apply(fill_service_dependencies, axis=1)

    # tenure groups
    if 'tenure' in df.columns:
        df['tenure_group'] = pd.cut(
            df['tenure'],
            bins=[0, 12, 24, 48, 60, 72],
            labels=['0-12', '13-24', '25-48', '49-60', '61-72'],
            include_lowest=True
        )

    # average monthly spend
    if {'Total_Charges', 'tenure'}.issubset(df.columns):
        df['avg_monthly_spend'] = df.apply(
            lambda row: row['Total_Charges'] / row['tenure'] if row['tenure'] > 0 else 0,
            axis=1
        )

    # number of services
    service_columns = [
        'Phone_Service', 'Internet_Service', 'Online_Security', 'Online_Backup',
        'Device_Protection', 'Tech_Support', 'Streaming_TV', 'Streaming_Movies'
    ]
    if all(col in df.columns for col in service_columns):
        df['Num_Services'] = df[service_columns].apply(lambda row: sum(row == 'Yes'), axis=1)

    # monthly/total ratio
    if {'Monthly_Charges', 'Total_Charges'}.issubset(df.columns):
        df['Monthly_to_Total_Ratio'] = df.apply(
            lambda row: row['Monthly_Charges'] / row['Total_Charges'] if row['Total_Charges'] > 0 else 0,
            axis=1
        )

    # automatic payment flag
    if 'Payment_Method' in df.columns:
        df['Automatic_Payment'] = df['Payment_Method'].isin(
            ['Bank transfer (automatic)', 'Credit card (automatic)']
        ).astype(int)

    # no internet flag
    if 'Internet_Service' in df.columns:
        df['No_Internet'] = (df['Internet_Service'] == 'No').astype(int)

    # any streaming flag
    if {'Streaming_TV', 'Streaming_Movies'}.issubset(df.columns):
        df['Any_Streaming'] = ((df['Streaming_TV'] == 'Yes') | (df['Streaming_Movies'] == 'Yes')).astype(int)

    # family type
    if {'Is_Married', 'Dependents'}.issubset(df.columns):
        def family_type(row):
            if row['Is_Married'] == 'No' and row['Dependents'] == 'No':
                return 'Single'
            elif row['Is_Married'] == 'Yes' and row['Dependents'] == 'No':
                return 'Married_No_Children'
            elif row['Is_Married'] == 'Yes' and row['Dependents'] == 'Yes':
                return 'Married_With_Children'
            elif row['Is_Married'] == 'No' and row['Dependents'] == 'Yes':
                return 'Single_With_Children'
            return 'Unknown'
        df['Family_Type'] = df.apply(family_type, axis=1)

    # contract tenure risk
    if {'Contract', 'tenure'}.issubset(df.columns):
        def contract_risk(row):
            if row['Contract'] == 'Month-to-month' and row['tenure'] <= 12:
                return "HighRisk"
            elif row['Contract'] == 'Month-to-month' and row['tenure'] > 12:
                return "MediumRisk"
            return "LowRisk"
        df['Contract_Tenure_Risk'] = df.apply(contract_risk, axis=1)

    return df
