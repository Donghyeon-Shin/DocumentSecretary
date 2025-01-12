# Detail
- [[Agent]]의 `OPENAI_FUNCTIONS Agent Type`을 활용하여 회사 이름이 주어졌을 때, 해당 회사의 주식 정보를 탐색해 보여주는 `Page`이다.
- 회사 이름의 `text` 값이 주어지면 4가지의 Tool을 활용하여 주식 정보를 받아오게 된다.
	- `StockMarketSymbolSearchTool` : `DuckDuckGoSearch` 활용하여 회사 이름이 주어지면 해당 회사의 `Stock symbol` 정보를 반환한다.
	- `CompanyOverviewTool` : `Alpha Vantage`의 `API`를 이용해 `Stock symbol` 전반적인 정보를 반환한다.
	- `CompanyIncomeStatementTool` : `Alpha Vantage`의 `API`를 이용해 `Stock symbol`의 수익 정보를 반환한다.
	- `CompanyStackPerformanceTool` : `Alpha Vantage`의 `API`를 이용해 `Stock symbol`의 주가 정보를 반환한다.
- `DuckDuckGoSearch`는 `from langchain.utilities import DuckDuckGoSearchAPIWrapper`를 통해 불러 올 수 있다. `DuckDuckGoSearchAPIWrapper.run()` function 안에 검색할 내용을 입력하면 해당 검색 결과 내용이 출력된다.
- [Alpha Vantage](https://www.alphavantage.co/)는 **주식에 대한 정보나 기업의 뉴스 정보들의 API**을 제공해주는 Site이다. 하루 25번은 무료이며 그 이상은 달에 25달러를 지불해야 한다.
- 각각의 `Tool`을 사용하면서 Prompt의 정보가 쌓이기 때문에 `Context Window`가 적은 `Model`의 경우 `Tool`의 사용하는 과정에서 오류가 날 수 있다. 따라서 `Context Window` 큰 `Model`을 사용해야 한다.
# Code
- `Alpha Vantage`의 API를 사용하기 위해선 개인의 `Api Key`가 필요하기 때문에 `import os`의 `.environ.get` function을 통해 `alpha_vantage_api_key`을 가져오도록 구현하였다.
- `import requests`의 `.get` function을 통해 외부 `API` 값을 가져올 수 있다.
- `SystemMessage`을 활용하여 `Agent`의 [[Prompt]]를 수정하여 `input`으로 회사 이름이 주어질 시 4개의 Tool이 모두 사용될 수 있도록 구현하였다.
- `StockMarketSymbolSearchTool`은 회사 이름을 받으면 `DuckDuckGoSearch`의 실행 할 수 있는 `Query`를 출력하여 `DuckDuckGoSearchAPIWrapper` 활용해 `Stock symbol` 정보를 반환한다.
- `CompanyStockSearchArgsSchema` 이용하여 `LLM`에게 `Stock symbol` 정보 값을 바탕으로 구체적인 `Stock symbol`을 요청하고 이를 통해 얻은 값을 활용하여 `CompanyOverviewTool`, `CompanyIncomeStatementTool`, `CompanyStackPerformanceTool`에 사용한다. **(이를 각각 Tool의 description에서 "You should enter a stock symbol."로 명시하고 있다.)**
- `CompanyStackPerformanceTool`에서 사용하는 `API`의 결과 값들은 그대로 쓰기엔 내용이 많기 때문에 Model의 `Context Window`을 초과할 수 있다. 따라서 `json` 값을 `List`화 하여 최근의 내용만 가져오도록 구현하였다.
- 최종 결과 값은 `json`형태이기 때문에 `["output"]` key 값만 가져와 `Page`에 출력한다.
```python
import streamlit as st
import os
import requests
from typing import Type
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.agents import initialize_agent, AgentType
from langchain.schema import SystemMessage
from langchain.utilities import DuckDuckGoSearchAPIWrapper

llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo-0125",)

alpha_vantage_api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")

class CompanyStockSearchArgsSchema(BaseModel):
    symbol: str = Field(description="Stock symbol of the company.Example: AAPL, TSLA")

class StockMarketSymbolSearchToolArgsSchema(BaseModel):
    query: str = Field(description="The query you will search for")

class CompanyStackPerformanceTool(BaseTool):
    name: Type[str] = "CompanyStackPerformance"
    description: Type[str] = """
    Use this to get the weekly performance of a company stock.
    You should enter a stock symbol.
    """
    args_schema: Type[CompanyStockSearchArgsSchema] = CompanyStockSearchArgsSchema

    def _run(self, symbol):
        r = requests.get(
            f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={alpha_vantage_api_key}"
        )
        response = r.json()
        return list(response["Weekly Time Series"].items())[:200]
        
class CompanyIncomeStatementTool(BaseTool):
    name: Type[str] = "CompanyIncomeStatement"
    description: Type[str] = """
    Use this to get an income statement of a company.
    You should enter a stock symbol.
    """
    args_schema: Type[CompanyStockSearchArgsSchema] = CompanyStockSearchArgsSchema

    def _run(self, symbol):
        r = requests.get(
            f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={alpha_vantage_api_key}"
        )
        return r.json()["annualReports"]

class CompanyOverviewTool(BaseTool):
    name: Type[str] = "CompanyOverview"
    description: Type[str] = """
    Use this to get an overview of the financials of the company.
    You should enter a stock symbol.
    """    
    args_schema: Type[CompanyStockSearchArgsSchema] = CompanyStockSearchArgsSchema

    def _run(self, symbol):
        r = requests.get(
            f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={alpha_vantage_api_key}"
        )
        return r.json()

class StockMarketSymbolSearchTool(BaseTool):
    name: Type[str] = "StockMarketSymbolSearch"
    description: Type[str] = """
    Use this tool to find the stock market symbool for a company.
    It takes a query as an argument.
    Example query: Stock Market Symbol for Apple Company.
    """
    args_schema: Type[StockMarketSymbolSearchToolArgsSchema] = (
        StockMarketSymbolSearchToolArgsSchema
    )

    def _run(self, query):
        ddg = DuckDuckGoSearchAPIWrapper()
        return ddg.run(query)

agent = initialize_agent(
    llm=llm,
    verbose=True,
    agent=AgentType.OPENAI_FUNCTIONS,
    handle_parsing_errors=True,
    tools=[
        StockMarketSymbolSearchTool(),
        CompanyOverviewTool(),
        CompanyIncomeStatementTool(),
        CompanyStackPerformanceTool(),
    ],
    agent_kwargs={
        "system_message": SystemMessage(
            content="""
            You are a hedge fund manager.

            You evaluate a company and provide your opinion and reasons why the stock is a boy or not.

            Consider the performance of a stock, the company overview and the inocome statement

            Be assertive in your judgement and recommend the stock or advise teh user against it.
            """
        )
    },
)

st.set_page_config(
    page_title="Investor GPT",
    page_icon="🤣",
)

st.markdown(
    """
    # Investor GPT
  
    Welcome to Investor GPT.

    Write down the name of a company and our Agent will do the resaerch for you.
    """
)

company = st.text_input("Write the name of company you are interested on.")

if company:
    result = agent.invoke(company)
    st.write(result["output"].replace("$","\$"))
```