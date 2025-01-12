# Detail
- [[Site Loader]]를 활용하여 `Site`의 정보를 가저와 그 정보를 바탕으로 질문에 답변을 해주는 출력해주는 Page이다.
- 기본 UI는 [[Document GPT]]와 유사하게 구현하였다.
- LLM은 크게 두 가지로 구성하였다.
	- `History Model` : [[Stuff LCEL Chain]]을 바탕으로 하여 User의 `Question`과 `Histroy`(AI와 user의 Message)를 받은 뒤, 해당 `Question`이 예전의 존재하였다면 해당 답변을 그대로 출력하고 존재하지 않았다면 `None`을 출력해주는 `Model`
	- `Research Model` : [[Map Re-rank LCEL Chain]]을 바탕으로 하여 Retriever에서 User의 `Question`에 알맞은 답변을 찾아 출력해주는 `Model`
- `Memory`, `Message`, `Chain` 등 여러 기능들을 쉽게 관리하기 위해 각각을 **package 분할**하였다.
	- `SiteGPT.py` : `SiteGPT`의 메인 Page를 UI을 구성하여 출력하는 file
	- `Utils.py` : User와 AI의 대화를 출력하고 기록하는 함수들을 모아놓은 package
	- `Data_process.py` :  [[Site Loader]]로 데이터를 받거나 해당 데이터를 전처리하는 함수들을 모아놓은 package
	- `Chain.py` : `LLM`, `Memory` 관련된 모든 기능들의 함수들을 모아놓은 package
