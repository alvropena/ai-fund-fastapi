import pytest
from app.agents.financial_metrics import FinancialMetrics


balance_sheet = {
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
        
    

income_statement = {
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
        
cash_flow_statement = {
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
        
    

def test_all_metrics():
    metrics = FinancialMetrics()
    
    # Test each method
    print("\nLiquidity Ratios:")
    print(metrics.calculate_liquidity_ratios(balance_sheet))
    
    print("\nEBITDA Ratios:")
    print(metrics.calculate_ebitda_ratios(income_statement, cash_flow_statement))
    
    print("\nLeverage Ratios:")
    print(metrics.calculate_leverage_ratios(balance_sheet))
    
    print("\nEfficiency Ratios:")
    print(metrics.calculate_efficiency_ratios(income_statement, balance_sheet))
    
    print("\nProfitability Ratios:")
    print(metrics.calculate_profitability_ratios(income_statement, balance_sheet))
    
    print("\nDuPont Ratios:")
    print(metrics.calculate_dupont_ratios(income_statement, balance_sheet))
    
    print("\nEconomic Value Ratios:")
    print(metrics.calculate_economic_value_ratios(income_statement, balance_sheet, cost_of_equity=0.10))
    
    print("\nStock Performance Ratios:")
    print(metrics.calculate_stock_performance_ratios(
        income_statement,
        balance_sheet,
        cash_flow_statement,
        stock_price=50.0
    ))

if __name__ == "__main__":
    test_all_metrics()