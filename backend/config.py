import os
from dotenv import load_dotenv

load_dotenv()

FINANCIAL_DATASETS_API_KEY = os.getenv('FINANCIAL_DATASETS_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
