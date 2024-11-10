from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional, List
from app.agents.financial_metrics import FinancialMetrics
from app.schemas.financial_metrics import GroupedMetrics
from models import BalanceSheetModel, IncomeStatementModel, CashFlowStatementModel
from app.endpoints.financial_datasets.financials import (
    get_income_statements,
    get_balance_sheets,
    get_cash_flow_statements,
    FinancialPeriod
)

router = APIRouter()

async def get_grouped_metrics(
    balance_sheets: List[BalanceSheetModel],
    income_statements: List[IncomeStatementModel], 
    cash_flow_statements: List[CashFlowStatementModel],
    stock_price: float,
    cost_of_equity: float,
    metrics: FinancialMetrics
) -> List[GroupedMetrics]:
    """Calculate all financial metric groups for each year of financial statements"""
    grouped_metrics = []    
    
    for balance_sheet, income_statement, cash_flow_statement in zip(
        balance_sheets, income_statements, cash_flow_statements
    ):
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
    income_statements = get_income_statements(ticker=ticker, period=period, limit=limit, cik=cik)
    balance_sheets = get_balance_sheets(ticker=ticker, period=period, limit=limit, cik=cik)
    cash_flows = get_cash_flow_statements(ticker=ticker, period=period, limit=limit, cik=cik)

    # Print the raw data and their types
    print("\n=== Financial Statements Data ===")
    print(f"Income Statements Type: {type(income_statements)}")
    print(f"Income Statements Data: {income_statements}")
    print("\n")
    print(f"Balance Sheets Type: {type(balance_sheets)}")
    print(f"Balance Sheets Data: {balance_sheets}")
    print("\n")
    print(f"Cash Flows Type: {type(cash_flows)}")
    print(f"Cash Flows Data: {cash_flows}")
    print("\n===========================")    

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