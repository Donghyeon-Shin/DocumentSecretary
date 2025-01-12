# Concept
- `Gpt-3.5-turbo`나 `GPT-4o` 같은 유료 Model을 사용할 수도 있지만, 직접 Model을 다운해 로컬 컴퓨터로 연산하는 `Offline Model`을 사용할 수도 있다.
- 컴퓨터 성능만 좋다면, 무료로 GPT-4와 비슷한 Model 성능을 발휘할 수 있다.
- 하지만 대부분의 컴퓨터가 성능이 좋지 않기 때문에 유료 Model에 비해 `Context Window, Input/Output Max Token`등이 적은 Offline Model을 사용하게 된다.
- 따라서 성능이 크게 중요하진 않은 Project에 사용하는게 좋다.
# Offline Model Types
- Offline Model을 사용하는 방법은 크게 `Hugging Face`, `Gpt4 all`, `Ollama`가 있다.
- 개인적으로는 UI가 보기 편한 `Ollama`을 주로 사용한다.
## Hugging Face
- [Hugging Face Model](https://huggingface.co/models)에서 여러 models을 볼 수 있다.
- model 마다 Parameter가 다르고 사용해야 되는 **instruct format(prompt format)** 이 다르기 때문에 각 model의 문서를 확인하고 사용해야 한다.
- `from langchain_huggingface import HuggingFaceEndpoint`을 이용해 hugging face의 model을 사용할 수 있다.
- `HuggingFaceEndpoint`에 `repo_id = {"model 이름"}`, `model_kwargs = {각 model에서 요구하는 parameter}`를 넣어주면 된다.
- 이는 `Hugging Face Hub`를 이용한 방법으로 API를 이용하는 것이기 때문에 model 마다 무료일 수는 있어도 데이터는 여전히 `Hugging Face`로 넘어가진다.
```python
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template("[INST]What is the meaning of {word}[/INST]")

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    model_kwargs={
        "max_new_token": 250,
    },
)

chain = prompt | llm

chain.invoke(
    {
        "word": "potato",
    }
)
```
- model을 다운로드 받고 싶으면 `from langchain.llms.huggingface_pipeline import HuggingFacePipeline`을 이용해서 `from_model_id` functoin으로 `model_id = "{model name}"`과 `task="{task name}"`을 적으면 된다.
- 모델의 크기가 클 시 다운로드 시간이 길어지고, 컴퓨터 사양에 따라 model이 작동되지 않을 수 있기 때문에 **공식문서**를 참고하여야 한다.
- `device = {0 or -1}` Parameter로 model 연산 장치를 정할 수 있는데, 0이면 GPU를 -1이면 CPU를 사용해 연산하겠다는 뜻이다.
```python
from langchain.llms.huggingface_pipeline import HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id="gpt2",
    task="text-generation",
    device = -1,
    pipeline_kwargs={
        "max_new_tokens": 150,
    },
)
```
## Gpt4 all
- `hugging face`와 마찬가지로 model을 다운로드 받고 사용할 수 있다.(각 사이트마다 존재하는 model이 다르다.)
- [Gpt4all Website](https://www.nomic.ai/gpt4all) 해당 사이트를 통해 사용 방법을 알 수 있다.
## Ollama
- [Ollama Website](https://ollama.com/download)에서 ollama을 다운로드 받아야 한다.
- ollama는 실제 내 컴퓨터에 서버(`http://localhost:11434/`)를 만들어 작동한다. 
- `cmd`에 `ollama list`을 입력하면 내가 가진 모델들과 내 컴퓨터에 있는 모델 크기를 볼 수 있다.
- `ollama rm {model name}`을 입력하면 model을 지울 수 있다.
- ollama는 UI가 보기 편하고 쉽게 정리 되어 있기 때문에 다른 것들보다 사용하기 편하다
- LangChain에서 `Ollama`을 지원해주는데. `from langchain.chat_models import ChatOllama`로 불러 올 수 있다.
- `ChatOllama`는 `ChatOpenAI`와 사용 방법이 동일한데, 추가로 `model="{model name}"`과 `base_url="{ㅡmodel server url}"`과 같은 Ollama 전용 Paramter가  존재한다.
```python
from langchain.chat_models import ChatOllama

llm = ChatOllama(
    model="mistral:latest",
    base_url="http://localhost:11434",
    temperature=0.1,
    streaming=True,
    callbacks=[ChatCallbackHandler()],
)
```
- Embedding 또한 `from langchain.embeddings import OllamaEmbeddings`로 불러 올 수 있다.
- `ChatOllama`와 마찬가지로 `model="{model name}"`과 `base_url="{ㅡmodel server url}"`과 같은 Ollama 전용 Paramter가 추가된다.
```python
embedder = OllamaEmbeddings(model="mistral:latest")
```
