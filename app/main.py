from app.endpoints.financial_datasets import company, financials, insider_transactions, prices
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import metrics

app = FastAPI(title="AI Fund API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://ai-fund-nextjs.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(company.router, prefix="/company", tags=["Company"])
app.include_router(financials.router, prefix="/financials", tags=["Financials"])
app.include_router(insider_transactions.router, prefix="/insider-transactions", tags=["Insider Transactions"])
app.include_router(prices.router, prefix="/prices", tags=["Prices"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])