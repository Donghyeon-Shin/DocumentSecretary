# Concept
- `Assistant`는 대화형 인공지능 어시스턴트를 구축하고 관리하는 데 사용되는 프로그래밍 인터페이스이다. 
- `Assistant`는 `openAI` 플랫폼 안에서 제공되는 `API`로 [[LCEL(LangChain Expression Language)]]으로 민들어진 `GPT`보다 더 범용적으로 사용할 수 있다.
- `Assistant`는 `Tool`이라는 도구가 있으며, `Assistant`는 `LLM`에게 해당 `Tool`을 사용하여 `User`에게 답변을 주도록 돕는 기능을 수행한다.
- `Assistant`는 기본적으로 무료이나, `Code Interpreter`나 `Retrieval`을 사용하려면 사용 `Model`에 따라 돈을 지불해야 한다.
- 아직 **Beta** Version이며 [assistant overview](https://platform.openai.com/docs/assistants/overview)에 자세한 내용이 나와있다.
# Components
- `Assistant`는 크게 4개의 `Components`로 구분되어 있다.
- `Assistant`, `Thread`, `Message`, `Run` 모두 고유의 번호(**id**)가 존재한다. 
- `Id`을 통해 긱 요소가 어떠한 다른 요소와 연결되어 있는지를 설정할 수 있다.
### Assistant
- `Assistant`의 옵션을 설정할 수 있다. ([OpenAI API](https://platform.openai.com/playground/assistants)에서도 만들 수 있고, `python`, `node.js`로도 만들 수 있다.)
- `Assistant`의 Attributes는 다음과 같다.
	- Name : `Assistant`의 이름이다.
	- Instructions : 어떠한 `Assistant`인지 설명하는 내용이다.
	- Model : `Assistant`에 사용할 Model(`GPT3, GPT4`)
	- Tool(retriever, code interpreter, function) : `LLM`에게 전달할 기능들을 선언/설정한다.
	- Response format : [[Output Parser]] 같은 기능으로 Reponse가 어떠한 형식으로 나올지를 결정한다.
	- Temperature : `Model`의 창의성을 설정한다.
	- Top p : 단어들의 확률을 누적하여 **특정 임계값 P**에 도달할 때까지의 단어들만을 고려합니다.
### Thread
- `User`와 `Assistant`가 주고받는 `Messages`의 모음이다.(사용자 각자의 Thread을 가지게 된다.)
- `Thraed`가 `Messages`을 다 가지고 있어 `Memory` 기능을 수행한다.(오래된 메시지는 지우거나 압축시켜서 용량이 너무 커지지 않게 관리한다.)
- [Threads Info](https://platform.openai.com/threads) - `Thread` 내용을 볼 수 있다. (Settings - Data Controls - Threads을 볼 수 있게 설정 해야 보인다.)
### Message
- `User` / `Assistant`의 대화 내용들이다. **(input/output)**
- `Message`의 Attributes는 다음과 같다.
	- `Thread Id` : 어떠한 `Thread`의 포함 시킬 것 인지를 설정한다.
	- `role`: 누구의 메시지인지를 설정한다. (`"user"/"assistant"`)
	- `content`: `Message`의 내용이다.
### Run
- `Thread`안의` Message`을 `model`을 통해 실행(run)하는 것을 의미한다.
- `Model`이 해당 `Message`를 보고 즉시 대답을 해줄지 아니면 적절한 `Tool`을 사용할지 결정하여 대답을 해준다.
- `Status`을 통해 `Run`의 진행 상황을 알 수 있다.
	- `in_progress` : `Run`이 진행되고 있는 상황이다.
	- `requires action` : `Tool`을 사용할 필요가 있어 대기하고 있는 상황이다.(이때 `Tool`이 `functions`이라면  `Assistant`에게 `Tool`을 사용한 결과를 보내주어야 한다.) 
	- `completed` : `Run`이 완료된 상황이다.
- `Run`의 Attributes는 다음과 같다. 
	- `Thread Id` : 어떠한 `Thread`을 사용할 것인지를 설정한다.
	- `Assistant Id` : 어떠한 `Assistant`을 사용할 것인지를 설정한다.
# Process
![[Assistant Process.webp]]
- `User`의 질문(`User's Message`)을 `Message`로 만들면 해당 `Message`가 `Thread`에 보관된다. 
- `Run`을 통해 `Model`을 작동시키면 `Thread`에 있는 `Message`가 `Model`에게 보내져 `User`의 질문의 답변(`Assistant Message`)을 만들어진다. 
- `Assistant Message` 또한 `Thread`에 저장되며 답변이 만들어지는 과정에서 `Tool`이 필요하다면 `Run`은 `requires action`가 되며 해당 **`Tool`이 `functions`이라면 어떠한 `function`이 필요하고 해당 `funtion`의 `Parameter`가 무엇인지를 `Model`을 통해 만들어 이를 반환한다.**(`Tool`이 `functions`이 아니라면 자동으로 해당 `Tool`이 실행된다.)
- `run`의 `submit_tool_outputs`을 통해 `Assistant`에게 `function Output`값을 전달하면 해당 값이 `Model`에게 넘어가 `Assistant Message`을 만들게 된다.(단 `Model`이 `functions`을 여러 번 호출하는 경우도 있기 때문에 `Run`의 `Stauts`을 통해 판단하여야 한다.)
- `Run`의 `Stauts`가 `completed`가 되면 `Assistant Message`가 `Thread`에 저장된다.
# Functions Tool Assistant
- `LLM`이 `Assistant Message`을 구하는 과정에서 특정 `function`이 필요한 경우 해당 `function`이 원하는 `Parameters`을 만들어 `function`에 전달하며, `function`을 실행시켜 얻은 결과를 바탕으로 `User`의 답변을 만들도록 하는 기능이다. ([[Agent]]랑 비슷한 기능이 비슷하다.)
- `Assistant`을 만드는 과정에서 `function`의 기능과 필요 `Parameters`의 정보를 전달하는 `functions`을 선언하여야 한다.
- `functions`는 `List` 형태이며 그 안에는 `"description"(해당 함수/변수에 대한 설명), "type"(해당 값의 type), "required"(해당 함수을 실행하기에 Model에게 요구되는 값)`등이 포함되어 있는 `json schema `형태의 `function` 값들이 들어있다. (자세한 내용 참고 : [OpenAI - Define Functions](https://platform.openai.com/docs/assistants/tools/function-calling))
- `Assistant`는 `Functions Tool`을 자동으로 실행하지 않는다. 대신, `function`을 실행시키기 위한 정보를 주기 때문에 이를 이용해 `function`을 실행하여 그 `output`을 `run`의 `submit_tool_outputs`에 전달하여야 한다.
- `submit_tool_outputs`은 `Run Id`와 `Thread Id`, `Tool Outputs`이 필요하다.
- `function`의 `output`은 항상 `String` 값이어야 하기 때문에 만약, `yfinance` 같은 라이브러리를 사용하여 얻은 값이 `json`이라면 `json.dumps` 같은 함수를 사용하여 `json`값을 `String`으로 바꾸어 반환해야 한다.
- 코드의 전체적인 내용은 [[Investor GPT]]와 비슷하기 때문에 `Assistant`을 제외한 Code의 내용은 해당 `Part`를 참고해라.
```python
from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
import yfinance
import json
import openai as client

def get_run(run_id, thread_id):
    return client.beta.threads.runs.retrieve(
        run_id=run_id,
        thread_id=thread_id
    )

def get_messages(thread_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    messages = list(messages)
    messages.reverse()
    for message in messages:
        print(f"{message.role}:{message.content[0].text.value}")

def get_tool_output(run_id, thread_id):
    run = get_run(run_id, thread_id)
    outputs = []
    for action in run.required_action.submit_tool_outputs.tool_calls:
        action_id = action.id
        function = action.function
        # print(f"Calling function {function.name} with arg {function.arguments}")
        outputs.append(
            {
                "output": functions_map[function.name](json.loads(function.arguments)),
                "tool_call_id": action_id,
            }
        )
    return outputs

def submit_tool_output(run_id, thread_id):
    outputs = get_tool_output(run_id, thread_id)
    return client.beta.threads.runs.submit_tool_outputs(
        run_id=run_id,
        thread_id=thread_id,
        tool_outputs=outputs
    )

def send_message(thread_id, content):
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content,
    )
  
def get_ticker(inputs):
    ddg = DuckDuckGoSearchAPIWrapper()
    company_name = inputs["company_name"]
    return ddg.run(f"Ticker symbol of {company_name}")

def get_income_statement(inputs):
    ticker = inputs["ticker"]
    stock = yfinance.Ticker(ticker)
    return json.dumps(stock.income_stmt.to_json())

def get_balance_sheet(inputs):
    ticker = inputs["ticker"]
    stock = yfinance.Ticker(ticker)
    return json.dumps(stock.balance_sheet.to_json())

def get_daily_stock_performance(inputs):
    ticker = inputs["ticker"]
    stock = yfinance.Ticker(ticker)
    return json.dumps(stock.history(period="3mo").to_json())

functions_map = {
    "get_ticker": get_ticker,
    "get_income_statement": get_income_statement,
    "get_balance_sheet": get_balance_sheet,
    "get_daily_stock_performance": get_daily_stock_performance,
}

functions = [
    {
        "type": "function",
        "function": {
            "name": "get_ticker",
            "description": "Given the name of a company returns its ticker symbol",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "The name of the company",
                    }
                },
                "required": ["company_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_income_statement",
            "description": "Given a ticker symbol (i.e AAPL) returns the company's income statement.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Ticker symbol of the company",
                    },
                },
                "required": ["ticker"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_balance_sheet",
            "description": "Given a ticker symbol (i.e AAPL) returns the company's balance sheet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Ticker symbol of the company",
                    },
                },
                "required": ["ticker"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_daily_stock_performance",
            "description": "Given a ticker symbol (i.e AAPL) returns the performance of the stock for the last 100 days.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Ticker symbol of the company",
                    },
                },
                "required": ["ticker"],
            },
        },
    },
]

assistant = client.beta.assistants.create(
    name="Investor Assistant",
    instructions="You help user do research on publicly traded companies and you help them decide if they should buy the stock or not.",
    model="gpt-3.5-turbo-0125",
    tools = functions
)

assistant_id = assistant.id

thread = client.beta.threads.create()

thread_id = thread.id

message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role= "user",
    content="I want to know if Health Catalyst stock is a good buy."
)

run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
)

run_id = run.id

print(get_run(run_id, thread_id).status)
print(submit_tool_output(run_id, thread_id))
print(get_messages(thread_id))
```
# File Search Assistant
- `File`을 받아 [[RAG(Retrieval-Augmented Generation)]]을 거쳐 나온 정보를 토대로 `User's Message`의 `Assistant's Message`을 구할 수 있도록 도와주는 `Tool`이다.
- `Assistant`을 만들 때 `tools`에 `file_search`을 지정해야 한다.
- `files.create`을 통해 `File`을 만들 수 있으며 고유의 `File Id`가 생성된다.
- `Message`의 `attachments`의 `File Id`와 `tool("file_search")` 넣으면 `Assistant`가 `File`을 받아 [[RAG(Retrieval-Augmented Generation)]]을 거쳐 저장한다.
```python
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content="I want you to help me with this file",
    attachments=[
        {
            "file_id": file.id,
            "tools": [
                {
                    "type": "file_search",
                }
            ],
        }
    ],
)
```
- `File`만 `Assistant`에 넣는다면 `Message`에 `User's Message`을 입력하면 자동으로 `File`의 내용을 참고하여 `Assistant's Message`을 반환한다.
- `Assistant's Message`에는 `annotations` 값이 포함되어 있는데 `annotations`에는 해당 `Assistant's Message`이 `File`의 어느 부분을 참고하였는지 저장되어 있다.
```python
import json
import openai as client

def get_run(run_id, thread_id):
    return client.beta.threads.runs.retrieve(
        run_id=run_id,
        thread_id=thread_id
    )

def get_messages(thread_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    messages = list(messages)
    messages.reverse()
    for message in messages:
        print(message)
        # print(f"{message.role}:{message.content[0].text.value}")
        for annotation in message.content[0].text.annotations:
            print(f"Source : {annotation.file_citation}")

def send_message(thread_id, content):
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content,
    )
  
assistant = client.beta.assistants.create(
    name="Book Assistant",
    instructions="You help user do research with their question on the files they upload.",
    model="gpt-3.5-turbo-0125",
    tools=[{"type": "file_search"}],
)

assistant_id = assistant.id

file = client.files.create(
    file = open("./files/chapter_one.txt", "rb"),
    purpose = "assistants"
)

thread = client.beta.threads.create()

thread_id = thread.id

message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content="I want you to help me with this file",
    attachments=[
        {
            "file_id": file.id,
            "tools": [
                {
                    "type": "file_search",
                }
            ],
        }
    ],
)

run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
)

run_id = run.id

send_message(thread_id, "Where dose he work?")
print(get_run(run_id, thread_id).status)
print(get_messages(thread_id))
```
# Assistant Streaming
- Assistant 2.0 이후로부터는 `Streaming`이 제공된다.
- `Run`을 실행하는 과정에서 `event_handler`을 지정하면 `Stream` 기능을 사용할 수 있다.
- `Streaming`을 사용하면 `Assistant`가 `function Tool` 사용을 원할 때, 이를 바로바로 넘겨줄 수 있다.
- `event_handler`는 Class로 `AssistantStreamEvent`을 **Parent class**로 두어야 하며 `from openai.types.beta import AssistantStreamEvent`로 불러올 수 있다.
- `AssistantStreamEvent`에는 `on_run_step_created`,  `on_text_delt`, `on_tool_call_done` 등 다양한 `function`이 제공된다. (`create` : 만들어질 때, `delt` : 실행중일 때, `done`: 끝났을 때)
- **`Run`을 실행할 때마다 `event_handler`을 지정해주어야** 하기 때문에 `submit_tool_outputs_stream`에서 `function output`을 넘겨주는 과정에서도 `event_handler`을 지정해주어야 한다.
```python
from typing_extensions import override
from openai import AssistantEventHandler
from openai.types.beta.threads import Message, MessageDelta
from openai.types.beta.threads.runs import ToolCall, RunStep
from openai.types.beta import AssistantStreamEvent

class EventHandler(AssistantEventHandler):
    def __init__(self, thread_id, assistant_id):
        super().__init__()
        self.output = None
        self.tool_id = None
        self.thread_id = thread_id
        self.assistant_id = assistant_id
        self.run_id = None
        self.run_step = None
        self.function_name = ""
        self.arguments = ""
        
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant on_text_created > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        # text가 만들어질때마다 작성하도록
        # print(f"\nassistant on_text_delta > {delta.value}", end="", flush=True)
        print(f"{delta.value}")

    @override
    def on_end(self):
        # 각 stream이 끝날 때때
        print(f"\n end assistant > ", self.current_run_step_snapshot, end="", flush=True)

    @override
    def on_exception(self, exception: Exception) -> None:
        """Fired whenever an exception happens during streaming"""
        print(f"\nassistant > {exception}\n", end="", flush=True)
        
    @override
    def on_message_created(self, message: Message) -> None:
        print(f"\nassistant on_message_created > {message}\n", end="", flush=True)

    @override
    def on_message_done(self, message: Message) -> None:
        print(f"\nassistant on_message_done > {message}\n", end="", flush=True)

    @override
    def on_message_delta(self, delta: MessageDelta, snapshot: Message) -> None:
        # print(f"\nassistant on_message_delta > {delta}\n", end="", flush=True)
        pass

    def on_tool_call_created(self, tool_call):
        # 4
        print(f"\nassistant on_tool_call_created > {tool_call}")
        self.function_name = tool_call.function.name
        self.tool_id = tool_call.id
        print(f"\on_tool_call_created > run_step.status > {self.run_step.status}")
        print(f"\nassistant > {tool_call.type} {self.function_name}\n", flush=True)
        
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=self.thread_id, run_id=self.run_id
        )

        while keep_retrieving_run.status in ["queued", "in_progress"]:
            keep_retrieving_run = client.beta.threads.runs.retrieve(
                thread_id=self.thread_id, run_id=self.run_id
            )

            print(f"\nSTATUS: {keep_retrieving_run.status}")

    @override
    def on_tool_call_done(self, tool_call: ToolCall) -> None:
        # tool_call이 끝났을 때
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=self.thread_id, run_id=self.run_id
        )
        # 현재 retrieving_run 정보
        print(f"\nDONE STATUS: {keep_retrieving_run.status}")

        if keep_retrieving_run.status == "completed":
            all_messages = client.beta.threads.messages.list(thread_id=thread_id.id)

            print(all_messages.data[0].content[0].text.value, "", "")
            return
        elif keep_retrieving_run.status == "requires_action":
            # keep_retrieving_run.status가 actoin을 요구하면
            print("here you would call your function")

            if self.function_name in functoins_map:
                # 해당 요구하는 action이 내가 정한 함수 안에 있을 때
                print(self.arguments)

                with client.beta.threads.runs.submit_tool_outputs_stream(
                    thread_id=self.thread_id,
                    run_id=self.run_id,
                    tool_outputs=[
                        {
                            "tool_call_id": self.tool_id,
                            "output": functoins_map[self.function_name](
                                json.loads(self.arguments)
                            ),
                        }
                    ],
                    event_handler=EventHandler(self.thread_id, self.assistant_id),
                ) as stream:
                    stream.until_done()
                # 해당 action에 대한 stream을 만듦
            else:
                print("unknown function")
                return

    @override
    def on_run_step_created(self, run_step: RunStep) -> None:
        # 2
        print(f"on_run_step_created")
        self.run_id = run_step.run_id
        self.run_step = run_step
        print("The type ofrun_step run step is ", type(run_step), flush=True)
        print(f"\n run step created assistant > {run_step}\n", flush=True)

    @override
    def on_run_step_done(self, run_step: RunStep) -> None:
        print(f"\n run step done assistant > {run_step}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == "function":
            print("Get function argument")
            # the arguments stream thorugh here and then you get the requires action event
            print(delta.function.arguments, end="", flush=True)
            self.arguments += delta.function.arguments
        elif delta.type == "code_interpreter":
            print(f"on_tool_call_delta > code_interpreter")
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)
        else:
            print("ELSE")
            print(delta, end="", flush=True)

    @override
    def on_event(self, event: AssistantStreamEvent) -> None:
        # print("In on_event of event is ", event.event, flush=True)
        if event.event == "thread.run.requires_action":
            print("\nthread.run.requires_action > submit tool call")
            print(f"ARGS: {self.arguments}")

with client.beta.threads.runs.stream(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions="You help user do research on publicly traded companies and you help them decide if they should buy the stock or not.",
    event_handler=EventHandler(thread_id, assistant_id),
) as stream:
    stream.until_done()
```