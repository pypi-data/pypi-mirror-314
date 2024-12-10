import uuid
from typing import List
from datetime import datetime

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage

from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState

from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.chat_models import ChatPerplexity
from langchain_core.language_models.chat_models import ChatGenerationChunk
from langchain_core.messages import AIMessageChunk
from langchain_core.runnables.config import (
    ensure_config,
    get_async_callback_manager_for_config,
)
from langchain_core.callbacks.manager import adispatch_custom_event

from botrun_flow_lang.langgraph_agents.agents.util.gemini_grounding import (
    respond_with_gemini_grounding,
)
from botrun_flow_lang.langgraph_agents.agents.util.perplexity_search import (
    respond_with_perplexity_search,
)


REQUIREMENT_NODE = "requirement_node"
ADD_REQUIREMENT_TOOL_MESSAGE_NODE = "add_requirement_tool_message"
SEARCH_NODE = "search_node"
RELATED_NODE = "related_node"

default_system_prompt = "妳是臺灣人，回答要用臺灣繁體中文正式用語，需要的時候也可以用英文，可以親切、但不能隨便輕浮。在使用者合理的要求下請盡量配合他的需求，不要隨便拒絕"

requirement_prompt = """
妳是臺灣人，回答要用臺灣繁體中文正式用語，需要的時候也可以用英文，可以親切，但不能隨便輕浮。在使用者合理的要求下請盡量配合他的需求，不要隨便拒絕
你是一個專業的助手，使用者會提出他的，你的任務就是判斷使用者是否有提出他的需求，所以你會需要獲得的資訊如下：

- 確認使用者是否有提出他的需求(有/沒有)

有需求的範例：
- 留學獎學金可以申請多少？
- 我上個月十月剛從馬偕醫院離職，我可以領勞保生育補助嗎
- 請問我有個兩歲的孩子，可以領育兒補助到幾歲？

請遵守以下規則：
- 瞭解使用者「有」需求之後，你不會跟他說類似「讓我先確認您是否有提出具體的需求。」、「需要更多細節」、「讓我先確認這個需求。」、「讓我先確認一下您是否已經提出具體的需求」、「我需要先了解一下您的情況。」的句子，你只會說「已經收到他的oo需求，讓我來處理」，但是你不會真的回覆。
- 你不會直接回覆使用者的需求，你只會說已經收到，會開始幫他研究。
- 你不會說任何有關「讓我先確認您是否有提出具體的需求。」、「讓我先確認您是否已經提出明確的需求」, 「讓我確認一下您目前是否有任何具體的需求。」的類似句子，如果你判斷他沒有提出需求，就直接先跟他聊天。
- 你不會跟使用者要更多的資訊

"""

default_search_prompt = """
001 你只會使用臺灣人習慣的語詞和繁體中文，採用正式但親和的語氣，以維護專業性並表達尊重。
002 妳會保持溫暖且親切的語氣，溫暖人心的護理師大姊姊，讓使用者在溝通時感受到支援和關愛。
003 妳會運用同理心來理解使用者的處境，特別是在討論敏感話題（如經濟困難）時，以謹慎和關懷的態度進行應，讓使用者感受到被傾聽和理解。 
004 請你使用清晰的格式呈現資訊，如項目符號或編號列表，以提高可讀性。 
005 請你在結尾附上參考來源，包含參考來源的名稱，以及參考來源的hyperlinks，以利使用者查詢。
"""

search_prompt = """
現在的西元時間：{western_date}
現在的民國時間：{taiwan_date}

{prompt}
"""

default_related_prompt = """
你是一個專業的助手，請根據使用者的原始問題以及之前的回答內容，提供 3-5 個相關的後續問題建議。
這些問題應該：
1. 與原始問題和回答內容相關
2. 能夠幫助使用者更深入了解相關的補助或福利
3. 涵蓋不同面向，但都要與福利補助有關
4. 使用繁體中文提問
5. 每個問題都要簡潔明瞭，不超過 30 個字

"""

