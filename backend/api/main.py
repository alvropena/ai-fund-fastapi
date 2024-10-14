from fastapi import FastAPI
from api.endpoints import stocks, news

app = FastAPI(title="AI Financial Analyst API")

app.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])
app.include_router(news.router, prefix="/news", tags=["News"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Financial Analyst API"}
