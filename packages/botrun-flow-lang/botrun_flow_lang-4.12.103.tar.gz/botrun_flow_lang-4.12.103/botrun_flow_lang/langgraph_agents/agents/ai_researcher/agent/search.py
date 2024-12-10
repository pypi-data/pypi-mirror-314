"""
The search node is responsible for searching the internet for information.
"""

import json
import os
from datetime import datetime
from typing import Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
from langchain_community.tools import TavilySearchResults

from botrun_flow_lang.langgraph_agents.agents.ai_researcher.agent.state import (
    AgentState,
)
from botrun_flow_lang.langgraph_agents.agents.search_agent_graph import format_dates
from botrun_flow_lang.models.nodes.utils import scrape_vertexai_search_results
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

    # get last HumanMessage
    last_human_message = next(
        (msg for msg in state["messages"] if isinstance(msg, HumanMessage)), None
    )

    instructions = f"""
妳是臺灣人，回答要用臺灣繁體中文正式用語，需要的時候也可以用英文，可以親切、但不能隨便輕浮。在使用者合理的要求下請盡量配合他的需求，不要隨便拒絕

你是一個專門協助生成精確搜尋關鍵字的 AI 助手。你的任務是根據使用者的原始問題和已分解的子任務，為特定子任務生成最有效的搜尋關鍵字組合。

輸入資訊：
使用者原始問題：{last_human_message.content}
這些是所有任務：{json.dumps(state["steps"], ensure_ascii=False)}

妳需要執行這個子任務：{json.dumps(current_step, ensure_ascii=False)}

關鍵字生成規則：
1. 從廣泛到特定逐步擴展：
   - 基礎關鍵字：使用最基本的描述詞，如「[領域] 補助」
   - 相關術語：尋找同義詞、專業術語或相關概念
   - 跨領域詞彙：考慮需求可能涵蓋的跨領域或跨部門項目

2. 多角度組合策略：
   - 政策導向：加入當前政府重點政策相關詞彙
   - 地域性考量：加入地方政府或特定區域相關詞彙
   - 身份標記：加入特定身份（如：原住民、新住民、身心障礙者）
   - 時效性：加入年度或時間相關詞彙（如：113年、最新）
   - 補助類型：加入不同補助形式（如：補助、津貼、獎助、獎勵）

3. 關鍵字優化原則：
   - 使用繁體中文
   - 避免使用簡體字或外語
   - 使用台灣的官方用語習慣
   - 注意新舊政策用語差異（如：環保署改為環境部）

4. 輸出格式要求：
針對當前子任務，提供一組合適的搜尋關鍵字組合：
搜尋關鍵字：[關鍵字組合]

避免事項：
- 不使用過時或已廢止的專有名詞
- 不使用非正式或俚俗用語
- 避免過於籠統的關鍵字（如：補助、福利）
- 避免使用可能導致混淆的同音詞
- 避免使用行政機關簡稱（應使用全名）

特別注意：
- 確保關鍵字涵蓋該子任務的核心要素
- 考慮政府網站的特殊術語習慣
- 適時加入年度或時效性標記
- 必要時納入相關法規名稱或條例

注意補助單位的正確性，比如：
- 不要使用『行政院農業委員會』，應該要使用「農業部」，補助的負責單位為「農業部農糧署」
- 不要使用「環保署」或是「環境保護署」，要使用的是 「環境部」

現在的西元時間：{western_date}
現在的民國時間：{taiwan_date}

請妳依據以上的規範想出一個好的搜尋查詢，請直接輸出關鍵字組合，不需要其他說明，關鍵字之間用空格分隔。
"""

    chat_model = ChatAnthropic(temperature=0, model="claude-3-5-sonnet-latest")
    chat_model = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-pro")
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
        search_results = vertex_ai_search.vertex_search(
            project_id="scoop-386004",
            location="global",
            data_store_id="tw-gov-welfare_1730944342934",
            search_query=keywords,
        )
        print(search_results)
        scrape_results = await scrape_vertexai_search_results(search_results)
    except Exception as e:
        import traceback

        traceback.print_exc()

    if scrape_results:
        current_step["keywords"] = scrape_results["results"]
        current_step["search_result"] = scrape_results["results"]
        current_step["updates"] = [
            *current_step["updates"],
            "Extracting information...",
        ]
    else:
        current_step["search_result"] = []
        current_step["keywords"] = ""
        current_step["updates"] = [
            *current_step["updates"],
            "No relevant information found...",
        ]

    return state
