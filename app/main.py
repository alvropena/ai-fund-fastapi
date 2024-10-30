from fastapi import FastAPI
from app.endpoints import company, financials, insider_transactions, prices
from app.endpoints.ratios.ratios import router as ratios_router
from app.agents.financial_analysis_agent import FinancialAnalysisAgent

app = FastAPI(title="AI Financial Analyst API")

app.include_router(company.router, prefix="/company", tags=["Company"])
app.include_router(financials.router, prefix="/financials", tags=["Financials"])
app.include_router(insider_transactions.router, prefix="/insider-transactions", tags=["Insider Transactions"])
app.include_router(prices.router, prefix="/prices", tags=["Prices"])
app.include_router(ratios_router, prefix="/ratios", tags=["Ratios"])

financial_agent = FinancialAnalysisAgent()

async def get_financial_agent():
    return FinancialAnalysisAgent()

@app.post("/analyze")
async def analyze_financials(
    query: str,
    ticker: str,
    financial_agent: FinancialAnalysisAgent = Depends(get_financial_agent)
):
    """
    Analyze financial ratios and provide insights
    Example queries:
    - "What are the liquidity ratios for AAPL?"
    - "Compare profitability ratios between current and previous quarter"
    - "Is the company's financial health improving?"
    """
    return await financial_agent.analyze(query=query, ticker=ticker)