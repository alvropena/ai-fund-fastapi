from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional
from app.agents.financial_metrics import FinancialMetrics
from app.schemas.financial_metrics import GroupedMetrics
from app.endpoints.financial_datasets.financials import (
    get_income_statements,
    get_balance_sheets,
    get_cash_flow_statements,
    FinancialPeriod
)

router = APIRouter()

async def get_grouped_metrics(
    balance_sheet: Dict,
    income_statement: Dict,
    cash_flow_statement: Dict,
    stock_price: float,
    cost_of_equity: float,
    metrics: FinancialMetrics
) -> GroupedMetrics:
    """Calculate all financial metric groups for the given financial statements"""
    return GroupedMetrics(
        liquidity=metrics.calculate_liquidity_ratios(balance_sheet),
        ebitda=metrics.calculate_ebitda_ratios(income_statement, cash_flow_statement),
        leverage=metrics.calculate_leverage_ratios(balance_sheet),
        efficiency=metrics.calculate_efficiency_ratios(income_statement, balance_sheet),
        profitability=metrics.calculate_profitability_ratios(income_statement, balance_sheet),
        dupont=metrics.calculate_dupont_ratios(income_statement, balance_sheet),
        economic_value=metrics.calculate_economic_value_ratios(income_statement, balance_sheet, cost_of_equity),
        stock_performance=metrics.calculate_stock_performance_ratios(
            income_statement, balance_sheet, cash_flow_statement, stock_price
        )
    )

@router.get("/grouped/{ticker}", response_model=GroupedMetrics)
async def get_ticker_metrics(
    ticker: str,
    period: FinancialPeriod = FinancialPeriod.ANNUAL,
    limit: int = 1,
    stock_price: float = 0,
    cost_of_equity: float = 0,
    cik: str | None = None,
    metrics: FinancialMetrics = Depends()
):
    # Get financial statements
    income_stmt = get_income_statements(ticker=ticker, period=period, limit=limit, cik=cik)
    balance_sheet = get_balance_sheets(ticker=ticker, period=period, limit=limit, cik=cik)
    cash_flow = get_cash_flow_statements(ticker=ticker, period=period, limit=limit, cik=cik)

    # Extract most recent period's data
    try:
        latest_income = income_stmt.data[0]
        latest_balance = balance_sheet.data[0]
        latest_cash_flow = cash_flow.data[0]
    except (IndexError, AttributeError) as e:
        raise HTTPException(
            status_code=404,
            detail=f"Unable to fetch complete financial data for {ticker}"
        )

    # Calculate grouped metrics
    return await get_grouped_metrics(
        balance_sheet=latest_balance,
        income_statement=latest_income,
        cash_flow_statement=latest_cash_flow,
        stock_price=stock_price,
        cost_of_equity=cost_of_equity,
        metrics=metrics
    )