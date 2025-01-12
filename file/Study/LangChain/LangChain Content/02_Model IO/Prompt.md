# Concept
- LLM과 의사소통 할 수 있는 방법이며, prompt가 좋아야 llm의 성능이 올라간다.
- **LangChain framework의 대부분의 기능도 이 prompt를 만드는 것에 집중되어 있다.**
# Using Template
- Prompt을 만들기 위해서는 Template이 필요하다.
- Template는 크게 `PromptTemplate`, `ChatPromptTemplate`로 나뉜다.
- response를 얻기 위해 `PromptTemplate`는 **predict**을 `ChatPromptTemplate`은 **predict_messages**을 사용하여야 한다.
# Template Type
### PromptTemplate
- PromptTemplate는 string으로부터 template을 만든다.
- 사용자에게 직접적으로 template을 노출시키고 싶지 않고 단어 or 문장만 전달받고 싶을 때 사용한다.
- 각 message 안에는 `{} - placeholder`를 넣을 수 있으며 {}안에 value를 넣어 **변수화** 시킬 수 있다.
- PromptTemplate은 디스크에 save/load가 가능하다.
- 만들어진 Template을 바탕으로 prompt를 만들기 위해 `format` function을 사용한다.
- 변수화된 value는 prompt을 만드는 과정안 format에서 입력할 수 있다.
```python
from langchain.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "What is the distance between {country_a} and {country_b}",
)
prompt = template.format(country_a = "Mexico", country_b = "Thailand")

chat.predict(prompt) # prompt is str
```
OR
```python
template = PromptTemplate(
    template="What is the capital of {country}",
    input_variables={"country"}
)

prompt = template.format(country="France")
```
### ChatPromptTemplate
- ChatPromptTemplate는 message를 통해 template을 만든다.
- `from_messages` function을 사용해 meesage template을 만드는데, parameter는 `system`, `ai`, `human`이 **tuple형태로 들어가있는 List**이다.
- 만들어진 Template을 바탕으로 prompt를 만들기 위해 `format_messages` function을 사용한다.
- 마찬가지로 ChatPromptTemplate에서는 `format_messages`에서 변수화된 value을 넣을 수 있다.
```python
from langchain.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages(

    [

        ("system", "You are a geography expert. And you only reply in {language}"),

        ("ai", "안녕하세요, 저는 {name}입니다."),

        ("human","What is the distance between {country_a} and {country_b} Also, what is your name?"),

    ]

)
prompt = template.format_messages(

    language="korea", name="ai", country_a="Mexico", country_b="Thailand"

)
chat.predict_messages(prompt)
```
### FewShotPromptTemplate
- 모델의 response에 대한 예제를 제공하여 예제와 비슷한 방식으로 출력하게 하는 Template
- 예제의 형식을 정하고 형식에 맞는 예제를 토대로 Template을 만든다.
- FewShotPromptTemplate에서 4개의 Parameter가 중요하다.
	- example_prompt=example_prompt : 예제의 형식
	- examples=examples : 예제
	- suffix="Human: What do you about {country}" : User의 답변 형식
	- input_variables=`["country"]` : template에 들어가는 value
```python
from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate

examples = [

    {

        "question": "What do you know about France?",

        "answer": """

        Here is what I know:

        Capital: Paris

        Language: French

        Food: Wine and Cheese

        CurrencyL Euro

        """,

    },

    {

        "question": "What do you know about Italy?",

        "answer": """

        I know this:

        Capital: Rome

        Language: Italian

        Food: Pizza and Pasta

        Currency: Euro

        """,

    },

    {

        "question": "What do you know about Greece?",

        "answer": """

        I know this:

        Capital: Athens

        Language: Greek

        Food: Souviaki and Feta Cheese

        Currency: Euro

        """,

    },

]

example_template = """

    Human: {question}

    AI: {answer}

"""

example_prompt = PromptTemplate.from_template(example_template)

prompt = FewShotPromptTemplate(

    example_prompt=example_prompt,

    examples=examples,

    suffix="Human: What do you about {country}",

    input_variables=["country"],

)

chain = prompt | chat

chain.invoke({"country": "Germany"})
```
- example_prompt을 다음과 같이 쓸 수도 있다. 
- **template, prompt의 변수명에 헷갈리지 않도록 주의하자.**
```python
example_prompt = PromptTemplate.from_template(example_template)
# OR
example_prompt = PromptTemplate.from_template("Human: {question}\nAI: {answer}")
```
- 예제들이 많은 경우는 비용의 절감과 정확한 response을 위해 **dynamic**하게 예제들을 선별할 필요가 있다.
- example_selector 사용 시, FewShotPromptTemplate Parameter에 exmaple 대신 example_selector을 넣어주어야 한다.
-  example_selector은 이미 만들어져 있기도 하지만 필요에 따라 직접 만들 수도 있다.
	- `LengthBasedExampleSelector` : exmaple의 개수를 제한하여 가져오는 Selector
		- example_prompt=example_prompt : 예제의 형식
		- examples=examples : 예제
		- max_length=180 : 예제의 총 길이
	- `BaseExampleSelector`을 통해 example_selector을 직접 만들 수 있다.
		- selector Class가 되기 위해 example_selector Class는 필수적으로 2개의 Function이 필요하다.
			- add_example(self, example) : 예제를 추가할 수 있는 함수
			- select_examples(self, input_variables)  : 예제를 조건에 따라 선택하는 함수

