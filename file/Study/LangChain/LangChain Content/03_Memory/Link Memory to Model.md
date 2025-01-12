# Link Method
- Model에 Memory을 연결할 Chain은 2가지 방법으로 만들 수 있다.
	- `off-the-shelf` Chain : LLM에서 제공하는 보편화된 방법
	- Manual Chain : [[LCEL(LangChain Expression Language)]]으로 수동으로 연결하는 방법.
- [[Memory Modules]]은 **String 형태**로 저장하거나 **Message형태**로 저장하기 때문에 어떠한 형태로 저장하는지에 따라 연결하는 방법이 달라진다.
# Off-The-Shelf Chain
- Memory에 `Load`와 `Save` function을 따로 만들고 연결할 필요가 없기 때문에 간편하게 만들 수 있다.
- 특정 목적을 위해 특수한 Chain을 만들고 싶다면 이 방법을 사용하긴 어렵다.
- `from langchain.chains import LLMChain`을 통해 LLMChain(`off-the-shelf Chain`) Module을 불러올 수 있다.
- LLMChain에서 알아야 할 Parameter는 총 4개이다.
	- `llm-llm` : llm model을 연결한다.
	- `memory=memory` : memory를 연결한다.
	- `prompt=PromptTemplate.from_template(template)` : prompt를 연결한다.
	- `verbose=True` :  prompt formatting이나 result 값은 결과를 보기 쉽게 나태내어준다. **(디버깅 역할)**
### Memory를 String 형태로 Prompt에게 전달하는 방법
- [[Prompt]]을 만들 때, Memory가 String 형태로 저장되기 때문에 `PromptTemplate`으로 만들어야 한다.
- 만들어진 Prompt와 memory를 연결하기 위해 `memory_key`와 template의 `{value}`를 서로 같게 하여야 한다.
```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=80,
    memory_key="chat_history",
)

template = """
    You are a helpful AI talking to a human.
    
    {chat_history}
    
    Human:{question}
    You:

"""

chain = LLMChain(
    llm=llm,
    memory=memory,
    prompt=PromptTemplate.from_template(template),
    verbose=True,
)

chain.predict(question="My name is KKY")
```
### Memory를 Message 형태로 Prompt에게 전달하는 방법
- Memory를 Message형태로 Prompt에게 전달하기 위해서는 [[Prompt]] 자체도 `ChatPromptTemplate`로 만들어야 한다.
- Memory 또한 Message 형태로 저장되게 하기 위해서 `return_messages=True`을 해야 한다.
- Prompt를 만들 때 Memory가 만들어낸 message가 누구(system, ai, human)인지, 얼마만큼 인지를 모르기 때문에 `from langchain.prompts import MessagesPlaceholder`을 사용해야 한다,
- `MessagesPlaceholder` 는 누가 보냈는지 **알 수 없는, 예측하기 어려운** 메세지의 양과 **제한 없는 양**의 메시지를 **Template에 넣기 위해 만들어진 Module**이다.
- `MessagesPlaceholder` Parameter에 `variable_name="{memory_key}"`로 설정하여 Prompt와 Memory 값을 연결 시켜 줄 수 있다.

```python
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=80,
    memory_key="chat_history",
    return_messages=True,
)

  

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI talking to a human"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

chain = LLMChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True,

)

chain.predict(question="My name is KKY")
```
# Manual Chain
- 수동으로 Chain을 만들 경우에는 memory의 `load`와 `save` functoin과 chain을 연결해주어야 한다.
- `off-the-shelf` Chain보다 복잡하지만, 원하는대로 수정이 용이하다는 장점이 있다.
### Connect Load Function to Chain
- `load_memory_variables({})["value"]`의 value값과 `memory_key`이 값이 같아야 한다.
- `memory_key` 값의 Default가 **history**이기 때문에 따로 설정하지 않을 시, `load_memory_variables` 값을 `history`로 설정하여야 한다.
- `invoke`과정에서 memory의 정보를 prompt에게 넘겨준다. 
- `(과정 요약 : memory.load가 chat_history value가 되고 이것이 prompt에게 전달되어MessagesPlaceholder에 들어감)`
```python
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=80,
    memory_key="chat_history",
    return_messages=True,
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI talking to a human"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

chain = prompt | llm

chain.invoke({
    "chat_history": memory.load_memory_variables({})["chat_history"],
    "question": "My name is KKY"
})
```
- 하지만 `invoke`에 `memory load` function를 넣게 되면 사용자가 질문할 때마다 memory 또한 load 해야 하는 상황이 발생한다.
- 이를 `from langchain.schema.runnable import RunnablePassthrough`를 사용하여 해결한다.
- `RunnablePassthrough`을 통해 **항상** Prompt가 format되기 전에 특정 함수를 실행시켜준다.
- 따라서 `RunnablePassthrough.assign()`을 사용해 `memory.load_memory_variables({})["chat_history"]`이 부분을 함수(`def load_memory(_):`)로 만들어 Chain과 연결시켜주면 된다. 
- 단 여기서 주의해야 할 것이 **Chain과 연결된 모든 component는 input과 output이 존재해야 한다.** 따라서 `RunnablePassthrough`을 통해 실행되는 함수 또한 input 하나를 받을 공간을 만들어야 한다.
```python
from langchain.schema.runnable import RunnablePassthrough

def load_memory(_):
    return memory.load_memory_variables({})["history"]
    
chain = RunnablePassthrough.assign(history=load_memory) | prompt | llm

chain.invoke(
    {
        "question": "My name is KKY",
    }
)
```
### Connect Save Function to Chain
- `invoke`를 통해 만들어진 결과 memory save function에 넣어주면 된다.
- 단 이러한 저장 과정은 `invoke`를 할 때마다 **필수적으로** 행해지기 때문에 `invoke` 동시에 memory에 저장하는 함수(`def invoke_chain(question)`)를 만들어 호출하는게 편리하다.
```python
def invoke_chain(question):
    result = chain.invoke(
        {
            "question": question,
        }
    )
    memory.save_context({"input": question}, {"output": result.content})
    print(result)

invoke_chain("Hi My name is KKY")
invoke_chain("What is my name?")
```