from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, AsyncGenerator
import uuid
from botrun_flow_lang.models.variable import InputVariable, OutputVariable
import re
import logging
from botrun_flow_lang.models.nodes.event import NodeEvent


class NodeType(str, Enum):
    START = "start"
    END = "end"
    ANSWER = "answer"
    LLM = "llm"
    CODE = "code"
    HTTP_REQUEST = "http-request"
    ITERATION = "iteration"
    SEARCH_AND_SCRAPE = "search-and-scrape"
    PERPLEXITY = "perplexity"
    VERTEX_AI_SEARCH = "vertex_ai_search"


class BaseNodeData(BaseModel):
    """
    @param printed_output: 可以指定一個 output_variables 裡面的變數名稱，在 NodeRunCompletedEvent 的時候會印出來
    """

    type: NodeType
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    desc: Optional[str] = ""
    input_variables: List[InputVariable] = Field(default_factory=list)
    output_variables: List[OutputVariable] = Field(default_factory=list)
    print_start: bool = False
    print_stream: bool = False
    print_complete: bool = False
    complete_output: Optional[str] = None


class BaseNode(BaseModel):
    data: BaseNodeData

    async def run(
        self,
        variable_pool: Dict[str, Dict[str, Any]],
    ) -> AsyncGenerator[NodeEvent, None]:
        raise NotImplementedError("This method should be implemented by subclasses")

    def get_variable(
        self, variable_pool: Dict[str, Dict[str, Any]], node_id: str, variable_name: str
    ) -> Any:
        if node_id in variable_pool and variable_name in variable_pool[node_id]:
            return variable_pool[node_id][variable_name]
        return None

    def update_variable_pool(
        self, variable_pool: Dict[str, Dict[str, Any]], node_output: Dict[str, Any]
    ):
        if self.data.id not in variable_pool:
            variable_pool[self.data.id] = {}
        variable_pool[self.data.id].update(node_output)

    def replace_variables(
        self, text: str, variable_pool: Dict[str, Dict[str, Any]]
    ) -> str:
        pattern = r"{{#([\w.-]+)#}}"
        matches = re.finditer(pattern, text)

        for match in matches:
            full_match = match.group(0)
            try:
                node_id, var_name = match.group(1).rsplit(".", 1)
                if node_id in variable_pool and var_name in variable_pool[node_id]:
                    replacement = str(variable_pool[node_id][var_name])
                    text = text.replace(full_match, replacement)
                else:
                    logging.warning(f"Variable not found in pool: {full_match}")
            except ValueError:
                logging.error(f"Invalid variable format: {full_match}")

        return text
