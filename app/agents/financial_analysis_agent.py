from langchain_openai import OpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from typing import Dict, List
from pydantic import BaseModel
from app.endpoints.financials import get_balance_sheets, get_income_statements

class FinancialMetrics(BaseModel):
    """Container for all financial metrics calculations"""
    
    def calculate_liquidity_ratios(self, balance_sheet: Dict) -> Dict:
        return {
            "current_ratio": balance_sheet["current_assets"] / balance_sheet["current_liabilities"],
            "acid_test_ratio": (balance_sheet["current_assets"] - balance_sheet["inventory"]) / balance_sheet["current_liabilities"],
            "defensive_interval_ratio": balance_sheet["cash_and_equivalents"] / balance_sheet["current_liabilities"]
        }
    
    def calculate_ebitda_ratios(self, income_statement: Dict, cash_flow_statement: Dict) -> Dict:
        return {
            "ebitda": income_statement["ebit"] + cash_flow_statement["depreciation_and_amortization"],
            "ebitda_margin": (income_statement["ebit"] + cash_flow_statement["depreciation_and_amortization"]) / income_statement["revenues"]
        }
    
    def calculate_leverage_ratios(self, balance_sheet: Dict) -> Dict:
        return {
            "debt_ratio": balance_sheet["total_liabilities"] / balance_sheet["total_assets"],
            "solvency_ratio": (balance_sheet["total_liabilities"] + balance_sheet["shareholders_equity"]) / balance_sheet["total_assets"],
            "leverage": balance_sheet["total_assets"] / (balance_sheet["total_liabilities"] + balance_sheet["shareholders_equity"])
        }

    def calculate_efficiency_ratios(self, income_statement: Dict, balance_sheet: Dict) -> Dict:
        # Calculate base turnover ratios
        inventory_turnover = income_statement["cost_of_revenue"] / balance_sheet["inventory"]
        receivables_turnover = income_statement["revenue"] / balance_sheet["trade_and_non_trade_receivables"]
        payables_turnover = income_statement["cost_of_revenue"] / balance_sheet["trade_and_non_trade_payables"]
        asset_turnover = income_statement["revenues"] / balance_sheet["total_assets"]
        
        return {
            "inventory_turnover": inventory_turnover,
            "stock_retention_period": 365 / inventory_turnover,
            "accounts_receivable_turnover": receivables_turnover,
            "collection_period": 365 / receivables_turnover,
            "accounts_payable_turnover": payables_turnover,
            "payment_period": 365 / payables_turnover,
            "asset_turnover": asset_turnover
        }

    def calculate_profitability_ratios(self, income_statement: Dict, balance_sheet: Dict) -> Dict:
        return {
            "sales_margin": income_statement["net_income"] / income_statement["revenues"],
            "return_on_assets": income_statement["net_income"] / balance_sheet["total_assets"],
            "return_on_equity": income_statement["net_income"] / (balance_sheet["total_assets"] + balance_sheet["total_liabilities"])
        }

    def calculate_dupont_ratios(self, income_statement: Dict, balance_sheet: Dict) -> Dict:
        return {
            "sales_margin": income_statement["net_income"] / income_statement["revenues"],
            "asset_turnover": income_statement["revenues"] / balance_sheet["total_assets"],
            "leverage": balance_sheet["total_assets"] / (balance_sheet["total_liabilities"] + balance_sheet["total_assets"])
        }
    
    def calculate_economic_value_ratios(
        self, 
        income_statement: Dict, 
        balance_sheet: Dict, 
        cost_of_equity: float
    ) -> Dict:
        sales_margin = income_statement["net_income"] / income_statement["revenues"]
        asset_turnover = income_statement["revenues"] / balance_sheet["total_assets"]
        leverage = balance_sheet["total_assets"] / (balance_sheet["total_liabilities"] + balance_sheet["total_assets"])
        
        roe = sales_margin * asset_turnover * leverage
        economic_margin = roe - cost_of_equity
        eva = economic_margin * (balance_sheet["total_assets"] + balance_sheet["total_liabilities"])
        
        return {
            "economic_margin": economic_margin,
            "economic_value_added": eva
        }

    def calculate_stock_performance_ratios(
        self,
        income_statement: Dict,
        balance_sheet: Dict,
        cash_flow_statement: Dict,
        stock_price: float
    ) -> Dict:
        outstanding_shares = balance_sheet["outstanding_shares"]
        net_income = income_statement["net_income"]
        total_equity = balance_sheet["total_assets"] + balance_sheet["total_liabilities"]
        dividends = cash_flow_statement["dividends_and_other_cash_distributions"]

        # Guard against division by zero
        if outstanding_shares == 0:
            return {
                "error": "Cannot calculate ratios - outstanding shares is zero"
            }

        earnings_per_share = net_income / outstanding_shares
        dividends_per_share = dividends / outstanding_shares
        market_value = stock_price * outstanding_shares
        market_value_added = market_value - total_equity
        
        result = {
            "earnings_per_share": earnings_per_share,
            "dividends_per_share": dividends_per_share,
            "market_value": market_value,
            "market_value_added": market_value_added,
        }

        # Only calculate P/E ratio if EPS is not zero
        if earnings_per_share != 0:
            result["price_to_earnings_ratio"] = stock_price / earnings_per_share

        return result

class FinancialAnalysisAgent:
    def __init__(self):
        self.llm = OpenAI(temperature=0.2)
        self.metrics = FinancialMetrics()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.tools = self._setup_tools()
        self.agent_chain = self._setup_agent_chain()

    def _setup_tools(self) -> List[Tool]:
        return [
            Tool(
                name="CalculateRatios",
                func=self._calculate_all_ratios,
                description="Calculate financial ratios for a given company ticker"
            )
        ]
    
    def _setup_agent_chain(self) -> AgentExecutor:
        prompt = PromptTemplate.from_template(
            """You are a financial calculator that provides ratio calculations. You do not provide analysis or comparisons, only calculations and their explanations.

        {tools}

        Use this format:
        Question: the input question you must answer
        Thought: consider which ratios need to be calculated
        Action: CalculateRatios
        Action Input: the ticker symbol
        Observation: the calculated ratios
        Thought: explain the calculated numbers
        Final Answer: explain what each calculated number represents without providing analysis or recommendations

        Question: {input}
        {agent_scratchpad}"""
        )

        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )

        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            return_intermediate_steps=False,
            output_key="output"
        )

    async def _calculate_all_ratios(self, ticker: str) -> Dict:
        """Calculate all financial ratios for a given ticker"""
        try:
            balance_sheet_data = get_balance_sheets(ticker=ticker, period="annual", limit=1)
            income_statement_data = get_income_statements(ticker=ticker, period="annual", limit=1)
            
            balance_sheet = balance_sheet_data.balance_sheets[0]  # Most recent
            income_statement = income_statement_data.income_statements[0]  # Most recent

            return {
                "liquidity_ratios": self.metrics.calculate_liquidity_ratios(balance_sheet),
                "profitability_ratios": self.metrics.calculate_profitability_ratios(income_statement, balance_sheet),
                "leverage_ratios": self.metrics.calculate_leverage_ratios(balance_sheet),
                "efficiency_ratios": self.metrics.calculate_efficiency_ratios(income_statement, balance_sheet)
            }
        except Exception as e:
            return {"error": f"Error calculating ratios: {str(e)}"}

    async def analyze(self, query: str, ticker: str) -> str:
        """Process a financial calculation query"""
        result = await self.agent_chain.ainvoke(
            {"input": f"For company {ticker}: {query}"}
        )
        return result["output"]