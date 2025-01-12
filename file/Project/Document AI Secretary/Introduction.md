# Motivation for development
- `Obsidian`을 이용해 공부했던 내용들을 정리하는 과정에서 상당히 많은 내용이 내 Site에 축적되었다.
- 문제는 이러한 내용들을 내가 다 기억하는 것이 아니라, 자주 까먹기도 하기 때문에 자주 내가 정리한 내용을 참고한다. 문제는 내가 어느 부분에서 해당 질문에 대한 답을 정리하였는지 기억하지 못한단느 것이다.
- 또한, 내가 강조할 만한 것이 남에ㅔㄱ~~~~
- `GPT-3/4` 같은 `LLM`이 등장하면서 20~30대가 검색 엔진을 대체하여 이를 이용하려 하고 있다.
- 



# Goals
- 대부분의 질문에 `LLM`은 잘 답변하지만, 학습된 데이터가 별로 없는 내용에 대해서 질문을 할 경우 `LLM`이 틀린 답을 마치 알고 있다는 듯이 얘기하는 `인공지능 환각` 문제가 발생하고 있다.
- `인공지능 환각` 문제를 해결하기 위해서는 참고할 만한 명확한 데이터를 `LLM`에게 제공하면 된다.
- 해당 `Program`을 이용해 `LLM`에게 질문을 하게 되면 사용자가 적은 내용을 바탕으로 답을 하기 때문에 `인공지능 환각` 문제를 완전히 해결할 수 있고, 사용자가 완전히 신뢰할만한 답변을 제공할 수 있다.
- 사람마


git 
```git
 git reset --hard "해당commit" 
```
->해당 commit 위치로 이동. **해당 지점 전에 있던 file들 다 날라감!!!**
```git
 git push -f origin master
```
-> 해당 위치 후의 push 내용들 다 사라짐