- **LengthBasedExampleSelector**
```python
from langchain.prompts.example_selector import LengthBasedExampleSelector

example_selector = LengthBasedExampleSelector(

    example_prompt=example_prompt, examples=examples, max_length=180,

)

prompt = FewShotPromptTemplate(

    example_prompt=example_prompt,

    example_selector=example_selector,

    suffix="Human: What do you about {country}",

    input_variables=["country"],

)
```
- **BaseExampleSelector (해당 Code에서는 Random Selector)**
```python
from langchain.prompts.example_selector.base import BaseExampleSelector

class RandomExampleSelector(BaseExampleSelector):

    def __init__(self, examples):

        self.examples = examples

    def add_example(self, example):

        self.examples.append(example)

    def select_examples(self, input_variables):

        from random import choice

        return [choice(self.examples)]

example_template = """

    Human: {question}

    AI: {answer}

"""

example_prompt = PromptTemplate.from_template(example_template)

example_selector = RandomExampleSelector(
    examples=examples
)

prompt = FewShotPromptTemplate(

    example_prompt=example_prompt,

    example_selector=example_selector,

    suffix="Human: What do you about {country}",

    input_variables=["country"],

)
```
# Load Prompt
- `langchain.prompts import load_prompt`을 통해 `json`이나 `yaml`, `xml`등 여러 파일로 Prompt을 만들어 불러 올 수 있다.
- 당연하게도 해당 파일들은 json형식과 yaml 형식을 만족해야 한다.
- `load_prompt` function을 통해 해당 경로에 있는 파일을 prompt로 만든다.
```python
from langchain.prompts import load_prompt

Json_prompt = load_prompt("./prompt.json")
Yaml_prompt = load_prompt("./prompt.yaml")
```
### Load Json Prompt
- `"_type": "prompt"` : prompt 형식임을 명시해야 한다.
- `"template": "What is the capital of {country}"` : 원하는 형식의 template을 적는다.
- `"input_variables": ["country"]` : tempalte의 value을 명시한다.
```json
{
    "_type": "prompt",
    "template": "What is the capital of {country}",
    "input_variables": [
        "country"
    ]
}
```
### Load Yaml Prompt
- `"_type": "prompt"` : prompt 형식임을 명시해야 한다.
- `"template": "What is the capital of {country}"` : 원하는 형식의 template을 적는다.
- `"input_variables": ["country"]` : tempalte의 value을 명시한다.
```yaml
_type: "prompt"
template: "What is the captial of {country}"
input_variables: ["country"]
```
# Connect Templates
- `from langchain.prompts import PipelinePromptTemplate`을 통해 여러 Templates을 하나로 합칠 수 있다.
- `PipelinePromptTemplate` function안에는 두 개의 Paramemter가 포함되어 있어야 한다.
	- `final_prompt=final_Prompt` : Templates을 합칠 최종 Prompt 형식
	- `pipeline_prompts=prompts`: 최종 Prompt안에 value **(value)** 들과 template **(key)** 간의 연결정보를 보여주는 prompt 형식

```python
from langchain.prompts import PipelinePromptTemplate

intro = PromptTemplate.from_template(
    """
    You are a role playing assistant.
    And you are impersonating a {character}
    """
)

example = PromptTemplate.from_template(
    """
    This is an example of how you talk:

    Human: {example_question}

    You: {example_answer}
    """
)

start = PromptTemplate.from_template(
    """

    Start now!

    Human: {question}

    You:

    """
)

final_Prompt = PromptTemplate.from_template(
    """

    {intro}

    {example}

    {start}

    """
)

prompts = [("intro", intro), ("example", example), ("start", start)]

full_Prompt = PipelinePromptTemplate(
    final_prompt=final_Prompt, pipeline_prompts=prompts
)

full_Prompt.format(
    character="spongebob",
    example_question="What is your hobby?",
    example_answer="haaaa!, I enjoy catching jellyfish ha haaaa!!!",
    question="What do you do on your birthhday?",
)
```