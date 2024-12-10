from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import time

from botrun_flow_lang.langgraph_agents.agents.agent_runner import (
    OnNodeStreamEvent,
    agent_runner,
)
from botrun_flow_lang.langgraph_agents.agents.search_agent_graph import SearchAgentGraph
from botrun_flow_lang.langgraph_agents.agents.ai_researcher.agent.agent import (
    graph as ai_researcher_graph,
)

router = APIRouter(prefix="/langgraph")


class Message(BaseModel):
    role: str = "assistant"
    content: str


class Delta(BaseModel):
    role: str = "assistant"
    content: str = ""


class Choice(BaseModel):
    index: int = 0
    message: Message
    finish_reason: str = "stop"
    delta: Delta = Delta()


class LangGraphRequest(BaseModel):
    graph_name: str
    thread_id: str
    user_input: str
    config: Optional[Dict[str, Any]] = None


class LangGraphResponse(BaseModel):
    """
    @param content: 這個是給評測用來評估結果用的
    @param state: 這個是graph的 final state，如果需要額外資訊可以使用
    """

    id: str
    object: str = "chat.completion"
    created: int
    model: str
    content: Optional[str] = None
    state: Optional[Dict[str, Any]] = None


class SupportedGraphsResponse(BaseModel):
    """Response model for listing supported graphs"""

    graphs: List[str]


PERPLEXITY_SEARCH_AGENT = "perplexity_search_agent"
TAVILY_RESEARCH_AGENT = "tavily_research_agent"
SUPPORTED_GRAPHS = {
    PERPLEXITY_SEARCH_AGENT: SearchAgentGraph().graph,
    TAVILY_RESEARCH_AGENT: ai_researcher_graph,
}


def get_graph(graph_name: str, config: Optional[Dict[str, Any]] = None):
    if graph_name not in SUPPORTED_GRAPHS:
        raise ValueError(f"Unsupported graph from get_graph: {graph_name}")
    graph = SUPPORTED_GRAPHS[graph_name]
    if graph_name == PERPLEXITY_SEARCH_AGENT:
        SearchAgentGraph().set_search_prompt(config.get("search_prompt", ""))
        SearchAgentGraph().set_related_prompt(config.get("search_vendor", "perplexity"))
        # SearchAgentGraph().set_user_prompt_prefix(config.get("user_prompt_prefix", ""))
        SearchAgentGraph().set_domain_filter(config.get("domain_filter", []))
    return graph


def get_init_state(
    graph_name: str, user_input: str, config: Optional[Dict[str, Any]] = None
):
    if graph_name == PERPLEXITY_SEARCH_AGENT:
        if config.get("user_prompt_prefix", ""):
            return {
                "messages": [
                    {
                        "role": "user",
                        "content": config.get("user_prompt_prefix", "")
                        + "\n\n"
                        + user_input,
                    }
                ]
            }

        return {"messages": [user_input]}
    elif graph_name == TAVILY_RESEARCH_AGENT:
        return {
            "messages": [user_input],
            "model": config.get("model", "anthropic"),
        }
    raise ValueError(f"Unsupported graph from get_init_state: {graph_name}")


def get_content(graph_name: str, state: Dict[str, Any]):
    if graph_name == PERPLEXITY_SEARCH_AGENT:
        return state["messages"][-3].content
    elif graph_name == TAVILY_RESEARCH_AGENT:
        content = state["answer"].get("markdown", "")
        if state["answer"].get("references", []):
            references = "\n\n參考資料：\n"
            for reference in state["answer"]["references"]:
                references += f"- [{reference['title']}]({reference['url']})\n"
            content += references
        return content
    raise ValueError(f"Unsupported graph from get_content: {graph_name}")


@router.post("/run", response_model=LangGraphResponse)
async def run_langgraph(request: LangGraphRequest):
    """
    執行指定的 LangGraph

    Args:
        request: 包含 graph_name 和輸入數據的請求

    Returns:
        執行結果和狀態
    """
    try:
        graph = get_graph(request.graph_name, request.config)
        init_state = get_init_state(
            request.graph_name, request.user_input, request.config
        )
        async for event in agent_runner(request.thread_id, init_state, graph):
            pass
            # if isinstance(event, OnNodeStreamEvent):
            #     content += event.chunk

        config = {"configurable": {"thread_id": request.thread_id}}
        state = graph.get_state(config)
        content = get_content(request.graph_name, state.values)
        return LangGraphResponse(
            id=request.thread_id,
            created=int(time.time()),
            model=request.graph_name,
            content=content,
            state=state.values,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"執行 LangGraph 時發生錯誤: {str(e)}"
        )


@router.get("/list", response_model=SupportedGraphsResponse)
async def list_supported_graphs():
    """
    列出所有支援的 LangGraph names

    Returns:
        包含所有支援的 graph names 的列表
    """
    return SupportedGraphsResponse(graphs=list(SUPPORTED_GRAPHS.keys()))
