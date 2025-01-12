Chat
[GPT Action](https://chatgpt.com/gpts)
-> 기본적인 plugin들이 미리 설치되어 있다. (ex. RAG을 위한 document가 load되어 있다던가)

여기 안에 있는 plugin들은 모두 API이다. 우리는 Chat GPT에게 API의 존재를 알려주는 것만 수행하면 된다.

`Cloudflare` - Command line utility tool인데 나의 localhost 주소를 외부로 노출시킬 수 있게 해준다. 우리가 localhost로  서버를 열고 cloudflare를 실행시키면 cloudflared가 우리에게 https url을 넘겨줄 것이다.

----

Amazon Bedrock은 AWS의 서비스이다. foundation models를 제공한다.

model types - Amazon Titan, Jurassic, Claude, Command, Llama2, Stable Difffusion

Claude - OpenAI에서 나간 사람이 `ANTHROPIC`이라는 회사를 만들어 GPT-4의 COPY한 Model이다.
20만 token 가량의 거대한 contextg window을 가지고 있다.


azure - MS가 openAI model을 사용할 수 있도록 한 System인데, MS는 내가 model에게 보내는 내용을 볼 수 있다. NOT Private. 

---

# CrewAI Concept
serper -> python에서 google 검색을 할 수 있게 해준다. 무료는 아니지만 2500개의 무료 쿼리를 제공한다.


대부분의 LLM Model은 Crew의 결과값이 좋지 않다. 그래서 GPT-4 or GPT-4o가 crew를 사용했을 때 결과값이 좋게 나온다.
큰 Context window가 필요하다.

Crew -> 일련의 작업을 달성하기 위해 함께 일하는 agent들로 이루어진 그룹을 말한다.
Crew을 만들기 위해서는 Tasks랑 Agents가 필요하다. (TEAM)
- Crew에서 tasks와 agents을 지정하는데 일반적으로 tasks는 넣는 순서가 존재한다. ( 후에 바꿀 수도 있음)


process / 기본 : sequential - 처음부터 끝까지 순서대로 실행되는 방법이다. / 계층형 : hierarchy - 관리형 `LLM` 직접 Task의 실행을 계획하고, 위임하고, 검증한다. manager_llm model을 따로 설정해주어야 한다.

Memory=True / Crew을 위해 Short-Time(현재 실행), Long-Time(지난 실행), Entity(사람, 장소, 개념 같은 Entitiy를 기억), Contextual Memory(상호작용의 Context를 기억한다.)을 활성화 할 수 있다. (memory를 embedding하고 Verctor Search를 수행하기 때문에 추가로 돈이 든다.)
원한다면 embedder을 딸로 지정할 수 있다. (기본값 openAI embedder)


Agent - 작업을 수행하고 결정을 내리고 다른 agent들과 통신 할 수 있는 자율 단위를 말한다.
(특정 스킬로 특정 업무를 수행하는 팀의 구성원) **하는 일을 구체적으로 명시해야 한다.** -> `LLM`에게 많은 것을 하라고 하면 잘 수행하지 못하지만, 하나의 것을 수행하라고 하면 엄청 잘 수행한다. (MEMBER)
- Perform tasks
- Make decisions
- Communicate with other agents
Agent(attribute)
- Role이 있어야 하는데 crew안에서 agent의 역할을 정해주는 것이다.
- Goal : 해당 Agent의 원하는 결과
- Backstory : `LLM`이 역할극을 시켰을 때 더 잘 작동한다는 사실이 밝혀져 이를 이용하기 위해 존재한다.
- verbose = True, console에서 Agent의 내용을 보여줌
- allow_delegation = 다른 agent나 tool을 사용할 수 있도록 하는 기능이다. 만약 해당 기능을 사용하지 않을 것이라면 `False`로 설정해야 한다. 아니면 `Agent`가 지 맘대로 다른 `agent`와 통신하려고 시도하면서 오류가 발생한다. (물론 CrewAI가 errorHandling이 되어 있어 동작이 멈추지는 않는다. Awsome!! )

`You want to impress your coworkers with your work.` 이 내용을 추가하면 `LLM`에게 무언가 요구할 때 더 효과를 볼 수 있다.

Agent가 tool을 사용할 때, 원하는 결과가 나오지 않아 게속 tool을 사용하는 경우가 발생한다. 이는 과한 token을 만들어내며 우리를 거지로 만든다. 따라서 우리는 2가지 옵션으로 이를 저지할 수 있 다. 1) max_execution_time : 최대 실행 시간 / 2) Max Iter : 최대 실행 횟수

