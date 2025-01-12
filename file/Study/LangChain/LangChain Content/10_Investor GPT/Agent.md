# Concept
- `Agent`는 `LLM`(token은 무엇인지 추측하여 text를 완성하는 `Model`)에게 특정 기능을 수행하게 하기 위해 만들어진 기능이다.
- `Agent`을 활용하면 `LLM`이 연산을 수행하거나 `API`를 활용하여 특정 데이터를 가져오는 등의 기능을 수행할 수 있다.
- `Agent`는 gpt3,4 같은 `LLM`이 수행하는 것이 아니라 `Langchain`에서 `function`을 수행하게 끔 `LLM`에게 전달하는 것임에 유의하자.
# How it works
- `agent`의 작동 방식은 쉽게 말해 Langchain에서 `LLM`에게 특정 기능을 수행할 수 있도록 [[Prompt]],[[Output Parser]]을 만들고 이를 실행시키는 방식이다.
- `agent`의 작동 방식 상 `LLM`을 여러 번 호출하기 때문에 저렴한 기능은 아니다.
- `agent`가 어떠한` prompt`와 `output parser`을 만드는지는 **어떠한 Agent Type을 가지고 있느냐**에 따라 다르다. 
- `from langchain.agents import initialize_agent`를 통해 `agent`을 불러 올 수 있다.
- `initialize_agent` class의 parameter는 여러가지가 있다.
	- `llm = {llm}` : 실행시킬 `LLM`을 지정한다.
	- `verbose = {True}` : `agent` 실행 상황을 `console`에 보여준다.
	- `agent = {agentType}` : `agent type`을 지정한다.
	- `tools = [{tool}, ...]` : `LLM`에게 시킬 특정 기능들을 `List` 형태로 지정한다.
	- `handle_parsing_errors={True}` : `LLM`의 output이 **output parser의 Parsing이 되지 않을 때** 자동으로 LLM에게 다시 하도록 설정하는 옵션이다. 
	- `agent_kwargs={ {option} }` : `Agent`의 세부 기능을 설정할 수가 있다. `OPENAI_FUNCTIONS Agent Type`을 사용할 때,  `Prmpt` 내용을 수정하기 위해 사용한다.
- `LLM`과 마찬가지로 `agent`도 `invoke()` function을 통해 실행시킬 수 있다.
```python
from langchain.chat_models import ChatOpenAI
from langchain.tools import StructuredTool
from langchain.agents import initialize_agent, AgentType

llm = ChatOpenAI(temperature=0.1)

def plus(a, b):
    return a + b

agent = initialize_agent(
    llm=llm,
    verbose = True,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    tools=[
        StructuredTool.from_function(
            func=plus,
            name="Sum Calculator",
            description="Use this to perform sums of two numbers. This tool take two arguments, both should be numbers.",
        )
    ],
)

prompt = "Cost of $355.39 + $924.87 + $721.2 + $1940.29 + $573.63 + $65.72 + $35.00 + $552.00 + $76.16 + $29.12"  

agent.invoke(prompt)
```
# Agent Types
- `from langchain.agents import AgentType`으로 다양한 `agnet Types`을 불러 올 수 있다.
#### ZERO_SHOT_REACT_DESCRIPTION
- **가장 범용적인 목적의** `agent Type`을 말한다
- `ZERO_SHOT_REACT`의 경우 `tool`에서 이용되는 `function`의 input을 하나만 받는 `Type`을 말한다.
- `function`의 input 값을 두 개 이상 받아와야 한다면, `description` 내용을 수정하여 **input을 string 형태로 받아와 변환해야 한다.**
- `ZERO_SHOT_REACT_DESCRIPTION`의 경우 `Tool`을 사용하며 `from langchain.tools import Tool`로 불러 올 수 있다.
```python
from langchain.chat_models import ChatOpenAI
from langchain.tools import StructuredTool, Tool
from langchain.agents import initialize_agent, AgentType

llm = ChatOpenAI(temperature=0.1)

def plus(inputs):
    a, b = inputs.split(",")
    return float(a) + float(b)
    
agent = initialize_agent(
    llm=llm,
    verbose = True,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    tools=[
        Tool.from_function(
            func=plus,
            name="Sum Calculator",
            description="Use this to perform sums of two numbers. Use this tool by sending a pair of numbers separated by a comma.\n Example :1,2",
        )
    ],
)

prompt = "Cost of $355.39 + $924.87 + $721.2 + $1940.29 + $573.63 + $65.72 + $35.00 + $552.00 + $76.16 + $29.12"

agent.invoke(prompt)
```
#### STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
- `STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION`는 3개의 의미가 합쳐진 이름이다.
	- `STRUCTURED` : `tool`에서 이용되는 `function`이 두 개 이상의 input을 가질 수 있다.
	- `CHAT` : `Chat model`의 특화되어 있다.
	- `ZERO_SHOT_REACT` : 가장 범용적인 목적의 `agent`을 뜻한다.
