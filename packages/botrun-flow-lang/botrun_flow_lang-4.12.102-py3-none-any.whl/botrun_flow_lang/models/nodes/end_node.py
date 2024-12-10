from pydantic import Field, field_validator
from botrun_flow_lang.models.nodes.base_node import BaseNode, BaseNodeData, NodeType
from typing import Dict, Any, List, AsyncGenerator

from botrun_flow_lang.models.variable import InputVariable, OutputVariable
from botrun_flow_lang.models.nodes.event import NodeEvent, NodeRunCompletedEvent


class EndNodeData(BaseNodeData):
    type: NodeType = NodeType.END
    output_variables: List[OutputVariable] = [
        OutputVariable(variable_name="final_output")
    ]

    @field_validator("input_variables")
    def validate_input_variables(cls, v):
        assert len(v) == 1, "EndNode must have exactly 1 input variable"
        return v

    @field_validator("output_variables")
    def validate_output_variables(cls, v):
        assert len(v) == 1, "EndNode must have exactly 1 output variable"
        assert (
            v[0].variable_name == "final_output"
        ), "EndNode's output variable must be named 'final_output'"
        return v


class EndNode(BaseNode):
    data: EndNodeData

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        input_value = self.get_variable(
            variable_pool,
            self.data.input_variables[0].node_id,
            self.data.input_variables[0].variable_name,
        )
        yield NodeRunCompletedEvent(
            node_id=self.data.id,
            node_title=self.data.title,
            node_type=self.data.type.value,
            outputs={"final_output": input_value},
            complete_output=self.data.complete_output,
            is_print=self.data.print_complete,
        )
