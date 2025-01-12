# Concept
- **gpt-3 / gpt-4** 에는 `Function Calling`이라는 독자적인 기능이 있다. 
- 이는 llm이 **특정 함수를 실행하도록 돕는 parameter**를 제공하는 기능이다.
- 어떠한 함수를 실행하기 위해 특정 Parameter를 원한다면 해당 함수의 기능에 대한 설명과 필요한 값들의 정보를 적고 이를 llm에게 제공한다면 llm이 **해당 Parameter**를 주는 기능이다.
- `Function Call` 사용하면 두 개의 Chain이 하는 일을 하나로 줄일 수 있다.
# Method
- `Function Call`을 사용하기 위해선 우선 `어떠한 함수를 실행할지`, 해당 함수에 `필요한 Parameter가 무엇인지`를 알려주는 일종의 **Function Prompt**를 작성하여야 한다.
- `Function Prompt`에는 3개의 dictionary 값이 필요하다.
	- `"name"` : 실행할 function 이름을 적는다.
	- `"description"` : 해당 함수의 기능을 적는다.
	- `"parameters"` : 해당 함수를 실행하기 위한 `format`과 `parameter`를 적는다.
- `ChatOpenAI`에서 `bind function`을 사용해서 `Function Call`을 Model과 연결 할 수 있다.
- `bind()` function에서는 두 개의 Parameter가 있다.
	- `function_call="{option}"` : 해당 함수를 강제적으로 사용할지 아니면 llm이 답변에 따라 자유롭게 사용할지 정 할 수 있다. 강제적으로 사용하게 할려면 `{"name":{function name}}`를, 자유롭게 사용하게 할려면 `"auto"`를 적으면 된다.
	- `functions=[{function}]` : `Model`에게 어떠한 함수를 사용할 것인지를 전달하는 값(function Prompt)을 적으면 된다.
```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

def get_weather(lon, lat):
    print("call an api.....")
    
function = {
    "name": "get_weather",
    "description": "function that takes longitude and latitude to find the weather of a place",
    "parameters": {
        "type": "object",
        "properties": {
            "lon": {
                "type": "string",
                "description": "The longitude coordinate",
            },
            "lat": {
                "type": "string",
                "description": "The latitude coordinate",
            },
        },
    },
    "required": ["lon", "lat"],
}

llm = ChatOpenAI(
    temperature=0.1,
).bind(
    function_call="auto",
    functions=[
        function,
    ],
)
prompt = PromptTemplate.from_template("Who is the weather in {city}")
chain = prompt | llm
response = chain.invoke({"city": "rome"})
response = response.additional_kwargs["function_call"]["arguments"]

import json
r = json.loads(response)

get_weather(r['lon'], r['lat'])
```