# Detail
- UI는 [[Document GPT]] 동일하게 제작하였다.
- `Ollama`의 `mistral:latest`와 `llama2:13b` [[Offline Model]]을 사용하였고, 이를 [[Streamlit]]의 `selectbox`을 이용하여 사용자가 어떠한 model을 사용할 것인지를 지정할 수 있게 구현하였다.
- model 지정 값은 초기화 되면 안되기 때문에 `st.session`을 이용해서 file이 없을 때만 model name이 초기화 되도록 설정한다.
- `embedding` 또한` OllamaEmbeddings`을 사용하여 chain과 동일한 model을 사용하도록 설정한다.
# Code
```python
import streamlit as st
from langchain.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings, CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.callbacks.base import BaseCallbackHandler
from langchain.memory import ConversationSummaryBufferMemory

st.set_page_config(
    page_title="Priavte GPT", 
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

if "model_name" not in st.session_state:
    st.session_state["model_name"] = "mistral:latest"

llm = ChatOllama(
    model=st.session_state["model_name"],
    temperature=0.1,
    streaming=True,
    callbacks=[ChatCallbackHandler()],
)

memory_llm = ChatOllama(
    model=st.session_state["model_name"],
    temperature=0.1,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful assistant. Answer questions using only the following context and not your training data.

            You remember conversations with human.

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
    file_path = f"./.cache/private_files/{file_name}"
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
    cache_dir = LocalFileStore(f"./.cache/private_embeddings/{file_name}")
    embedder = OllamaEmbeddings(model=st.session_state["model_name"])
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
        memory_key="history",
        return_messages=True,
    )
    
memory = st.session_state["memory"]

st.title("Private GPT")

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
    with st.sidebar:
        model_name = st.selectbox("Choose offline models", ["mistral", "llama2"])
        if model_name == "mistral":
            st.session_state["model_name"] = "mistral:latest"
        elif model_name == "llama2":
            st.session_state["model_name"] = "llama2:13b"
            
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
    st.session_state["model_name"] = "mistral:latest"
    memory.clear()
```