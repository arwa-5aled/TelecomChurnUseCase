

 Telecom Churn Use Case
📂 Project Description

This project demonstrates a churn prediction use case in the telecom industry.
It combines:

* Data preprocessing & feature engineering
* Model training and evaluation
* A chatbot interface to interact with the churn prediction model
* API endpoints for integration

The main goal is to predict whether a customer is likely to churn and allow users to query predictions through a chatbot.

---

⚙️ Installation & Setup


# Clone the repository
git clone https://github.com/username/telecom-churn-use-case.git

# Navigate to project folder
cd telecom-churn-use-case

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt


---

▶️ How to Run
Run chatbot locally (entry point)


python src/chatbot.py


Run API

uvicorn source.api:app --reload

---

📂 Repository Structure

use-case/
│── data/                     # Dataset(s) used in the project
│
│── notebooks/                
│   ├── exploratingdataandpreprocessing.ipynb   # Data separation & preprocessing
│   ├── modeling.ipynb             # Model training & evaluation
│   └── chatbot.ipynb              # Chatbot prototype
│
│── src/
│   ├── chatbot.py             # Entry point to run chatbot locally
│   ├── api.py                 # API endpoints for churn prediction
│   ├── model.py               # Defines and manages ML model
│   ├── feature_engineering.py # Feature transformation & preprocessing logic
│   ├── test.py                # Tests to validate functions
│
│            
│
│── diagram                # Architecture diagrams
│
│── requirements.txt           # Dependencies
│── customer.json              # Example customer input
│── README.md                  # Project documentation


---

📝 File Explanations

`chatbot.py` → Main entry point to run chatbot locally.
`api.py` → Provides REST API endpoints to query churn predictions.
`model.py` → Contains ML model definition and training loop.
`feature_engineering.py` → Feature preprocessing and transformation functions.
`test.py` → Unit tests for validating components.
`requirements.txt` → Python dependencies.
`customer.json` → Example input for testing chatbot/API.
`diagrams/` → Visual diagram of project workflow.

Notebooks:

01\_data\_preprocessing.ipynb → Handles splitting and cleaning of raw data.
02\_modeling.ipynb → Experiments with models, evaluates metrics, and chooses best model.
03\_chatbot.ipynb → Prototype of the chatbot before integrating into scripts.


 📈 Project Diagram

https://mermaid.live/view#pako:eNptVE1zmzAQ_SsadaYnO7XBxoFDZxywHTv-ipPpoXIOCixYM1jyCClpmsl_r5BwQ9Jy0LB67-2uVg9ecSoywBHOS_GcHqhU6D7Zc2SeMRlv52jOT1qhLlrcbdboVoN8eUDd7nd0ReIDVY9CPTj2ld2NyXiOZsBBUgUZ2kF1EryChhNbTkISeNQFojxDseBPYGoa1UarutJU81QxwRtJYiUTshOPulJouVx5KGGWQU0rjjSxpCmZMk7LFoyemTqgKVClJVToK_pBSw1Vo3Lr1GpnZEXTA-OAlkAlZ7xAW3aC0uw07JnlXZPz4d7Tfur42hLnpMHRhBcmC8g6ZxfFEmqxbYVl7TyNfG7lC7Iy11J-bsKtC0u5IVsJJylSqCohG8KNhZZkfjSzBGkKrvXR1E7NXD4VctQVmfDaATU1Nu0U4r9kty6tZE3iklYVyxmcy64c4IK1DTZ1exlrT6Z9wK0ZpLlsmioh_xnhxlFcsLXBLdkBrYyXUC4kig9a8m9r4V4-pL-19N3Znc4CWymOp7NTd5ZxVzv17E9z-AQUZaX1rK3TkO8s-d5-Cs5ezqcfalbqpQQ0Rjkry-gL9PNhDm3kvkHSSwjSsI1sGiTPcx96bWR2RnwY5sM2sjgjKQwgxR1cSJbhKKdlBR1sbvtI6xi_1qI9Vgc4wh5H5jWDnOpS7fGevxndifKfQhxxpKQ2Sil0cfibR59qdyaMFpK-U4Abq8RCc4WjUWhT4OgV_8JRv9cbXQz8UeD1gtD3gzDo4Bccdf3e5UUYBF7ohcGlNwiC4VsH_7Zl-xeD3qDv-eGgP_IHXt_zOthYxjhi5f5JqeA5K_DbHwh-azg



Arwa Khaled– Data Scientist 


