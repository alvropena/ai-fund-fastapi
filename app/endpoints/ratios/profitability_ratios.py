from models import RatioResponse, IncomeStatementModel, BalanceSheetsResponse
from app.endpoints import financials
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

@router.get("/sales-margin/{ticker}", response_model=RatioResponse)
async def get_sales_margin(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements)
):
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/return-on-assets/{ticker}", response_model=RatioResponse)
async def get_return_on_assets(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements),
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets)
):
    try:
        if not income_statements or not income_statements.income_statements:
            raise HTTPException(status_code=404, detail="Income statement data not found")
        if not balance_sheets or not balance_sheets.balance_sheets:
            raise HTTPException(status_code=404, detail="Balance sheet data not found")
        
        latest_income_statement = income_statements.income_statements[0]
        latest_balance_sheet = balance_sheets.balance_sheets[0]
        
        net_income = latest_income_statement.net_income
        total_assets = latest_balance_sheet.total_assets
        
        if total_assets == 0:
            raise HTTPException(status_code=400, detail="Total assets are zero, cannot calculate ratio")
        
        return_on_assets = net_income / total_assets
        
        return RatioResponse(
            ticker=ticker,
            ratio_name="Return on Assets (ROA)",
            ratio_value=return_on_assets,
            date=latest_income_statement.calendar_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/return-on-equity/{ticker}", response_model=RatioResponse)
async def get_return_on_equity(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements),
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets)
):
    try:
        if not income_statements or not income_statements.income_statements:
            raise HTTPException(status_code=404, detail="Income statement data not found")
        if not balance_sheets or not balance_sheets.balance_sheets:
            raise HTTPException(status_code=404, detail="Balance sheet data not found")
        
        latest_income_statement = income_statements.income_statements[0]
        latest_balance_sheet = balance_sheets.balance_sheets[0]
        
        net_income = latest_income_statement.net_income
        equity = latest_balance_sheet.total_equity
        
        if equity == 0:
            raise HTTPException(status_code=400, detail="Equity is zero, cannot calculate ratio")
        
        return_on_equity = net_income / equity
        
        return RatioResponse(
            ticker=ticker,
            ratio_name="Return on Equity (ROE)",
            ratio_value=return_on_equity,
            date=latest_income_statement.calendar_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
