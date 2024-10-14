import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Base URL for the financial datasets API
BASE_URL = "https://api.financialdatasets.ai"
API_KEY = "<api-key>"
HEADERS = {"X-API-KEY": API_KEY}

# Insider Transactions Endpoint
@router.get("/insider-transactions/{ticker}")
def get_insider_transactions(ticker: str, limit: int = 5):
    url = f"{BASE_URL}/insider-transactions?ticker={ticker}&limit={limit}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching insider transactions")
