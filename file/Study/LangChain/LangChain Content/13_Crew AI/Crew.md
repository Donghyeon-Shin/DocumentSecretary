# Concept
- [`Crew`](https://www.crewai.com/)는 일련의 작업을 달성하기 위해 함께 일하는 `Agents`로 이루어진 그룹을 말한다.
- [[Assistant]]와 비슷한 기능을 수행하지만, `Crew`는 이해하기 쉬운 원리와 섬세한 `errorHandle` 그리고 무엇보다 **뛰어난 결과물**을 만들어낼 수 있어 자동화 시스템을 만들 때, 많이 사용된다.
- `Crew`는 여러 `Agent`들이 많은 결과물을 만들어내고 이를 서로 공유하기 때문에 **Context window**가 큰 `Model`을 사용해야 한다. 그래서 `GPT-4o` or `GPT-4o-mini`가 `Crew`를 사용했을 때 결과 값이 좋게 나온다.
- `Input Token`과 `Output Token`이 많이 나오기 때문에 비용적인 부분에서는 저렴하지 않다.
# Components
- `Crew`은 크게 4가지 `Components`로 나누어져 있다.
### Crew
- 일련의 작업을 달성하기 위해 함께 일하는 `Agent`들로 이루어진 그룹을 말한다. (`TEAM`이라고 볼 수 있다.)
- `from crewai import Crew`로 불러올 수 있다.
- `Crew`의 Attributes는 다음과 같다.
	- `agents = {List[agent]}` : `Crew`의 필요한 `Agent`를 `List` 형태로 명시한다.
	- `tasks = {List[task]}` : `Crew`의 필요한 `Task`를 `List` 형태로 명시한다. **해당 Task은 순서대로 진행된다.**
	- `verbose = {2}` : `Crew`의 작동 내용을 `console`에 출력한다.
	- `process = Process.hierarchical` : `from crewai.process import Process`을 통해 `LLM`에게 직접 `Task`의 실행을 계획하고, 위임하고, 검증하도록 한다. (`manager_llm model`을 따로 설정하여야 한다.)
	- `manager_llm = {ChatModel}` : `Task`의 실행을 계획하고, 위임하고, 검증하는 `LLM`을 지정한다.
	- `memory = {boolean}` : `Short-Time`(현재 실행), `Long-Time`(지난 실행), `Entity`(사람, 장소, 개념 같은 Entitiy를 기억), `Contextual Memory`(상호작용의 Context를 기억)을 활성화 할 수 있다. **memory를 embedding(embedder는 openAI embedder이며 따로 지정할 수도 있다.)하고 Verctor Search를 수행하기 때문에 추가로 비용이 발생한다.**
```python
from crewai import Crew
from crewai.process import Process
from langchain_openai import ChatOpenAI

crew = Crew(
    agents=[...],
    tasks=[...],
    verbose=2,
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-4o-mini"),
    memory=True,
)
```
- 만들어진 `Crew` 객체의 `kickoff` function을 이용해 `Crew`을 실행시킬 수 있다. 
- `inputs` Parameter을 사용하여 `Task`, `Agant`내의 `{} : Place Holder` 안에 값을 채워 넣는다. **`dict` 형태로 값을 전달**하여야 한다.
```python
result = crew.kickoff(
    inputs=dict(
        topic="The biggest box offfice flops of 2024",
    ),
)
```
### Agent
- 특정 목표(`Goal`)을 수행하기 위해 필요한 `Task`를 수행하고 다른 `Agents`과 통신하는 자율 단위를 말한다. (`Team member`라고 볼 수 있다.)
- `from crewai import Agent`로 불러올 수 있다.
- `Agent`는 **하나의 일을 구체적으로 명시**해야 결과 값이 잘 나온다.
- 따라서 `Crew`는 하나의 큰 일을 수행하기 위해 여러 `Agent`를 호출하고 각각의 `Agent`도 최고의 결과를 얻기 위해 **서로 통신하며 결과 값을 공유한다.**
- `Agent`의 Attributes는 다음과 같다.
	- `role = {str}` : `Crew`안에서 `Agent`의 역할을 명시한다.
	- `goal = {str}` : 해당 `Agent`의 원하는 결과를 명시한다. **구체적이며 하나의 일이야 한다.**
	- `backstory = {str}` : `Agent`에게 역할을 명시한다. (**특정 역할극을 수행하도록 명령했을 때, 더 결과가 잘나온다.**) 또한, `You want to impress your coworkers with your work.` 같은 내용(`보상`, `격려` 등)을 추가하면 더 좋은 결과를 이끌어 낼 수 있다.
	- `verbose = {True}` : `Agent`의 진행 과정을 `console`에 출력한다.
	- `tools = {List[tool]}` : `Agent`가 `Goal`을 달성하기 위해 사용할 `Tools`을 `List` 형태로 명시한다.
	- `allow_delegation = {False}` : 다른 `Agent`나 `Tool`을 사용할 수 있도록 하는 기능이다. 만약 해당 기능을 사용하지 않을 것이라면 `False`로 설정해야 한다. 아니면 `Agent`가 올바르지 않은 `Agent`나 `Tool`을 통신하려고 시도하면서 오류가 발생한다. (물론 `CrewAI`가 `errorHandling`이 되어 있어 동작이 멈추지는 않는다. Awsome!! )
	- `max_execution_time = {number} OR Max Iter = {number}` : `Agent`가 `Tool`을 사용할 때, 원하는 결과가 나오지 않아 게속 `Tool`을 사용하는 경우가 발생한다. **이는 과한 token을 만들어내며 우리를 거지로 만든다.** 이를 방지하기 위해 `Tool` 사용을 제한하는 2가지 옵션(`1) max_execution_time : 최대 실행 시간 / 2) Max Iter : 최대 실행 횟수`)이 존재한다. 

```python
from crewai import Agent

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
```
### Task
- `Agent`가 완수하고자 하는 특정 과제를 말한다.(`Mission`이라고 볼 수 있다.)
- `from crewai import Task`로 불러 올 수 있다.
- `Task`의 Attributes는 다음과 같다.
	- `description = {str}` : `Task`의 내용을 명시한다.
	- `agent = {agent}` : 어떠한 `Agent`가 수행하는 `Task`인지 명시한다.
	- **`expected output = {str}`** : 결과에 어떤 내용을 포함해야 되는지를 명시한다. 결과값의 질을 결정짓기 때문에 **가장 중요한 Attributes**이다.
	- `context = {List[task]}`: 다른 `Tasks`의 결과값을 가져올 수 있다. (**가져올 `Task`가 먼저 실행되어야 한다.**)
	- `human_input = {True}` : `Agnet`가 `Task`를 실행하고 나서 해당 결과 값을 승인이나 거절을 요청하도록 하는 확인 메시지를 보도록 설정한다.
	- `async_execution = {True}` : **비동기 실행**을 활성화하여 서로에 대한 의존성이 없는 `Tasks`를 동시에 실행한다.
	- `output_file = {file_name}` : `Agent`가 `Task`를 실행한 결과 값을 `File`로 저장하도록 설정한다.
	- `output_json = {pydantic class}` : `pydantic`으로 `output Type`을 규정하여 해당 값들로 결과 값을 `Json` 형식으로 출력할 수 있다. 일반적으로 `output_pydantic={pydantic class}`을 사용해 결과 값을 가져올 수 있으나, `Unknow Error`가 발생한다.
```python
from crewai import Task
from pydantic import BaseModel
from typing import List

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
    context=[...],
    output_file="blog_post.md",
    output_json=BlogPost,
)
```
### Tool
- `Agent`가 `Task`을 완수하기 위해 사용하는 도구이다.
- `from crewai_tools import {Tool_name}`으로 여러 `Crew Tool`을 불러올 수 있다.
#### Base Tools 
- `SerperDevTool` : `from crewai_tools import SerperDevTool`로 불러 올 수 있으며 `python`에서 `google` 검색을 할 수 있게 해주는 도구이다. `SERPER_API`가 따로 필요하며 무료는 아니지만 2500개의 무료 쿼리를 제공한다. 
- `ScrapeWebsiteTool` : `from crewai_tools ScrapeWebsiteTool`로 불러 올 수 있으며 특정 웹사이트의 내용을 읽고 추출할 수 있게 해주는 도구이다.
```python
from crewai import Crew, Agent, Task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
```
#### Custom Tool
- `from crewai_tools import tool`을 한 다음 특정 `function`에 `@tool` 데코레이터를 추가하여 특정 함수를 `Tool`로 지정할 수 있다.
- `@tool` 내에는 어떠한 `Tool`인지를 간략히 설명하면 `Agent`가 이를 보고 해당 `Tool`을 사용할 것인지를 결정한다.
- **function 안에는 `"""description"""`으로 `LLM`에게 이 Tool 이떠한 역할을 수행하는지 어떠한 값의 Parameter을 갖는지를 알려주어야 한다.** 
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
```
# Setting CrewAI Model
- `import os`을 이용해 `"OPENAI_MODEL_NAME"` 환경변수를 원하는 `Model`로 설정하면 된다.
```python
import os

os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"
```
- 만약 Ollama 같은 [[Offline Model]]을 사용하고 싶으면 환경 변수를 `NA`로 채운 뒤 `ChatOpenAI`로 `model`을 만든 뒤, `base_url`를 채우면 된다.
```python
import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_MODEL_NAME"] = "NA"

llm = ChatOpenAI(
	model = "llama2:13b",
	base_url = "https://localhost:11434.v1"
)
```
# CrewAI Ex ) Search Google and Script blog post
## Detail
- 특정 주제(`topic`)을 제시하면 해당 주제와 관련된 내용을 `Google`에 찾고 그 내용과 관련된 `Blog Post`를 작성하는 `Crew`이다.
- `Google` 검색과 `Web Site` 탐색을 을 하기 위해 `SerperDevTool`, `ScrapeWebsiteTool`을 사용하였다.
- `researcher Agent`는 `SerperDevTool`, `ScrapeWebsiteTool`을 사용하여 웹 검색 및 탐색 역할을 수행한다. 
- `researcher Agent`의 많은 검색을 제한하기 위해 `max_iter`을 10으로 지정하였다.
- `editor Agent`을 만들고 `Blog`글을 작성하는 `Task`을 지정한다.
## Crew Process
- `Crew`가 실행되면 `editor Agent`가 해당 `Topic`의 자료를 얻기 위해 `researcher Agent`에게 도움을 요청한다. 
- `researcher Agent`는 `editor` 요청한 값을 바탕으로 `tool`을 사용해 `Searching` 시작하고 `Searching`이 끝나면 해당 결과값을 `editor Agent`에게 보낸다.
- `editor Agent`는 `researcher Agent`가 보낸 값으로 최종 결과값(`blog post`)을 만들어 `blog_post.md`에 저장한다.
## Code
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
    You are working for a very important client.
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
    verbose=2,
)

result = crew.kickoff(
    inputs=dict(
        topic="The biggest box offfice flops of 2024",
    ),
)
```