Task - agent가 완료시키는 특정 과제를 말한다. (JUST TASK)

Task(attribute)
- description 
- agent
- **expected output** : 결과가 어떤식으로 나올지에 대해 구현할 수 있다.
- context: 해당 task에 다른 task의 output이 필요하다고 얘기하는 거임
- human_input=True : `Agnet`가 Task를 실행하고 나서 해당 값읋 승인이나 거절을 요청하도록 하는 확인 메시지를 보낸다.
- async_execution=True : **비동기실행** - 서로에 대한 의존성이 없는 동시에 실행 가능한 여러 개의 Task를 가질 수 있다...!(동시에 여러 Task를 돌릴수 있다는 얘기)
-
 
```python
crew = Crew(
    tasks=[
        normal_recipe,
        healthy_recipe,
    ],
    agents=[
        international_chef,
        healthy_chef,
    ],
)
```


---
# Setting CrewAI Model
```python
import os

os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"
```

만약 Ollama 같은 model을 사용하고 싶으면
환경 변수를 `NA`로 채운 뒤 ChatOpenAI로 model을 만든 뒤, base_url를 채우면 된다.
```python
import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_MODEL_NAME"] = "NA"

llm = ChatOpenAI(
	model = "llama2:13b",
	base_url = "https://localhost:11434.v1"
)
```

---
# Search Google and Script blog post
```python
from crewai import Crew, Agent, Task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

researcher = Agent(
    role="Senior Researcher",
    goal="Search the web, extract and analyze information",
    backstory="""
    You produce the highest quality research possible.
    You use multiple sources of information and you always double check your
    sources to make sure they are true and up to date.
    You want to impress your coworkers with your work.
    """,
    allow_delegation=False,
    verbose=True,
    tools=[
        search_tool,
        scrape_tool,
    ],
    max_iter=10,
)

editor = Agent(
    role="Senior Writer/Editor",
    goal="Write engaging blog posts.",
    backstory="""
    You write content that keeps people engaged and entertained.
    Your content is easy to read it is informative and it makes poeple want to share it with their friends.
    You are working ffor a very important client.
    """,
    verbose=True,
)

task = Task(
    description="Write a blog post about {topic}",
    agent=editor,
    expected_output="A blog post with an introduction, at least three sub-sections off content, links to sources, a set of suggested hashtags for social media and a catchy title.",
    output_file="blog_post.md",
)

crew = Crew(
    agents=[researcher, editor],
    tasks=[
        task,
    ],
    verbose=True,
)

result = crew.kickoff(
    inputs=dict(
        topic="The biggest box offfice flops of 2024",
    ),
)
```

---
# pydantic
`pydantic`으로 output 형태를 설정할 수 있다.
`output_json=BlogPost,`로 불러오면 json 형태의 output값이 만들어진다.
```python
from pydantic import BaseModel
from typing import List

class SubSection(BaseModel):
    title: str
    content: str

class BlogPost(BaseModel):
    title: str
    introduction: str
    sections: List[SubSection]
    sources: List[str]
    hashtags: List[str]
    
task = Task(
    description="Write a blog post about {topic}",
    agent=editor,
    expected_output="A blog post with an introduction, at least three sub-sections of content, links to sources, a set of suggested hashtags for social media and a catchy title.",
    output_file="blog_post.md",
    output_json=BlogPost,
)
```

