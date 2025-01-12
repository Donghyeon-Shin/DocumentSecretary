# LangChain?
	LLM을 사용하여 앱을 쉽게 만들 수 있게 만들어진 프레임워크이다.
	LLM 모델 변환이 자유로우며 모델 구현을 `Chain`으로 단순화 한 것이 특징이다.
	여러 앱의 LLM 기술을 접목시킬려는 시도가 증가함에 따라 LangChain의 중요도 또한 증가하고 있다.
![[LangChain Icon.png]]
- 해당 Part는 Langchian에 대한 개념 및 사용법에 대해 정리해놓은 것이다.
- 🌐[노마드코더](https://nomadcoders.co)의 강의를 보며 공부하였으며 🌐[GitHub Site](https://github.com/Donghyeon-Shin/langchain-practice)에서 Detail을 볼 수 있다.
- LangChain를 공부해 최종적으로 나만의 앱을 만들어보는 것이 최종 목표이다.
# Before learning LangChain
## Setting
- Python version은 강의와 같은 환경에서 하기 위해 `3.11.6`을 이용하였다.
- Langchain을 공부하기 위해서는 여러 libraries을 사용하게 되는데, 내가 평소 사용하는 환경 안에서 해당 libraries을 설치하면 충돌 및 오류가 발생 할 수 있다.
- 따라서 `python -m venv <env>`로 env 가상환경을 만들어 그 안에서 필요한 libraries을 설치하였다.
- `<env>\Scripts\activate.bat:(Window 환경)`으로 가상환경 안으로 들어갈 수 있다.
- 여러 libraries을 한 번에 설치하는 방법은 필요한 libraies 목록을 `.txt` 형식으로 따로 만들어 `pip install -r <requirements>.txt` 명령어를 사용하면 된다.
- 가상환경은 `deactivate` 명령어를 사용하여 빠져나올 수 있다.
## Jupter NoteBook
- 코드를 **블럭(cell) 단위**로 실행할 수 있게끔 하여 Interpreter의 장점을 극대화 할 수 있게 하는 웹기반 플랫폼이다.
- `.ipynb` 확장자로 열 수 있다.
- Shortcut Key (Window Ver)
	- ESC : Cell 편집 모드 -> Cell 선택 모드
	- ENTER : Cell 선택 모드 -> Cell 편집 모드
	- CTRL + ENTER : 해당 Cell 실행
	- SHIFT + ENTER : 해당 Cell 실행 후 Cell 생성
	- A / B : (Cell 선택 모드에서) 위(A) 또는 아래(B)로 Cell 생성
	- DD or DELETE : (Cell 선택 모드에서) 선택된 Cell 삭제
- Cell 내부의 마지막 값은 Cell 실행 시 별도의 `Print()` 출력 없이 결과 값이 나온다.
- 위 Cell들의 값이 보존되기 때문에 구현 및 수정을 편하게 할 수 있다.
# Study Langchain
## LangChain Basic
##### 🔗[[Using OpenAI models And LangChain]]
## Model IO
##### 🔗[[Prompt]]
##### 🔗[[Output Parser]]
##### 🔗[[LCEL(LangChain Expression Language)]]
## Memory
##### 🔗[[Caching]]
##### 🔗[[Memory Modules]]
##### 🔗[[Link Memory to Model]]
## RAG(Retrieval-Augmented Generation)
##### 🔗[[RAG(Retrieval-Augmented Generation)]]
##### 🔗[[Retrieval]]
##### 🔗[[Stuff LCEL Chain]]
##### 🔗[[Refine LCEL Chain]]
##### 🔗[[Map Reduce LCEL Chain]]
##### 🔗[[Map Re-rank LCEL Chain]]
## Document GPT
##### 🔗[[Streamlit]]
##### 🔗[[Document GPT]]
## Private GPT
##### 🔗[[Offline Model]]
##### 🔗[[Private GPT]]
## Quiz GPT
##### 🔗[[WikipediaRetriever]]
##### 🔗[[Function Call Method]]
##### 🔗[[Quiz GPT]]
## Site GPT
##### 🔗[[Site Loader]]
##### 🔗[[Site GPT]]
## Meeting GPT
##### 🔗[[Video Preprocessing]]
##### 🔗[[Meeting GPT]]
## Investor GPT
##### 🔗[[Agent]]
##### 🔗[[Investor GPT]]
## Chef GPT
...
## Assistants API
##### 🔗[[Assistant]]
##### 🔗[[Investor and RAG GPT Using OpenAI Assistant]]
## Crew AI
##### 🔗[[Crew]]
##### 🔗[[Investment Recommendation CrewAI]]