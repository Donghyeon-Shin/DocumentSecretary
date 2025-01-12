# Concept
- 크롤링(`웹 페이지에서 데이터를 추출하는 작업`) 위해 사용하는 `Package`를 말한다.
- `Python`에서 크롤링을 하는 방법은 여러가지가 있지만 여기선 `Playwright`와 `sitemapLoader`을 소개한다.
# Site Loader Types
### Playwright  & Async Chromium 
- **json이 많은 웹 사이트**는 동적이기 때문에 바로 불러올 수 없다. 그래서 `Playwright`와 `Async Chromium`을 사용한다.
- 하지만 이는 직접 내 컴퓨터로 브라우저를 열고 데이터를 얻는 것이기 때문에 많은 양의 url을 넣어 실행하면 작업 시간이 오래 걸릴 수 있다.
#### Playwright
- `Playwright`는 브라우저 컨트롤을 할 수 있는 Package로 [Selenium](https://www.selenium.dev/)하고 비슷하다.
- Microsoft에서 개발하였고 브라우저 테스트 및 웹 스크래핑을 위한 **오픈 소스 자동화 라이브러리**이다.
- `from langchain.document_loaders import AsyncChromiumLoader`로 불러올 수 있다.
#### Async Chromium 
- `Chromium`은 브라우저 자동화를 제어하는 데 사용되는 라이브러리인 `Playwright`에서 지원하는 브라우저 중 하나이다.
#### NotImplementedError
- window에서 Async Chromium 사용 시, `NotImplementedError`가 나오는 데 이를 `asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())` 사용하여 해결 할 수 있다.

```python
import sys

if "win32" in sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    cmds = [['C:/Windows/system32/HOSTNAME.EXE']]
else:
    cmds = [
    ['du', '-sh', '/Users/fredrik/Desktop'],
    ['du', '-sh', '/Users/fredrik'],
    ['du', '-sh', '/Users/fredrik/Pictures']
]
```
#### Use Playwright  & Async Chromium 
- `AsyncChromiumLoader([{url}])`를 통해 loader를 만들 수 있다. URL를 `list`형태로 전달해야 함에 주의해야 한다.
- 또한 `AsyncChromiumLoader`의 `.load()` function을 통해 load 한 값을 문서화 시킬 수 있다.
- load한 데이터를 `text`로 변환하기 위해서는 `Html2TextTransformer`를 사용해야 하는데 이는 `from langchain.document_transformers import Html2TextTransformer`로 불러 올 수 있다.
- `Html2TextTransformer`에서 `transform_documents({docs})` function을 사용해 `load`한 문서를 `text`로 변환한다.

```python
import asyncio
import sys
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import Html2TextTransformer
import streamlit as st

html2text_transformer = Html2TextTransformer()

if "win32" in sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    cmds = [['C:/Windows/system32/HOSTNAME.EXE']]
else:
    cmds = [
    ['du', '-sh', '/Users/fredrik/Desktop'],
    ['du', '-sh', '/Users/fredrik'],
    ['du', '-sh', '/Users/fredrik/Pictures']
]

with st.sidebar:
    url = st.text_input(
        "Write down a URL",
        placeholder="https://example.com",
    )

if url:
    loader = AsyncChromiumLoader([url])
    docs = loader.load()
    trsanformde = html2text_transformer.transform_documents(docs)
    st.write(docs)
```
###  SitemapLoader
- 웹 사이트가 동적인 것이 아닌 **단순 text가 많은 정적인 사이트**라면 `SitemapLoader`을 이용할 수 있음
- `.xml` 형식의 사이트를 `크롤링`할 수 있다. (**html 사이트는 안된다.**)
#### Check if it is xml site
-  `SitemapLoader`에서 지원이 되는 사이트인지 체크해보려면 아래와 같이 request 했을 때 xml 형식을 주는지 html 형식을 주는지 보면 된다. `xml 형식`을 print하면 지원이 되는 것이다.
```python  
import requests  
response = requests.get("https://openai.com/sitemap.xml")  
print(response.text)  
```
#### Use SitemapLoader
##### URL Loader
- SitemapLoader는 `from langchain.document_loaders import SitemapLoader`로 불러 올 수 있다.
- `SitemapLoader({url})`로 loader 만들 수 있고 `.load()` function을 통해 해당 URL를 크롤링 할 수 있다.
- `Sitemap`이 되는 site의 URL은 웹 사이트가 Google 등 다른 크롤러의 스크랩을 허용해놓은 거지만 너무 빠르면 정책의 위배될 수 있다.
- `.requests_per_second = {num}`를 통해 해당 사이트의 데이터를 얼머나 빠르게 가져올 지를 정할 수 있으나 너무 빠르게 설정하면 해당 site에서 block 할 수 있다.
 
```python
from langchain.document_loaders import SitemapLoader
import streamlit as st

@st.cache_data(show_spinner="Loading website....")
def load_website(url):
    loader = SitemapLoader(url)
    loader.requests_per_second = 5
    docs = loader.load()
    return docs
```
##### Filter URLS
- `Sitemap`에서 스크립트 대상을 URL의 하위 페이지만 포함하거나 제외하기 위해선, `SitemapLoader`에 filter_urls parameter를 넘겨주면 된다.
	- `r"^(.*\/research\/).*"` : url의 하위 페이지(research)만 포함하여 스크립트 하기
	- `r"^(?!.*\/research\/).*"` : url의 하위 페이지(research)를 제외하고 스크립트 하기

```python
loader = SitemapLoader(
	url,
	filter_urls=[
		r"^(?!.*\/research\/).*"
	],
)
```
##### Beautiful soup
- 스크립트 받은 `html` 값에는 `header`나 `footer`, `'\n` 같은 필요 없는 정보들도 들어가 있다. 따라서 이러한 값들을 수정하기 위해선 `beautiful soup` 사용한다. 
- `SitemapLoader`에 `parsing_function`을 지정할 수 있는데 이를 지정하면 자동으로 `soup`를 Parameter로 넘겨준다.
- [beautiful soup](https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser))이란 인터넷 문서의 구조에서 명확한 데이터를 추출하고 처리하는 가장 쉬운 라이브러리이다.
- `soup.find("header")`를 통해 해당 html tag가 달린 내용을 찾을 수 있고
- `header.decompose()`로 해당 내용을 제거할 수 있다.
- 나머지 context 중에 수정할 내용은 `.get_text()`로 string 형태로 값을 가져온 다음 `replace()`을 통해 수정하면 된다.
```python
def parse_page(soup):
    header = soup.find("header")
    footer = soup.find("footer")
    if header:
        header.decompose()
    if footer:
        footer.decompose()
    return str(soup.get_text()).replace("\n", " ").replace("\xa0", " ")
```
##### RecursiveCharacterTextSplitter 
- 전처리를 통해 필요한 데이터만을 얻었다면, 이를 LLM에 넘겨주기 위해 `splitter`로 splite을 해주어야 한다.**(model의 `Context Window`를 만족시키거나 [[Map Reduce LCEL Chain]]나 [[Map Re-rank LCEL Chain]]을 수행하기 위해)**
- `RecursiveCharacterTextSplitter`는 일반 텍스트에 권장되는 분할 기법이다. 
- 이 spliter는 문자 목록에 `매개변수화`(기본 목록 : ["\n\n", "\n", " ", ""])되어 있는데, 이 목록에 순서대로 분할을 시도하여 청크가 충분히 작아질 때까지 계속 splite 한다.
- 이 spliter는 의미론적으로 관련된 텍스트의 가장 강력한 조각으로 보이는 문단 (그리고 그 다음 문장, 그리고 단어)을 최대한 유지하려고 시도한다.
```python
@st.cache_data(show_spinner="Loading website....")
def load_website(url):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=200,
    )
    loader = SitemapLoader(
        url, filter_urls=[r"^(.*\/research\/).*"], parsing_function=parse_page
    )
    loader.requests_per_second = 5
    docs = loader.load_and_split(text_splitter=splitter)
    return docs
```
