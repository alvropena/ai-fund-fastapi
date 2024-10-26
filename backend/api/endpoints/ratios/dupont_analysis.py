from backend.models import RatioResponse, IncomeStatementModel, BalanceSheetsResponse
from backend.api.endpoints import financials
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()    

@router.get("/sales-margin/{ticker}", response_model=RatioResponse)
async def get_sales_margin(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements)
):
    if not income_statements or not income_statements.income_statements:
        raise HTTPException(status_code=404, detail="Income statement data not found")
    
    latest_income_statement = income_statements.income_statements[0]
    net_income = latest_income_statement.net_income
    sales = latest_income_statement.revenues
    
    if sales == 0:
        raise HTTPException(status_code=400, detail="Sales are zero, cannot calculate ratio")
    
    sales_margin = net_income / sales
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Sales Margin",
        ratio_value=sales_margin,
        date=latest_income_statement.calendar_date
    )

@router.get("/asset-turnover/{ticker}", response_model=RatioResponse)
async def get_asset_turnover(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements),
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets)
):
    if not income_statements or not income_statements.income_statements:
        raise HTTPException(status_code=404, detail="Income statement data not found")
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    latest_income_statement = income_statements.income_statements[0]
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    
    sales = latest_income_statement.revenues
    total_assets = latest_balance_sheet.total_assets
    
    if total_assets == 0:
        raise HTTPException(status_code=400, detail="Total assets are zero, cannot calculate ratio")
    
    asset_turnover = sales / total_assets
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Asset Turnover",
        ratio_value=asset_turnover,
        date=latest_income_statement.calendar_date
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
    equity = latest_balance_sheet.total_equity
    
    if equity == 0:
        raise HTTPException(status_code=400, detail="Equity is zero, cannot calculate ratio")
    
    leverage = total_assets / equity
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Leverage",
        ratio_value=leverage,
        date=latest_balance_sheet.calendar_date
    )