related_question_text = """

使用者的原始問題是：
{original_question}

之前的回答內容是：
{previous_response}

請提供相關的後續問題建議。
"""


def get_requirement_messages(messages):
    # 過濾掉最後的 assistant 消息
    filtered_messages = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            filtered_messages.append(msg)
        elif isinstance(msg, AIMessage) and not msg.tool_calls:
            # 只保留不含 tool_calls 的 AI 消息
            filtered_messages.append(msg)

    # 確保最後一條消息是 HumanMessage
    if filtered_messages and not isinstance(filtered_messages[-1], HumanMessage):
        filtered_messages.pop()

    return [SystemMessage(content=requirement_prompt)] + filtered_messages


def format_dates(dt):
    """
    將日期時間格式化為西元和民國格式
    西元格式：yyyy-mm-dd hh:mm:ss
    民國格式：(yyyy-1911)-mm-dd hh:mm:ss
    """
    western_date = dt.strftime("%Y-%m-%d %H:%M:%S")
    taiwan_year = dt.year - 1911
    taiwan_date = f"{taiwan_year}-{dt.strftime('%m-%d %H:%M:%S')}"

    return {"western_date": western_date, "taiwan_date": taiwan_date}


def get_search_messages(state):
    filtered_messages = []

    # 取得當前時間並格式化
    now = datetime.now()
    dates = format_dates(now)

    for m in state["messages"]:
        if isinstance(m, HumanMessage):
            filtered_messages.append(m)
        elif isinstance(m, AIMessage) and not m.tool_calls:
            filtered_messages.append(m)

    return [
        SystemMessage(
            content=search_prompt.format(
                western_date=dates["western_date"],
                taiwan_date=dates["taiwan_date"],
                prompt=SearchAgentGraph().get_search_prompt(),
            )
        )
    ] + filtered_messages


class RequirementPromptInstructions(BaseModel):
    has_requirement: bool


class RelatedQuestionsInstructions(BaseModel):
    related_questions: list[str]


llm_requirement = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0,
)
llm_with_requirement_tool = llm_requirement.bind_tools(
    [RequirementPromptInstructions],
)
llm_search = ChatPerplexity(
    model="llama-3.1-sonar-huge-128k-online",
    temperature=0.7,
)
llm_related = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,  # 使用較高的溫度以獲得更多樣化的建議
)
llm_with_related_tool = llm_related.bind_tools(
    [RelatedQuestionsInstructions], tool_choice="RelatedQuestionsInstructions"
)


def requirement_node(state):
    messages = get_requirement_messages(state["messages"])

    # 確保最後一條消息是 HumanMessage
    if not messages or not isinstance(messages[-1], HumanMessage):
        return {"messages": state["messages"]}

    response = llm_with_requirement_tool.invoke(messages)
    return {"messages": [response]}


