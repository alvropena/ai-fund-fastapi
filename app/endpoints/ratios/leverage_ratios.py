from models import RatioResponse, BalanceSheetsResponse
from app.endpoints import financials
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

@router.get("/debt-ratio/{ticker}", response_model=RatioResponse)
async def get_debt_ratio(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets)
):
    try:
        if not balance_sheets or not balance_sheets.balance_sheets:
            raise HTTPException(status_code=404, detail="Balance sheet data not found")
        
        latest_balance_sheet = balance_sheets.balance_sheets[0]
        total_liabilities = latest_balance_sheet.total_liabilities
        total_assets = latest_balance_sheet.total_assets
        
        if total_assets == 0:
            raise HTTPException(status_code=400, detail="Total assets are zero, cannot calculate ratio")
        
        debt_ratio = total_liabilities / total_assets
        
        return RatioResponse(
            ticker=ticker,
            ratio_name="Debt Ratio",
            ratio_value=debt_ratio,
            date=latest_balance_sheet.calendar_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/solvency-ratio/{ticker}", response_model=RatioResponse)
async def get_solvency_ratio(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets)
):
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    total_equity = latest_balance_sheet.shareholders_equity
    total_assets = latest_balance_sheet.total_assets
    
    if total_assets == 0:
        raise HTTPException(status_code=400, detail="Total assets are zero, cannot calculate ratio")
    
    solvency_ratio = total_equity / total_assets
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Solvency Ratio",
        ratio_value=solvency_ratio,
        date=latest_balance_sheet.calendar_date
    )

@router.get("/leverage/{ticker}", response_model=RatioResponse)
async def get_leverage(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets)
):
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    total_assets = latest_balance_sheet.total_assets
    total_equity = latest_balance_sheet.shareholders_equity
    
    if total_equity == 0:
        raise HTTPException(status_code=400, detail="Total equity is zero, cannot calculate ratio")
    
    leverage = total_assets / total_equity
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Leverage",
        ratio_value=leverage,
        date=latest_balance_sheet.calendar_date
    )
