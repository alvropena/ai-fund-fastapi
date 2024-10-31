from fastapi import FastAPI, Depends
from app.endpoints import company, financials, insider_transactions, prices
from app.agents.financial_metrics_agent import FinancialAnalysisAgent

app = FastAPI(title="AI Financial Analyst API")

# Include routers
app.include_router(company.router, prefix="/company", tags=["Company"])
app.include_router(financials.router, prefix="/financials", tags=["Financials"])
app.include_router(insider_transactions.router, prefix="/insider-transactions", tags=["Insider Transactions"])
app.include_router(prices.router, prefix="/prices", tags=["Prices"])

# Create a single instance of the agent
financial_agent = FinancialAnalysisAgent()

# Use closure to return the same instance
async def get_financial_agent():
    return financial_agent

@app.post("/analyze", 
    response_model=str,
    responses={
        200: {
            "description": "Financial analysis response",
            "content": {
                "application/json": {
                    "example": "Based on the liquidity ratios, AAPL shows strong short-term solvency..."
                }
            }
        }
    }
)
async def analyze_financials(
    query: str,
    ticker: str,
    financial_agent: FinancialAnalysisAgent = Depends(get_financial_agent)
):
    """
    Analyze financial metrics and provide insights for a given company.

    Parameters:
    - query: What you want to analyze (e.g., "What are the liquidity ratios?")
    - ticker: Company stock symbol (e.g., "AAPL")

    Example queries:
    - "What are the liquidity ratios for this company?"
    - "Compare profitability ratios between current and previous quarter"
    - "Is the company's financial health improving?"
    - "What's the trend in EBITDA margin?"
    """
    return await financial_agent.analyze(query=query, ticker=ticker)