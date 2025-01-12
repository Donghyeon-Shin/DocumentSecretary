# Concept
- `Streamlit`은 `AI/ML engineer`들이 데화형 데이터 앱을 만들 수 있도록 돕는 `open-source Python framework`이다.
- 다양한 Widgit이 구현되어 있으며 이를 불러와 **나만의 UI을 쉽게 제작할 수 있다.**
- `import streamlit`을 통해 불러올 수 있다.
- Steamlit이 설치되어있는 가상환경에서 cmd에서 `streamlit run {file}.py`를 하면 streamlit server(offline)을 작동시킬 수 있다.
- cmd에서 `Ctrl+c`를 하게 될 시 Server가 종료된다.
# Reference
#### with
- 특정 `Resource`를 사용할 때 `with` 구문을 사용해서 간편화 할 수 있다.
```python
st.sidebar.title("sidebar titile")
st.sidebar.text_input("XXX")
```
->
```python
with st.sidebar:
    st.title("sidebar title")
    st.subheader("sidebar Subheader")
```
#### session_state
- `.session_state`을 사용하면 페이지가 초기화(사용자 상호 작용이나 코드 변경마다) 돼도 특정 값을 유지 할 수 있다.
- `session_state["{variable name}"] = {type}`을 하게 되면 streamlit에서 `session_state["{variable name}"]`의 값은 초기화 하지 않는다.
- 단 `session_state["{variable name}"] = {type}`만 단독으로 쓰게 될 시, 전체 코드가 다시 실행되면서 값이 초기화 되기 때문에 `if "messages" not in st.session_state` 같은 조건을 추가해 해당 변수에 값이 없을 때만 초기화 할 수 있도록 조정해주어야 한다.
- 변수를 사용할 때도 `st.session_state["variable"]`로 불러오면 된다.
```python
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.session_state["messages"].append({"message" : message, "role" : role})
```
#### @st.cache_data or resource
- `@st.cache_data` or `@st.cache_resource`을 사용하면 streamlit에서 해당 함수의 데이터가 변하기 전까지 함수를 다시 실행하지 않고 전의 있던 결과를 return 시킨다.
- `st.cache_data`는 함수의 return 값이 **`pickle`로 직렬화 될 수 있는 type인 경우** 사용할 수 있고 `st.cache_resource`는 데이터베이스 연결이나 `Tensorflow` 세션 같이 **`pickle`가 직렬화 할 수 없는 type**를 cache 하려고 할 때 사용한다.
```python
@st.cache_resource(show_spinner="Embedding file...")
def embed_file(file):
```
- `st.cache`안에 함수의 Parameter가 **hash** 할 수 없는 경우에 `UnhashableParamError`가 발생한다.
- `hash`의 뜻은 들어오는 데이터의 **서명**을 생성한다는 것을 의미한다. `st.cache`는 해당 데이터의 서명을 근거로 데이터가 바뀌였는지, 아닌지를 판단하고 이를 기준으로 **함수의 실행 여부**를 결정한다.
- 따라서 hash 할 수 없는 데이터가 들어왔을 경우 `st.cache`는 오류를 발생시킨다.
- 이를 해결하기 위해 hash 할 수 없는 데이터의 변수명 앞에 `_` 을 포함 시키면 streamlit에서 해당 문서를 hash 하려 하지 않는다. 그리고 **다른 hash 할 수 있는 변수를 추가로 포함**한다면 `UnhashableParamError`를 해결할 수 있다.
```python
@st.cache_data(show_spinner="Making quiz...")
def run_quiz_chain(_docs, topic):
    chain = {"context": questions_chain} | formatting_chain | output_parser
    return chain.invoke(_docs)
```
- * hash를 할 수 없다는 뜻은 해당 데이터가 **변경 가능(Mutable)한 인자**를 가지고 있다는 뜻이다. ex) list, dic, etc..
#### pages
- streamlit `{main}.py`에 `pages` 폴더를 만들고 거기에 하위 python file를 넣는다면 streamlit에서 자동으로`sidebar`에 해당 files을 연결시켜준다.
![[Streamlit Page Detail.png]]
# Widget
- `Streamlit`에는 수 많은 `Widget`이 있다. 여기 문서에는 [[LangChain Introduction]]에서 사용한 `Widgit`만 정리 하였다.
- [Steamlit widget 문서](https://docs.streamlit.io/develop/api-reference)을 통해 더 자세한 정보를 알 수 있다.
## Display Widget
#### write and magic
- `.write({any types})` : write 함수는 어떤 타입의 값이 나와도 화면에 출력해준다. LangChain의 module을 그대로 출력하면 module의 사용방법, funtion 등도 함께 포함되어 나온다.(LangChain에서 module의 적어놓은 정보들)
- `write` 함수를 쓰지 않아도 그냥 변수만 적으면 write와 동일하게 화면에 출력 시켜주는데 이를 streamlit에서는 `magic`이라고 표현한다.
```python
st.write("hello")
st.write([1, 2, 3])
st.write({"x": 1})

ChatPromptTemplate # 이렇게 적어도 화면에 표시된다. -> it's magic
```
#### set_page_config
- `page_title` : web 상단 이름을 지정한다.
- `page_title` : web 상단 아이콘을 지정한다.
```python
st.set_page_config(
    page_title="FullstackGPT",
    page_icon="🤣",
)
```
#### title
- 화면에 title 양식으로 값을 출력한다.
```python
st.title("Hello world!")
```
#### subheader
- 화면에 subheader 양식으로 값을 출력한다.
```python
st.subheader("Welcome to Streamlit!")
```
#### markdown
- 화면에 markdown 형식으로 값을 출력한다.
```python
st.markdown(
    """
    #### I love it!
    """
)
```
#### sidebar
- `.sidebar` 형식으로 사이트 옆에 값들을 출력한다.
```python
with st.sidebar:
	st.title("sidebar titile")
    st.text_input("XXX")
```
#### tabs
- `.tabs(["tab1", "tab2", ...])` : 여러 tab 항목을 List 형식을 지정한다.
- `.tab_name` 형식으로 각 tab 안의 내용들을 구성할 수 있다.
```python
transcript_tabs, summary_tabs, qa_tab = st.tabs(
	[
		"A_tabs",
		"B_tabs",
		"C_tabs",
	]
)

with A_tabs:
	st.write("A_tabs")

with B_tabs:
	st.write("B_tabs")

with C_tabs:
	st.write("C_tabs")
```
#### chat_message
- `role`은 "ai", "human" 등이 있으며 해당 역할로 값들을 출력한다.
```python
with st.chat_message(role):
	st.markdown(message)
```
#### success
- 해당 `String`을 success format으로 출력한다.
```python
st.success("Correct!")
```
#### error
해당 `String`을 error format으로 출력한다.
```python
st.error("Wrong!")
```
## Input Widget
- `Stremlit`에서 input widget을 사용하여 data가 변경될 때 마다, **python 파일 전체가 다시 실행**된다.
- `session_state`을 통해 특정 데이터를 **Caching**할 수 있다.
#### selectbox
- `{String}, {tuple}`로 `String`은 selectbox widgit의 내용을 표현하고 `tuple`은 selectbox의 options을 설정한다.
```python
model = st.selectbox(
    "Choose your model",
    ("GPT-3", "GPT-4"),
)
if model == "GPT-3":
    st.write("cheep")
else:
    st.write("not cheep")
```
#### slider
- `{String}, min_value={float}, max_value={float}`로 `String`은 slider widgit의 내용을 표현하고 `min_value`는 slider의 최소값을 `max_value`는 최대값을 설정한다.
```python
value = st.slider(
    "htemperature",
    min_value=0.1,
    max_value=1.0,
)
```
#### text_input
- `text` 형태의 `input bar`가 생기며 `String` 값을 전달 받는다.
```python
name = st.text_input("What is your name?")
```
#### chat_input
- 사이트 하단에 `chatting bar`이 생기며 `String` 값을 전달 받는다.
```python
message = st.chat_input("Send a message to the ai")
```
#### radio
- 여러 `options`들 중 하나를 선택할 수 있는 `select bar`을 만들어 준다.
- `String`으로 해당radio를 설명할 수 있으며, `list`로 options을 표현한다. `index`는 처음 상태에서 어떤 값이 선택되어있는지를 설정할 수 있는 Parameter이다.
```python
value = st.radio(
	"Select an options",
	[answer["answer"] for answer in question["answers"]],
	index=None,
)
```
#### uploading file
- `{String}, type = {list}`로 `String`은 upload widgit의 내용을 표현하고 `type`은 `list`에 포함된 확장자만 input 받을 수 있도록 설정한다.
```python
file = st.file_uploader(
    "Upload a .txt .pdf or .docx file",
    type=["pdf", "txt", "docx"],
)
```
#### form
- 값들을 `form` 형식으로 출력해준다.
- `form` 내부에는 form을 이루는 값들과 `form_submit_button()`이 있어야 한다.
- `form` 내부에서 작동하는 일들은 `streamlit`에서 `form_submit_button()`을 누르기 전까지 데이터를 업데이트 시키지 않는다.
```python
with st.form("questions_form"):
	for question in response["questions"]:
		st.write(question["question"])
		value = st.radio(
			"Select an options",
			[answer["answer"] for answer in question["answers"]],
			index=None,
		)
	button = st.form_submit_button()
```