import requests
import pandas as pd
from backend.config import FINANCIAL_DATASETS_API_KEY

BASE_URL = "https://api.financialdatasets.ai/"

from database import SessionLocal
from models import IncomeStatement
from sqlalchemy.orm import Session
from datetime import datetime

def store_income_statements(ticker, data):
    db: Session = SessionLocal()
    for record in data['data']:
        income = IncomeStatement(
            ticker=ticker,
            fiscal_date=datetime.strptime(record['fiscalDateEnding'], '%Y-%m-%d'),
            revenue=record['totalRevenue'],
            net_income=record['netIncome']
            # Add other fields accordingly
        )
        db.add(income)
    db.commit()
    db.close()

def get_income_statements(ticker, period='annual', limit=5):
    endpoint = f"{BASE_URL}/financials/income-statements"
    params = {
        'ticker': ticker,
        'period': period,
        'limit': limit,
        'apikey': FINANCIAL_DATASETS_API_KEY
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def main():
    ticker = 'AAPL'
    income_data = get_income_statements(ticker)
    df = pd.DataFrame(income_data['data'])
    print(df)

if __name__ == "__main__":
    main()
