# Detail
- [[Crew]]을 사용하여 특정 회사의 주가, 재무상태표, 손익계산서, 내부자거래 지표, 뉴스 정보를 토대로 해당 주식을 사는것이 합리적인지를 판단해주는 `AI`이다.
- `yfinance`을 이용해 실시간으로 회사의 대한 금융 정보를 받아왔다.
- `from crewai_tools import tool`을 이용하여 금융 `Custom Tool`을 만들어 `Agent`에게 넘겨주었다.
- `Agents`는 4개로 구성되어 있다.
	- `technical_analyst` : `주가표`을 보고 주식의 움직임을 분석하고 추세, 진입 지점, 저항 및 지지 수준에 대한 인사이트를 제공하는 `Agent`이다.
	- `researcher` : `뉴스`를 보고 해석 및 요약하여 주식을 둘러싼 심리와 뉴스에 대한 포괄적인 개요를 제공하는 `Agent`이다.
	- `financial_analyst` : `재무상태표`, `손익계산서`, `내부자거래`를 보고 주식의 재무 건전성과 성과를 평가하는 `Agent`이다.
	- `hedge_fund_manager` : `technical_analyst`, `researcher`, `financial_analyst`을 활용하여 수익을 극대화하기 위한 전략적 투자 결정을 내리는 `Agent`이다.
- `Tasks`는 4개로 구성되어 있다.
	- `research` : `researcher`가 하는 `Task`이며 주식을 둘러싼 뉴스와 시장 심리을 자세히 요약하고 이러한 요인이 주식 실적에 어떤 영향을 미칠 수 있는지를 알려주어야 하는 `Task`이다.
	- `technical_analysis` : `technical_analyst`가 하는 `Task`이며 주요 지원 및 저항 수준, 차트 패턴 및 기술 지표를 포함하는 상세한 기술 분석 보고서를 만들고 잠재적 진입 지점, 목표 가격 및 고객이 정보에 입각한 투자 결정을 내리는 데 도움이 될 수 있는 기타 관련 정보에 대한 식견을 제공하는 `Task`이다.
	- `finacial_analysis` : `finacial_analysis`가 하는 `Task`이며 회사의 재무 건전성, 성과 및 가치에 대한 식견이 포함된 상세한 재무 분석 보고서를 만들고 주식의 가치와 성장 잠재력을 평가하는 `Task`이다.
	- `investment_recommendation` : `hedge_fund_manager`가 하는 `Task`이며 주식의 잠재적 위험과 보상에 대한 분석을 포함한 자세한 투자 추천 보고서 만들고 기술 분석 및 재무 분석 보고서를 바탕으로 추천에 대한 명확한 근거를 제시하는 `Task`이다.
- `Tool`은 5개로 구성되어 있다.
	- `stock_price` : 한 달 동안의 종목에 대한 주가 정보를 `csv` 형식으로 반환한다.
	- `stock_news` : 주식 종목에 대한 뉴스를 링크를 `List` 형식으로 반환한다.
	- `income_stmt` : 종목에 대한 손익계산서를 `csv` 형식으로 반환한다.
	- `balance_sheet` : 종목에 대한 재무상태표를 `csv` 형식으로 반환한다.
	- `insider_transaction` : 종목에 대한 내부자거래 지표를 `csv` 형식으로 반환한다.
