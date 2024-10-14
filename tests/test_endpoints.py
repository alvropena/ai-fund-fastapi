from fastapi.testclient import TestClient
from api.main import app  # Import your FastAPI app

client = TestClient(app)

# Test for Root Endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI Financial Analyst API"}


# Test for Financials Endpoint (example: Income Statements)
def test_get_income_statements():
    ticker = "AAPL"
    response = client.get(f"/financials/income-statements/{ticker}")
    assert response.status_code == 200
    assert "ticker" in response.json()
    assert "dcf_value" in response.json()


# Test for Insider Transactions
def test_get_insider_transactions():
    ticker = "AAPL"
    response = client.get(f"/insider-transactions/{ticker}?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)  # Example check if it's a dict

# Test for Price Snapshot
def test_get_price_snapshot():
    ticker = "AAPL"
    response = client.get(f"/prices/snapshot/{ticker}")
    assert response.status_code == 200
    assert "price" in response.json()  # Example check if "price" field is in the response
