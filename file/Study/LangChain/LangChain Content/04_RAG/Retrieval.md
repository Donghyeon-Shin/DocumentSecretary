# Process
- `Retrieval`를 수행하는 과정은 크게 5가지로 분류된다.![[Retrieval Process.jpg]]
	- Load : Source를 가져오는 과정이다.
	- Transform : Load된 문서를 적절하게 **Split**하는 과정이다.
	- Embed : 나누어진 문서들을 컴퓨터가 이해할 수 있도록 숫자로 변환하는 과정이다.
	- Store : `Embedded` 데이터(vectors)를 저장소에 저장하는 과정이다.
	- Retrieve : 저장된 데이터를 [[Prompt]]와 조합하여 model이 `Question`을 **Response** 할 수 있도록 적용하는 과정이다.
## Load
- LangChain에서는 `.txt`, `.docx`, `.md`, `.pdf` 등 여러가지 문서들을 Load 할 수 있도록 지원해준다.
- 문서의 확장자에 따라 Load module이 다르지만 `from langchain.document_loaders import UnstructuredFileLoader`을 사용하면 **대부분의 files을 load** 할 수 있다.
- `UnstructuredFileLoader('Path')`에서 Path의 올바른 경로를 지정한 뒤 `load()` function으로 파일을 불러올 수 있다.
```python
from langchain.document_loaders import UnstructuredFileLoader
loader = UnstructuredFileLoader("./files/chapter_one.txt")

loader.load()
```
## Transform
- Transform의 대부분은 **Split**하는 과정을 말한다.
- 문서를 나누는 이유는 model에게 문서의 전체 내용을 줄 시, 해당 문서에서 필요한 정보를 찾는 시간도 길어지고 이를 계산하는 비용도 올라가 **비효율적인 model**이 되기 때문이다.
- Splitter는 여러가지가 있지만 가장 보편적인 `RecursiveCharacterTextSplitter`와 특정 separator로 문서를 나누게 해주는 `CharacterTextSplitter`가 가장 많이 사용된다.
#### RecursiveCharacterTextSplitter
- `RecursiveCharacterTextSplitter`는 텍스트를 의미적으로 관련 있는 텍스트들 끼리 같이 있도록 분할 시켜준다.
- `from langchain.text_splitter import RecursiveCharacterTextSplitter`로 불러올 수 있다.
- `RecursiveCharacterTextSplitter`는 문서를 얼만큼의 크기로 나눈 것인지를 정하는 **chunk_size**와 나누는 과정에서 문장이 잘리는 것을 대비해 나누어진 앞뒤 문장이 얼마만큼 겹치게 할 것인지 정하는 **chunk_overlap**이 있다.
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

 splitter = RecursiveCharacterTextSplitter(
    chunk_size = 200,
    chunk_overlap = 50,
)
```
#### CharacterTextSplitter
- `from langchain.text_splitter import CharacterTextSplitter`로 불러올 수 있다.
- `CharacterTextSplitter` 또한 RecursiveCharacterTextSplitter 같이 chunk_size와 chunk_overlap이 있지만 특정 separator을 기준으로 나누는 **separator** parameter도 있다.
```python
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size = 600,
    chunk_overlap = 100,
)
```
#### Token Splitter
- `RecursiveCharacterTextSplitter`와 `CharacterTextSplitter`는 기본적으로 우리가 이해하는 **문자**을 기준으로 분리를 한다.
- LLM은 우리가 글자를 세는 것과 달리 **Token**이라는 특정 단위로 글을 세며, 이해한다. 따라서 Model이 문서를 이해하기 위해서는 문자가 아닌 Token을 기준으로 문서를 나누는 것이 좋다.
- `from_tiktoken_encoder` function으로 Token을 기준으로 chunk를 나눌 수 있다.
```python
splitter = CharacterTextSplitter.from_tiktoken_encoder(
    separator="\n\n",
    chunk_size = 300,
    chunk_overlap = 50,
    length_function=len,
)
```
#### Use Text Splitter
- Splitter을 사용하는 방법은 두 가지가 있다.
	- `loader.load()`을 통해 불러온 **List 형태**의 문서를 각 Splitter Class에 `split_documents()` function을 사용해 나누는 방법
	- loader 자체의 `load_and_split` function에서 `text_splitter` parameter 값에 splitter을 넣어 load하는 방법
```python
docs = loader.load()
splitter.split_documents(docs)
```
OR
```python
loader.load_and_split(text_splitter=splitter)
```
## Embed
- 컴퓨터가 이해할 수 있도록 단어를 숫자로 변환하는 것을 말한다. 다시 말해, 한 단어를 여러 특징들의(Ex : Easculinity, Femininity, Royalty) 조합으로(vector) 표현하는 것이다.
- 이를 **vector representaion**이라고 하며 단어를 vector로 표현했을 시, 단어들의 연산이 가능해지며 이러한 단어들의 연산으로 또 다른 단어를 만들 수 있다. (참고 사이트 : [Word2Vec Example Site](https://turbomaze.github.io/word2vecjson/))
- OpenAI에서는 `from langchain.embeddings import OpenAIEmbeddings`로 embedding을 할 수 있게 해준다.
- `OpenAIEmbeddings`의 `embed_query("Str")` function으로 Str을 embedding 할 수 있다.
```python
from langchain.embeddings import OpenAIEmbeddings

