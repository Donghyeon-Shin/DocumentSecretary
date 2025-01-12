# Concept
- 사용자의 `Question`과 Model의 `Response`을 저장하는 기능이다.
- 대표적으로 `Conversatoin Buffer memory`, `Conversatoin Summary Memory`, `Conversatoin Knowledge Graph Memory`등이 있다.
- Memory를 통해 Model이 과거 대화들을 기억하게 함으로써 `Response`의 연속성을 부여해준다.
# Common Feature
- `save_context()`와 `load_memory_variables({})` function을 가지고 있다.
	- `save_context()`는 Memory에 값을 저장하는 function이다. Parameter를 dic형태로 "input"과 "output"을 받는데 이는 각각, `Human`과 `AI`이다. **(Human과 AI로 쓰는게 아닌 `input`과 `output`으로 적음에 유의하자.)**
	- `load_memory_variables({})`는 메모리를 load하는 function이다. 빈 dic를 Parameter로 받는다.
- `return_messages="True/Flase"` : Parameter를 가지고 있는데 이는, 저장 형식을 단순 str이 아니라 `AI message`, `Human message`형식으로 바꾸어줄지 여부를 정할 수 있다.
- `memory_key="value"` : 저장된 Memory 값을 Prompt에게 전달하고 싶을 때 **Template의 `value`명을 `memory_key`에 입력**하면 Chain 연결 시 자동으로 Prompt에게 전달된다.
# Memory Type
### Conversation Buffer memory
- 대화 내용 전체를 저장할 때 사용하는 메모리다.
- `from langchain.memory import ConversationBufferMemory`로 사용할 수 있다.
 - 대화가 길어질 수록 비용이 많이 들 뿐 아니라, 비효율적이게 된다.
 - `Text completion` 할 때 즉, 텍스트를 자동 완성하고 싶을 때 사용하면 유용하다.
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages="True")

memory.save_context({"input": "Hi"}, {"output": "How are you?"})

memory.load_memory_variables({})
```
#### Conversation Buffer Window Memory
- 대화의 특정 부분(최근) 만 저장하는 메모리다.
- `K` parameter을 가지고 있는데 이는 얼마 만큼의 최근 데이터를 저장할 것인지를 정하는 값이다.
```python
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(return_messages="True", k=4)

def add_message(input, output):
    memory.save_context({"input":input}, {"output":output})
   
add_message(1,1)
add_message(2,2)
add_message(3,3)
add_message(4,4)
memory.load_memory_variables({})

add_message(5,5)
memory.load_memory_variables({})
```
#### Conversation Summary Memory
- llm을 사용하여 대화 내용을 요약하여 저장하는 메모리이다.
- `llm` Parameter을 통해 llm 모델과 연결 시켜주어야 한다.
- 초반에는 대화 내용을 쌓아야 하기 때문에 내용이 길어지지만 대화를 할 수록 요약을 해 효율적으로 관리해준다.
```python
from langchain.memory import ConversationSummaryMemory

memory_chat = ChatOpenAI(temperature=0.1)

memory = ConversationSummaryMemory(llm=memory_chat)

def add_message(input, output) :
    memory.save_context({"input":input}, {"output":output})

def get_summary():
    return memory.load_memory_variables({})

add_message("Hi my name is KKY, I live in South Korea", "WOW that is so cool")
add_message("South Korea is so pretty", "I wish I could go!!!")

get_summary()
```
- Memory 출력 결과
```json
{
	'history': 'The human introduces themselves as KKY from South Korea. The AI expresses excitement and finds it cool, wishing it could visit South Korea because it is so pretty.'
}
```
#### Conversation Summary Buffer Nemory
- Conversatoin Summary memory와 Conversatoin Buffer memory의 결합한 메모리이다.
- 즉, 최근(max token)의 내용까지는 모두 저장하지만 그 이전의 내용들은 요약되어 저장된다.
- `max_token_limit` Parameter에서 최대 저장할 token 수를 정할 수 있음.
```python
from langchain.memory import ConversationSummaryBufferMemory

memory_chat = ChatOpenAI(temperature=0.1)

memory = ConversationSummaryBufferMemory(
    llm=memory_chat, max_token_limit=150, return_messages=True
)

add_message("Hi my name is KKY, I live in South Korea", "WOW that is so cool")
add_message("South Korea is so pretty", "I wish I could go!!!")
add_message("How far is Korea from Argentina?", "I don't know! Super far!")
add_message("How far is Brazil from Argentina?", "I don't know! Super far!")

get_summary()
```
- Memory 출력 결과
```json
{
	'history': [
		SystemMessage(content='The human introduces themselves as KKY and mentions they live in South Korea. The AI responds with enthusiasm, saying "WOW that is so cool."'),
		 HumanMessage(content='South Korea is so pretty'), 
		 AIMessage(content='I wish I could go!!!'),
		 ...
```
#### Conversation Knowledge Graph Memory
- 대화 중 중요한 것들(Knowledge Graph)만 뽑아내 요약하는 메모리이다.
- `Conversatoin Summary Buffer Nemory`와 마찬가지로 llm을 따로 지정해주어야 한다.
```python
from langchain.memory import ConversationKGMemory

memory_chat = ChatOpenAI(temperature=0.1)

memory = ConversationKGMemory(llm=memory_chat, return_messages=True)

def add_message(input, output):
    memory.save_context({"input": input}, {"output": output})

add_message("Hi my name is KKY, I live in South Korea", "WOW that is so cool")
add_message("KKY likes kimchi", "WOW that is so cool")

memory.load_memory_variables({"input":"What does KKY like?"})
```
- Memory 출력 결과
```json
{
	'history': [
		SystemMessage(content='On KKY: KKY lives in South Korea. KKY likes kimchi.')
	]
}
```