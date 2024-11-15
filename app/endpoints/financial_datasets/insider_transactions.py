import requests
from fastapi import APIRouter, HTTPException
from config import BASE_URL, HEADERS  # Import from config

router = APIRouter()

# Insider Transactions Endpoint
@router.get("/{ticker}")
def get_insider_transactions(ticker: str, limit: int = 5):
    url = f"{BASE_URL}?ticker={ticker}&limit={limit}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching insider transactions")