embedder = OpenAIEmbeddings()
embedder.embed_query("Hi")
```
- 문서를 embedding 하기 위해선 `embed_documents` function을 사용한다.
- 이는 각 List 원소마다 map을 통해 각 vector를 구해주는 과정(embed)으로 이해하면 된다.
```python
embedder.embed_documents(["HI", "how", "are", "you longer sentence because"])
```
## Store
- embbeding 과정은 문서 당 한 번만 수행하면 되기 떄문에  Caching을 통해 저장해두었다 활용하는 것이 좋다.
- (vector) Store는 `Chroma`, `FAISS` 같은 것들이 있지만 나는 `Chroma`로 사용하였다.
### Chroma
- `Chroma`는 `from langchain.vectorstores import Chroma`로 불러올 수 있으며 `from_documents(docs, embedder)` function을 이용하면 해당 `docs`가 `embedder`을 거쳐 ebedding 된 상태로 저장된다.
```python
from langchain.vectorstores import Chroma

docs = loader.load_and_split(text_splitter=splitter)
embedder = OpenAIEmbeddings()

vectorStore = Chroma.from_documents(docs, embedder)
```
### Local File Store
- `Chroma`는 내 컴퓨터 메모리에 저장되는 vector store 이기 때문에 실행 환경이 초기화되면 저장 내용이 삭제된다.
- 따라서 저장 내용을 파일로 저장할려면 저장할 파일 경로와 `embedder`를 Cache 해줄 `CacheBackedEmbeddings`가 추가로 필요하다.
#### Set File Path
- 파일 경로는 `from langchain.storage import LocalFileStore`을 통해서 지정할 수 있다.
```python
from langchain.storage import LocalFileStore

cache_dir = LocalFileStore("./.cache/")
```
#### Cache Embedder
- `from langchain.embeddings import CacheBackedEmbeddings`의 `from_bytes_store(embeder, path)` function을 통해 embedder와 저장 경로를 입력하면 embedder가 embedding 후 해당 경로에 파일을 Cache 할 수 있도록 설정해준다.
```python
from langchain.embeddings import CacheBackedEmbeddings

cached_embedding = CacheBackedEmbeddings.from_bytes_store(embedder, cache_dir)
```
#### Save File and Search
- `Chroma`의 `from_documents()` function에서 `embedder` 대신 cache 하도록 설정된 `cached_embedding`을 넣어주면 Chroma가 문서를 embedding 하기 전에 cached_embedding로 접근해 지정 경로에 embedding된 파일이 있는지 확인 후, 있다면 불러오고 **없다면 emdding 후 저장**하도록 설정하여 줄 수 있다.
```python
vectorStore = Chroma.from_documents(docs, cached_embedding)
```
- 저장된 embeded files에서 무언가 seacrh 하고 싶을 땐 `similarity_search("Question")` function을 사용하면 된다.
```python
vectorStore.similarity_search("where does winston live")
```
#### Converte vector Store to Retriver
- `Retriver`는 특정 저장 공간에서 선별해서 문서를 가져오는 과정을 말한다.
- LangChain에서는 쉽게 **선별된 문서들**이라고 생각하면 된다.
- LangChain의 `vector Store`은 `as_retriever()`function을 사용하여 `vector Store`에서 `Retriver`로 쉽게 변환할 수 있다.
```python
retriver = vectorStore.as_retriever()
```