- `STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION`의 내부 prompt는 크게 3가지 속성으로 이루어져 있다.
	- `action` : 전에 만들었던 `text` 결과물들(`action : ~, observation : ~, thought : ~`)이다. [[Memory Modules]]과 비슷한 기능을 수행한다.
	- `observation` : `text` 결과물들을 `tool`을 넣어 만들어낸 최종 결과물들이다.
	- `thought` : 다음 `LLM`이 만들어야 할 내용들이다. [[Prompt]]의 `Question`과 비슷한 기능을 수행한다.
- `prompt`의 내용은 [[Function Call Method]]와 비슷한 기능을 수행하도록 구성되어 있다. `LLM`은 해당 `tool`에 있는 `function`이 필요하다 판단이 들면 해당 `function`을 사용하기 위해 해당 `function`의 `action_input(Parameter)`을 `json` 형식으로 채운다. 해당 값들은 `output pareser`를 거쳐 `tool`에 있는 `function`에 들어가 최종 `output`이 나온다. 이 `output`은 다시 `function`의 `input`에 들어갈 수도 있는데, `agent`는 위의 과정을 필요할 때 까지 **(agent가 해당 값이 final answer임을 명시한 시점까지)** 반복한다. 
- ex) `10+15+7+8=sum(10+15)+7+8=sum(25+7)+8=sum(32+8)=40`
- `STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION`는 `StructuredTool`를 사용하며 `from langchain.tools import StructuredTool`로 불러올 수 있다.
- `LLM`의 결과물은 `json`형태로 주어지는데 이때 중간 과정에서 `LLM`이 `json`형식이 아닌 `text`형식으로 값을 반환하게 되면 `output pareser`가 `parsing` 할 수 없기 때문에 오류를 일으킬 수 있다. 따라서 이때는 `handle_parsing_errors`를 `True`로 설정해주면 된다.
```python
from langchain.chat_models import ChatOpenAI
from langchain.tools import StructuredTool
from langchain.agents import initialize_agent, AgentType

llm = ChatOpenAI(temperature=0.1)

def plus(a, b):
    return a + b

agent = initialize_agent(
    llm=llm,
    verbose = True,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    tools=[
        StructuredTool.from_function(
            func=plus,
            name="Sum Calculator",
            description="Use this to perform sums of two numbers. This tool take two arguments, both should be numbers.",
        )
    ],
)

prompt = "Cost of $355.39 + $924.87 + $721.2 + $1940.29 + $573.63 + $65.72 + $35.00 + $552.00 + $76.16 + $29.12"  

agent.invoke(prompt)
```
#### OPENAI_FUNCTIONS
- `OPENAI_FUNCTIONS`은 [[Function Call Method]]을 이용하면서, 다른 `Agent Types`보다 훨씬 적은 `prompt` 내용으로도 `function`을 작동 시킬 수 있다. 이는 비교적 적은 `input Window`가 든다는 것을 의미한다.
- 또한 `OPENAI_FUNCTIONS` `Tool`을 직접 만들어 작동 시켜야 하는데, 이를 만들기 위해선 `BaseTool`과 `pydantic`이 필요하다.
- 만들어진 `Tool`을 `List`안에 포함시키면 `Agent`와 `Tool`을 연결 시킬 수 있다.
- `OPENAI_FUNCTIONS`의 기본 prompt는 `"You are a helpful Ai assistant."`이기 때문에 이를 수정 하려면 agent_kwargs에 따로 `from langchain.schema import SystemMessage` 사용해 명시에 주면 된다.
##### BaseTool
- `from langchain.tools import BaseTool`로 불러 올 수 있다.
- `BaseTool`의 상속을 통해 특정 class에 Tool 기능을 사용할 수 있다.
- `BaseTool`에는 여러 `Component`가 있다.
	- `name: Type[str] = "{toolnName}"` : `Tool`의 이름을 명시한다.
	- `description: Type[str] = "{tooln description}"` :  `Tool`의 기능을 명시한다.
	- `args_schema: Type[{Tool Arguments Schema Class}] = {Tool Arguments Schema Class}` : `tool`이 사용할 `function`의 `parameter`을 명시한다. 명시 `Type`은 `pydantic`을 사용해 **각 Parameter의 타입을 명시한 특정 Class(Pydantic Class)이여야 한다.**
	- `def _run({function parameter}): {function()}` : `tool`에서 사용할 함수를 명시힌다.
