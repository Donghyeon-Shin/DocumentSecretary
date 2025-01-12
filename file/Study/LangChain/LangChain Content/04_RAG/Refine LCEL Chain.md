# Concept
- 각 문서들의 순서대로 순회하면서 답변(Response)을 **정제(Refine)** 하여 최종 답변을 구하는 `Model`이다.
- 구현하는데 여러 방법이 있겠지만, 해당 페이지에는 첫 번째 문서를 기준으로 답변을 하나 구한 뒤, 나머지 문서들을 순회하며 답변 내용을 추가하거나 수정하는 방법을 사용한다.
- 첫 번째 문서의 답변을 구해주는 `first_chain`과 해당 `Chain`에서 얻은 결과를 바탕으로 나머지 문서를 순회하며 `Refine`하는 `refine_chain`으로 구성되어 있다.
[Refine Process 이미지](https://js.langchain.com/v0.1/docs/modules/chains/document/refine/)![[Refine Chain Process.jpg]]
# Code
- 이 `Code`는 특정 `txt` 문서를 `Summary`하는 Model을 `Refine LCEL Chain`로 구현한 것이다.
- 모든 문서를 다 사용하기 때문에 굳이 [[Retrieval]]을 사용할 필요 없이 문서를 `Splitter`로 나눈 뒤 바로 `Chain`에 넣으면 된다. 
- `first_summary_chain`은 첫 번째 문서의 정보를 받아 이에 대한 답변을 내놓는다.
- `refine_chain`에는 참고할 문서인 `context`와 요약된 내용(**정제된 내용**)인 `existing_summary`가 필요하다. 
- 처음의 `existing_summary`은 `first_summary_chain`에서 얻은 정보이며, 그 다음부턴 나머지 문서의 `context`을 토대로 `existing_summary`을 수정하거나 추가한다.
- 모든 문서를 순회하여 얻은 `summary_content`가 `Refine LCEL Chain`의 최종 `Response`이다.
```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.output_parser import StrOutputParser
  
llm = ChatOpenAI(temperature=0.1)

loader = UnstructuredFileLoader("./files/chapter_one.txt")

splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size = 500,
    chunk_overlap = 100,
)

docs = loader.load_and_split(text_splitter=splitter)

first_summary_prompt = ChatPromptTemplate.from_template(
    """
    Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY
    """
)

first_summary_chain = first_summary_prompt | llm | StrOutputParser()

summary_content = first_summary_chain.invoke({"text": docs[0].page_content})

refine_prompt = ChatPromptTemplate.from_template(
    """
    Your job is to produce a final summary.
    We have provied an existing summary up to a certain point : {existing_summary}
    We have the opportunity to refine the existing summary (only if needed) with some more context below.
    ------
    {context}
    ------
    Given the new context, refine the original summary.
    If the context ins't useful, RETURN the original summary.
    """
)

refine_chain = refine_prompt | llm | StrOutputParser()
  
for i, doc in enumerate(docs[1:]):
    print(f"Progress : {i+1}/{len(docs) - 1}")
    summary_content = refine_chain.invoke({"existing_summary" : summary_content, "context" : doc.page_content})

print(summary_content)
```