from typing import Dict, Any, AsyncGenerator, List
from pydantic import Field, field_validator

from botrun_flow_lang.models.nodes.base_node import BaseNode, BaseNodeData, NodeType
from botrun_flow_lang.models.variable import InputVariable
from botrun_flow_lang.models.nodes.event import NodeEvent


class IterationNodeData(BaseNodeData):
    type: NodeType = NodeType.ITERATION
    input_selector: InputVariable
    output_selector: InputVariable
    is_async: bool = True  # 新增字段，默认为 True

    @field_validator("input_selector")
    def validate_input_selector(cls, v):
        assert v is not None, "IterationNode must have an input_selector"
        return v

    @field_validator("output_selector")
    def validate_output_selector(cls, v):
        assert v is not None, "IterationNode must have an output_selector"
        return v


class IterationNode(BaseNode):
    data: IterationNodeData

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        # This method is now handled by WorkflowEngine._execute_iteration
        raise NotImplementedError("IterationNode.run should not be called directly")
