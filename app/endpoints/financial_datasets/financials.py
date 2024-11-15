import requests
from enum import Enum
from fastapi import APIRouter, HTTPException
from config import BASE_URL, HEADERS
from models import FinancialSearchPayload, LineItemsPayload, IncomeStatementsResponse, BalanceSheetsResponse, CashFlowStatementsResponse, SegmentedFinancialsResponse, AllFinancialsResponse, FinancialSearchResponse, LineItemSearchResponse

router = APIRouter()

class FinancialPeriod(str, Enum):
    ANNUAL = "annual"
    QUARTERLY = "quarterly" 
    TTM = "ttm"

# 1. Income Statements
@router.get("/financials/income-statements/{ticker}", response_model=IncomeStatementsResponse)
def get_income_statements(
    ticker: str, 
    period: FinancialPeriod = FinancialPeriod.ANNUAL, 
    limit: int | None = None,
    cik: str | None = None
):
    period_value = period.value
    
    url = f"{BASE_URL}/financials/income-statements?ticker={ticker}&period={period_value}"
    if limit:
        url += f"&limit={limit}"
    if cik:
        url += f"&cik={cik}"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            try:
                data = response.json()
                validated_data = IncomeStatementsResponse(**data)
                return validated_data
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Data validation error: {str(e)}")
        else:
            try:
                error_detail = response.json()
            except:
                pass
            raise HTTPException(status_code=response.status_code, detail=f"Error fetching income statements: Status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

# 2. Balance Sheets
@router.get("/financials/balance-sheets/{ticker}", response_model=BalanceSheetsResponse)
def get_balance_sheets(
    ticker: str, 
    period: FinancialPeriod = FinancialPeriod.ANNUAL,
    limit: int | None = None,
    cik: str | None = None
):
    # Convert the FinancialPeriod enum to its value
    period_value = period.value  # This will convert FinancialPeriod.ANNUAL to "annual"

    url = f"{BASE_URL}/financials/balance-sheets?ticker={ticker}&period={period_value}"
    if limit:
        url += f"&limit={limit}"
    if cik:
        url += f"&cik={cik}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        try:
            data = response.json()            
            validated_data = BalanceSheetsResponse(**data)
            return validated_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Data validation error: {str(e)}")
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching balance sheets")

# 3. Cash Flow Statements
@router.get("/financials/cash-flow-statements/{ticker}", response_model=CashFlowStatementsResponse)
def get_cash_flow_statements(
    ticker: str, 
    period: FinancialPeriod = FinancialPeriod.ANNUAL,
    limit: int | None = None,
    cik: str | None = None
):
    # Convert the FinancialPeriod enum to its value
    period_value = period.value  # This will convert FinancialPeriod.ANNUAL to "annual"

    url = f"{BASE_URL}/financials/cash-flow-statements?ticker={ticker}&period={period_value}"
    if limit:
        url += f"&limit={limit}"
    if cik:
        url += f"&cik={cik}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        try:
            data = response.json()            
            validated_data = CashFlowStatementsResponse(**data)
            return validated_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Data validation error: {str(e)}")
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching cash flow statements")

# 4. Segmented Financials
@router.get("/financials/segmented/{ticker}", response_model=SegmentedFinancialsResponse)
def get_segmented_financials(ticker: str, period: str = "annual", limit: int = 5):
    url = f"{BASE_URL}/financials/segmented?ticker={ticker}&period={period}&limit={limit}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        try:
            data = response.json()
            # Validate the response with the SegmentedFinancialsResponse model
            validated_data = SegmentedFinancialsResponse(**data)
            return validated_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Data validation error: {str(e)}")
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching segmented financials")
    
# 5. All Financials for a Ticker
@router.get("/financials/{ticker}", response_model=AllFinancialsResponse)
def get_all_financials(ticker: str, period: str = "annual", limit: int = 5):
    url = f"{BASE_URL}/financials/{ticker}?period={period}&limit={limit}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        try:
            data = response.json()            
            validated_data = AllFinancialsResponse(**data)
            return validated_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Data validation error: {str(e)}")
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching financials")

# 6. Search Financials (POST)
@router.post("/financials/search", response_model=FinancialSearchResponse)
def search_financials(payload: FinancialSearchPayload):
    url = f"{BASE_URL}/financials/search"
    response = requests.post(url, json=payload.dict(), headers={**HEADERS, "Content-Type": "application/json"})
    
    if response.status_code == 200:
        try:
            data = response.json()            
            validated_data = FinancialSearchResponse(**data)
            return validated_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Data validation error: {str(e)}")
    else:
        raise HTTPException(status_code=response.status_code, detail="Error performing financial search")

# 7. Search Line Items (POST)
@router.post("/financials/search/line-items", response_model=LineItemSearchResponse)
def search_line_items(payload: LineItemsPayload):
    url = f"{BASE_URL}/financials/search/line-items"
    response = requests.post(url, json=payload.dict(), headers={**HEADERS, "Content-Type": "application/json"})
    
    if response.status_code == 200:
        try:
            data = response.json()            
            validated_data = LineItemSearchResponse(**data)
            return validated_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Data validation error: {str(e)}")
    else:
        raise HTTPException(status_code=response.status_code, detail="Error performing line items search")
