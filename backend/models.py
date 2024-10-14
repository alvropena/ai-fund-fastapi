from pydantic import BaseModel
from typing import List

# Models for POST requests
class FinancialSearchPayload(BaseModel):
    period: str = "annual"
    limit: int = 50
    filters: List[dict]
    order: str = "asc"

class LineItemsPayload(BaseModel):
    line_items: List[str]
    tickers: List[str]
    period: str = "annual"
    limit: int = 2
