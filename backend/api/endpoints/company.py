import requests
from fastapi import APIRouter, HTTPException
from backend.config import BASE_URL, HEADERS  # Import from config

router = APIRouter()

# Company Facts Endpoint
@router.get("/company/facts/{ticker}")
def get_company_facts(ticker: str):
    url = f"{BASE_URL}/company/facts?ticker={ticker}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching company facts")
