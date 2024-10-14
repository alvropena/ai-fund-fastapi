import requests
import pandas as pd
from backend.config import FINANCIAL_DATASETS_API_KEY

BASE_URL = "https://api.financialdatasets.ai/"

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
