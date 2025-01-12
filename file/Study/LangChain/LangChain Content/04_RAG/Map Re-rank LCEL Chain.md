# Concept
- 선별된 문서들 각각의 점수(scroe)가 포함된 답변(Response)을 구한 뒤, 모든 답변들 중 가장 Score가 높은 Response를 출력하는 Model이다.
- 각각의 문서들의 답변을 구하는 `answer_chain`과 그 답변을 토대로 최종 답변을 선별하는 `choose_chain` 그리고 이 둘을 잇는 `chain` 총 3개의 chain이 필요하다.
- Map Re-rank Process 이미지![[Map Re-rank Process.png]]
# Code
- `answer_chain`은 [[Retrieval]]를 통해 얻은 문서 `list`를 for문을 통해 하나하나 마다 `invoke`하여 각 문서의 질문에 대한 답변과 Score를 얻는다.
- for문을 통해 `answer_chain`을 여러 번 `invoke`하고 이를 하나의 값으로 전달해야 하기 때문에 `get_answer()` 라는 function를 만들고 **`RunnableLambda`로 chain을 연결시켜주는 방식**이 좋다.
- `choose_chian` 또한 `데이터 전처리`를 위해 `RunnableLambda`를 사용하여 `choose_answer()` function안에서 실행되는데(필수는 아님), `RunnableLambda` 안에 들어가는 `function`의 `Parameter`의 경우는 **`dictionary` or `callable object`** 이어야 한다. 따라서  **`get_answer()`의 return 값을 `dictionary` 형태로 만들어** `choose_answer()`에 넘겨준다.
- `choose_prompt`에 `"Return the sources of the answers as they are, do not change them."`라는 문장을 활용하여 `answer_chain`에서 얻은 문서들의 score들 중 가장 큰 값을 출력하도록 llm에게 시킬 수 있다.

```python
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain.vectorstores import FAISS
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.prompts import ChatPromptTemplate

answer_prompt = ChatPromptTemplate.from_template(
    """
    Using ONLY the following context answer the user's question. If you can't
    Just say you don't know, don't make anyting up.
    
    Then, give a score to the answer between 0 and 5. 0 being not helpful to
    the user and 5 being helpful to the user.
    
    Make sure to include the answer's score.
    ONLY one result should be output.
    
    Context : {context}
    
    Examples:

    Question: How far away is the moon?
    Answer: The moon is 384,400 km away.
    Score: 5

    Question: How far away is the sun?
    Answer: I don't know
    Score: 0

    Your turn!
    
    Question : {question}
    """

)


choose_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Use ONLY the following pre-existing answers to the user's question.

            Use the answers that have the highest score (more helpful).

            Return the sources of the answers as they are, do not change them.
            You must print out only one answer.
            Answer: {answers}
            """,
        ),
        ("human", "{question}"),
    ]
)

llm = ChatOpenAI(
    temperature=0.1,
)

loader = UnstructuredFileLoader("./.cache/files/chapter_one.txt")

splitter = CharacterTextSplitter.from_tiktoken_encoder(
    separator="\n\n",
    chunk_size=600,
    chunk_overlap=100,
)

docs = loader.load_and_split(text_splitter=splitter)
cache_dir = LocalFileStore("./.cache/embeddings/chapter_one.txt.")
embedder = OpenAIEmbeddings()
cache_embedder = CacheBackedEmbeddings.from_bytes_store(embedder, cache_dir)
vectorstore = FAISS.from_documents(docs, cache_embedder)
retriever = vectorstore.as_retriever()

def format_docs(inputs):
    return "\n\n".join(doc for doc in inputs)

def get_answer(inputs):
    docs = inputs["docs"]
    question = inputs["question"]
    answer_chain = answer_prompt | llm
    return {
        "question": question,
        "answer": [
            answer_chain.invoke({"context": doc, "question": question}).content
            for doc in docs
        ],
    }

def choose_answer(inputs):
    question = inputs["question"]
    answer = inputs["answer"]
    format_answer = format_docs(answer)
    choose_chain = choose_prompt | llm
    response = choose_chain.invoke({"answers" : format_answer, "question" : question})
    return response

main_chain = (
    {"docs": retriever, "question": RunnablePassthrough()}
    | RunnableLambda(get_answer)
    | RunnableLambda(choose_answer)
)

response = main_chain.invoke("Where does Winston live?")

print(response)
```

