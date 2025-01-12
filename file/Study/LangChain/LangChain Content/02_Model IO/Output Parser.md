# Concept
- LLM의 response을 변형할 때 사용된다. (ex, response를 str에서 list, dictionary로 바꾸기)
- schema에 다양한 Output Parser가 존재한다.'
# Parser Shape
### BaseOutputParser
- `Output Parser`가 constructor인 Parser class로 만든 뒤, parse functoin을 만들어 원하는 값으로 데이터를 가공하는 것이 `BaseOutputParser` 기본적인 형태이다.
- `from langchain.schema import BaseOutputParser`로 불러 올 수 있다.
- 해당 parser의 올바른 parameter가 들어오도록 **template를 설정**해야 한다.
- predict_messages의 response 값은 **content component** 에 있음을 주의하자.
```python
from langchain.schema import BaseOutputParser

class CommaOutputParser(BaseOutputParser):

    def parse(self, text):

        itmes = text.strip().split(",")

        return list(map(str.strip, itmes))
        
template = ChatPromptTemplate.from_messages(

    [

        ("system","You are a list generating machine. Everything you are asked will be answered with a comma seperated list of max {max_items} in lowercase. Do NOT reply with anything else"),

        ("human", "{question}"),

    ]

)

prompt = template.format_messages(max_items = 10, question = "What are the colors?")

result = chat.predict_messages(prompt)

p = CommaOutputParser()

p.parse(result.content)
```
### StrOutputParser
- `Chain`의 결과값을 `String`으로 바꿔 출력해주는 `Output Parser`이다.
- `from langchain.schema.output_parser import StrOutputParser`로 불러 올 수 있다.
- `StrOutputParser`를 사용하면 `invoke()` 시 `.content` component를 따로 구하지 않아도 된다.
```python
from langchain.schema.output_parser import StrOutputParser
chain = prompt | llm | StrOutputParser()
response = refine_chain.invoke({"content" : content, "question" : question})
print(response)
```