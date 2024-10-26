from backend.models import RatioResponse, IncomeStatementModel
from backend.api.endpoints import financials
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

@router.get("/ebitda-margin/{ticker}", response_model=RatioResponse)
async def get_ebitda_margin(
    ticker: str,
    period: str = "annual",
    limit: int = 1,
    income_statements: IncomeStatementModel = Depends(financials.get_income_statements)
):
    try:
        if not income_statements or not income_statements.income_statements:
            raise HTTPException(status_code=404, detail="Income statement data not found")
        
        latest_income_statement = income_statements.income_statements[0]
        revenue = latest_income_statement.revenue
        ebit = latest_income_statement.ebit        
        
        if revenue == 0:
            raise HTTPException(status_code=400, detail="Revenue is zero, cannot calculate ratio")
        
        ebitda = ebit
        ebitda_margin = ebitda / revenue
        
        return RatioResponse(
            ticker=ticker,
            ratio_name="EBITDA Margin",
            ratio_value=ebitda_margin,
            date=latest_income_statement.calendar_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
   