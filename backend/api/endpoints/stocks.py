from fastapi import APIRouter, HTTPException
from data_fetcher import get_income_statements
from financial_models import calculate_pe_ratio
import pandas as pd

router = APIRouter()

@router.get("/{ticker}/income-statements")
def fetch_income_statements(ticker: str):
    try:
        data = get_income_statements(ticker)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{ticker}/pe-ratio")
def get_pe_ratio(ticker: str, price: float, eps: float):
    pe = calculate_pe_ratio(price, eps)
    return {"ticker": ticker, "pe_ratio": pe}
