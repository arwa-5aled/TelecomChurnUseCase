from model import classify_customer

sample_row = {
    "customerID": "7590-VHVEG",
    "gender": "Male",
    "Senior_Citizen": 0,   # note the trailing space
    "Is_Married": "No",
    "Dependents": "Yes",
    "tenure": 72,
    "Phone_Service": "Yes",
    "Dual": "No",
    "Internet_Service": "No internet service",
    "Online_Security": None,
    "Online_Backup": None,
    "Device_Protection": "no internet service",
    "Tech_Support": "no internet service",
    "Streaming_TV": "no internet service",
    "Streaming_Movies": "no internet service",
    "Contract": "One year",
    "Paperless_Billing": "No",
    "Payment_Method": "Bank transfer (automatic)",
    "Monthly_Charges": 56.15,
    "Total_Charges": 3487.95
}

result = classify_customer(sample_row)
print(result)
