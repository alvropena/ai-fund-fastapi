import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Base URL for the financial datasets API
BASE_URL = "https://api.financialdatasets.ai"
API_KEY = "<api-key>"  # Replace with your actual API key
HEADERS = {"X-API-KEY": API_KEY}

# Get Filings
@router.get("/filings/{ticker}")
def get_filings(ticker: str, limit: int = 5):
    url = f"{BASE_URL}/filings?ticker={ticker}&limit={limit}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching filings")
