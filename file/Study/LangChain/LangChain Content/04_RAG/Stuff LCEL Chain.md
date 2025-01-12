# Concept
- 가장 보편적인 [[RAG(Retrieval-Augmented Generation)]] Chain이다.
- 참고되는 모든 문서들을 **단일 [[Prompt]]** 에 넣어 Model을 만드는 방식이다.
- [Struff Process 이미지](https://js.langchain.com/v0.1/docs/modules/chains/document/map_reduce/) ![[Stufff Chain Process.jpg]]
# Code
- [[Prompt]], [[LCEL(LangChain Expression Language)]], [[Retrieval]]을 이해하고 있다면 단순히 연결하면 되기 떄문에 Chain을 만드는데 크게 어려움이 없을 것이다.
- `Prompt`에 `System Message`에서 `If you don't know the answer just say you don't know, dont't makt it up`이라는 문장은 model이 잘못된 정보를 생성하지 않도록 방지하는 역할을 수행한다.
- 단일 Chain이며 `Context`에 `Retriever` 전체가 들어간다는 것이 `Stuff`의 핵심 포인트이다.
- chain에서 `"context":retriver`로 입력 시 자동으로 **`retriver["{question}"]`** 로 바뀌게 되어 질문에 맞는 문서만 가져오게 된다.
```python
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.storage import LocalFileStore
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough

llm = ChatOpenAI(temperature=0.1)

cache_dir = LocalFileStore("./.cache/")

splitter = CharacterTextSplitter.from_tiktoken_encoder(
    separator="\n",
    chunk_size=600,
    chunk_overlap=50,

)

loader = UnstructuredFileLoader("./files/chapter_one.txt")

docs = loader.load_and_split(text_splitter=splitter)

embedder = OpenAIEmbeddings()

cached_embedding = CacheBackedEmbeddings.from_bytes_store(embedder, cache_dir)

vectorStore = Chroma.from_documents(docs, cached_embedding)

retriver = vectorStore.as_retriever()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer questions using only the following context. If you don't know the answer just say you don't know, dont't make it up:\n\n{context}",
        ),
        ("human", "{question}"),
    ]
)

chain = {"context":retriver, "question" : RunnablePassthrough()} | prompt | llm

chain.invoke("Describe Victory Mansions")
```

