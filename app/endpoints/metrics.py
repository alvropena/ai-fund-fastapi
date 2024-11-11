from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional, List
from app.agents.financial_metrics import FinancialMetrics
from app.schemas.financial_metrics import GroupedMetrics, MetricGroup, MetricCategory
from models import BalanceSheetsResponse, IncomeStatementsResponse, CashFlowStatementsResponse
from app.endpoints.financial_datasets.financials import (
    get_income_statements,
    get_balance_sheets,
    get_cash_flow_statements,
    FinancialPeriod
)

router = APIRouter()

async def get_grouped_metrics(
    balance_sheets: BalanceSheetsResponse,
    income_statements: IncomeStatementsResponse, 
    cash_flow_statements: CashFlowStatementsResponse,
    stock_price: float,
    cost_of_equity: float,
    metrics: FinancialMetrics
) -> List[GroupedMetrics]:
    """Calculate all financial metric groups for each year of financial statements"""
    grouped_metrics = []
    
    for balance_sheet, income_statement, cash_flow_statement in zip(
        balance_sheets.balance_sheets,
        income_statements.income_statements,
        cash_flow_statements.cash_flow_statements
    ):
        try:
            # Calculate all metrics
            liquidity_metrics = metrics.calculate_liquidity_ratios(balance_sheet)
            ebitda_metrics = metrics.calculate_ebitda_ratios(income_statement, cash_flow_statement)
            leverage_metrics = metrics.calculate_leverage_ratios(balance_sheet)
            efficiency_metrics = metrics.calculate_efficiency_ratios(income_statement, balance_sheet)
            profitability_metrics = metrics.calculate_profitability_ratios(income_statement, balance_sheet)
            dupont_metrics = metrics.calculate_dupont_ratios(income_statement, balance_sheet)
            economic_value_metrics = metrics.calculate_economic_value_ratios(
                income_statement, 
                balance_sheet, 
                cost_of_equity
            )
            stock_performance_metrics = metrics.calculate_stock_performance_ratios(
                income_statement, 
                balance_sheet, 
                cash_flow_statement, 
                stock_price
            )

            # Create MetricGroup objects for each category
            metric_groups = [
                MetricGroup(category=MetricCategory.LIQUIDITY, metrics=liquidity_metrics),
                MetricGroup(category=MetricCategory.EBITDA, metrics=ebitda_metrics),
                MetricGroup(category=MetricCategory.LEVERAGE, metrics=leverage_metrics),
                MetricGroup(category=MetricCategory.EFFICIENCY, metrics=efficiency_metrics),
                MetricGroup(category=MetricCategory.PROFITABILITY, metrics=profitability_metrics),
                MetricGroup(category=MetricCategory.DUPONT, metrics=dupont_metrics),
                MetricGroup(category=MetricCategory.ECONOMIC_VALUE, metrics=economic_value_metrics),
                MetricGroup(category=MetricCategory.STOCK_PERFORMANCE, metrics=stock_performance_metrics),
            ]

            metrics_for_period = GroupedMetrics(groups=metric_groups)
            grouped_metrics.append(metrics_for_period)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error calculating metrics: {str(e)}"
            )
        
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
    try:
        # Get financial statements with logging
        print(f"Fetching financial data for {ticker}")
        
        income_statements = get_income_statements(ticker=ticker, period=period, limit=limit, cik=cik)
        print(f"Income statements retrieved: {bool(income_statements)}")
        if income_statements:
            print(f"Number of income statements: {len(income_statements.income_statements)}")
        
        balance_sheets = get_balance_sheets(ticker=ticker, period=period, limit=limit, cik=cik)
        print(f"Balance sheets retrieved: {bool(balance_sheets)}")
        if balance_sheets:
            print(f"Number of balance sheets: {len(balance_sheets.balance_sheets)}")
        
        cash_flows = get_cash_flow_statements(ticker=ticker, period=period, limit=limit, cik=cik)
        print(f"Cash flows retrieved: {bool(cash_flows)}")
        if cash_flows:
            print(f"Number of cash flows: {len(cash_flows.cash_flow_statements)}")

        # Validate we have data with more specific error messages
        if not income_statements:
            raise HTTPException(
                status_code=404,
                detail=f"No income statements found for {ticker}"
            )
        if not balance_sheets:
            raise HTTPException(
                status_code=404,
                detail=f"No balance sheets found for {ticker}"
            )
        if not cash_flows:
            raise HTTPException(
                status_code=404,
                detail=f"No cash flow statements found for {ticker}"
            )

        # Additional validation for empty lists
        if not income_statements.income_statements:
            raise HTTPException(
                status_code=404,
                detail=f"Income statements list is empty for {ticker}"
            )
        if not balance_sheets.balance_sheets:
            raise HTTPException(
                status_code=404,
                detail=f"Balance sheets list is empty for {ticker}"
            )
        if not cash_flows.cash_flow_statements:
            raise HTTPException(
                status_code=404,
                detail=f"Cash flow statements list is empty for {ticker}"
            )

        print(f"All financial data retrieved successfully for {ticker}")

        try:
            # Calculate grouped metrics for each period
            result = await get_grouped_metrics(
                balance_sheets=balance_sheets,
                income_statements=income_statements,
                cash_flow_statements=cash_flows,
                stock_price=stock_price,
                cost_of_equity=cost_of_equity,
                metrics=metrics
            )
            print(f"Metrics calculated successfully for {ticker}")
            return result
        except Exception as calc_error:
            print(f"Error calculating metrics for {ticker}: {str(calc_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error calculating metrics for {ticker}: {str(calc_error)}"
            )

    except HTTPException as http_error:
        # Re-raise HTTP exceptions
        raise http_error
    except Exception as e:
        print(f"Unexpected error processing {ticker}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error processing {ticker}: {str(e)}"
        )