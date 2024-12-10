from typing import Any, AsyncGenerator, Dict, List, Optional
from pydantic import Field, field_validator, BaseModel
from botrun_flow_lang.models.nodes.base_node import BaseNode, BaseNodeData, NodeType
from botrun_flow_lang.models.nodes.event import (
    NodeEvent,
    NodeRunStreamEvent,
    NodeRunCompletedEvent,
    NodeRunFailedEvent,
)
from botrun_flow_lang.models.variable import InputVariable, OutputVariable
import aiohttp
import os
import json
from dotenv import load_dotenv

load_dotenv()


class PerplexityModelConfig(BaseModel):
    completion_params: Dict[str, Any] = Field(default_factory=dict)
    name: str = "llama-3.1-sonar-huge-128k-online"


class PerplexityNodeData(BaseNodeData):
    """
    @param input_variables: 輸入變數，可以傳入 prompt 和 history
    @param model: 模型設定，包含模型名稱和完成參數
    @param temperature: 控制隨機性的參數，介於 0-2 之間
    @param search_recency_filter: 搜尋結果的時間範圍，可選值為 month、week、day、hour
    @param prompt_template: 提示詞模板，格式為 List[Dict[str, str]]，每個 dict 包含 role 和 content
    """

    type: NodeType = NodeType.PERPLEXITY
    model: PerplexityModelConfig = Field(default_factory=PerplexityModelConfig)
    prompt_template: List[Dict[str, str]] = []
    temperature: float = Field(default=0.2, ge=0, lt=2)
    # search_recency_filter: str = "day"
    input_variables: List[InputVariable] = []
    output_variables: List[OutputVariable] = [
        OutputVariable(variable_name="perplexity_output")
    ]
    print_stream: bool = True

    @field_validator("output_variables")
    def validate_output_variables(cls, v):
        assert len(v) == 1, "PerplexityNode must have exactly 1 output variable"
        assert (
            v[0].variable_name == "perplexity_output"
        ), "PerplexityNode's output variable must be named 'perplexity_output'"
        return v


PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


class PerplexityNode(BaseNode):
    data: PerplexityNodeData

    def _get_api_key(self) -> str:
        api_key = os.getenv("PPLX_API_KEY")
        if not api_key:
            raise ValueError("PPLX_API_KEY environment variable not set")
        return api_key

    def prepare_messages(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        messages = []

        # Add messages from prompt template
        for message in self.data.prompt_template:
            content = self.replace_variables(message["content"], variable_pool)
            messages.append({"role": message["role"], "content": content})

        # Add history if provided
        history_var = next(
            (
                var
                for var in self.data.input_variables
                if var.variable_name == "history"
            ),
            None,
        )
        if history_var:
            history = self.get_variable(variable_pool, history_var.node_id, "history")
            if isinstance(history, list):
                if len(history) > 0:
                    if history[-1]["role"] == "user":
                        history.pop()
                history.extend(messages)
                messages = history

        # Add prompt if provided
        prompt_var = next(
            (var for var in self.data.input_variables if var.variable_name == "prompt"),
            None,
        )
        if prompt_var:
            prompt = self.get_variable(variable_pool, prompt_var.node_id, "prompt")
            if isinstance(prompt, str):
                messages.append({"role": "user", "content": prompt})

        return messages

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        try:
            messages = self.prepare_messages(variable_pool)
            if not messages:
                raise ValueError("No messages provided")

            headers = {
                "Authorization": f"Bearer {self._get_api_key()}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.data.model.name,
                "messages": messages,
                "temperature": self.data.temperature,
                "stream": True,
                # "search_recency_filter": self.data.search_recency_filter,
                **self.data.model.completion_params,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    PERPLEXITY_API_URL, headers=headers, json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise ValueError(f"Perplexity API error: {error_text}")

                    full_response = ""
                    async for line in response.content:
                        if line:
                            line = line.decode("utf-8").strip()
                            if line.startswith("data: "):
                                line = line[6:]  # Remove 'data: ' prefix
                                if line == "[DONE]":
                                    break

                                try:
                                    chunk_data = json.loads(line)
                                    if (
                                        chunk_data["choices"][0]
                                        .get("delta", {})
                                        .get("content")
                                    ):
                                        content = chunk_data["choices"][0]["delta"][
                                            "content"
                                        ]
                                        full_response += content
                                        yield NodeRunStreamEvent(
                                            node_id=self.data.id,
                                            node_title=self.data.title,
                                            node_type=self.data.type.value,
                                            chunk=content,
                                            is_print=self.data.print_stream,
                                        )
                                except json.JSONDecodeError:
                                    continue

            yield NodeRunCompletedEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                outputs={"perplexity_output": full_response},
                complete_output=self.data.complete_output,
                is_print=self.data.print_complete,
            )

        except Exception as e:
            yield NodeRunFailedEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                error=str(e),
                is_print=True,
            )
            raise
