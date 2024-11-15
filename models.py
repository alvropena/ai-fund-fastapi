from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class FinancialSearchPayload(BaseModel):
    period: str = "annual"
    limit: int = 50
    filters: List[dict]
    order: str = "asc"

class LineItemsPayload(BaseModel):
    line_items: List[str]
    tickers: List[str]
    period: str = "annual"
    limit: int = 2

class IncomeStatementModel(BaseModel):
    ticker: str
    calendar_date: date
    report_period: date
    period: str
    currency: str
    revenue: float
    cost_of_revenue: float
    gross_profit: float
    operating_expense: float
    selling_general_and_administrative_expenses: Optional[float] = None
    research_and_development: Optional[float] = None
    operating_income: float
    interest_expense: Optional[float] = None
    ebit: float
    income_tax_expense: Optional[float] = None
    net_income_discontinued_operations: Optional[float] = None
    net_income_non_controlling_interests: Optional[float] = None
    net_income: float
    net_income_common_stock: Optional[float] = None
    preferred_dividends_impact: Optional[float] = None
    consolidated_income: float
    earnings_per_share: float
    earnings_per_share_diluted: Optional[float] = None
    dividends_per_common_share: Optional[float] = None
    weighted_average_shares: float
    weighted_average_shares_diluted: Optional[float] = None

class IncomeStatementsResponse(BaseModel):
    income_statements: List[IncomeStatementModel]

class BalanceSheetModel(BaseModel):
    ticker: str
    calendar_date: date
    report_period: date
    period: str
    currency: str
    total_assets: float
    current_assets: Optional[float] = None
    cash_and_equivalents: Optional[float] = None
    inventory: Optional[float] = None
    current_investments: Optional[float] = None
    trade_and_non_trade_receivables: Optional[float] = None
    non_current_assets: Optional[float] = None
    property_plant_and_equipment: Optional[float] = None
    goodwill_and_intangible_assets: Optional[float] = None
    investments: Optional[float] = None
    non_current_investments: Optional[float] = None
    outstanding_shares: Optional[float] = None
    tax_assets: Optional[float] = None
    total_liabilities: float
    current_liabilities: Optional[float] = None
    current_debt: Optional[float] = None
    trade_and_non_trade_payables: Optional[float] = None
    deferred_revenue: Optional[float] = None
    deposit_liabilities: Optional[float] = None
    non_current_liabilities: Optional[float] = None
    non_current_debt: Optional[float] = None
    tax_liabilities: Optional[float] = None
    shareholders_equity: float
    retained_earnings: Optional[float] = None
    accumulated_other_comprehensive_income: Optional[float] = None
    total_debt: Optional[float] = None

class BalanceSheetsResponse(BaseModel):
    balance_sheets: List[BalanceSheetModel]
    
class CashFlowStatementModel(BaseModel):
    ticker: str
    calendar_date: date
    report_period: date
    period: str
    currency: str
    net_cash_flow_from_operations: float
    depreciation_and_amortization: Optional[float] = None
    share_based_compensation: Optional[float] = None
    net_cash_flow_from_investing: float
    capital_expenditure: Optional[float] = None
    business_acquisitions_and_disposals: Optional[float] = None
    investment_acquisitions_and_disposals: Optional[float] = None
    net_cash_flow_from_financing: float
    issuance_or_repayment_of_debt_securities: Optional[float] = None
    issuance_or_purchase_of_equity_shares: Optional[float] = None
    dividends_and_other_cash_distributions: Optional[float] = None
    change_in_cash_and_equivalents: float
    effect_of_exchange_rate_changes: Optional[float] = None

class CashFlowStatementsResponse(BaseModel):
    cash_flow_statements: List[CashFlowStatementModel]

class SegmentedItemModel(BaseModel):
    axis: str
    key: str
    value: float
    period: str

class SegmentedFinancialModel(BaseModel):
    ticker: str
    report_period: date
    period: str
    items: List[SegmentedItemModel]

class SegmentedFinancialsResponse(BaseModel):
    segmented_financials: List[SegmentedFinancialModel]

class FinancialsModel(BaseModel):
    income_statements: List[IncomeStatementModel]
    balance_sheets: List[BalanceSheetModel]
    cash_flow_statements: List[CashFlowStatementModel]
    
class AllFinancialsResponse(BaseModel):
    financials: FinancialsModel
    
class SearchResultModel(BaseModel):
    ticker: str
    report_period: date
    period: str

class FinancialSearchResponse(BaseModel):
    search_results: List[SearchResultModel]
    
class LineItemSearchResultModel(BaseModel):
    ticker: str
    report_period: date
    period: str

class LineItemSearchResponse(BaseModel):
    search_results: List[LineItemSearchResultModel]

class RatioResponse(BaseModel):
    ticker: str
    ratio_name: str
    ratio_value: Optional[float] = None
    date: date