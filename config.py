import os
from dotenv import load_dotenv

load_dotenv()

FINANCIAL_DATASETS_API_KEY = os.getenv('FINANCIAL_DATASETS_API_KEY')
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
BASE_URL = "https://api.financialdatasets.ai"

HEADERS = {
    "X-API-KEY": FINANCIAL_DATASETS_API_KEY
}
