# Motivation for development
- 군대에서 알고리즘을 공부하면서 `Obsidian`에 해당 내용들을 정리하기 시작했다.
- 알고리즘 특성 상 서로 연관되어 있는 경우가 많다 보니, 실제로 내가 정리한 알고리즘을 찾아볼 때 해당 문서를 찾고 검색하는 과정이 복잡하고 귀찮았다.
- 또한 `Obsidian`에 정리한 내용들이 점점 많아지면서 이것들을 따로 정리 및 요약하고 하는 기능을 만들고 싶어졌다.
- 그래서 내가 직접 파일을 찾는게 아나라, 인터넷에 검색하는 것처럼 내 문서를 바탕으로 한 검색 엔진 기능과 해당 파일들을 정리 해줄 수 있는 프로그램을 만들어야겠다고 생각했다.
# Project Goals(MVP)
- *LangChain*과 *Crew*을 이용해 파일 검색 기능을 만든다.
- 키워드를 입력 받고 해당 키워드에 해당되는 문서를 찾는 기능을 만든다.
- 문서 안의 개념을 이해 할 수 있도록 하는 도와주는 다른 파일들을 찾는 기능을 만든다.
- 키워드에 맞는 문서의 내용을 요약하는 기능을 만든다.
- 키워드의 맞는 문서의 개념 이해도를 체크할 수 있는 퀴즈 기능을 만든다.
- 불러온 파일들을 `LLM`에게 전달하여 관련 문서들에 대해 검색할 수 있는 채팅 기능을 만든다.
- *Streamlit*을 사용해 UI를 구현하고 이를 Stream Cloud로 배포한다.
 
# Proejct Detail
- [Document Link](https://dongle-portfolio.org/Project/Document+AI+Secretary/Document+J.A.R.V.I.S+Introduction)

# Service Screenshot
### 메인 화면
<img width="718" height="439" alt="file selecting screen" src="https://github.com/user-attachments/assets/7c1c488a-f5cc-4476-a867-739f65fa45c1" />

### 키워드에 관련된 파일 검색 
<img width="718" height="439" alt="file selecting screen" src="https://github.com/user-attachments/assets/7b2482c2-48ec-4708-98ad-38fb0d8b5603" />****

### 불러온 파일 목록
<img width="780" height="672" alt="file list screen" src="https://github.com/user-attachments/assets/fe587254-f0b7-43ff-a2ce-f6c730aec9c3" />

### 관련 파일 선택
<img width="781" height="853" alt="file select option screen" src="https://github.com/user-attachments/assets/d2c41e49-b042-424a-9564-0581472d25f2" />

### 문서 요약
<img width="773" height="599" alt="document summary screen" src="https://github.com/user-attachments/assets/b57ce1d0-74a2-41fd-90d9-297011efe3a8" />

### Quiz
<img width="726" height="192" alt="quiz make screen" src="https://github.com/user-attachments/assets/69fb04b3-73db-41e1-a08e-eb833a83a25a" />
<img width="723" height="1005" alt="quiz list screen" src="https://github.com/user-attachments/assets/db678bda-c765-4887-bedb-5cd6d6066ff7" />
