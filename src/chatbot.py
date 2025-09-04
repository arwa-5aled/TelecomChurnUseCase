import os
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
import importlib
import model
importlib.reload(model)

from model import classify_customer

import json

# Load query from JSON file instead of hardcoding
with open("customer.json", "r") as f:
    data = json.load(f)





system_prompt = f"""
You are a customer churn prediction assistant.
Extract customer features in the exact format:

customerID: string, use "unknown" if not provided
gender: "Male" or "Female"
Senior_Citizen : 0 or 1
Is_Married: "Yes" or "No"
Dependents: "Yes" or "No"
tenure: integer
Phone_Service: "Yes" or "No"
Dual: "Yes" or "No"
Internet_Service: "DSL", "Fiber optic", or "No"
Online_Security: "Yes" or "No"
Online_Backup: "Yes" or "No"
Device_Protection: "Yes" or "No"
Tech_Support: "Yes" or "No"
Streaming_TV: "Yes" or "No"
Streaming_Movies: "Yes" or "No"
Contract: "Month-to-month", "One year", "Two year"
Paperless_Billing: "Yes" or "No"
Payment_Method: "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
Monthly_Charges: float
Total_Charges: float

Return ONLY a Python dictionary with these exact keys:
customerID, gender, Senior_Citizen , Is_Married, Dependents,
tenure, Phone_Service, Dual, Internet_Service, Online_Security,
Online_Backup, Device_Protection, Tech_Support, Streaming_TV,
Streaming_Movies, Contract, Paperless_Billing, Payment_Method,
Monthly_Charges, Total_Charges

- Fill missing features with None (or leave missing if you want NaN) except customerID fill it with unKnown .
- Do NOT add explanations or text outside the dictionary. 
- Use this format: 
{{{{"customerID": "unknown", "gender": "Female", "Senior_Citizen ": 0, ...}}}}

"""

# human_prompt= "I have a female customer  , 45 years old, married, no dependents, no internet Service, has phone service, monthly charges 75, total charges 1200 , Paperless_Billing yes, contract month to month, payment method is electronic check, tenure 16 months, no online security, no online backup, no device protection, no tech support, no streaming TV, no streaming movies. What are her features?"
human_prompt = data.get("query", "")
chat_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{customer_paragraph}")
])

# --- Format the prompt with the human input ---
final_prompt = chat_template.format_messages(customer_paragraph=human_prompt)
llm = ChatOllama(model="gemma3")
response = llm(final_prompt)

import json
import re
import ast

def debug_and_convert_llm_output(llm_string):
    """
    Debug and convert LLM output to dictionary with detailed error handling
    """
    
    print("="*50)
    print("DEBUGGING LLM OUTPUT")
    print("="*50)
    
    # Step 1: Check what we received
    print(f"Raw output type: {type(llm_string)}")
    print(f"Raw output length: {len(llm_string) if llm_string else 0}")
    print(f"Raw output (first 200 chars): {repr(llm_string[:200])}")
    
    if not llm_string or len(llm_string.strip()) == 0:
        print("ERROR: Empty or None input!")
        return None
    
    # Step 2: Clean the string
    cleaned = llm_string.strip()
    
    # Step 3: Try to extract JSON from the response
    # Look for JSON-like patterns (starts with { and ends with })
    json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
    
    if json_match:
        json_candidate = json_match.group(0)
        print(f"\nFound JSON-like content: {json_candidate[:100]}...")
    else:
        print(f"\nNo JSON pattern found. Full content:\n{cleaned}")
        # Try to find any dictionary-like content
        dict_patterns = [
            r'```python\s*(\{.*?\})\s*```',  # Python code blocks
            r'```json\s*(\{.*?\})\s*```',    # JSON code blocks  
            r'```\s*(\{.*?\})\s*```',        # Generic code blocks
        ]
        
        for pattern in dict_patterns:
            match = re.search(pattern, cleaned, re.DOTALL)
            if match:
                json_candidate = match.group(1)
                print(f"Found content in code block: {json_candidate[:100]}...")
                break
        else:
            return None
    
    # Step 4: Try different conversion methods
    conversion_methods = [
        ("JSON with None->null replacement", lambda x: json.loads(x.replace('None', 'null').replace('True', 'true').replace('False', 'false'))),
        ("AST literal eval", ast.literal_eval),
        ("JSON direct", json.loads),
        ("Eval (unsafe)", eval),
    ]
    
    for method_name, method_func in conversion_methods:
        try:
            print(f"\nTrying method: {method_name}")
            result = method_func(json_candidate)
            print(f"✅ SUCCESS with {method_name}")
            print(f"Result type: {type(result)}")
            print(f"Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            return result
        except Exception as e:
            print(f"❌ Failed with {method_name}: {str(e)}")
    
    return None

def robust_llm_to_dict(llm_string):
    """
    More robust conversion function
    """
    if not llm_string:
        return None
    
    # Clean the input
    cleaned = str(llm_string).strip()
    
    # Extract JSON-like content
    patterns = [
        r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Simple nested braces
        r'\{.*\}',  # Any content between braces
    ]
    
    json_content = None
    for pattern in patterns:
        matches = re.findall(pattern, cleaned, re.DOTALL)
        if matches:
            # Take the longest match (likely the most complete)
            json_content = max(matches, key=len)
            break
    
    if not json_content:
        return None
    
    # Try conversion methods in order of preference
    methods = [
        lambda x: json.loads(re.sub(r'\b(None|True|False)\b', 
                                   lambda m: {'None': 'null', 'True': 'true', 'False': 'false'}[m.group()], x)),
        ast.literal_eval,
    ]
    
    for method in methods:
        try:
            result = method(json_content)
            if isinstance(result, dict):
                return result
        except:
            continue
    
    return None

# Test with your actual response
# Replace this with your actual response.content
response = response.content

print("TESTING WITH SAMPLE DATA:")
result = debug_and_convert_llm_output(response)
if result:
    print(f"\n✅ Final result: {result}")
else:
    print("\n❌ Could not convert to dictionary")
import sys
import os

# Add the source folder to sys.path
sys.path.append(os.path.abspath('../src'))

# Now you can import functions from model.py
from model import classify_customer

final_result = classify_customer(result)

def build_marketing_prompt(output: dict) -> str:
    pred = "will churn" if output["prediction"] == 1 else "will stay"
  
    
    reasons = "\n".join([f"- {r}" for r in output["Reasons"]])
    
    return f"""
You are a customer success advisor. 
The model predicts that this customer {pred} .

Here are the technical factors:
{reasons}

Now explain to a marketing team in very natural business language:
- Why the customer is likely to {pred}
- What the key reasons are, phrased in everyday terms
- Keep the explanation clear, short, and actionable
"""
system_prompt_response = (
    "You are a helpful assistant that explains customer churn predictions "
    "in plain, natural language for a marketing team."
)

# Use the marketing-friendly prompt builder instead of the old one
human_prompt_response = build_marketing_prompt(final_result)

chat_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt_response),
    ("human", "{customer_paragraph}")
])

final_reason_prompt = chat_template.format_messages(
    customer_paragraph=human_prompt_response
)

llm = ChatOllama(model="gemma3")
reasons = llm(final_reason_prompt)
print(reasons.content)


