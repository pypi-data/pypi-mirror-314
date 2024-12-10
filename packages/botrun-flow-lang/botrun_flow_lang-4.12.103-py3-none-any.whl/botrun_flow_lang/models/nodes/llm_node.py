from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, AsyncGenerator
from botrun_flow_lang.models.nodes.base_node import BaseNode, BaseNodeData, NodeType
import litellm
from botrun_flow_lang.models.nodes.event import (
    NodeEvent,
    NodeRunStreamEvent,
    NodeRunCompletedEvent,
)

import os
from dotenv import load_dotenv

from botrun_flow_lang.models.variable import InputVariable, OutputVariable

load_dotenv()


class LLMModelConfig(BaseModel):
    completion_params: Dict[str, Any] = Field(default_factory=dict)
    name: str


class LLMNodeData(BaseNodeData):
    """
    @param input_variables: 輸入變數，目前只有 history 可以傳入，如果有輸入的話，回答時會帶入 history 的內容，也可以不傳入
    @param stream: 是否要以 stream 的方式返回訊息
    """

    type: NodeType = NodeType.LLM
    model: LLMModelConfig
    prompt_template: List[Dict[str, str]]
    context: Dict[str, Any] = Field(default_factory=dict)
    vision: Dict[str, bool] = Field(default_factory=dict)
    stream: bool = True
    print_stream: bool = True
    output_variables: List[OutputVariable] = [
        OutputVariable(variable_name="llm_output"),
    ]

    @field_validator("output_variables")
    def validate_output_variables(cls, v):
        assert len(v) == 1, "LLMNode must have exactly 1 output variable"
        assert (
            v[0].variable_name == "llm_output"
        ), "LLMNode's output variable must be named 'llm_output'"
        return v


class LLMNode(BaseNode):
    data: LLMNodeData

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        messages = self.prepare_messages(variable_pool)
        if len(self.data.input_variables) > 0:
            history = self.get_variable(
                variable_pool,
                self.data.input_variables[0].node_id,
                self.data.input_variables[0].variable_name,
            )
            if isinstance(history, list):
                history.extend(messages)
                messages = history
        if self.data.stream:
            stream = await litellm.acompletion(
                model=self.data.model.name,
                messages=messages,
                stream=True,
                api_key=get_api_key(self.data.model.name),
                **self.data.model.completion_params
            )

            full_response = ""
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    yield NodeRunStreamEvent(
                        node_id=self.data.id,
                        node_title=self.data.title,
                        node_type=self.data.type.value,
                        chunk=content,
                        is_print=self.data.print_stream,
                    )
        else:
            response = litellm.completion(
                model=self.data.model.name,
                messages=messages,
                api_key=get_api_key(self.data.model.name),
                **self.data.model.completion_params
            )
            full_response = response.choices[0].message.content

        yield NodeRunCompletedEvent(
            node_id=self.data.id,
            node_title=self.data.title,
            node_type=self.data.type.value,
            outputs={"llm_output": full_response},
            complete_output=self.data.complete_output,
            is_print=self.data.print_complete,
        )

    def prepare_messages(self, variable_pool):
        messages = []
        for message in self.data.prompt_template:
            content = self.replace_variables(message["content"], variable_pool)
            messages.append({"role": message["role"], "content": content})
        return messages


def get_api_key(model_name: str) -> str:
    if model_name.find("TAIDE-") != -1:
        return os.getenv("TAIDE_API_KEY", "")
    elif model_name.startswith("anthropic"):
        return os.getenv("ANTHROPIC_API_KEY", "")
    elif model_name.startswith("openai"):
        return os.getenv("OPENAI_API_KEY", "")
    elif model_name.startswith("gemini"):
        return os.getenv("GEMINI_API_KEY", "")
    elif model_name.startswith("together_ai"):
        return os.getenv("TOGETHERAI_API_KEY", "")
    elif model_name.startswith("deepinfra"):
        return os.getenv("DEEPINFRA_API_KEY", "")
    else:
        return ""
