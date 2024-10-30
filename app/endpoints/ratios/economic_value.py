from models import RatioResponse, IncomeStatementModel, BalanceSheetsResponse
from app.endpoints import financials
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

router = APIRouter()

@router.get("/economic-margin/{ticker}", response_model=RatioResponse)
async def get_economic_margin(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    cost_of_equity: Optional[float] = None,
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
        total_equity = latest_balance_sheet.total_equity
        
        if total_equity == 0:
            raise HTTPException(status_code=400, detail="Total equity is zero, cannot calculate ROE")
        
        roe = net_income / total_equity
        
        if cost_of_equity is None:
            raise HTTPException(status_code=400, detail="Cost of equity (Ke) is required to calculate Economic Margin")
        
        economic_margin = roe - cost_of_equity
        
        return RatioResponse(
            ticker=ticker,
            ratio_name="Economic Margin",
            ratio_value=economic_margin,
            date=latest_income_statement.calendar_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/economic-value-added/{ticker}", response_model=RatioResponse)
async def get_economic_value_added(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    cost_of_equity: Optional[float] = None,
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
        total_equity = latest_balance_sheet.total_equity
        
        if total_equity == 0:
            raise HTTPException(status_code=400, detail="Total equity is zero, cannot calculate ROE")
        
        roe = net_income / total_equity
        
        if cost_of_equity is None:
            raise HTTPException(status_code=400, detail="Cost of equity (Ke) is required to calculate EVA")
        
        eva = (roe - cost_of_equity) * total_equity
        
        return RatioResponse(
            ticker=ticker,
            ratio_name="Economic Value Added (EVA)",
            ratio_value=eva,
            date=latest_income_statement.calendar_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
