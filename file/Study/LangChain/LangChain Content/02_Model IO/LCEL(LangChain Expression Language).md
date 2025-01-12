# Concept
- `LangChain Expression Languaged`은 [[Output Parser]]을 포함한 template, [[Prompt]], predict 과정을 효과적으로 줄일 수 있다.
- `|` `operator`를 이용해 여러 과정들을 하나로 묶어 **Chain**을 만든다.
- **ex ) Chain = Template | Language Model | Output Parser**
- `|`에 들어가는 `Input`과 `Output` Component는 다음과 같다. 
![[Expression language Input and Output.png]]
- **이전 Ouput Type과 다음 Input Type이 같아야 Chain으로 연결 가능하다.**
- Chain에 연결된 **모든 components은 Input과 Output이 존재해야 한다**
# Model Invoke
- Chain을 작동시키기 위해선 `invoke` funtion을 사용해야 한다.
- `invoke`에 `template`에서 만들었던 `value`를 넣어야 한다.

```python
chain = template | chat | CommaOutputParser()

chain.invoke({"max_items": 5, "question": "What are the pokemons?"})
```

# Multeple Chains
- 두 개의 `Chain`을 사용하여 하나의 모델 결과 `input`으로 하여 다른 모델과 연결하여금 다른 결과를 도출하도록 하는 `Chain`을 만들 수도 있다.
- **ex ) Main_Chain =  one_Chain | two_Chain | Output Parser**
- 두 개의 Chain을 연결하는 경우에는 다음 `Chain`의 `Input`을 이전 `Chain`에서 넘겨주어야 하기 떄문에 **{"input Data Name" : one_Chain} | two_Chain** 와 같이 `template`의 `value`를 넣어주는 과정을 포함해야 한다.
```python
chef_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a world-class international chef. You create esay to follow recipies for any type of cuisine with easy to find ingredients",),
        ("human", "I want to cook {cuisine} food"),
    ]
)

chef_chain = chef_prompt | chat

veg_chef_prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a vegetarian chef specialized on making traditional recipies vegetarian. You find alternative ingredients and explain their preparation. You don't radically modify the recipe. If there is no alternative for a food just say you don't know how to replace it.",),
        ("human", "{recipe}"),
    ]
)

veg_chain = veg_chef_prompt | chat

final_chain = {"recipe" : chef_chain} | veg_chain

final_chain.invoke({
    "cuisine" : "indian"
})
```
