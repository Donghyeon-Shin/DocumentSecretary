# Concept
- **Caching**을 통해 Human의 질문과 AI의 답변을 저장하여 같은 질문이 나왔을 때, 저장한 데이터를 보여줌으로써 시간과 비용을 효과적으로 줄일 수 있다.
- Caching을 사용하기 위해선 `from langchain.globals import set_llm_cache`을 사용하여야 한다.
- set_llm_cache function Parameter에 어디에 저장할 지를 지정해주어야 한다.
```python
from langchain.globals import set_llm_cache
set_llm_cache() #저장소
```
- Caching은 다양한 저장소에서 저장할 수 있지만 대표적으로 `InMemoryCache`와 `SQLiteCache`가 있다.
# InMemoryCache
- 말 그대로 **Memory**에 저장하는 방법이다.
- `from langchain.cache import InMemoryCache`로 불러올 수 있다.
- Memory에 저장하게 될 시, 재시작 할 때 저장 데이터가 날라간다는 단점이 있다.
```python
set_llm_cache(InMemoryCache())
```
# SQLiteCache
- `.db`파일인 데이터 베이스에 저장하는 방법이다.
- `from langchain.cache import SQLiteCache`로 불러올 수 있다.
- SQLiteCache function Parameter에 경로와 저장 파일 이름을 지정해주어야 한다.
```python
set_llm_cache(SQLiteCache("cache.db"))
```