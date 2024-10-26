from backend.models import RatioResponse, IncomeStatementModel, BalanceSheetsResponse
from backend.api.endpoints import financials
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

@router.get("/earnings-per-share/{ticker}", response_model=RatioResponse)
async def get_earnings_per_share(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements),
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets)
):
    if not income_statements or not income_statements.income_statements:
        raise HTTPException(status_code=404, detail="Income statement data not found")
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    latest_income_statement = income_statements.income_statements[0]
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    
    net_income = latest_income_statement.net_income
    outstanding_shares = latest_balance_sheet.shares_outstanding
    
    if outstanding_shares == 0:
        raise HTTPException(status_code=400, detail="Number of outstanding shares is zero, cannot calculate EPS")
    
    earnings_per_share = net_income / outstanding_shares
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Earnings Per Share (EPS)",
        ratio_value=earnings_per_share,
        date=latest_income_statement.calendar_date
    )

@router.get("/dividends-per-share/{ticker}", response_model=RatioResponse)
async def get_dividends_per_share(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements),
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets)
):
    if not income_statements or not income_statements.income_statements:
        raise HTTPException(status_code=404, detail="Income statement data not found")
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    latest_income_statement = income_statements.income_statements[0]
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    
    dividends = latest_income_statement.dividends
    outstanding_shares = latest_balance_sheet.shares_outstanding
    
    if outstanding_shares == 0:
        raise HTTPException(status_code=400, detail="Number of outstanding shares is zero, cannot calculate DPS")
    
    dividends_per_share = dividends / outstanding_shares
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Dividends Per Share (DPS)",
        ratio_value=dividends_per_share,
        date=latest_income_statement.calendar_date
    )

@router.get("/pe-ratio/{ticker}", response_model=RatioResponse)
async def get_pe_ratio(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements),
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets),
    stock_price: float = Depends(financials.get_current_stock_price)
):
    if not income_statements or not income_statements.income_statements:
        raise HTTPException(status_code=404, detail="Income statement data not found")
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    latest_income_statement = income_statements.income_statements[0]
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    
    net_income = latest_income_statement.net_income
    outstanding_shares = latest_balance_sheet.shares_outstanding
    
    if outstanding_shares == 0:
        raise HTTPException(status_code=400, detail="Number of outstanding shares is zero, cannot calculate EPS")
    
    earnings_per_share = net_income / outstanding_shares
    
    if earnings_per_share == 0:
        raise HTTPException(status_code=400, detail="Earnings per share is zero, cannot calculate P/E ratio")
    
    pe_ratio = stock_price / earnings_per_share
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Price-to-Earnings (P/E) Ratio",
        ratio_value=pe_ratio,
        date=latest_income_statement.calendar_date
    )

@router.get("/market-value/{ticker}", response_model=RatioResponse)
async def get_market_value(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets),
    stock_price: float = Depends(financials.get_current_stock_price)
):
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    
    outstanding_shares = latest_balance_sheet.shares_outstanding
    
    if outstanding_shares == 0:
        raise HTTPException(status_code=400, detail="Number of outstanding shares is zero, cannot calculate market value")
    
    market_value = stock_price * outstanding_shares
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Market Value",
        ratio_value=market_value,
        date=latest_balance_sheet.calendar_date
    )

@router.get("/market-value-added/{ticker}", response_model=RatioResponse)
async def get_market_value_added(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    balance_sheets: BalanceSheetsResponse = Depends(financials.get_balance_sheets),
    stock_price: float = Depends(financials.get_current_stock_price)
):
    if not balance_sheets or not balance_sheets.balance_sheets:
        raise HTTPException(status_code=404, detail="Balance sheet data not found")
    
    latest_balance_sheet = balance_sheets.balance_sheets[0]
    
    outstanding_shares = latest_balance_sheet.shares_outstanding
    total_equity = latest_balance_sheet.total_equity
    
    if outstanding_shares == 0:
        raise HTTPException(status_code=400, detail="Number of outstanding shares is zero, cannot calculate market value")
    
    market_value = stock_price * outstanding_shares
    market_value_added = market_value - total_equity
    
    return RatioResponse(
        ticker=ticker,
        ratio_name="Market Value Added (MVA)",
        ratio_value=market_value_added,
        date=latest_balance_sheet.calendar_date
    )
