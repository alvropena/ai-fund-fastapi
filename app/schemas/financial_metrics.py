from enum import Enum
from typing import Dict, List, Optional, Any, Union
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
    metrics: Dict[str, Optional[float]]

class GroupedMetrics(BaseModel):
    """Pydantic model for grouped financial metrics with nullable values"""
    groups: List[MetricGroup]
    liquidity: Dict[str, Optional[float]]
    ebitda: Dict[str, Optional[float]]
    leverage: Dict[str, Optional[float]]
    efficiency: Dict[str, Optional[float]]
    profitability: Dict[str, Optional[float]]
    dupont: Dict[str, Optional[float]]
    economic_value: Dict[str, Optional[float]]
    stock_performance: Dict[str, Union[float, str, None]]

    class Config:
        from_attributes = True