from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional, List
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
    balance_sheets: List[Dict],
    income_statements: List[Dict], 
    cash_flow_statements: List[Dict],
    stock_price: float,
    cost_of_equity: float,
    metrics: FinancialMetrics
) -> List[GroupedMetrics]:
    """Calculate all financial metric groups for each year of financial statements"""
    grouped_metrics = []
    
    for balance_sheet, income_statement, cash_flow_statement in zip(
        balance_sheets, income_statements, cash_flow_statements
    ):
        print("Balance Sheet Data:", balance_sheet)
        print("Income Statement Data:", income_statement) 
        print("Cash Flow Statement Data:", cash_flow_statement)
        
        metrics_for_period = GroupedMetrics(
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
        grouped_metrics.append(metrics_for_period)
        
    return grouped_metrics

@router.get("/grouped/{ticker}", response_model=List[GroupedMetrics])
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

    # Extract the actual statement data from the response tuples
    income_statements = income_stmt[1] if isinstance(income_stmt, tuple) else income_stmt
    balance_sheets = balance_sheet[1] if isinstance(balance_sheet, tuple) else balance_sheet
    cash_flows = cash_flow[1] if isinstance(cash_flow, tuple) else cash_flow

    # Validate we have data
    if not (income_statements and balance_sheets and cash_flows):
        raise HTTPException(
            status_code=404,
            detail=f"Unable to fetch complete financial data for {ticker}"
        )

    # Calculate grouped metrics for each period
    return await get_grouped_metrics(
        balance_sheets=balance_sheets,
        income_statements=income_statements,
        cash_flow_statements=cash_flows,
        stock_price=stock_price,
        cost_of_equity=cost_of_equity,
        metrics=metrics
    )