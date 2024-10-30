from langchain_openai import OpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from typing import Dict, List
from pydantic import BaseModel

class FinancialMetrics(BaseModel):
    """Container for all financial metrics calculations"""
    
    def calculate_liquidity_ratios(self, balance_sheet: Dict) -> Dict:
        return {
            "current_ratio": balance_sheet["current_assets"] / balance_sheet["current_liabilities"],
            "acid_test_ratio": (balance_sheet["current_assets"] - balance_sheet["inventory"]) / balance_sheet["current_liabilities"],
            "defensive_interval_ratio": balance_sheet["cash_and_equivalents"] / balance_sheet["current_liabilities"]
        }
    
    def calculate_profitability_ratios(self, income_statement: Dict, balance_sheet: Dict) -> Dict:
        return {
            "sales_margin": income_statement["net_income"] / income_statement["revenues"],
            "return_on_assets": income_statement["net_income"] / balance_sheet["total_assets"],
            "return_on_equity": income_statement["net_income"] / balance_sheet["total_equity"]
        }
    
    def calculate_ebitda_ratios(self, income_statement: Dict) -> Dict:
        return {
            "ebitda_margin": income_statement["ebit"] / income_statement["revenue"]
        }
    
    def calculate_dupont_ratios(self, income_statement: Dict, balance_sheet: Dict) -> Dict:
        return {
            "sales_margin": income_statement["net_income"] / income_statement["revenues"],
            "asset_turnover": income_statement["revenues"] / balance_sheet["total_assets"],
            "leverage": balance_sheet["total_assets"] / balance_sheet["total_equity"]
        }
    
    def calculate_economic_value_ratios(
        self, 
        income_statement: Dict, 
        balance_sheet: Dict, 
        cost_of_equity: float
    ) -> Dict:
        roe = income_statement["net_income"] / balance_sheet["total_equity"]
        economic_margin = roe - cost_of_equity
        eva = economic_margin * balance_sheet["total_equity"]
        
        return {
            "economic_margin": economic_margin,
            "economic_value_added": eva
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
    
    def calculate_leverage_ratios(self, balance_sheet: Dict) -> Dict:
        return {
            "debt_ratio": balance_sheet["total_liabilities"] / balance_sheet["total_assets"],
            "solvency_ratio": balance_sheet["shareholders_equity"] / balance_sheet["total_assets"],
            "leverage": balance_sheet["total_assets"] / balance_sheet["shareholders_equity"]
        }

    def calculate_stock_performance_ratios(
        self,
        income_statement: Dict,
        balance_sheet: Dict,
        stock_price: float
    ) -> Dict:
        outstanding_shares = balance_sheet["shares_outstanding"]
        net_income = income_statement["net_income"]
        total_equity = balance_sheet["total_equity"]
        dividends = income_statement.get("dividends", 0)

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
                description="Calculate all financial ratios for a given company"
            ),
            Tool(
                name="AnalyzeRatios",
                func=self._analyze_ratios,
                description="Provide analysis of financial ratios"
            ),
            Tool(
                name="CompareRatios",
                func=self._compare_ratios,
                description="Compare ratios between periods or companies"
            )
        ]
    
    def _setup_agent_chain(self) -> AgentExecutor:
        prompt = PromptTemplate.from_template(
            """You are a financial analyst assistant. Use the following tools to help answer questions:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

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

    def _calculate_all_ratios(self, ticker: str) -> Dict:
        # Implement comprehensive ratio calculation
        pass

    def _analyze_ratios(self, ratios: Dict) -> str:
        # Implement ratio analysis
        pass

    def _compare_ratios(self, ratios_a: Dict, ratios_b: Dict) -> str:
        # Implement ratio comparison
        pass

    async def analyze(self, query: str, ticker: str) -> str:
        """Process a financial analysis query"""
        result = await self.agent_chain.ainvoke(
            {"input": f"For company {ticker}: {query}"}
        )
        return result["output"]