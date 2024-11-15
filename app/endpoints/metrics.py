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
        # Calculate all metrics with safe error handling
        metric_calculations = {
            MetricCategory.LIQUIDITY: lambda: metrics.calculate_liquidity_ratios(balance_sheet),
            MetricCategory.EBITDA: lambda: metrics.calculate_ebitda_ratios(income_statement, cash_flow_statement),
            MetricCategory.LEVERAGE: lambda: metrics.calculate_leverage_ratios(balance_sheet),
            MetricCategory.EFFICIENCY: lambda: metrics.calculate_efficiency_ratios(income_statement, balance_sheet),
            MetricCategory.PROFITABILITY: lambda: metrics.calculate_profitability_ratios(income_statement, balance_sheet),
            MetricCategory.DUPONT: lambda: metrics.calculate_dupont_ratios(income_statement, balance_sheet),
            MetricCategory.ECONOMIC_VALUE: lambda: metrics.calculate_economic_value_ratios(
                income_statement, 
                balance_sheet, 
                cost_of_equity
            ),
            MetricCategory.STOCK_PERFORMANCE: lambda: metrics.calculate_stock_performance_ratios(
                income_statement, 
                balance_sheet, 
                cash_flow_statement, 
                stock_price
            )
        }

        metric_groups = []
        for category, calculation in metric_calculations.items():
            try:
                metrics_result = calculation()
                # Filter out None values from the metrics result
                valid_metrics = {k: v for k, v in metrics_result.items() if v is not None}
                metric_groups.append(MetricGroup(category=category, metrics=valid_metrics))
            except Exception as e:
                # Add empty metrics group instead of failing
                metric_groups.append(MetricGroup(category=category, metrics={}))

        metrics_for_period = GroupedMetrics(
            period=income_statement.period,
            report_date=income_statement.report_period,
            groups=metric_groups
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
    try:
        # Get financial statements
        income_statements = get_income_statements(ticker=ticker, period=period, limit=limit, cik=cik)
        balance_sheets = get_balance_sheets(ticker=ticker, period=period, limit=limit, cik=cik)
        cash_flows = get_cash_flow_statements(ticker=ticker, period=period, limit=limit, cik=cik)

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
            return result
        except Exception as calc_error:
            raise HTTPException(
                status_code=500,
                detail=f"Error calculating metrics for {ticker}: {str(calc_error)}"
            )

    except HTTPException as http_error:
        # Re-raise HTTP exceptions
        raise http_error
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error processing {ticker}: {str(e)}"
        )