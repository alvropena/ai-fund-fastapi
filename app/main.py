from app.endpoints.financial_datasets import company, financials, insider_transactions, prices
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import metrics
import os

app = FastAPI(title="AI Fund API")

# Get port from environment variable with Railway's default
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)