# Concept
- 검색(Retrieval)과 생성(Augmented Generation)을 결합하여 자연어 처리(NLP) 및 기계 학습 분야, 특히 챗봇이나 질문-응답 시스템과 같은 고급 언어 모델을 구축하는 데 사용되는 기술이다.
- RAG System은 질문이나 Prompt가 주어지면 Model이 관련된 정보를 탐색하고 정보들을 바탕으로 **일관적인** 답변을 생성하도록 작동하는 System을 말한다.
- RAG Process ![[RAG Process.svg]]
- 관련 논문 : [RAP Paper](https://arxiv.org/abs/2005.11401)
# Retrieval
- 대규모 데이터베이스나 문서 컬렉션을 검색하는 과정을 말한다.
- 자세한 내용은 [[Retrieval]]을 참고하면 된다.
# Augmented Generation
- 검색된 정보를 바탕으로 일관되고 맥락적으로 적절한 텍스트를 생성하는 과정을 말한다.
- RAG를 활용하여 Chain을 만드는 방법은 총 3개가 있다. (이는 `LangChain v0.1`에서 제공했던 내용들이며, 현재 v0.2, v0.3에서는 따로 나와있는 공식 문서가 없다.)
	- [[Stuff LCEL Chain]] : 모든 문서를 단일 Prompt에 넣어 답을 구하는 모델
	- [[Refine LCEL Chain]] : 모든 문서를 순회하면서 반복적으로 답변을 업데이트하는 모델
	- [[Map Reduce LCEL Chain]] : 각 문서들을 질문에 대해 요약한 다음 최종 답을 구하는 모델
	- [[Map Re-rank LCEL Chain]] : 각 문서들을 질문에 대해 답을 구한 다음 그 답변의 점수를 매긴다. 그 후 매긴 점수들에서 가장 높은 점수를 가지고 있는 답을 출력하는 모델
- LangChain에서는 `RetrievalQA`라는 Chain을 지원한다. 하지만, [[LCEL(LangChain Expression Language)]] 보다 설정이 자유롭지 못하며 과정 자체가 생략이 많이 되어 이해하기 어렵기 때문에 이를 사용하는 것을 권장하지 않는다.
- 이미 알려진 방법에 국한되지 않고 상황에 맞게 직접 Chian을 만들어 사용하는 것이 가장 좋은 방법이다.