from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.endpoints import financials
from models import RatioResponse, BalanceSheetsResponse, IncomeStatementModel
from app.endpoints.ratios.liquidity_ratios import get_current_ratio, get_acid_test, get_defensive_interval
from app.endpoints.ratios.ebitda_ratios import get_ebitda_margin
from app.endpoints.ratios.leverage_ratios import get_debt_ratio, get_solvency_ratio, get_leverage
from app.endpoints.ratios.efficiency_ratios import get_inventory_turnover, get_stock_retention_period, get_accounts_receivable_turnover

router = APIRouter()

# TODO: Validate the ratios' formulas

@router.get("/all-ratios/{ticker}", response_model=List[RatioResponse])
async def get_all_ratios(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets),
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements)
):
    ratios = []
    
    ratio_functions = [
        get_current_ratio,
        get_acid_test,
        get_defensive_interval,
        get_ebitda_margin,
        get_debt_ratio,
        get_solvency_ratio,
        get_leverage,
        get_inventory_turnover,
        get_stock_retention_period,
        get_accounts_receivable_turnover
    ]
    
    for func in ratio_functions:
        try:
            if func.__name__ in ['get_inventory_turnover', 'get_stock_retention_period', 'get_accounts_receivable_turnover']:
                ratio = await func(ticker, period, limit, balance_sheets, income_statements)
            elif func.__name__ == 'get_ebitda_margin':
                ratio = await func(ticker, period, limit, income_statements)
            else:
                ratio = await func(ticker, period, limit, balance_sheets)
            ratios.append(ratio)
        except HTTPException as e:
            # If a specific ratio calculation fails, add an error message instead
            ratios.append(RatioResponse(
                ticker=ticker,
                ratio_name=func.__name__.replace('get_', '').replace('_', ' ').title(),
                ratio_value=None,
                date=None,
                error=str(e.detail)
            ))
    
    return ratios
