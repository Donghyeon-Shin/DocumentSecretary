# Concept
- [`Wikipedia`](https://ko.wikipedia.org/wiki)는 위키(wiki)와 백과사전(encyclopedia)이 합쳐진 단어로, 누구나 자유롭게 쓰는 다언어판 온라인 백과사전을 뜻한다.
- `LangChain`에서는 `Wikipedia`의 데이터를 받아 Retriever를 불러오는 `WikipediaRetriever` module을 지원한다.
- `WikipediaRetriever`은 `from langchain.retrievers import WikipediaRetriever`로 불러 올 수 있다.
- `Wikipedia`에서 받아온 데이터들은 크기가 크기 때문에 보통의 modeld은 한 번에 input 받을 수가 없다. 하지만 gpt-3 turbo or gpt-4는 **Context window**가 매우 크기 때문에 한번에 받아올 수 있다.
# Method
- WikipediaRetriever에는 다음과 같은 `Parameter`가 있다.
	- `top_k_results={integer}` : 관련 문서 몇 개를 다운로드 할 지를 결정한다.
	- `lang: "{language}"` : 특정 언어(language)로 되어 있는 위키피디아를 검색한다. default는 영어(`en`)이며 `ko`가 한국어이다.
	- `load_max_docs:{integer}` :  다운로드하는 문서의 수를 설정할 수 있다. 값이 크면(ex, 300) 그만큼 시간이 오래 걸리기 때문에 적절한 값을 넣는 것이 좋다. default는 100이다.
	- `load_all_available_meta:{boolean}`: 중요한 `필드`만 다운로드 할 지, 다 다운로드 할 지를 결정한다. default는 False이다.
- WikipediaRetriever에는 `get_relevant_documents("{topic}")`이라는 function이 존재하는데, 이는 관련 단어 or 문장에 해당하는 문서를 `Wikipedia`에서 찾는데 사용된다.
```python
topic = st.text_input("Search Wikipedia")
if topic:
	retriever = WikipediaRetriever(top_k_results=5, lang="ko")
	with st.status("Searching wikipedia....."):
		docs = retriever.get_relevant_documents(topic)
	st.write(docs)
```
