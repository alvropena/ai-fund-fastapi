from enum import Enum
from typing import Dict, List
from pydantic import BaseModel

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
    metrics: Dict[str, float]

class GroupedMetrics(BaseModel):
    groups: List[MetricGroup]