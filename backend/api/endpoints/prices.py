import requests
from fastapi import APIRouter, HTTPException
from config import BASE_URL, HEADERS  # Import from config

router = APIRouter()

# 1. Get Prices
@router.get("/prices/{ticker}")
def get_prices(ticker: str, period: str = "daily", limit: int = 5):
    url = f"{BASE_URL}/prices?ticker={ticker}&period={period}&limit={limit}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching prices")


# 2. Get Price Snapshot
@router.get("/prices/snapshot/{ticker}")
def get_price_snapshot(ticker: str):
    url = f"{BASE_URL}/prices/snapshot?ticker={ticker}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching price snapshot")
