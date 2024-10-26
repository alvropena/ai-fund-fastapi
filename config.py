import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# API Key and Base URL for financialdatasets.ai
FINANCIAL_DATASETS_API_KEY = os.getenv('FINANCIAL_DATASETS_API_KEY')
BASE_URL = "https://api.financialdatasets.ai"

# Headers to be used in all requests
HEADERS = {
    "X-API-KEY": FINANCIAL_DATASETS_API_KEY
}
