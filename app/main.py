from fastapi import FastAPI, Depends
from app.endpoints import company, financials, insider_transactions, prices, metrics

app = FastAPI(title="AI Financial Analyst API")

app.include_router(company.router, prefix="/company", tags=["Company"])
app.include_router(financials.router, prefix="/financials", tags=["Financials"])
app.include_router(insider_transactions.router, prefix="/insider-transactions", tags=["Insider Transactions"])
app.include_router(prices.router, prefix="/prices", tags=["Prices"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])