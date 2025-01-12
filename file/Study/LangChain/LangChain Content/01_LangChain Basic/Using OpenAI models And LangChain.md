# OpenAI
- LangChain에서는 다양한 model을 사용할 수 있다. 그 중에서 해당 Part에서는 OpenAI Models를 사용할 것이다.
- OpenAI에서는 GPT-4o, GPT-4o mini, GPT-4, GPT-3.5 Turbo 등 다양한 models이 있다.
- [Models Info](https://platform.openai.com/docs/models)에서 각 model의 정보와  context window, output max tokens, trainin를 알 수 있다.
- [Models Pricing](https://openai.com/api/pricing/)에서 model의 1M output tokens 당 얼마 인지를 알 수 있다.
- [Models Usage](https://platform.openai.com/settings/organization/usage)에서 내 model 사용량과 비용을 알 수 있다.
- [Tokenizer](https://platform.openai.com/tokenizer)에서 GPT model이 각 단어가 몇 개의 token으로 인식하는를 알 수 있다.
# Declaring model
- LangChain에서 ChatOpenAI를 import 한다.
```python
from langchain.chat_models import ChatOpenAI
```
- 모델을 선언하기 위해서는 `ChatOpenAI()`로 객체를 만들어주어야 한다.
-  `ChatOpenAI()`의 constructor는 여러가지가 있지만, 알아두어야 몇 가지는
	- model_name="gpt-3.5-turbo-1106" : openAI의 model 명을 입력한다. 
	- temperature=0.1 : chatbot이 얼마나 창의적 인지를 결정하는 parameter이다. `0~1` 사이이며 `1`에 가까워질 수록 창의적이게 된다.
	- streaming=True : response가 끝날때 나오는 것이 아니라 진행되는 자체를 보여준다.
	- callbacks=`[StreamingStdOutCallbackHandler()]` : 다양한 callback이 있으며 `[StreamingStdOutCallbackHandler()]`은 console에서 response의 진행 상황을 보여준다.
```python
from langchain.callbacks import StreamingStdOutCallbackHandler

chat = ChatOpenAI(

    model_name="gpt-3.5-turbo-1106", temperature=0.1, streaming=True, callbacks=[StreamingStdOutCallbackHandler()]

)
```
# Predicts
- model에게 response을 얻을 때 사용하는 function이다.
- predicts는 크게 `predict`, `predict_messages`로 나뉜다.
### predict
- chat.predict('text') 해당 text(str) 내용의 답을 return으로 출력한다.
```python
response = chat.predict("How many colors are there?")
```
### predict_messages
- 단순한 str말고 더 복잡한 내용으로 질문하고 싶을 때는 chat.predict_messages(messages)를 사용한다.
- parameter인 messages는 리스트 형태이며 리스트 안에는 총 3개의 msg를 넣을 수 있다.
	- SystemMessage -> LLM의 설정들을 제공하기 위한 msg
	- AIMessage -> Ai한테 보내는 msg
	- HumanMessage -> 우리가 물어볼 msg
- 이 3개의 msg는 LangChain에서 지원하는 형식으로 schema에서 불러올 수 있다.
```python
from langchain.schema import HumanMessage, AIMessage, SystemMessage

messages = [

    SystemMessage(content="You are a geography expert. And you only reply in Korea"),

    AIMessage(content="My name is AI robot"),

    HumanMessage(content="What is the distance between Mexico and Thailand. Also, what is your name?"),

]

response = chat.predict_messages(messages)
```
# Debug
- `from langchain.globals import set_debug`을 통해 [[Prompt]]나 실행 결과 같은 내용들을 표시할 수 있다.
- 일반적으로 우리가 만든 Prompt가 올바르게 작성되었는지 확인하는데 사용된다.
```Python
from langchain.globals import set_debug

set_debug(True)
```
- 결과
```json
[llm/start] [1:llm:ChatOpenAI] Entering LLM run with input: 
{ 
	"prompts": [ 
		"Human: How do you make Italian pasta?" 
	] 
} 
[llm/end] [1:llm:ChatOpenAI] [2.63s] Exiting LLM run with output: 
{ 
	"generations": [
		[ 
			{ 
				"text": "To make Italian pasta, ... before serving.\n\nEnjoy your homemade Italian pasta!", 
				"generation_info": { 
					"finish_reason": "stop" 
				}, 
				"type": "ChatGeneration", 
				"message": { 
					"lc": 1, 
					"type": "constructor", 
					"id": [ "langchain", "schema", "messages", "AIMessage" ],

...

"system_fingerprint": null }, "run": null }
```
# Calculate OpenAI model Usage
- `from langchain.callbacks import get_openai_callback`을 통해 Code에서 model의 사용량과 비용을 알 수 있다.
- `with get_openai_callback() as usage:` 안에 사용된 model Usage에 대해 print를 통해 Prompt Tokens, Completion Tokens, Total Cost 등을 알 수 있다.
```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as usage:
    chat.predict("What is the recipe for soju")
    print(usage)
```
# Model Save and Load
- `from langchain.llms.openai import OpenAI`에서는 model을 save하고 load 할 수 있는 function이 있다.
- **단 이 module이 현재 정식으로 사용하지 않기 때문에 `ChatOpenAI`에서는 지원하지 않는다.**
### Save
- openAI model에 save function을 활용하여 원하는 경로에 파일로 저장할 수 있다.
```python
from langchain.llms.openai import OpenAI

chat = OpenAI(
    temperature=0.1,
    max_tokens=450,
    model="gpt-3.5-turbo-16k"
)

chat.save("model.json")
```
- 저장된 값
```json
{
    "model_name": "gpt-3.5-turbo-16k",
    "temperature": 0.1,
    "max_tokens": 450,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "n": 1,
    "request_timeout": null,
    "logit_bias": {},
    "_type": "openai"

}
```
### Load
- `from langchain.llms.loading import load_llm`을 통해 원하는 경로에 있는 model 정보를 불러올 수 있다.
```python
from langchain.llms.loading import load_llm

chat = load_llm("model.json")
```