# Code
- `Agent`, `Task`, `Tool`을 각각의 `Class`로 만들어 관리하였다.
## Setting
- 외부에 받아오는 정보가 매우 많기 때문에 `Context Window`가 크고 가격이 `GPT-4o`보다 저렴한 `GPT-4o-mini`을 사용하였다.
```python
import os

os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"
```
## Tools
- 모든 `Tool`은 `yfinance`을 통해 해당 종목에 대한 주식 정보를 받아올 수 있도록 구현하였다.
- `function` 내의 `Description`에 `The input to this tool should be a ticker`을 추가해 `agent`에게 `input` Parameter를 올바르게 받도록 구현하였다.
```python
from crewai_tools import tool
import yfinance as yf

class Tools:

    @tool("One month stock price history")
    def stock_price(ticker):
        """
        Useful to get a month's worth of stock price data as CSV.
        The input of this tool should a ticker, for example AAPL, NET, TSLA etc....
        """
        stock = yf.Ticker(ticker)
        return stock.history(period="1mo").to_csv()

    @tool("Stock news URLs")
    def stock_news(ticker):
        """
        Useful to get URLs of news articles related to a stock.
        The input to this tool should be a ticker, for example AAPL, NET
        """
        stock = yf.Ticker(ticker)
        return list(map(lambda x: x["link"], stock.news))
        
    @tool("Company's income statement")
    def income_stmt(ticker):
        """
        Useful to get the income statement of a stock as CSV.
        The input to this tool should be a ticker, for exampel AAPL, NET
        """
        stock = yf.Ticker(ticker)
        return stock.income_stmt.to_csv()

    @tool("Balance sheet")
    def balance_sheet(ticker):
        """
        Useful to get the balance sheet of a stock as CSV.
        The input to this tool should be a ticker, for example AAPL, NET
        """
        stock = yf.Ticker(ticker)
        return stock.balance_sheet.to_csv()
        
    @tool("Get insider transactions")
    def insider_transaction(ticker):
        """
        Useful to get insider transactions of a stock as CSV.
        The input to this tool should be a ticker, for example AAPL, NET
        """
        stock = yf.Ticker(ticker)
        return stock.insider_transactions.to_csv()
```
## Agents
- `technical_analyst` :  `stock_price tool`을 사용한다.
- `researcher` :  `stock_news tool`과 `SerperDevTool`을 사용해 해당 종목에 대한 `news link`을 가져와  `ScrapeWebsiteTool`로 해당 `Web link`의 정보를 가져올 수 있도록 총 3개의 `Tool`을 사용한다.
- `financial_analyst` :  `balance_sheet tool`, `income_stmt tool`, `insider_transaction tool`을 사용한다.
- `hedge_fund_manager` :  `tool`을 사용하지 않고 다른 `Agents`의 결과를 종합하여 최종 결과를 만든다.
```python
from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

class Agents:

    def technical_analyst(self):
        return Agent(
            role="Technical Analyst",
            goal="Analyses the movements of a stock and provides insights on trends, entry points, resistance and support levels.",
            backstory="An expert in technical analysis, you're known for your ability to predict stock movements and trends based on historical data. You provide valuable insights to your customers.",
            verbose=True,
            tools=[
                Tools.stock_price,
            ],
        )

    def researcher(self):
        return Agent(
            role="Researcher",
            goal="Gathers, interprets and summarizes vasts amounts of data to provide a comprehensive overview of the sentiment and news surrounding a stock.",
            backstory="You're skilled in gathering and interpreting data from various sources to give a complete picture of a stock's sentiment and news. You read each data source carefuly and extract the most important information. Your insights are crucial for making informed investment decisions.",
            verbose=True,
            tools=[
                Tools.stock_news,
                SerperDevTool(),
                ScrapeWebsiteTool(),
            ],
        )
        
    def financial_analyst(self):
        return Agent(
            role="Financial Analyst",
            goal="Uses financial statements, insider trading data, and other financial metrics to evaluate a stock's financial health and performance.",
            backstory="You're a very experienced investment advisor who uses a combination of technical and fundamental analysis to provide strategic investment advice to your clients. You look at a company's financial health, market sentiment, and qualitative data to make informed recommendations.",
            verbose=True,
            tools=[
                Tools.balance_sheet,
                Tools.income_stmt,
                Tools.insider_transaction,
            ],
        )

    def hedge_fund_manager(self):
        return Agent(
            role="Hedge Fund Manager",
            goal="Manages a portfolio of stocks and makes strategic investment decisions to maximize returns using insights from financial analysts, technical analysts, and researchers.",
            backstory="You're a seasoned hedge fund manager with a proven track record of making profitable investment decisions. You're known for your ability to manage risk and maximize returns for your clients.",
            verbose=True,
        )
```
## Tasks
- 각각의 `Tasks`은 `output_file`을 가지고 있어 `Crew` 실행 후, 결과를 `md file`로 볼 수 있다.
- `investment_recommendation`은 다른 `Tasks`의 결과물을 바탕으로 투자 추천 보고서를 만든다.
```python
from crewai import Task

class Tasks:

    def research(self, agent):
        return Task(
            description="Gather and analyze the latest news and market sentiment surrounding the stock of {company}. Provide a summary of the news and any notable shifts in market sentiment.",
            expected_output=f"Your final answer MUST be a detailed summary of the news and market sentiment surrounding the stock. Include any notable shifts in market sentiment and provide insights on how these factors could impact the stock's performance.",
            agent=agent,
            output_file="stock_news.md",
        )

    def technical_analysis(self, agent):
        return Task(
            description="Conduct a detailed technical analysis of the price movements of {company}'s stock and trends identify key support and resistance levels, chart patterns, and other technical indicators that could influence the stock's future performance. Use historical price data and technical analysis tools to provide insights on potential entry points and price targets.",
            expected_output=f"Your final answer MUST be a detailed technical analysis report that includes key support and resistance levels, chart patterns, and technical indicators. Provide insights on potential entry points, price targets, and any other relevant information that could help your customer make informed investment decisions.",
            agent=agent,
            output_file="technical_analysis.md",
        )

    def finacial_analysis(self, agent):
        return Task(
            description="Analyze {company}'s financial statements, insider trading data, and other financial metrics to evaluate the stock's financial health and performance. Provide insights on the company's revenue, earnings, cash flow, and other key financial metrics. Use financial analysis tools and models to assess the stock's valuation and growth potential.",
            expected_output=f"Your final answer MUST be a detailed financial analysis report that includes insights on the company's financial health, performance, and valuation. Provide an overview of the company's revenue, earnings, cash flow, and other key financial metrics. Use financial analysis tools and models to assess the stock's valuation and growth potential.",
            agent=agent,
            output_file="financial_analysis.md",
        )

    def investment_recommendation(self, agent, context):
        return Task(
            description="Based on the research, technical analysis, and financial analysis reports, provide a detailed investment recommendation for {company}'s stock. Include your analysis of the stock's potential risks and rewards, and provide a clear rationale for your recommendation.",
            expected_output=f"Your final answer MUST be a detailed investment recommendation report to BUY or SELL the stock that includes your analysis of the stock's potential risks and rewards. Provide a clear rationale for your recommendation based on the research, technical analysis, and financial analysis reports.",
            agent=agent,
            context=context,
            output_file="investment_recommendation.md",
        )
```
## Crew
- `Crew`의 `process`을 `hierarchical`로 설정하여 `LLM(gpt-4o-mini)`에게 직접 `Task`의 실행을 계획하고, 위임하고, 검증하도록 구현하였다.
- `memory` 기능을 활성화하여 `Task`나 `Agent`가 여러 번 실행되지 않도록 설정하였다.
- `kickoff`의 `input` 값에 `company`(종목)을 넣어 `Task`의 `{} PlaceHolder`안에 값을 채워 `Crew`가 실행되도록 하였다.
```python
from crewai import Crew
from crewai.process import Process
from langchain_openai import ChatOpenAI

agent = Agents()
tasks = Tasks()

researcher = agent.researcher()
technical_analyst = agent.technical_analyst()
financial_analyst = agent.financial_analyst()
hedge_fund_manager = agent.hedge_fund_manager()

researcher_task = tasks.research(researcher)
technical_task = tasks.technical_analysis(technical_analyst)
financial_task = tasks.finacial_analysis(financial_analyst)
recommend_task = tasks.investment_recommendation(
    hedge_fund_manager,
    [
        researcher_task,
        technical_task,
        financial_task,
    ],
)

crew = Crew(
    agents=[
        researcher,
        technical_analyst,
        financial_analyst,
        hedge_fund_manager,
    ],
    tasks=[
        researcher_task,
        technical_task,
        financial_task,
        recommend_task,
    ],
    verbose=2,
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-4o-mini"),
    memory=True,
)

result = crew.kickoff(
    inputs=dict(
        company="Salesforce",
    ),
)
```