async def search_with_perplexity_stream(state, config=None):
    messages = get_search_messages(state)

    # 確保配置正確
    config = ensure_config(config | {"tags": ["agent_llm"]})
    callback_manager = get_async_callback_manager_for_config(config)

    # 開始 LLM 運行
    llm_run_managers = await callback_manager.on_chat_model_start({}, [messages])
    llm_run_manager = llm_run_managers[0]

    # 將 messages 轉換為 Gemini 格式
    messages_for_llm = []
    input_content = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            messages_for_llm.append({"role": "user", "content": msg.content})
            input_content = msg.content
        elif isinstance(msg, AIMessage) and not msg.tool_calls:
            if (
                isinstance(msg.content, list)
                and isinstance(msg.content[0], dict)
                and msg.content[0].get("text", "")
            ):
                messages_for_llm.append(
                    {"role": "assistant", "content": msg.content[0].get("text", "")}
                )
            else:
                messages_for_llm.append({"role": "assistant", "content": msg.content})
        elif isinstance(msg, SystemMessage):
            if len(messages_for_llm) > 0 and messages_for_llm[0]["role"] != "system":
                messages_for_llm.insert(0, {"role": "system", "content": msg.content})
            elif len(messages_for_llm) > 0 and messages_for_llm[0]["role"] == "system":
                messages_for_llm[0]["content"] = msg.content
            elif len(messages_for_llm) == 0:
                messages_for_llm.append({"role": "system", "content": msg.content})

    full_response = ""
    async for event in respond_with_perplexity_search(
        input_content,
        SearchAgentGraph().get_user_prompt_prefix(),
        messages_for_llm,
        SearchAgentGraph().get_domain_filter(),
    ):
        # 將回應包裝成 ChatGenerationChunk 以支援 stream_mode="messages"
        chunk = ChatGenerationChunk(
            message=AIMessageChunk(
                content=event.chunk,
            )
        )

        # 使用 callback manager 處理新的 token
        await llm_run_manager.on_llm_new_token(
            event.chunk,
            chunk=chunk,
        )
        full_response += event.chunk

    return {"messages": [AIMessage(content=full_response)]}


async def search_with_gemini_grounding(state, config=None):
    messages = get_search_messages(state)

    # 確保配置正確
    config = ensure_config(config | {"tags": ["agent_llm"]})
    callback_manager = get_async_callback_manager_for_config(config)

    # 開始 LLM 運行
    llm_run_managers = await callback_manager.on_chat_model_start({}, [messages])
    llm_run_manager = llm_run_managers[0]

    # 將 messages 轉換為 Gemini 格式
    messages_for_llm = []
    input_content = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            messages_for_llm.append({"role": "user", "content": msg.content})
            input_content = msg.content
        elif isinstance(msg, AIMessage) and not msg.tool_calls:
            if (
                isinstance(msg.content, list)
                and isinstance(msg.content[0], dict)
                and msg.content[0].get("text", "")
            ):
                messages_for_llm.append(
                    {"role": "assistant", "content": msg.content[0].get("text", "")}
                )
            else:
                messages_for_llm.append({"role": "assistant", "content": msg.content})

    full_response = ""
    async for event in respond_with_gemini_grounding(input_content, messages_for_llm):
        # 將回應包裝成 ChatGenerationChunk 以支援 stream_mode="messages"
        chunk = ChatGenerationChunk(
            message=AIMessageChunk(
                content=event.chunk,
            )
        )

        # await adispatch_custom_event(
        #     "on_custom_event",
        #     {"chunk": event.chunk},
        #     config=config,  # <-- propagate config
        # )
        # 使用 callback manager 處理新的 token
        await llm_run_manager.on_llm_new_token(
            event.chunk,
            chunk=chunk,
        )
        full_response += event.chunk

    return {"messages": [AIMessage(content=full_response)]}


async def search_node(
    state,
    config=None,
):
    if SearchAgentGraph().get_search_vendor() == SEARCH_VENDOR_PLEXITY:
        return await search_with_perplexity_stream(state, config=config)
    else:
        return await search_with_gemini_grounding(state, config=config)


def get_related_messages(state):
    """
    獲取用於生成相關問題的消息列表
    """
    # 只保留人類消息和不含工具調用的 AI 消息
    filtered_messages = []
    previous_question = ""
    previous_response = ""

    for m in state["messages"]:
        if isinstance(m, HumanMessage):
            previous_question = m.content
            filtered_messages.append(m)
        elif isinstance(m, AIMessage) and not m.tool_calls:
            previous_response = m.content
            filtered_messages.append(m)
        elif isinstance(m, ToolMessage):
            filtered_messages.append(AIMessage(content=f"Tool Result: {m.content}"))

    # 驗證 related_prompt 格式
    related_prompt = SearchAgentGraph().get_related_prompt()
    related_prompt += related_question_text

    # 添加用於生成相關問題的提示
    filtered_messages.append(
        HumanMessage(
            content=related_prompt.format(
                original_question=previous_question,
                previous_response=previous_response,
            )
        )
    )

    return filtered_messages


