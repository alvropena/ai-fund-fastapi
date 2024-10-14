from fastapi import FastAPI
from api.endpoints import company, financials, insider_transactions, prices

app = FastAPI(title="AI Financial Analyst API")

app.include_router(company.router, prefix="/company", tags=["Company"])
app.include_router(financials.router, prefix="/financials", tags=["Financials"])
app.include_router(insider_transactions.router, prefix="/insider-transactions", tags=["Insider Transactions"])
app.include_router(prices.router, prefix="/prices", tags=["Prices"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Financial Analyst API"}