---
# Create Youtube Script

```python
from crewai import Crew, Agent, Task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, YoutubeChannelSearchTool
  
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
youtube_tool = YoutubeChannelSearchTool()

researcher = Agent(
    role="Senior Researcher",
    goal="Search the web, extract and analyze information.",
    backstory="""
    You produce the highest quality research possible.
    You use multiple sources of information and you always double check your sources to make sure they are true and up to date.
    You want to impress your coworkers with your work.
    """,
    allow_delegation=False,
    tools=[
        search_tool,
        scrape_tool,
        youtube_tool,
    ],
    max_iter=10,
    verbose=True,
)


marketer = Agent(
    role="Senior Marketer",
    goal="Come up with ideas that generate viral and useful content.",
    backstory="""
    You work at a marketing agency.
    You are the best at coming up with ideas to make content go viral.
    Your ideas are used for video, advertising, social media marketing, the content you produce appeals to a young audience.
    """,
    verbose=True,
)

writer = Agent(
    role="Senior Writer",
    goal="Write scripts for viral Youtube videos.",
    backstory="""
    You write scripts for videos that keep people engaged and entertained.
    Your content is easy and fun to watch, it is informative and it makes people want to share it with their friends.
    You are working for a very important client.
    """
    verbose=True,
)

brainstorm_task = Task(
    description="Come up with 5 video ideas for a Youtube channel in the {industry} industry",
    agent=marketer,
    expected_output="Your answer MUST be a list of 5 ideas for a Youtube video with an explanation of what the angle of the video would be.",
    output_file="ideas_task.md",
    human_input=True,
)

selection_task = Task(
    description="Select a video idea that has the highest potential of going viral.",
    agent=writer,
    expected_output="Your answer MUST include the idea that was selected as well as an explanation of why that selection was made.",
    human_input=True,
    context=[
        brainstorm_task,
    ],
    output_file="selection_task.md",
)

research_task = Task(
    description="Do all the research required to write the script of a medium length video about the selected idea.",
    agent=researcher,
    expected_output="You answer must have all the information a writer would need to write a Youtube script.",
    async_execution=True,
    context=[
        selection_task,
    ],
    output_file="research_task.md",
)

competitors_task = Task(
    description="Search for videos or articles in the {industry} industry that are similar to the video idea we are working on and suggest ways our video can be different from theirs.",
    expected_output="Your answer must have a list of suggestions writers can follow to make sure the video is as unique and as different from competitors as possible.",
    agent=researcher,
    async_execution=True,
    context=[
        selection_task,
    ],
    output_file="competitors_task.md",
)


inspiration_task = Task(
    description="Search for videos or articles that are similar to the video idea we are working on but from other industries.",
    expected_output="Your answer must have a list of examples of articles and videos that have a similar angle as the video we are making but that are in different industries.",
    agent=researcher,
    async_execution=True,
    context=[
        selection_task,
    ],
    output_file="inspiration_task.md",
)

script_task = Task(
    description="Write the script for a Youtube video for a channel in the {industry} industry.",
    expected_output="A script for a Youtube video with a title, an introduction, at least three sections, and an outro. Make sure to also include the prompt to generate a thumbnail for the video.",
    agent=writer,
    context=[
        selection_task,
        research_task,
        competitors_task,
        inspiration_task,
    ],
    output_file="script_task.md",
)

crew = Crew(
    agents=[
        researcher,
        writer,
        marketer,
    ],
    tasks=[
        brainstorm_task,
        selection_task,
        research_task,
        inspiration_task,
        competitors_task,
        script_task,
    ],
    verbose=2,
)

result = crew.kickoff(
    inputs=dict(
        industry="Hot Sauce",
    ),
)

result
```

---





----
# investment_recommendation Crew
## Setting
```python
import os

os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"
```
## Tools
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