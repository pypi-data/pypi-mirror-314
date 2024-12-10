"""
The search node is responsible for searching the internet for information.
"""

import json
import os
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_google_community import VertexAISearchRetriever
from google.oauth2 import service_account
from langchain.tools import tool
from langchain_community.tools import TavilySearchResults

from botrun_flow_lang.langgraph_agents.agents.ai_researcher.agent.model import get_model
from botrun_flow_lang.langgraph_agents.agents.ai_researcher.agent.state import (
    AgentState,
)
from botrun_flow_lang.langgraph_agents.agents.search_agent_graph import format_dates
from botrun_flow_lang.models.nodes.vertex_ai_search_node import VertexAISearch


class SearchKeywords(BaseModel):
    """Model for search keywords"""

    keywords: str = Field(
        description="The search keywords to be used for the search query"
    )


@tool
def ExtractKeywordsTool(keywords: SearchKeywords):  # pylint: disable=invalid-name
    """
    Extract and format search keywords from the user's query.
    Return the formatted keywords as a string.
    """


async def search_node(state: AgentState, config: RunnableConfig):
    """
    The search node is responsible for searching the internet for information.
    """

    tavily_tool = TavilySearchResults(
        max_results=10,
        search_depth="advanced",
        include_answer=False,
        include_raw_content=True,
        include_images=False,
        include_domains=["*.gov.tw"],
    )

    current_step = next(
        (step for step in state["steps"] if step["status"] == "pending"), None
    )

    if current_step is None:
        raise ValueError("No step to search for")

    if current_step["type"] != "search":
        raise ValueError("Current step is not a search step")

    now = datetime.now()
    dates = format_dates(now)
    western_date = dates["western_date"]
    taiwan_date = dates["taiwan_date"]

    # todo: 使用新的 prompt

    instructions = f"""
妳是臺灣人，回答要用臺灣繁體中文正式用語，需要的時候也可以用英文，可以親切、但不能隨便輕浮。在使用者合理的要求下請盡量配合他的需求，不要隨便拒絕



這是一個步驟，這些步驟正在被執行，來回答使用者的查詢。
這些是所有步驟：{json.dumps(state["steps"], ensure_ascii=False)}

妳需要執行這個步驟：{json.dumps(current_step, ensure_ascii=False)}

你是一個專門協助產生臺灣政府補助和津貼搜尋關鍵字的 AI 助手。當收到搜尋子任務時，你需要產生精確且有效的關鍵字組合。

關鍵字產生原則：
1. 多層次關鍵字組合：
   - 從一般到特殊的遞進式關鍵字
   - 包含同義詞或相近詞
   - 考慮官方用語和常用表述
   - 納入地理位置相關詞

2. 搜尋限定詞：
   - 加入 "補助"、"津貼"、"獎助"、"輔助" 等後綴
   - 必要時加入年份限定

3. 關鍵字組合方式：
   - 身分類別 + 補助類型
   - 地區 + 補助項目
   - 特定需求 + 補助性質
   - 專業術語 + 一般用語

請依照以下格式輸出：

一般搜尋關鍵字：
- {{列出一般性的關鍵字組合}}
- {{建議的同義詞組合}}

精確搜尋關鍵字：
- {{加入限定詞的精確關鍵字}}
- {{加入地區或單位的精確關鍵字}}

進階搜尋組合：
- {{建議的進階搜尋語法}}

相關詞擴展：
- {{相關領域的關鍵詞}}
- {{可能的跨領域關鍵詞}}

注意事項：
- 關鍵字應考慮官方用語習慣
- 包含傳統用語和新興術語
- 避免使用不常用或模糊的詞彙
- 關鍵字組合應該簡潔有力
- 考慮不同政府部門的用語差異

注意補助單位的正確性，比如：
- 不要使用『行政院農業委員會』，應該要使用「農業部」，補助的負責單位為「農業部農糧署」
- 不要使用「環保署」或是「環境保護署」，要使用的是 「環境部」

現在的西元時間：{western_date}
現在的民國時間：{taiwan_date}

這是妳需要搜尋的內容：{current_step["description"]}
請妳依據以上的規範想出一個好的搜尋查詢，請直接輸出關鍵字組合，不需要其他說明，關鍵字之間用空格分隔。
"""

    chat_model = ChatAnthropic(temperature=0, model="claude-3-5-sonnet-latest")
    model = chat_model.bind_tools(
        [ExtractKeywordsTool], tool_choice=ExtractKeywordsTool.name
    )
    response = await model.ainvoke([HumanMessage(content=instructions)], config)

    # Extract keywords from the tool response
    keywords = response.tool_calls[0]["args"]["keywords"]["keywords"]
    print(f"keywords: {keywords}")

    # Use the extracted keywords for the search
    try:
        vertex_ai_search = VertexAISearch()
        results = vertex_ai_search.vertex_search(
            project_id="scoop-386004",
            location="global",
            data_store_id="tw-gov-welfare_1730944342934",
            search_query=keywords,
        )
        print(results)
    except Exception as e:
        import traceback

    search_results = retriever.invoke(keywords)

    if search_results:
        # Convert the Document objects to a format similar to the previous search results
        formatted_results = []
        for doc in search_results:
            formatted_result = {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": doc.metadata.get(
                    "score", 0
                ),  # If score is available in metadata
            }
            formatted_results.append(formatted_result)

        current_step["search_result"] = formatted_results
        current_step["updates"] = [
            *current_step["updates"],
            "Extracting information...",
        ]
    else:
        current_step["search_result"] = []
        current_step["updates"] = [
            *current_step["updates"],
            "No relevant information found...",
        ]

    return state
