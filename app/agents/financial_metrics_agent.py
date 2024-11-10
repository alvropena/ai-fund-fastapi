from langchain_openai import OpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from typing import Dict, List
from app.endpoints.financial_datasets.financials import get_balance_sheets, get_income_statements
from app.agents.financial_metrics import FinancialMetrics

class FinancialMetricsAgent:
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

        Tools available: {tool_names}

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
            
            balance_sheet_data = await get_balance_sheets(ticker=ticker, period="annual", limit=1)
            income_statement_data = await get_income_statements(ticker=ticker, period="annual", limit=1)
            
            if not balance_sheet_data.balance_sheets or not income_statement_data.income_statements:
                return {"error": f"No financial data available for {ticker}"}

            balance_sheet = balance_sheet_data.balance_sheets[0]
            income_statement = income_statement_data.income_statements[0]
            
            ratios = {
                "liquidity_ratios": self.metrics.calculate_liquidity_ratios(balance_sheet),
                "profitability_ratios": self.metrics.calculate_profitability_ratios(income_statement, balance_sheet),
                "leverage_ratios": self.metrics.calculate_leverage_ratios(balance_sheet),
                "efficiency_ratios": self.metrics.calculate_efficiency_ratios(income_statement, balance_sheet)
            }
                        
            if any(not ratio for ratio in ratios.values()):
                return {"error": f"Invalid ratio calculations for {ticker}"}
                
            return ratios
            
        except Exception as e:
            return {"error": f"Error calculating ratios for {ticker}: {str(e)}"}

    async def analyze(self, query: str, ticker: str) -> str:
        """Process a financial calculation query"""
        result = await self.agent_chain.ainvoke(
            {"input": f"For company {ticker}: {query}"}
        )
        return result["output"]