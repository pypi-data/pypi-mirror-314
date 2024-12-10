"""
This node is responsible for creating the steps for the research process.
"""

# pylint: disable=line-too-long

from typing import List
from datetime import datetime
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
from botrun_flow_lang.langgraph_agents.agents.ai_researcher.agent.model import get_model
from botrun_flow_lang.langgraph_agents.agents.ai_researcher.agent.state import (
    AgentState,
)
from copilotkit.langchain import copilotkit_customize_config
from pydantic import BaseModel, Field


class SearchStep(BaseModel):
    """Model for a search step"""

    id: str = Field(
        description="The id of the step. This is used to identify the step in the state. Just make sure it is unique."
    )
    description: str = Field(
        description='The description of the step, i.e. "search for information about the latest AI news"'
    )
    status: str = Field(
        description='The status of the step. Always "pending".', enum=["pending"]
    )
    type: str = Field(description="The type of step.", enum=["search"])


@tool
def SearchTool(steps: List[SearchStep]):  # pylint: disable=invalid-name,unused-argument
    """
    Break the user's query into smaller steps.
    Use step type "search" to search the web for information.
    Make sure to add all the steps needed to answer the user's query.
    """


async def steps_node(state: AgentState, config: RunnableConfig):
    """
    The steps node is responsible for building the steps in the research process.
    """

    config = copilotkit_customize_config(
        config,
        emit_intermediate_state=[
            {"state_key": "steps", "tool": "SearchTool", "tool_argument": "steps"},
        ],
    )

    instructions = f"""
妳是臺灣人，回答要用臺灣繁體中文正式用語，需要的時候也可以用英文，可以親切、但不能隨便輕浮。在使用者合理的要求下請盡量配合他的需求，不要隨便拒絕

你是一個專門協助使用者搜尋臺灣政府補助和津貼資訊的 AI 助手。你的主要任務是將使用者的查詢需求，分解成最多三個具體的搜尋子任務。

任務要求：
1. 仔細分析使用者的查詢，識別關鍵資訊：
   - 申請者身份（如：一般民眾、原住民、新住民、身心障礙者等）
   - 需求類型（如：醫療、教育、就業、創業等）
   - 地理位置（如：特定縣市或地區）
   - 特殊條件（如：年齡、收入、資格限制等）

2. 將查詢轉換為最多三個具體的搜尋子任務：
   - 每個子任務應明確指出搜尋目標
   - 子任務應按優先順序排列
   - 確保子任務涵蓋使用者的核心需求
   - 避免重複或過於籠統的任務

3. 使用以下格式輸出：
搜尋子任務：
[1] {{第一個子任務的具體描述}}

[2] {{第二個子任務的具體描述}}

[3] {{第三個子任務的具體描述}}

注意事項：
- 確保每個子任務都是具體且可執行的
- 優先考慮主管機關的官方網站（domain 為 .gov.tw）
- 避免生成不確定或過時的資訊
- 如果使用者提供的資訊不足，應該生成適當的追問任務

這些步驟會被依序執行。最後，會產生一個最後的答案，以markdown格式呈現。

"""
    model = ChatAnthropic(temperature=0, model="claude-3-5-sonnet-latest")

    response = await model.bind_tools([SearchTool], tool_choice="SearchTool").ainvoke(
        [
            state["messages"][0],
            HumanMessage(content=instructions),
        ],
        config,
    )

    if len(response.tool_calls) == 0:
        steps = []
    else:
        steps = response.tool_calls[0]["args"]["steps"]

    if len(steps) != 0:
        steps[0]["updates"] = ["Searching the web..."]

    return {
        "steps": steps,
    }