def related_node(state):
    messages = get_related_messages(state)
    response = llm_with_related_tool.invoke(messages)
    if response.tool_calls:
        return {
            "messages": [
                response,
                ToolMessage(
                    content=str(response.tool_calls[0]["args"]["related_questions"]),
                    tool_call_id=response.tool_calls[0]["id"],
                ),
            ],
            "related_questions": response.tool_calls[0]["args"]["related_questions"],
        }
    return {"messages": [response]}


def get_requirement_next_state(state):
    messages = state["messages"]
    if isinstance(messages[-1], AIMessage) and messages[-1].tool_calls:
        tool_call = messages[-1].tool_calls[0]
        if tool_call["args"].get("has_requirement", False):
            return ADD_REQUIREMENT_TOOL_MESSAGE_NODE
        else:
            return END
    elif not isinstance(messages[-1], HumanMessage):
        return END
    return END


class SearchState(MessagesState):
    related_questions: list[str] = []


SEARCH_VENDOR_PLEXITY = "perplexity"
SEARCH_VENDOR_GOOGLE = "google"


class SearchAgentGraph:
    _instance = None
    _graph = None
    _search_prompt = default_search_prompt
    _user_prompt_prefix = ""
    _related_prompt = default_related_prompt
    _search_vendor = SEARCH_VENDOR_PLEXITY
    _domain_filter = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SearchAgentGraph, cls).__new__(cls)
            cls._instance._initialize_graph()
        return cls._instance

    def _initialize_graph(self):
        memory = MemorySaver()
        workflow = StateGraph(SearchState)
        workflow.add_node(REQUIREMENT_NODE, requirement_node)

        @workflow.add_node
        def add_requirement_tool_message(state: MessagesState):
            return {
                "messages": [
                    ToolMessage(
                        content=f"""
                        使用者有提出需求
                        """,
                        tool_call_id=state["messages"][-1].tool_calls[0]["id"],
                    )
                ],
                "has_requirement": True,
            }

        workflow.add_node(SEARCH_NODE, search_node)
        workflow.add_node(RELATED_NODE, related_node)

        workflow.add_edge(START, REQUIREMENT_NODE)
        workflow.add_conditional_edges(
            REQUIREMENT_NODE,
            get_requirement_next_state,
            [ADD_REQUIREMENT_TOOL_MESSAGE_NODE, END],
        )
        workflow.add_edge(ADD_REQUIREMENT_TOOL_MESSAGE_NODE, SEARCH_NODE)

        workflow.add_edge(SEARCH_NODE, RELATED_NODE)
        workflow.add_edge(RELATED_NODE, END)
        self._graph = workflow.compile(checkpointer=memory)

    def set_search_prompt(self, prompt: str):
        if prompt.strip():
            self._search_prompt = prompt

    def get_search_prompt(self):
        return self._search_prompt

    def set_related_prompt(self, prompt: str):
        if prompt.strip():
            self._related_prompt = prompt

    def get_related_prompt(self):
        return self._related_prompt

    def set_search_vendor(self, vendor: str):
        if vendor == SEARCH_VENDOR_GOOGLE:
            self._search_vendor = SEARCH_VENDOR_GOOGLE
        else:
            self._search_vendor = SEARCH_VENDOR_PLEXITY

    def get_search_vendor(self):
        return self._search_vendor

    def set_domain_filter(self, domain_filter: list[str]):
        self._domain_filter = domain_filter

    def get_domain_filter(self):
        return self._domain_filter

    def set_user_prompt_prefix(self, prefix: str):
        self._user_prompt_prefix = prefix

    def get_user_prompt_prefix(self):
        return self._user_prompt_prefix

    @property
    def graph(self):
        return self._graph


graph = SearchAgentGraph().graph
