# Detail
- [[Streamlit]]을 사용하여 UI를 제작했고 내부에는 [[Stuff LCEL Chain]]에 [[Memory Modules]](ConversationSummaryBufferMemory)을 연결하여 Chain을 구성하였다.
- UI는 `ai`와 `user`의 Chat 형식으로 구성하였고 Streamlit 특성 상 input widgit을 사용하는 순간 값들이 초기화 되기 때문에 st.sessoin을 이용하여 message data와 memory data을 caching 하였다.
- `ai`는 `user`가 넣은 file의 데이터와 user의 대화 기록(memory)을 바탕으로 답변하도록 [[Prompt]]을 작성하였다.
- file은 `SideBar`에서 넣을 수 있도록 하였고  file을 넣은 뒤 해당 file을 [[Retrieval]](load, splite, embedding) 처리하였다.
-  Retrieval 과정에서 `@st.cache_resource(show_spinner="Embedding file...")`을 적용해 file값이 바뀌지 않는 이상 해당 과정을 반복하여 수행하지 않도록 설정하였다.
- `UnstructuredFileLoader` loader을 사용하여 **어떠한 file이 들어와도** load 할 수 있도록 구현하였다.
- [[LCEL(LangChain Expression Language)]]를 사용하여 file Retriever과 massage, memory history를 prompt에 넣고 llm과 결합하여 `Chain`을 완성하였다.
- "ai"가 답변을 하는 과정에서 작성중인 값들을 실시간으로 화면에 띄우기 위해 `Stream=True And ChatCallbackHandler`을 사용하였다.
- `ChatCallbackHandler` class는 `BaseCallbackHandler` extend 해서 만들었으며 `on_llm_new_token` function으로 실시간 새로운 token이 나올 때마다 값이 화면에 띄울 수 있도록 구현하였다.
- **자세한 내용은 Code을 참조하자**
# Code
```python
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.callbacks.base import BaseCallbackHandler
from langchain.memory import ConversationSummaryBufferMemory

st.set_page_config(
    page_title="document GPT",
    page_icon="🤣",
)

class ChatCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.response = ""

    def on_llm_start(self, *arg, **kwargs):
        self.message_box = st.empty()

    def on_llm_end(self, *arg, **kwargs):
        save_message(self.response, "ai")

    def on_llm_new_token(self, token, *arg, **kwargs):
        self.response += token
        self.message_box.markdown(self.response)

llm = ChatOpenAI(
    temperature=0.1,
    streaming=True,
    callbacks=[ChatCallbackHandler()],
)

memory_llm = ChatOpenAI(temperature=0.1)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful assistant. Answer questions using only the following context.
            and You remember conversations with human.
            If you don't know the answer just say you don't know, dont't makt it
            ------
            {context}            
            """,
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

@st.cache_resource(show_spinner="Embedding file...")
def embed_file(file):
    file_name = file.name
    file_path = f"./.cache/files/{file_name}"
    file_context = file.read()
    with open(file_path, "wb") as f:
        f.write(file_context)
    loader = UnstructuredFileLoader(file_path)
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n\n",
        chunk_size=500,
        chunk_overlap=60,
    )
    documents = loader.load_and_split(text_splitter=splitter)
    cache_dir = LocalFileStore(f"./.cache/embeddings/{file_name}")
    embedder = OpenAIEmbeddings()
    cache_embedder = CacheBackedEmbeddings.from_bytes_store(embedder, cache_dir)
    vectorStore = Chroma.from_documents(documents, cache_embedder)
    retriever = vectorStore.as_retriever()
    return retriever
    
def paint_history():
    for dic_message in st.session_state["messages"]:
        send_message(dic_message["message"], dic_message["role"], save=False)

def save_message(message, role):
    st.session_state["messages"].append({"message": message, "role": role})

def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
        if save:
            save_message(message, role)

def format_doc(documents):
    return "\n\n".join(doc.page_content for doc in documents)
    
def memory_load(input):
    return memory.load_memory_variables({})["history"]

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationSummaryBufferMemory(
        llm=memory_llm,
        max_token_limit=150,
        memory_key="history",
        return_messages=True,
    )

memory = st.session_state["memory"]

st.title("Document GPT")

st.markdown(
    """
    Welcome!
    Use this chatbot to ask questions to an AI about your files!
    Upload your files on the sidebar.
    """
)

with st.sidebar:
    file = st.file_uploader(
        "Upload a .txt .pdf or .docx file",
        type=["txt", "pdf", "docx"],
    )

if file:
    retriever = embed_file(file)
    send_message("How can I help you?", "ai", save=False)
    paint_history()
    answer = st.chat_input("Ask anything about your file....")
    if answer:
        send_message(answer, "human")
        chain = (
            {
                "context": retriever | RunnableLambda(format_doc),
                "history": RunnableLambda(memory_load),
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
        )
        with st.chat_message("ai"):
            response = chain.invoke(answer)
            memory.save_context({"input": answer}, {"output": response.content})
else:
    st.session_state["messages"] = []
    memory.clear()
```