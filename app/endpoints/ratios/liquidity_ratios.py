from models import RatioResponse, BalanceSheetsResponse
from app.endpoints import financials
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

@router.get("/current-ratio/{ticker}", response_model=RatioResponse)
async def get_current_ratio(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets)
):
    try:
        if not balance_sheets or not balance_sheets.balance_sheets:
            raise HTTPException(status_code=404, detail="Balance sheet data not found")
        
        latest_balance_sheet = balance_sheets.balance_sheets[0]
        current_assets = latest_balance_sheet.current_assets
        current_liabilities = latest_balance_sheet.current_liabilities
        
        if current_liabilities == 0:
            raise HTTPException(status_code=400, detail="Current liabilities are zero, cannot calculate ratio")
        
        current_ratio = current_assets / current_liabilities
        
        return RatioResponse(
            ticker=ticker,
            ratio_name="Current Ratio",
            ratio_value=current_ratio,
            date=latest_balance_sheet.calendar_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/acid-test/{ticker}", response_model=RatioResponse)
async def get_acid_test(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets)
):
    try:
        if not balance_sheets or not balance_sheets.balance_sheets:
            raise HTTPException(status_code=404, detail="Balance sheet data not found")
        
        latest_balance_sheet = balance_sheets.balance_sheets[0]
        current_assets = latest_balance_sheet.current_assets
        inventory = latest_balance_sheet.inventory
        current_liabilities = latest_balance_sheet.current_liabilities
        
        if current_liabilities == 0:
            raise HTTPException(status_code=400, detail="Current liabilities are zero, cannot calculate ratio")
        
        acid_test_ratio = (current_assets - inventory) / current_liabilities
        
        return RatioResponse(
            ticker=ticker,
            ratio_name="Acid Test Ratio",
            ratio_value=acid_test_ratio,
            date=latest_balance_sheet.calendar_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/defensive-interval/{ticker}", response_model=RatioResponse)
async def get_defensive_interval(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets)
):
    try:
        if not balance_sheets or not balance_sheets.balance_sheets:
            raise HTTPException(status_code=404, detail="Balance sheet data not found")
        
        latest_balance_sheet = balance_sheets.balance_sheets[0]
        cash_and_equivalents = latest_balance_sheet.cash_and_equivalents        
        current_liabilities = latest_balance_sheet.current_liabilities
        
        if current_liabilities == 0:
            raise HTTPException(status_code=400, detail="Current liabilities are zero, cannot calculate ratio")
        
        cash_and_equivalents = cash_and_equivalents
        defensive_interval_ratio = cash_and_equivalents / current_liabilities
        
        return RatioResponse(
            ticker=ticker,
            ratio_name="Defensive Interval Ratio",
            ratio_value=defensive_interval_ratio,
            date=latest_balance_sheet.calendar_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
