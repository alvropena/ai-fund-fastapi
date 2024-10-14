from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class IncomeStatement(Base):
    __tablename__ = 'income_statements'
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    fiscal_date = Column(Date)
    revenue = Column(Float)
    net_income = Column(Float)
    # Add other relevant fields

# Define other models similarly