##### Pydantic
- `Pydantic`은 `python`에서 데이터 유효성 검사 및 설정 관리를 위한 라이브러리이다.
- `BaseModel`을 사용하여 데이터의 유효성을 검사할 수 있는데, `BaseModel`을 상속하여 특정 class을 `데이터 유효성 검사 class`로 만들 수 있다.
- `Field`를 사용하여 변수의 대한 `description`(검사 규칙)을 적을 수도 있다. `Field`는 **pydantic의 데이터 모델 Class 안에서 사용 가능하다.**
```python
from typing import Type
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.agents import initialize_agent, AgentType
from pydantic import BaseModel, Field

llm = ChatOpenAI(temperature=0.1)  

def plus(a, b):
    return a + b

class CalculatorTooolArgsSchema(BaseModel):
    a: float = Field(description="The first number")
    b: float = Field(description="The second number")

class CalculatorToool(BaseTool):
    name: Type[str] = "CalculatorToool"
    description: Type[str] = """
    Use this to perform sums of two numbers.
    The first and second arguments should be numbers.
    Only receives two arguments.
    """
    
    args_schema: Type[CalculatorTooolArgsSchema] = CalculatorTooolArgsSchema

    def _run(self, a, b):
        return plus(a,b)
        
agent = initialize_agent(
    llm=llm,
    verbose=True,
    agent=AgentType.OPENAI_FUNCTIONS,
    handle_parsing_errors=True,
    tools=[
        CalculatorToool(),
    ],
    agent_kwargs={
        "system_message": SystemMessage(
            content="""
            You are an excellent mathematician.
            
            You calculate two numbers given.
            """
        )
    },        
)

prompt = "Cost of $355.39 + $924.87 + $721.2 + $1940.29 + $573.63 + $65.72 + $35.00 + $552.00 + $76.16 + $29.12"

agent.invoke(prompt)
```
# Toolkit
- `Agent`에는 다양한 toolkit([Langchain tools](https://python.langchain.com/docs/integrations/tools/))이 있다.
- 이를 이용해 다양한 데이터를 불러와 `LLM`에게 질문할 수 있다. (ex sql, yahoo, google, youtube etc..)
- [Langchain tools](https://python.langchain.com/docs/integrations/tools/) 사이트를 참고해 각각의 사용 방법을 보고 사용하면 된다.
- `Toolkit`의 `.get_tools()` finction을 사용하면 각 툴에 대한 정보를 전달해준다. 이 정보들을 더해서 `Agent`에게 전달하면 여러 `Toolkit`을 합칠 수 있다.
```python
from langchain.agents import create_sql_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase

llm = ChatOpenAI(
    temperature=0.1,
)

db = SQLDatabase.from_uri("sqlite:///movies.sqlite")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

agent.invoke("Give me movies that have the highest votes byt the lowest budgets and give me the name of their directors also include their gross revenus.")
```