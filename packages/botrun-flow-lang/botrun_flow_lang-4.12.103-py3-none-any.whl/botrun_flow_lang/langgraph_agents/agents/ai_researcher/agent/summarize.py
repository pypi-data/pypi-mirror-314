"""
The summarize node is responsible for summarizing the information.
"""

from copy import deepcopy
import json
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from botrun_flow_lang.langgraph_agents.agents.ai_researcher.agent.model import get_model
from botrun_flow_lang.langgraph_agents.agents.ai_researcher.agent.state import (
    AgentState,
)
from copilotkit.langchain import copilotkit_customize_config
from pydantic import BaseModel, Field
from datetime import datetime

from botrun_flow_lang.langgraph_agents.agents.search_agent_graph import format_dates


class Reference(BaseModel):
    """Model for a reference"""

    title: str = Field(description="The title of the reference.")
    url: str = Field(description="The url of the reference.")


class SummarizeInput(BaseModel):
    """Input for the summarize tool"""

    markdown: str = Field(
        description="""
                          The markdown formatted summary of the final result.
                          If you add any headings, make sure to start at the top level (#).
                          Use actual newline characters (\n) instead of escaped newlines (\\n).
                          """
    )
    references: list[Reference] = Field(description="A list of references.")


@tool(args_schema=SummarizeInput)
def SummarizeTool(
    summary: str, references: list[Reference]
):  # pylint: disable=invalid-name,unused-argument
    """
    Summarize the final result. Make sure that the summary is complete and
    includes all relevant information and reference links.
    """


async def summarize_node(state: AgentState, config: RunnableConfig):
    """
    The summarize node is responsible for summarizing the information.
    """

    config = copilotkit_customize_config(
        config,
        emit_intermediate_state=[
            {
                "state_key": "answer",
                "tool": "SummarizeTool",
            }
        ],
    )

    steps = deepcopy(state["steps"])
    for step in steps:
        step["search_result"] = None
    now = datetime.now()
    dates = format_dates(now)
    western_date = dates["western_date"]
    taiwan_date = dates["taiwan_date"]

    system_message = f"""
現在的西元時間：{western_date}
現在的民國時間：{taiwan_date}

## 系統狀態信息
這個系統已經完成了一連串的研究步驟，來回答使用者的問題。

使用者的問題：
<使用者問題>
{state["messages"][0].content}
</使用者問題>

系統的研究結果：
<所有研究結果>
{json.dumps(steps, ensure_ascii=False)}
</所有研究結果>

## 核心指令

你是一位專業的台灣政府補助和獎助辦法諮詢顧問。請嚴格遵守以下指示：

### 1. 角色定位與行為準則

你必須：
- 以親切護理師大姊姊的形象與使用者互動
- 使用台灣繁體中文正式用語，必要時可使用英文
- 展現專業、溫暖且有同理心的態度
- 保持親切但不隨便輕浮的互動方式

### 2. 回應規則

每次回應都必須：
1. 以溫暖的問候開始
2. 根據系統提供的研究結果進行回答
3. 確保所有資訊來自台灣政府網站（*.gov.tw）
4. 使用以下格式提供資訊：
```
🌼 津貼補助名稱
🌼 主辦單位
🌼 申請對象與資格
🌼 補助金額與費用計算
🌼 申請期限
🌼 申請流程
🌼 準備資料
🌼 受理申請單位
🌼 資料來源網址
```

5. 使用優先順序標記：
```
🔴 最高優先：立即處理事項
🟠 高優先：儘快處理事項
🟡 中優先：計劃性處理事項
🟢 低優先：彈性處理事項
🔵 參考：長期規劃事項
```

### 3. 資訊準確性要求

你必須：
- 基於系統提供的研究結果進行回答
- 僅使用有效期內的補助方案
- 提供準確的金額、期限和申請資格
- 使用正確的政府部門名稱（如：使用「農業部」而非「農委會」）
- 清楚區分新住民與原住民族群

### 4. 引用規範

所有資訊必須：
- 在句中標註來源：[來源名稱][編號]
- 在回答末尾提供完整參考連結：
```markdown
[1]: http://example.gov.tw "標題"
```

### 5. 禁止事項

你嚴禁：
- 生成未經驗證的資訊
- 預測或揣測政策
- 提供已過期的補助資訊
- 自行創造不存在的補助方案
- 超出系統提供的研究結果範圍

### 6. 特殊情況處理

當系統研究結果中找不到符合的補助時：
1. 誠實告知無法找到符合的方案
2. 提供最接近的替代方案（如果研究結果中有）
3. 建議其他可能的資源管道

### 7. 數據驗證流程

處理每個補助方案時必須：
1. 確認補助年度對應現在時間
2. 驗證申請期限是否有效
3. 核實補助金額計算方式
4. 確認申請資格條件完整性

記住：你的首要任務是基於系統提供的研究結果，協助台灣民眾找到最適合的政府補助資源，同時確保提供的所有資訊準確可靠。

請注意：
1. 使用實際的換行符號（\n），而不是轉義的換行符號（\\n）
2. 確保 markdown 格式正確
3. 參考連結要放在最後
"""
    chat_model = ChatAnthropic(temperature=0, model="claude-3-5-sonnet-latest")
    chat_model = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-pro")

    response = await chat_model.bind_tools(
        [SummarizeTool], tool_choice="SummarizeTool"
    ).ainvoke(
        [
            HumanMessage(content=system_message),
        ],
        config,
    )

    return {
        "answer": response.tool_calls[0]["args"],
    }
