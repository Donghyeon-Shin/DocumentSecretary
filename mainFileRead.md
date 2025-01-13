```markdown
# Detail ( Common )
- `file`을 입력 받거나 `Wikipedia`에서 검색한 값을 바탕으로 Quiz을 만들어 출력해주는 `site`이다.
- Streamlit의 `sidebar`에 `file upload`와 `Wikipedia` 검색 기능을 구현하였다.
- `file upload`는 [[Document GPT]]와 동일한 기능이 사용하고 `Wikipedia`의 경우는 [[WikipediaRetriever]]을 사용하였다.
- `file upload`와 `Wikipedia` 모두 값이 변하지 않는 이상 초기화 할 필요가 없기 때문에 `@st.cache`을 사용한다.
- `Chain`을 만드는 과정 또한 `file upload`와 `Wikipedia`에서 얻은 값(`docs`)이 바뀌지 않는다면 초기화 할 필요가 없기 때문에 `@st.cache`을 이용한다. 하지만 `docs`이 hash 할 수 없는 값이기 때문에 따로 `hash`할 수 있는 값을 포함하여 function을 구성해야 한다. (자세한 내용은 [[Streamlit]] 참고)
- Streamlit의 `form`을 이용하여 `Chain`을 통해 얻은 `json 값`을 바탕으로 quiz UI를 구현하였고 `success`와 `error` Widgit을 활용하여 `Submit Button`을 누를 시,  정답 유/무가 나오도록 구현하였다.
# Code
#### Two chains and json output_parser Ver.
- `questions_chain`을 이용하여 `input docs`를 바탕으로 Quiz 형식의 `output`을 받는다.
- 그 값을 `formatting_chain`을 넣어 json 형식의 `string` 값으로 변환 시킨다.
- 마지막으로 string으로 된 값을 `OutputParser`을 이용하여 `json` 형식으로 값을 `return` 한다.
- 모든 과정을 `chain = {"context": questions_chain} | formatting_chain | output_parser`으로 연결 시킨다.
- `formatting_chain`의 `formatting_prompt`의 경우 `example input`과 `example out`을 넣어 model이 `json` 형식으로 나올 수 있도록 설정할 수 있는데 여기서 `'''json`을 사용하는 이유는 llm에게 일종의 시작점을 알려주는 것이다. 이렇게 하지 않으면 보통 `알겠습니다.` or `기꺼이 하겠습니다.` 같은 말로 시작을 하기 때문에 **json 결과 값**만 얻기 위해 이런 식으로 작성한 것이다. `{{ `을 사용하는 것 또한 `prompt`에서 template variable(`{}`)과 헷갈리게 하고 싶지 않아서 이다.
- `output_parser`는 결과 값의 일부를 수정(`text = text.replace("```", "").replace("json", "")`)하고 이를 `import json`을 통해 `json` 형식으로 값을 `return`한다.
```python
import streamlit as st
import json
from langchain.chat_models import ChatOpenAI
from langchain.retrievers import WikipediaRetriever
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.schema.runnable import RunnableLambda
from langchain.schema import BaseOutputParser

class JsonOutputParser(BaseOutputParser):
    def parse(self, text):
        text = text.replace("```", "").replace("json", "")
        return json.loads(text)

output_parser = JsonOutputParser()

st.set_page_config(
    page_title="QuizGpt",
    page_icon="🤣",
)

st.title("QuizGPT")

llm = ChatOpenAI(
    temperature=0.1,
    model="gpt-3.5-turbo-0125",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
)

def format_docs(documents):
    return "\n\n".join(doc.page_content for doc in documents)
  
questions_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful assistant that is role playing as a teacher.
            Based ONLY on the following context make 10 questoins to test the user's knowledge about the text.
            Each question should have 4 answers, three of them must be incorrect and one should be correct.
            Use (o) to signal the correct answer.
            
            Question examples

            Question: What is the color of the occean?
            Answers: Red|Yellow|Green|Blue(o)

            Question: What is the capital or Georgia?
            Answers: Baku|Tbilisi(o)|Manila|Beirut

            Question: When was Avator released?
            Answers: 2007|2001|2009(o)|1998
            
            Question: Who was Julius Caesar?
            Answers: A Roman Emperor(o)|Painter|Actor|Model
            
            Your turn!
            Context: {context}
            """,
        )
    ]
)

questions_chain = {"context": RunnableLambda(format_docs)} | questions_prompt | llm

formatting_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a powerful formatting algorithm.
            You format exam question into JSON format.
            
            Answers with (o) are the correct ones.

            Example Input:

            Question: What is the color of the occean?
            Answers: Red|Yellow|Green|Blue(o)
            
            Question: What is the capital or Georgia?
            Answers: Baku|Tbilisi(o)|Manila|Beirut

            Question: When was Avator released?
            Answers: 2007|2001|2009(o)|1998

            Question: Who was Julius Caesar?
            Answers: A Roman Emperor(o)|Painter|Actor|Model

            Example Output:
            ```json
            {{ "questions": [
                    {{
                        "question": "What is the color of the occean?",
                        "answers": [
                            {{
                                "answer": "Red",
                                "correct": false
                            }},
                            {{
                                "answer": "Yellow"
                                "correct": false
                            }},
                            {{
                                "answer": "Green",
                                "correct": false
                            }},
                            {{
                                "answer": "Blue",
                                "correct": true
                            }},
                        ]
                    }},
                    {{
                        "question": "What is the capital or Georgia?",
                        "answers": [
                            {{
                                "answer": "Baku",
                                "correct": false
                            }},
                            {{
                                "answer": "Tbilisi"
                                "correct": true
                            }},
                            {{
                                "answer": "Manila",
                                "correct": false
                            }},
                            {{
                                "answer": "Beirut",
                                "correct": false
                            }},
                        ]
                    }},
                    {{
                        "question": "When was Avator released?",
                        "answers": [
                            {{
                                "answer": "2007",
                                "correct": false
                            }},
                            {{
                                "answer": "2001"
                                "correct": false
                            }},
                            {{
                                "answer": "2009",
                                "correct": true
                            }},
                            {{
                                "answer": "1998",
                                "correct": false
                            }},
                        ]
                    }},
                    {{
                        "question": "Who was Julius Caesar?",
                        "answers": [
                            {{
                                "answer": "A Roman Emperor",
                                "correct": true
                            }},
                            {{
                                "answer": "Painter"
                                "correct": false
                            }},
                            {{
                                "answer": "Actor",
                                "correct": false
                            }},
                            {{
                                "answer": "Model",
                                "correct": false
                            }},
                        ]
                    }}                                        
                ]
            }}```

            Your turn!

            Question : {context}
            """,
        )
    ]
)

formatting_chain = formatting_prompt | llm

@st.cache_resource(show_spinner="Loading file...")
def split_file(file):
    file_name = file.name
    file_path = f"./.cache/quiz_files/{file_name}"
    file_context = file.read()
    with open(file_path, "wb") as f:
        f.write(file_context)
        
    loader = UnstructuredFileLoader(file_path)
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    documents = loader.load_and_split(text_splitter=splitter)
    return documents

@st.cache_data(show_spinner="Making quiz...")
def run_quiz_chain(_docs, topic):
    chain = {"context": questions_chain} | formatting_chain | output_parser
    return chain.invoke(_docs)

@st.cache_data(show_spinner="Searching wikipedia...")
def wiki_search(topic):
    retriever = WikipediaRetriever(top_k_results=5)
    docs = retriever.get_relevant_documents(topic)
    return docs
    
with st.sidebar:
    docs = None
    topic = None
    file = None
    choice = st.selectbox(
        "Choose what you want to use.",
        (
            "File",
            "Wikipedia Article",
        ),
    )
    if choice == "File":
        file = st.file_uploader(
            "Upload a .docx, .txt, .pdf file", type=["pdf", "txt", "docx"]
        )
        if file:
            docs = split_file(file)
    else:
        topic = st.text_input("Search Wikipedia")
        if topic:
            docs = wiki_search(topic)
            
if not docs:
    st.markdown(
        """
        Welcome to QuizGPT.

        I will make a quiz from Wikipedia articles or files you upload to test your knowledge and help you study.

        Get Started by uploading a file or searching on Wikipedia in the sidebar.
        """
    )
else:
    response = run_quiz_chain(docs, topic if topic else file.name)
    with st.form("questions_form"):
        for question in response["questions"]:
            st.write(question["question"])
            value = st.radio(
                "Select an options",
                [answer["answer"] for answer in question["answers"]],
                index=None,
            )
            if {"answer": value, "correct" : True} in question["answers"]:
                st.success("Correct!")
            elif value is not None:
                for answer in question["answers"]:
                    if answer["correct"] == True:
                        st.error(answer["answer"])
        button = st.form_submit_button()
```