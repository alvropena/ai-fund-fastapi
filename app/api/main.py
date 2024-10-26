from fastapi import FastAPI
from backend.api.endpoints import company, financials, insider_transactions, prices
from backend.api.endpoints.ratios import ratios
from backend.api.endpoints.ratios import ebitda_ratios, efficiency_ratios, leverage_ratios, liquidity_ratios
from backend.api.endpoints.ratios.ratios import router as ratios_router

app = FastAPI(title="AI Financial Analyst API")

app.include_router(company.router, prefix="/company", tags=["Company"])
app.include_router(financials.router, prefix="/financials", tags=["Financials"])
app.include_router(insider_transactions.router, prefix="/insider-transactions", tags=["Insider Transactions"])
app.include_router(prices.router, prefix="/prices", tags=["Prices"])
app.include_router(ratios.router, prefix="/ratios", tags=["Ratios"])
app.include_router(ebitda_ratios.router, prefix="/ebitda_ratios", tags=["EBITDA Ratios"])
app.include_router(efficiency_ratios.router, prefix="/efficiency_ratios", tags=["Efficiency Ratios"])
app.include_router(leverage_ratios.router, prefix="/leverage_ratios", tags=["Leverage Ratios"])
app.include_router(liquidity_ratios.router, prefix="/liquidity_ratios", tags=["Liquidity Ratios"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Financial Analyst API"}
