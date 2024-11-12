from pydantic import BaseModel
from typing import Dict, Any
from models import BalanceSheetModel, IncomeStatementModel, CashFlowStatementModel

class FinancialMetrics(BaseModel):
    """Container for all financial metrics calculations"""
    
    def calculate_liquidity_ratios(self, balance_sheet: BalanceSheetModel) -> Dict[str, float]:
        return {
            "current_ratio": balance_sheet.current_assets / balance_sheet.current_liabilities,
            "acid_test_ratio": (balance_sheet.current_assets - balance_sheet.inventory) / balance_sheet.current_liabilities,
            "defensive_interval_ratio": balance_sheet.cash_and_equivalents / balance_sheet.current_liabilities
        }
    
    def calculate_ebitda_ratios(self, income_statement: IncomeStatementModel, cash_flow_statement: CashFlowStatementModel) -> Dict[str, float]:
        return {
            "ebitda": income_statement.ebit + cash_flow_statement.depreciation_and_amortization,
            "ebitda_margin": (income_statement.ebit + cash_flow_statement.depreciation_and_amortization) / income_statement.revenue
        }
    
    def calculate_leverage_ratios(self, balance_sheet: BalanceSheetModel) -> Dict[str, float]:
        return {
            "debt_ratio": balance_sheet.total_liabilities / balance_sheet.total_assets,
            "solvency_ratio": (balance_sheet.total_liabilities + balance_sheet.shareholders_equity) / balance_sheet.total_assets,
            "leverage": balance_sheet.total_assets / (balance_sheet.total_liabilities + balance_sheet.shareholders_equity)
        }

    def calculate_efficiency_ratios(self, income_statement: IncomeStatementModel, balance_sheet: BalanceSheetModel) -> Dict[str, float]:        
        inventory_turnover = income_statement.cost_of_revenue / balance_sheet.inventory
        receivables_turnover = income_statement.revenue / balance_sheet.trade_and_non_trade_receivables
        payables_turnover = income_statement.cost_of_revenue / balance_sheet.trade_and_non_trade_payables
        asset_turnover = income_statement.revenue / balance_sheet.total_assets
        
        return {
            "inventory_turnover": inventory_turnover,
            "stock_retention_period": 365 / inventory_turnover,
            "accounts_receivable_turnover": receivables_turnover,
            "collection_period": 365 / receivables_turnover,
            "accounts_payable_turnover": payables_turnover,
            "payment_period": 365 / payables_turnover,
            "asset_turnover": asset_turnover
        }

    def calculate_profitability_ratios(self, income_statement: IncomeStatementModel, balance_sheet: BalanceSheetModel) -> Dict[str, float]:
        return {
            "sales_margin": income_statement.net_income / income_statement.revenue,
            "return_on_assets": income_statement.net_income / balance_sheet.total_assets,
            "return_on_equity": income_statement.net_income / (balance_sheet.total_assets + balance_sheet.total_liabilities)
        }

    def calculate_dupont_ratios(self, income_statement: IncomeStatementModel, balance_sheet: BalanceSheetModel) -> Dict[str, float]:
        return {
            "sales_margin": income_statement.net_income / income_statement.revenue,
            "asset_turnover": income_statement.revenue / balance_sheet.total_assets,
            "leverage": balance_sheet.total_assets / (balance_sheet.total_liabilities + balance_sheet.total_assets)
        }
    
    def calculate_economic_value_ratios(
        self, 
        income_statement: IncomeStatementModel, 
        balance_sheet: BalanceSheetModel, 
        cost_of_equity: float
    ) -> Dict[str, float]:
        sales_margin = income_statement.net_income / income_statement.revenue
        asset_turnover = income_statement.revenue / balance_sheet.total_assets
        leverage = balance_sheet.total_assets / (balance_sheet.total_liabilities + balance_sheet.total_assets)
        
        roe = sales_margin * asset_turnover * leverage
        economic_margin = roe - cost_of_equity
        eva = economic_margin * (balance_sheet.total_assets + balance_sheet.total_liabilities)
        
        return {
            "economic_margin": economic_margin,
            "economic_value_added": eva
        }

    def calculate_stock_performance_ratios(
        self,
        income_statement: IncomeStatementModel,
        balance_sheet: BalanceSheetModel,
        cash_flow_statement: CashFlowStatementModel,
        stock_price: float
    ) -> Dict[str, Any]:
        if balance_sheet.outstanding_shares == 0:
            return {
                "error": "Cannot calculate ratios - outstanding shares is zero"
            }

        earnings_per_share = income_statement.net_income / balance_sheet.outstanding_shares
        dividends_per_share = cash_flow_statement.dividends_and_other_cash_distributions / balance_sheet.outstanding_shares
        market_value = stock_price * balance_sheet.outstanding_shares
        total_equity = balance_sheet.total_assets + balance_sheet.total_liabilities
        market_value_added = market_value - total_equity
        
        result = {
            "earnings_per_share": earnings_per_share,
            "dividends_per_share": dividends_per_share,
            "market_value": market_value,
            "market_value_added": market_value_added,
        }

        if earnings_per_share != 0:
            result["price_to_earnings_ratio"] = stock_price / earnings_per_share

        return result