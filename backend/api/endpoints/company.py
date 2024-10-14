import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/company/facts/{ticker}")
def get_company_facts(ticker: str):
    url = f"https://api.financialdatasets.ai/company/facts?ticker={ticker}"
    headers = {"X-API-KEY": "<api-key>"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching company facts")
