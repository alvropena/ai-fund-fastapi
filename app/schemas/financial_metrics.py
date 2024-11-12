from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel
from datetime import date
class MetricCategory(str, Enum):
    LIQUIDITY = "liquidity"
    EBITDA = "ebitda"
    LEVERAGE = "leverage"
    EFFICIENCY = "efficiency"
    PROFITABILITY = "profitability"
    DUPONT = "dupont"
    ECONOMIC_VALUE = "economic_value"
    STOCK_PERFORMANCE = "stock_performance"

class MetricGroup(BaseModel):
    category: MetricCategory
    metrics: Dict[str, Optional[float]]

class GroupedMetrics(BaseModel):
    """Pydantic model for grouped financial metrics"""
    period: str
    report_date: date
    groups: List[MetricGroup]

    class Config:
        from_attributes = True