import requests

url = "http://127.0.0.1:8000/predict"
data = {
    "query": "I have a female customer  , 45 years old, married, no dependents, no internet Service, has phone service, monthly charges 75, total charges 1200 , Paperless_Billing yes, contract month to month, payment method is electronic check, tenure 16 months, no online security, no online backup, no device protection, no tech support, no streaming TV, no streaming movies. What are her features?"

}

response = requests.post(url, json=data)
print(response.json())
