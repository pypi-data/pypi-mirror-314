from typing import AsyncGenerator, Dict, List, Union
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel


class StepsUpdateEvent(BaseModel):
    """
    for step in steps:
        print("Description:", step.get("description", ""))
        print("Status:", step.get("status", ""))
        print("Updates:", step.get("updates", ""))
    """

    steps: List = []


class OnNodeStreamEvent(BaseModel):
    chunk: str


async def agent_runner(
    thread_id: str, init_state: dict, graph: CompiledStateGraph
) -> AsyncGenerator[Union[StepsUpdateEvent, OnNodeStreamEvent], None]:
    config = {"configurable": {"thread_id": thread_id}}

    async for event in graph.astream_events(
        init_state,
        config,
        version="v2",
    ):
        if event["event"] == "on_chain_end":
            pass
            # print(event)
        if event["event"] == "on_chat_model_end":
            for step_event in handle_copilotkit_intermediate_state(event):
                yield step_event
        if event["event"] == "on_chat_model_stream":
            data = event["data"]
            if (
                data["chunk"].content
                and isinstance(data["chunk"].content[0], dict)
                and data["chunk"].content[0].get("text", "")
            ):
                yield OnNodeStreamEvent(chunk=data["chunk"].content[0].get("text", ""))
            elif data["chunk"].content and isinstance(data["chunk"].content, str):
                yield OnNodeStreamEvent(chunk=data["chunk"].content)


def handle_copilotkit_intermediate_state(event: dict):
    print("Handling copilotkit intermediate state")
    copilotkit_intermediate_state = event["metadata"].get(
        "copilotkit:emit-intermediate-state"
    )
    print(f"Intermediate state: {copilotkit_intermediate_state}")
    if copilotkit_intermediate_state:
        for intermediate_state in copilotkit_intermediate_state:
            if intermediate_state.get("state_key", "") == "steps":
                for tool_call in event["data"]["output"].tool_calls:
                    if tool_call.get("name", "") == intermediate_state.get("tool", ""):
                        steps = tool_call["args"].get(
                            intermediate_state.get("tool_argument")
                        )
                        print(f"Yielding steps: {steps}")
                        yield StepsUpdateEvent(steps=steps)
    print("--------------------------------")