# Code
#### SiteGPT.py
- [[Streamlit]]의 `Side bar` Widgit을 활용하여 유저에게 `URL`을 받고 해당 값을 `Data_process.py`에 넘겨 Retreiver을 받는다.
- Retreiver 값에 유저의 질문을 더하여 `Chain.py` 넘겨 `AI`의 Response을 넘겨 받는다. 
- 이러한 과정을 거쳐 얻은 Response을 `Utils.py`의 function을 이용해 Site에 출력한다.
- URL의 값이 없을 때, `Memory` 값과 `Message`이 초기화 되도록 구현하였다.
```python
import streamlit as st
from pages.SiteGPT.utils import paint_message, send_message
from pages.SiteGPT.data_process import get_retriever_in_website
from pages.SiteGPT.chain import invoke_chain, initialize_memory

st.set_page_config(
    page_title="Site GPT",
    page_icon="🤣",
)

st.title("Site GPT")

st.markdown(
    """
    Ask questions about the content of a website.

    Start by writing the URL of the website on the sidebar.
    """
)

# ex) https://deepmind.google/sitemap.xml

with st.sidebar:
    url = st.text_input(
        "Write down a URL",
        placeholder="https://example.com/sitemap.xml",
    )

if url:
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please write down a Stiemap URL")
    else:
        retriever = get_retriever_in_website(url)
        send_message(st.session_state["messages"], "How can I help you?", "ai", save=False)
        paint_message(st.session_state["messages"])
        question = st.chat_input("Ask any questions in the document!")
        if question:
            send_message(st.session_state["messages"], question, "human")
            invoke_chain(st.session_state["messages"], retriever, question)
else:
    st.session_state["messages"] = []
    initialize_memory()
```
#### Utils.py
- `paint_message` : 기록된 모든 messages을 출력한다.
- `save_message` : message와 role를 저장한다.
- `send_message` : message을 출력하고 `Save` 여부에 따라 message를 저장한다.
```python
import streamlit as st

def paint_message(messages):
    for message in messages:
        send_message(messages, message["message"], message["role"], save=False)
        
def save_message(messages, message, role):
    messages.append({"message": message, "role": role})

def send_message(messages, message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
        if save:
            save_message(messages, message, role)
```
#### Data_process.py
- `parse_page` : `SitemapLoader`을 통해 가져온 `Data`의 전처리 과정을 수행한다.
- `get_retriever_in_website` : `st.cache_resource`을 사용하여 URL이 바뀔 때만 실행하도록 설정하였고, [[Retrieval]]의 전반적인 과정을 수행한다.
```python
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import SitemapLoader
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings

def parse_page(soup):
    header = soup.find("header")
    footer = soup.find("footer")
    if header:
        header.decompose()
    if footer:
        footer.decompose()
    return str(soup.get_text()).replace("\n", " ").replace("\xa0", " ")

@st.cache_resource(show_spinner="Loading website....")
def get_retriever_in_website(url):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=200,
    )
    loader = SitemapLoader(
        url,
        parsing_function=parse_page,
    )
    loader.requests_per_second = 5
    docs = loader.load_and_split(text_splitter=splitter)
    url_name = (
        str(url).replace("https://", "").replace(".", "").replace("/sitemapxml", "")
    )
    cache_dir = LocalFileStore(f"./.cache/Site_embeddings/{url_name}")
    embedder = OpenAIEmbeddings()
    cache_embedder = CacheBackedEmbeddings.from_bytes_store(embedder, cache_dir)
    vector_store = FAISS.from_documents(docs, cache_embedder)
    return vector_store.as_retriever()
```
#### Chain.py
##### History Model
- `History Model`은 user와 ai의 대화를 기반으로 user의 질문이 과거의 했던 질문과 비슷한 내용인지를 판단하고 비슷하다면 과거 답변을 그대로 출력하고 비슷한 답변이 없다면 `None`을 출력하도록 설정한 Model이다.
- 해당 `prompt`에 example을 제시하여 원하는 답변을 얻을 수 있도록 유도하였다. 
- user와 ai의 대화를 `format_message()` function을 통해 example에 맞게 `전처리`하였고, 마지막에 **유저의 질문이 message에 포함되어 있기 떄문에 이는 포함되지 않게 처리**하였다. (중복 내용 제거)
- 비슷한 질문에 대해서는 과거 기록을 가져와 그대로 출력 하였지만 비슷한 질문이 없을 시에 처음에는 `None`을 출력하다가 다음부턴 `Answer: None`을 출력하는 문제가 발생했다. 이에 `Prompt`에 `Answer: None`을 출력하지 말라고 명시하였으나, example 때문인지 해당 내용을 듣지 않고 계속 `None`이 아닌 `Answer: None`을 출력하는 문제가 발생하였다.
- 이를 해결하기 위해서 message가 처음일 때는 `History Model`을 사용하지 않게 하여 `None`을 출력 하지 않게 하거나, `Prompt`의 example을 수정하여 `Answer: None`을 출력하지 않게 하는 등의 수정이 필요할 것 같다.
##### Research Model
- History Model에서 값이 `None`이 나온다면 `Research Model`을 실행하여 Retriever에서 User의 질문에 알맞은 답변을 찾아 출력해주는 Model이다.
- `Research Model`은 `Answers Chain`과 `Choose Chain`으로 구성되어 있으며, 자세한 내용은 [[Map Re-rank LCEL Chain]]을 참고하면 된다.
- `Choose Chain`에는 [[Memory Modules]](ConversationSummaryBufferMemory) 기능을 추가하여 결과를 출력할 때, 과거의 답변 또한 고려되게 구현하였다.
- 각각의 Chain들이 `RunnableLambda`로 이어져 있기 때문에 안에 실행되는 `function`의 `Parameter`의 경우는 **`dictionary` or `callable object`** 이어야 한다는 점을 주의해야 한다.
```python
import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.memory import ConversationSummaryBufferMemory
from pages.SiteGPT.utils import save_message, send_message

class ChatCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.response = ""
        
    def on_llm_start(self, *arg, **kwargs):
        self.message_box = st.empty()
        
    def on_llm_end(self, *arg, **kwargs):
        save_message(st.session_state["messages"], self.response, "ai")
        self.response = ""

    def on_llm_new_token(self, token, *arg, **kwargs):
        self.response += token
        self.message_box.markdown(self.response)

history_prompt = ChatPromptTemplate.from_template(
    """
    You are given a 'history' that the user and ai talked about.

    BASED on this history If a user asks for something SIMILAR, find the answer in history and print it out.

    If the question is not in history, JUST SAY 'None'
    DO NOT SAY 'answer: None' and 'Answer: None'

    examples_1

    History:
    human: What is the color of the occean?
    ai: Blue. Source:https://ko.wikipedia.org/wiki/%EB%B0%94%EB%8B%A4%EC%83%89 Date:2024-10-13

    Question : What color is the ocean?
    Answer : Blue. Source:https://ko.wikipedia.org/wiki/%EB%B0%94%EB%8B%A4%EC%83%89 Date:2024-10-13

    examples_2
    History:
    human: What is the capital of Georgia?
    ai: Tbilisi Source:https://en.wikipedia.org/wiki/Capital_of_Georgia Date:2022-08-22

    Question : What are the major cities in Georgia?
    Answer : Tbilisi Source:https://en.wikipedia.org/wiki/Capital_of_Georgia Date:2022-08-22

    examples_3
    human: When was Avator released?
    ai: 2009 Source:https://en.wikipedia.org/wiki/Avatar_(franchise) Date:2022-12-18

    Question : What is Avator2?
    Answer : None

    examples_4

    History:
    human: What is the capital of the United States?
    ai: Washington, D.C. Source:https://ko.wikipedia.org/wiki/%EB%AF%B8%EA%B5%AD Date:2022-10-18

    Question : What is the capital of the Korea?
    Answer : None

    Your turn!
    History: {history}
    
    Question: {question}
    """
)

  
answers_prompt = ChatPromptTemplate.from_template(
    """
    Using ONLY the following context answer the user's question. If you can't answer,
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

            Use the answers that have the highest score (more helpful) and favor the most recent ones.

            Return the sources of the answers as they are, do not change them.

            You must print out only one answer. and Don't print out the score
            
            Answer: {answers}

            You also have a past answer. Please refert o them and write your answers
            """,
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

history_llm = ChatOpenAI(
    temperature=0.1,
    model="gpt-3.5-turbo-0125",
)

common_llm = ChatOpenAI(
    temperature=0.1,
)

choose_llm = ChatOpenAI(
    temperature=0.1,
    streaming=True,
    callbacks=[ChatCallbackHandler()],
)

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationSummaryBufferMemory(
        llm=common_llm,
        memory_key="history",
        max_token_limit=150,
        return_messages=True,
    )

memory = st.session_state["memory"]

def get_answers(inputs):
    docs = inputs["docs"]
    question = inputs["question"]
    answers_chain = answers_prompt | common_llm
    return {
        "question": question,
        "answers": [
            {
                "answer": answers_chain.invoke(
                    {
                        "context": doc.page_content,
                        "question": question,
                    }
                ).content,
                "source": doc.metadata["source"],
                "date": doc.metadata["lastmod"],
            }
            for doc in docs
        ],
        "history": memory.load_memory_variables({})["history"],
    }

def choose_answer(inputs):
    answers = inputs["answers"]
    question = inputs["question"]
    history = inputs["history"]
    choose_chain = choose_prompt | choose_llm
    condensed = "\n\n".join(
        f"{answer['answer']}\nSource:{answer['source']}\nDate:{answer['date']}\n"
        for answer in answers
    )
    return choose_chain.invoke(
        {"question": question, "answers": condensed, "history": history}
    )

def format_message(messages):
    history = ""
    i = 0
    for message in messages:
        if i is not len(messages) - 1:
            history += f"{message['role']} : {message['message']}\n"
        if i % 2 == 1:
            history += "\n"
        i = i + 1
        
    return history

def invoke_chain(messages, retriever, question):  
    history = format_message(messages)
    history_chain = history_prompt | history_llm
    result = history_chain.invoke({"history": history, "question": question})
    response = result.content
    
    if response == "None" or response == "Answer: None":
        research_chain = (
            {
                "docs": retriever,
                "question": RunnablePassthrough(),
            }
            | RunnableLambda(get_answers)
            | RunnableLambda(choose_answer)
        )
        with st.chat_message("ai"):
            answer = research_chain.invoke(question)
            memory.save_context({"input": question}, {"output": answer.content})
    else:
        send_message(messages, response, "ai")
        
def initialize_memory():
    memory.clear()
```