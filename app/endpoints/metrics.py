from fastapi import APIRouter, Depends
from typing import Dict
from app.agents.financial_metrics import FinancialMetrics
from app.schemas.financial_metrics import GroupedMetrics, MetricGroup, MetricCategory

router = APIRouter()

@router.get("/grouped", response_model=GroupedMetrics)
async def get_grouped_metrics(
    balance_sheet: Dict,
    income_statement: Dict,
    cash_flow_statement: Dict,
    stock_price: float = 0,
    cost_of_equity: float = 0,
    metrics: FinancialMetrics = Depends()
):
    groups = [
        MetricGroup(
            category=MetricCategory.LIQUIDITY,
            metrics=metrics.calculate_liquidity_ratios(balance_sheet)
        ),
        MetricGroup(
            category=MetricCategory.EBITDA,
            metrics=metrics.calculate_ebitda_ratios(income_statement, cash_flow_statement)
        ),
        MetricGroup(
            category=MetricCategory.LEVERAGE,
            metrics=metrics.calculate_leverage_ratios(balance_sheet)
        ),
        MetricGroup(
            category=MetricCategory.EFFICIENCY,
            metrics=metrics.calculate_efficiency_ratios(income_statement, balance_sheet)
        ),
        MetricGroup(
            category=MetricCategory.PROFITABILITY,
            metrics=metrics.calculate_profitability_ratios(income_statement, balance_sheet)
        ),
        MetricGroup(
            category=MetricCategory.DUPONT,
            metrics=metrics.calculate_dupont_ratios(income_statement, balance_sheet)
        ),
        MetricGroup(
            category=MetricCategory.ECONOMIC_VALUE,
            metrics=metrics.calculate_economic_value_ratios(income_statement, balance_sheet, cost_of_equity)
        ),
        MetricGroup(
            category=MetricCategory.STOCK_PERFORMANCE,
            metrics=metrics.calculate_stock_performance_ratios(
                income_statement, balance_sheet, cash_flow_statement, stock_price
            )
        )
    ]
    
    return GroupedMetrics(groups=groups)