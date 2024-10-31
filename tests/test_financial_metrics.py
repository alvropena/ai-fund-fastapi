import pytest
from app.agents.financial_metrics import FinancialMetrics

@pytest.fixture
def sample_balance_sheet_data():
    return {
        "balance_sheet": {
            "ticker": "AAPL",
            "calendar_date": "2024-01-01",
            "report_period": "2024-01-01",
            "period": "annual",
            "currency": "USD",
            "total_assets": 1000,
            "current_assets": 1000,
            "cash_and_equivalents": 1000,
            "inventory": 1000,
            "current_investments": 1000,
            "trade_and_non_trade_receivables": 1000,
            "non_current_assets": 1000,
            "property_plant_and_equipment": 1000,
            "goodwill_and_intangible_assets": 1000,
            "investments": 1000,
            "non_current_investments": 1000,
            "outstanding_shares": 1000,
            "tax_assets": 1000,
            "total_liabilities": 1000,
            "current_liabilities": 1000,
            "current_debt": 1000,
            "trade_and_non_trade_payables": 1000,
            "deferred_revenue": 1000,
            "deposit_liabilities": 1000,
            "non_current_liabilities": 1000,
            "non_current_debt": 1000,
            "tax_liabilities": 1000,
            "shareholders_equity": 1000,
            "retained_earnings": 1000,
            "accumulated_other_comprehensive_income": 1000,
            "total_debt": 1000
        },
        
    }

@pytest.fixture
def sample_income_statement_data():
    return {
        "income_statement": {
            "ticker": "AAPL",
            "calendar_date": "2024-01-01",
            "report_period": "2024-01-01",
            "period": "annual",
            "currency": "USD",
            "revenue": 1000,
            "cost_of_revenue": 1000,
            "gross_profit": 1000,
            "operating_expense": 1000,
            "selling_general_and_administrative_expenses": 1000,
            "research_and_development": 1000,
            "operating_income": 1000,
            "interest_expense": 1000,
            "ebit": 1000,
            "income_tax_expense": 1000,
            "net_income_discontinued_operations": 1000,
            "net_income_non_controlling_interests": 1000,
            "net_income": 1000,
            "net_income_common_stock": 1000,
            "preferred_dividends_impact": 1000,
            "consolidated_income": 1000,
            "earnings_per_share": 1000,
            "earnings_per_share_diluted": 1000,
            "dividends_per_common_share": 1000,
            "weighted_average_shares": 1000,
            "weighted_average_shares_diluted": 1000
        },
        
    }

@pytest.fixture
def sample_cash_flow_statement_data():
    return {
        "cash_flow_statement": {
            "ticker": "AAPL",
            "calendar_date": "2024-01-01",
            "report_period": "2024-01-01",
            "period": "annual",
            "currency": "USD",
            "net_cash_flow_from_operations": 1000,
            "depreciation_and_amortization": 100,
            "share_based_compensation": 100,
            "net_cash_flow_from_investing": 1000,
            "capital_expenditure": 100,
            "business_acquisitions_and_disposals": 100,
            "investment_acquisitions_and_disposals": 100,
            "net_cash_flow_from_financing": 1000,
            "issuance_or_repayment_of_debt_securities": 100,
            "issuance_or_purchase_of_equity_shares": 100,
            "dividends_and_other_cash_distributions": 100,
            "change_in_cash_and_equivalents": 100,
            "effect_of_exchange_rate_changes": 100
        },
        
    }

def test_liquidity_ratios(sample_balance_sheet_data):
    metrics = FinancialMetrics()
    ratios = metrics.calculate_liquidity_ratios(sample_balance_sheet_data["balance_sheet"])
    
    assert ratios["current_ratio"] == 2.0
    assert ratios["acid_test_ratio"] == 1.6
    assert ratios["defensive_interval_ratio"] == 0.6

def test_stock_performance_ratios(sample_income_statement_data, sample_balance_sheet_data, sample_cash_flow_statement_data):
    metrics = FinancialMetrics()
    ratios = metrics.calculate_stock_performance_ratios(
        sample_income_statement_data["income_statement"],
        sample_balance_sheet_data["balance_sheet"],
        sample_cash_flow_statement_data["cash_flow_statement"],
        stock_price=10.0
    )
    
    assert ratios["earnings_per_share"] == 0.4
    assert ratios["price_to_earnings_ratio"] == 25.0