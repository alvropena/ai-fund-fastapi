import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Base URL for the financial datasets API
BASE_URL = "https://api.financialdatasets.ai"
API_KEY = "<api-key>"  # Replace with your actual API key
HEADERS = {"X-API-KEY": API_KEY}

# Models for POST requests
class FinancialSearchPayload(BaseModel):
    period: str = "annual"
    limit: int = 50
    filters: List[dict]
    order: str = "asc"

class LineItemsPayload(BaseModel):
    line_items: List[str]
    tickers: List[str]
    period: str = "annual"
    limit: int = 2


# 1. Income Statements
@router.get("/financials/income-statements/{ticker}")
def get_income_statements(ticker: str, period: str = "annual", limit: int = 5):
    url = f"{BASE_URL}/financials/income-statements?ticker={ticker}&period={period}&limit={limit}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching income statements")


# 2. Balance Sheets
@router.get("/financials/balance-sheets/{ticker}")
def get_balance_sheets(ticker: str, period: str = "annual", limit: int = 5):
    url = f"{BASE_URL}/financials/balance-sheets?ticker={ticker}&period={period}&limit={limit}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching balance sheets")


# 3. Cash Flow Statements
@router.get("/financials/cash-flow-statements/{ticker}")
def get_cash_flow_statements(ticker: str, period: str = "annual", limit: int = 5):
    url = f"{BASE_URL}/financials/cash-flow-statements?ticker={ticker}&period={period}&limit={limit}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching cash flow statements")


# 4. Segmented Financials
@router.get("/financials/segmented/{ticker}")
def get_segmented_financials(ticker: str, period: str = "annual", limit: int = 5):
    url = f"{BASE_URL}/financials/segmented?ticker={ticker}&period={period}&limit={limit}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching segmented financials")


# 5. All Financials for a Ticker
@router.get("/financials/{ticker}")
def get_all_financials(ticker: str, period: str = "annual", limit: int = 5):
    url = f"{BASE_URL}/financials?ticker={ticker}&period={period}&limit={limit}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching financials")


# 6. Search Financials (POST)
@router.post("/financials/search")
def search_financials(payload: FinancialSearchPayload):
    url = f"{BASE_URL}/financials/search"
    response = requests.post(url, json=payload.dict(), headers={**HEADERS, "Content-Type": "application/json"})
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error performing financial search")


# 7. Search Line Items (POST)
@router.post("/financials/search/line-items")
def search_line_items(payload: LineItemsPayload):
    url = f"{BASE_URL}/financials/search/line-items"
    response = requests.post(url, json=payload.dict(), headers={**HEADERS, "Content-Type": "application/json"})
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error performing line items search")
