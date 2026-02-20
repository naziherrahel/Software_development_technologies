import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

API_VERSION = os.environ["API_VERSION"]
ENVIRONMENT = os.environ["ENVIRONMENT"]
THRESHOLD = float(os.environ["FRAUD_THRESHOLD"])

app = FastAPI(
    title="Cloud Fraud Detection API",
    description="Simulated fraud detection service deployed on a cloud VM.",
    version=API_VERSION
)

class Transaction(BaseModel):
    amount: float
    country: str
    risk_score: float

@app.get("/")
def root():
    return {
        "service": "Fraud Detection API",
        "environment": ENVIRONMENT,
        "version": API_VERSION
    }

@app.post("/analyze")
def analyze(transaction: Transaction):

    if transaction.amount < 0:
        raise HTTPException(status_code=400, detail="Amount cannot be negative")

    if transaction.risk_score < 0 or transaction.risk_score > 1:
        raise HTTPException(status_code=400, detail="Risk score must be between 0 and 1")

    flagged = transaction.risk_score > THRESHOLD

    return {
        "amount": transaction.amount,
        "country": transaction.country,
        "risk_score": transaction.risk_score,
        "fraud_detected": flagged,
        "threshold_used": THRESHOLD
    }
