# Concept
- 선별된 문서들 각각의 답변(Response)을 구한 뒤, 모든 답변을 토대로 최종 답변을 구하는 `Model`이다.
- 각 문서의 답변을 구하는 `map_docs_chain`과 최종 답변을 구하는 `final_Chain`으로 구성되어 있다.
- `map_chain`의 경우 `map_docs_chain`에서 얻은 결과를  `final_Chain`에 넘겨주는 역할을 수행한다.
- [Map Reduce Process 이미지](https://js.langchain.com/v0.1/docs/modules/chains/document/map_reduce/) ![[Map Reduce Chain Process.jpg]]
# Code
- `from langchain.schema.runnable import RunnableLambda`을 이용해 `map_chain`을 사용할 때마다 `map_docs` function을 수행하도록 할 수 있다.
- `RunnableLambda`는 `input parameter`를 무조건 하나를 받는데, type이 **`dictionary` or `callable object`** 이어야 한다. 
- 이를 이용해 `retriver`에서 받은 모든 문서들을 `for`문을 통해 문서 하나하나마다 `map_docs_chain`을 거쳐 `question`에 관한 답을 얻는다.
- 얻은 답들은 `join`을 통해 하나의 문장으로 만들어진다. 하나의 문장으로 만드는 이유는 `final_Chain`에서 각각의 답변을 하나의 `context` String value로 받기 떄문이다.
- `final_Chain`과 `map_chain`, `map_docs_chain` 모두 `question` value을 받는데, 이는 `final_Chain` `invoke`에서 받은 값을 `RunnablePassthrough()`로 넘겨주면 된다.
- `map_docs_prompt`에서 `verbatim`라는 단어를 사용함으로써 **중간에 model이 값을 수정하지 않도록** 설정한다.
- [[Stuff LCEL Chain]]과 마찬가지로 `final_prompt`에 `If you don't know the answer, just say that you don't know. Don't try to make up an answer` 문장을 사용하여 model이 잘못된 정보를 생성하지 않도록 설정한다.
```python
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

llm = ChatOpenAI(temperature=0.1)

loader = UnstructuredFileLoader("./files/chapter_one.txt")

splitter = CharacterTextSplitter.from_tiktoken_encoder(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=60,
)

doc = loader.load_and_split(text_splitter=splitter)

cache_dir = LocalFileStore("./.cache/")

embedder = OpenAIEmbeddings()

cache_embedder = CacheBackedEmbeddings.from_bytes_store(embedder, cache_dir)

vectorStore = Chroma.from_documents(doc, cache_embedder)

retriver = vectorStore.as_retriever()

map_docs_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Use the following portion of a long document to see if any of the
            text is relevant to answer the question. Return any relevant text
            verbatim.
            ------
            {context}
            """,
        ),
        ("human", "{question}"),
    ]
)

map_docs_chain = map_docs_prompt | llm

def map_docs(inputs):
    documents = inputs["documents"]
    question = inputs["question"]
    return "\n\n".join(
        map_docs_chain.invoke(
            {
                "context": doc.page_content,
                "question": question,
            }
        ).content
        for doc in documents
    )

map_chain = {"documents": retriver, "question": RunnablePassthrough()} | RunnableLambda(
    map_docs
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Given the following extracted parts of a long document and a
            question, create a final answer.
            If you don't know the answer, just say that you don't know. Don't try
            to make up an answer
            ------
            {context}
            """,
        ),
        ("human", "{question}"),
    ]
)

final_Chain = (
    {"context": map_chain, "question": RunnablePassthrough()} | final_prompt | llm
)

final_Chain.invoke("Describe Victory Mansions")
```