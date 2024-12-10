from pydantic import field_validator
from botrun_flow_lang.models.nodes.base_node import BaseNode, BaseNodeData, NodeType
from typing import Dict, Any, List, AsyncGenerator

from botrun_flow_lang.models.variable import InputVariable, OutputVariable
from botrun_flow_lang.models.nodes.event import NodeEvent, NodeRunCompletedEvent


class StartNodeData(BaseNodeData):
    type: NodeType = NodeType.START
    input_variables: List[InputVariable] = []
    output_variables: List[OutputVariable] = [
        OutputVariable(variable_name="user_input"),
        OutputVariable(variable_name="history"),
    ]

    @field_validator("input_variables")
    def validate_input_variables(cls, v):
        assert len(v) == 0, "StartNode must have 0 input variables"
        return v

    @field_validator("output_variables")
    def validate_output_variables(cls, v):
        assert len(v) == 2, "StartNode must have exactly 2 output variable"
        assert (
            v[0].variable_name == "user_input"
        ), "StartNode's output variable must be named 'user_input'"
        assert (
            v[1].variable_name == "history"
        ), "StartNode's output variable must be named 'history'"
        return v


class StartNode(BaseNode):
    data: StartNodeData

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        yield NodeRunCompletedEvent(
            node_id=self.data.id,
            node_title=self.data.title,
            node_type=self.data.type.value,
            outputs={
                "user_input": variable_pool.get(self.data.id, {}).get("user_input", ""),
                "history": variable_pool.get(self.data.id, {}).get("history", []),
            },
            complete_output=self.data.complete_output,
            is_print=self.data.print_start,
        )
