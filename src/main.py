from fastapi import FastAPI
from pydantic import BaseModel
import json
import subprocess


app = FastAPI()

# Define the input format for the API
class CustomerQuery(BaseModel):
    query: str

@app.post("/predict")
def predict_customer(query: CustomerQuery):
    # Step 1: Save the query to customer.json so chatbot.py can use it
    with open("customer.json", "w") as f:
        json.dump({"query": query.query}, f)

    # Step 2: Run chatbot.py as a subprocess
    result = subprocess.run(
        ["python", "chatbot.py"],
        capture_output=True,
        text=True
    )

    # Step 3: Extract chatbot.py's output
    if result.returncode != 0:
        return {"error": "chatbot.py failed", "details": result.stderr}

    output_lines = result.stdout.strip().splitlines()
    final_response = output_lines[-1] if output_lines else "No output from chatbot.py"

    return {"response": final_response}
