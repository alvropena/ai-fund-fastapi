from models import RatioResponse, BalanceSheetsResponse, IncomeStatementModel
from app.endpoints import financials
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

@router.get("/inventory-turnover/{ticker}", response_model=RatioResponse)
async def get_inventory_turnover(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets),
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements)
):
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    if not income_statements or not income_statements.income_statements:
        raise HTTPException(status_code=404, detail="Income statement data not found")
    
    latest_income_statement = income_statements.income_statements[0]
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    
    cogs = latest_income_statement.cost_of_revenue
    inventory = latest_balance_sheet.inventory
    
    if inventory == 0:
        raise HTTPException(status_code=400, detail="Inventory is zero, cannot calculate ratio")
    
    inventory_turnover = cogs / inventory
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Inventory Turnover",
        ratio_value=inventory_turnover,
        date=latest_income_statement.calendar_date
    )

@router.get("/stock-retention-period/{ticker}", response_model=RatioResponse)
async def get_stock_retention_period(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets),
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements)
):
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    if not income_statements or not income_statements.income_statements:
        raise HTTPException(status_code=404, detail="Income statement data not found")
    
    latest_income_statement = income_statements.income_statements[0]
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    
    cogs = latest_income_statement.cost_of_revenue
    inventory = latest_balance_sheet.inventory
    
    if inventory == 0:
        raise HTTPException(status_code=400, detail="Inventory is zero, cannot calculate ratio")
    
    inventory_turnover = cogs / inventory
    stock_retention_period = 365 / inventory_turnover
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Stock Retention Period",
        ratio_value=stock_retention_period,
        date=latest_income_statement.calendar_date
    )

@router.get("/accounts-receivable-turnover/{ticker}", response_model=RatioResponse)
async def get_accounts_receivable_turnover(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets),
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements)
):
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    if not income_statements or not income_statements.income_statements:
        raise HTTPException(status_code=404, detail="Income statement data not found")
    
    latest_income_statement = income_statements.income_statements[0]
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    
    sales = latest_income_statement.revenue
    accounts_receivable = latest_balance_sheet.trade_and_non_trade_receivables
    
    if accounts_receivable == 0:
        raise HTTPException(status_code=400, detail="Accounts receivable is zero, cannot calculate ratio")
    
    accounts_receivable_turnover = sales / accounts_receivable
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Accounts Receivable Turnover",
        ratio_value=accounts_receivable_turnover,
        date=latest_income_statement.calendar_date
    )

@router.get("/collection-period/{ticker}", response_model=RatioResponse)
async def get_collection_period(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets),
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements)
):
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    if not income_statements or not income_statements.income_statements:
        raise HTTPException(status_code=404, detail="Income statement data not found")
    
    latest_income_statement = income_statements.income_statements[0]
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    
    sales = latest_income_statement.revenue
    accounts_receivable = latest_balance_sheet.trade_and_non_trade_receivables
    
    if accounts_receivable == 0:
        raise HTTPException(status_code=400, detail="Accounts receivable is zero, cannot calculate ratio")
    
    accounts_receivable_turnover = sales / accounts_receivable
    collection_period = 365 / accounts_receivable_turnover
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Collection Period",
        ratio_value=collection_period,
        date=latest_income_statement.calendar_date
    )

@router.get("/accounts-payable-turnover/{ticker}", response_model=RatioResponse)
async def get_accounts_payable_turnover(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets),
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements)
):
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    if not income_statements or not income_statements.income_statements:
        raise HTTPException(status_code=404, detail="Income statement data not found")
    
    latest_income_statement = income_statements.income_statements[0]
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    
    # Estimate purchases as Cost of Revenue
    purchases = latest_income_statement.cost_of_revenue
    accounts_payable = latest_balance_sheet.trade_and_non_trade_payables
    
    if accounts_payable is None or accounts_payable == 0:
        raise HTTPException(status_code=400, detail="Accounts payable is zero or not available, cannot calculate ratio")
    
    accounts_payable_turnover = purchases / accounts_payable
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Accounts Payable Turnover",
        ratio_value=accounts_payable_turnover,
        date=latest_income_statement.calendar_date
    )

@router.get("/payment-period/{ticker}", response_model=RatioResponse)
async def get_payment_period(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets),
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements)
):
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    if not income_statements or not income_statements.income_statements:
        raise HTTPException(status_code=404, detail="Income statement data not found")
    
    latest_income_statement = income_statements.income_statements[0]
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    
    # Estimate purchases as Cost of Revenue
    purchases = latest_income_statement.cost_of_revenue
    accounts_payable = latest_balance_sheet.trade_and_non_trade_payables
    
    if accounts_payable is None or accounts_payable == 0:
        raise HTTPException(status_code=400, detail="Accounts payable is zero or not available, cannot calculate ratio")
    
    accounts_payable_turnover = purchases / accounts_payable
    payment_period = 365 / accounts_payable_turnover
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Payment Period",
        ratio_value=payment_period,
        date=latest_income_statement.calendar_date
    )

@router.get("/asset-turnover/{ticker}", response_model=RatioResponse)
async def get_asset_turnover(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets),
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements)
):
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    if not income_statements or not income_statements.income_statements:
        raise HTTPException(status_code=404, detail="Income statement data not found")
    
    latest_income_statement = income_statements.income_statements[0]
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    
    sales = latest_income_statement.revenues
    total_assets = latest_balance_sheet.total_assets
    
    if total_assets == 0:
        raise HTTPException(status_code=400, detail="Total assets are zero, cannot calculate ratio")
    
    asset_turnover = sales / total_assets
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Asset Turnover",
        ratio_value=asset_turnover,
        date=latest_income_statement.calendar_date
    )