# Development process
- AI를 사용하여 개인 문서를 
# Problmes
- [25.01.05.] - 사용자의 질문에 답을 하기 위해 여러 `File`들을 찾게 되는데 여러 `File`을 AI가 직접 찾게 하기 위해서 `Crew AI` 사용하기로 하였다. `Crew AI`의 FileReadTool()을 사용하여 질문에 답을 할만한 file을 특정 경로에서 찾고 이를 요약하게 하는 것을 목표로 구현을 진행하였다. 문제는 `Crew AI` 가 해당 답을 구할 수 있는 `file`을 찾지 못하는 문제가 계속 발생한다는 것이었다. 이를 해결하기 위해선 우선 답을 구할 수 있는 `File`을 찾도록 시키는 것이 아니라 우선 모든 `File`을 다 `Load`하고 거기서 질문에 대한 답을 찾을 수 있도록 구현해야 할 것 같다. 하지만 이렇게 하면 모든 file을 load하는 과정에서 너무 많은 token을 사용하게 돼. 비용적인 측면에서 부담이 생길 것 같다. / 우선 DirectorySearchTool을 사용하여 특정 경로에 있는 모든 md files을 불러오도록 설정하였는데 어떤 이유에서 인지 md file을 찾지 못함 -> md file들을 우선 다 caching 한 상태에서 불러오는 형식으로 진행하는 것이 `RAG`을 계속 사용하지 않기 때문에 저렴하다. 따라서 우선 Caching한 후 데이터를 불러 오는 것까지 구현하는 것이 1차 목표이다. --->>>> `DirectorySearchTool`이 아닌 `DirectoryReadTool`을 사용했어야 했다. 정상적으로 지정 경로 안의 모든 `markdown` file 경로를 가져온다. [git commit](https://github.com/Donghyeon-Shin/DocumentSecretary/commit/343c7f18e7fce0ad6dd4c8943c3ef7aba888c4df) 
- [25.01.06.] - `pathSearcher`로 폴더에 있는 markdown file을 다 가져온 뒤, `research`가 질문에 답을 할 수 있는 markdown file을 읽고 이를 요약해 출력하도록 구현해보았다. 문제는 해당 markdown file안에 연관 되어 있는 다른 file은 읽어드리지 못한다는 것인데, 이를 해결하기 위해서 `agent`와 `tool`을 여러 개로 쪼개 사용하도록 하는 것이 나을 것 같다. ex) `fileSelector` Agent를 만들어서 우선 메인 markdown 파일을 읽고 거기에 연관된 모든 file을 선별해내고 `research`로 선별된 모든 파일들을 읽고 요약하는 방법.. [git commit](https://github.com/Donghyeon-Shin/DocumentSecretary/commit/fd5d7e0bc46d0edaec172d625b388e2701ed4ca3) / 성공했다!!!, 문제는 잘못된 파일을 불러오는 경우는 없었으나, 여러 파일들 중 한 두개가 포함되지 않는 경우가 있었다는 것... 결과가 매번 달라져서 이를 어떻게 해결해야될지 고민이다...[git commit](https://github.com/Donghyeon-Shin/DocumentSecretary/commit/b1e59ce441b9ee20bf3b29a6fe1ce7803142656f)
- [25.01.07.] - crewAI의 Vision Tool을 사용하여 해당 file에 있는 img를 text로 변환하는 과정을 수행하려 하였다. 문제는 Vision Tool가 svg 이미지을 지원하지 않는다는 것이다. 내가 정리한 obsidian의 IMG 파일들은 모두 svg 파일이기 때문에 Vision Tool이 해당 Img를 로드하는 과정에 오류가 발생했다... 이를 해결하기 위해서 obsidian의 Excalidraw의 플러그인의 자동 변환 파일을 png로 설정하여 모든 file을 png로 변환하고 Vision Tool을 사용해야 한다. [git commit](https://github.com/Donghyeon-Shin/DocumentSecretary/commit/d470ab7539b41e70c0f9e9b80834566c23faef4e)
- [25.01.07.] - `textOrganizer`이라는 Agent을 사용하여 각각의 markdown 파일을 읽고 분석하여 출력하도록 만들었다. 문제는 이러한 과정이 너무나 오래 걸린다는 것이다... 재대로 작동하지도 않음... 그래서 CrewAI는 imgExtracter로만 이용하고 path를 json 형식으로 만들어 따로 LangChian으로 이들을 읽고 분석하여 하나의 결과 값으로 만들도록 해야 할 것 같다.  [git commit](https://github.com/Donghyeon-Shin/DocumentSecretary/commit/e36ae94baa2cfe7e0a80e33511edbfa8f72a0fc6
- [25.01.08.] - `Agemnt`에게 `FileReadTool()`을 사용하라고 했을 때, 계속해서 파일을 읽지 못하고 오류가 발생함을 발견하였다. 처음에는 file의 경로의 이상이 있어 불러오지 못하는 것이라 생각했는데 파일의 경로 양식을 지정하여도 오류가 계속해서 발생하였다. 이를 계속 탐구해보니 FileReadTool의 Parameter가 `file_path`인데 간헐적으로 `filepath`로 넘겨 `FileReadToolSchema Error`가 발생한다. 따라서 `Agent`에게 `file_path`로 넘기라는 것을 명시해주어야 한다. 
- [25.01.09.] - `CrewAI`의 `Agent`가 같은 input을 가지고 동일한 Task을 계속 수행하는 문제가 발생했다. 때문에 계속 input taken이 초과되고 올바른 결과 값이 나오지 않았다. 이를 해결하기 위해, 여러 사이트를 찾아봤지만, 대부분의 사람들이 같은 문제를 겪고 있었고 이를 해결할 특별한 방도가 없음을 알았다. 정확히 말하자면 `LLM`이 `Agent`에게 계속해서 `Tool`을 사용하도록 요구해 발생하는 문제로, `GPT-3.5-turbo-1106`은 해당 문제가 발생하지 않지만 `GPT-4o-mini`에서는 발생하였다. .. 하지만 `GPT-3.5-turbo-1106`의 경우는 `Agent`의 결과값이 매우 좋지 않았다.. 그래서 `CrewAI` 말고 직접 `LCEL`로 구현하는 방법도 사용해보려 하였지만, `Agent`가 수행하는 일을 시키는 것이 불가능했다. 일반 `Agent`의 `Model`을 `GPT-4o`로 바꾸니 무한 루프 문제는 해결되었으나, 제대로 된 결과 값이 나오지 않는다... 이를 해결하기 위해 하나의 Crew을 만들어 사용하려고 한다. Dir load 같은 경우는 gpt-4o-mini로도 잘 작동하기 때문에 이걸 사용하고 file road 부분만`GPT-3.5-turbo-1106`을 사용하여 불러올려고 한다....  [git commit](https://github.com/Donghyeon-Shin/DocumentSecretary/commit/728b6678203696c0e7afb8b8121438e2bf4b397f)
- [25.01.10.] - 불러온 파일들을 바탕으로 question에 답을 해주는 chain을 만들었다. 여러 파일들을 사용하여 답을 구해야 하기 때문에 `Refine LCEL Chain`을 2번 사용하였다. 처음 Chain의 경우는 mainFile에서 question에 답을 구하기 할 때 사용하였고. 두 번째 Chain의 경우는 relatedFiles을 사용하여 답의 내용을 보충하기 위해 사용하였다. 시간이 좀 걸리긴 하지만, 잘 작동하였고 이미지의 경우 Error 계속 발생하여, 나중에 시도해야 할 것 같다....[git commit](https://github.com/Donghyeon-Shin/DocumentSecretary/commit/84e262b1e1b06e49bab10aa9fa41646a8437293f) 여기서 5가지 개선할 필요가 있다. 
	1. 너무 오랜 시간...  파일 Load부터 결과 값 도출까지 약 20분의 시간이 걸린다. 여기서 대부분의 소모 시간은 마지막 mainFile에 내용을 보충하는 refine chain에서 17분이나 소요된다. -> 따로 옵션을 만들어서 추가 설명을 듣기를 윈할 때, 작성해주는 것이 좋을듯
	2. 많은 비용 소모... question을 할 때 마다, fileSelector을 작동시켜야 하는데, 이때 gpt-4o를 사용해 너무 많은 비용이 발생한다. (대략 한번 할 때 마다 0.05달러 정도 발생함) fileSelector을 작동시키지 말지를 정하는 llm을 사용하는 게 좋을 지... 근데 잘 작동할지는 모르겠음... 이 문제에 대해서는 해결 방법이 막 떠오르지 않음.. `CrewAI`의 버그만 해결되도 이 문제가 줄어들긴 함
	3. Img file RAG을 헤서 이를 적용해야 한다...? 정도
	4. 지금은 질문에 해결하기 위한 정보를 file name으로 판단하고 있음... 만약에 file_name이 이상하면 근본적으로 작동이 되지 않음... 이를 해결 하려면 각각의 문서를 읽고 파일 이름을 정해주는 Chain을 만들어야 할 것 같긴 함 -> 근데 이거 비용적으로도 시간적으로도 비효율적임.. 그냥 사용자에게 file name을 잘 명시하라고 해야 할 듯...
	5. 만약 obsidain file이 아니라 더 광범위 하게 (ex. notion 같은 웹 사이트) 적용 가능한 비서를 만들려면 agent에서 webScring을 통해 file path가 아닌 site를 정리하고 이를 가져오도록 만들어야 할 듯... 이건 우선 obsidian file을 다 적용한 뒤 진행해야 할 듯...
- [25.01.11.] - Image를 Encoding해서 분석하는 Refine Chain을 만들었다. [git commit](https://github.com/Donghyeon-Shin/DocumentSecretary/commit/a091ecdab864cf054aabe21028190ef2163cf1a2) 하지만 Refine 특성상 너무 오래 걸리며 결과 값도 좋지 않았다.. 따라서 이미지 분석은 CrewAI를 통해서 하는 것이 좋을 것 같다.[git commit](https://github.com/Donghyeon-Shin/DocumentSecretary/commit/ad9f62d3ba4ab5a3132ced019856130e37636029)
- [25.01.12.] - Streamlit에서 UI를 구현하는 과정에서 문서와 이미지를 지정하는 과정에서 





# 구현해야 할 것
1. file 안에 있는 IMG를 text로 변환 후 저장한다. -> 완료
2. `fileSelector`을 이용해 만들어진 path을 사용해 question에 맞는 `researcher` 만들기 
3. Streamlit으로 CrewAI 연결하기 (CrewAI Streaming을 공부해야 할 듯/있나..?)
4. AWS를 사용하여 E2C Streaming 연결 (최종 목표)
5. 지금은 내 Obsidian file을 기준으로 Agent을 만들었지만 Notion, 아이패드 노트 등등 여러가지 것들이 가능하게 업그레이드!!!



문제 첫 번째, mainFilesearcher가 여러 번 실행되면서, 첫 번째 값은 무조건 잘 실행되는데 두 세번째에 결과가 희석되면서 file 정리가 잘 안되는 문제가 발생
문제 두 번째, Image file tool이 parameter를 두 번 보내는 경우가 발생할 때가 있음, 이를 agent을 수정해 고쳐야 함.



있으면 좋을 것 같은 기능들
- 연관 파일들 리스트를 보여주며 연관 파일을 선택하여 질문할 수 있게 해주는 기능 (이미지도)
- 현재 질문을 내 문서 내에서 찾지 말고 GPT-4o-mini에게 제공해주는 기능
