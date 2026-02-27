import os
import json
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from dotenv import load_dotenv

load_dotenv()

DATA_FILE = "data/transactions.json"
APP_TITLE = os.environ["APP_TITLE"]

app = FastAPI(title=APP_TITLE)

templates = Jinja2Templates(directory="templates")

def load_transactions():
    if not os.path.exists(DATA_FILE):
        return []
    
    with open(DATA_FILE, "r") as f:
        return json.load(f)
   
def save_transaction(transaction):
    transactions = load_transactions()
    transactions.append(transaction)
    with open(DATA_FILE, "w") as f:
        json.dump(transactions, f, indent=4)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    transactions = load_transactions()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "transactions": transactions}
    )

@app.post("/add")
def add_transaction(amount: float = Form(...), description: str = Form(...)):
    transaction = {"amount": amount, "description": description}
    save_transaction(transaction)
    return {"status": "Transaction added"}