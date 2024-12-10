import ast
from typing import Dict, Any, AsyncGenerator
from pydantic import Field, field_validator

from botrun_flow_lang.models.nodes.base_node import BaseNode, BaseNodeData, NodeType
from botrun_flow_lang.models.variable import InputVariable, OutputVariable
from botrun_flow_lang.models.nodes.event import (
    NodeEvent,
    NodeRunCompletedEvent,
)


class CodeNodeData(BaseNodeData):
    """
    function回傳一個 dict，key 是 output_variables 的 variable_name，value 是對應的值
    """

    type: NodeType = NodeType.CODE
    code: str = Field(..., description="Python3 code to be executed")
    input_variables: list[InputVariable] = Field(default_factory=list)
    output_variables: list[OutputVariable] = Field(default_factory=list)

    @field_validator("code")
    def validate_code(cls, v):
        try:
            ast.parse(v)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python code: {str(e)}")
        return v


class CodeNode(BaseNode):
    data: CodeNodeData

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        input_args = {}
        for input_var in self.data.input_variables:
            input_args[input_var.variable_name] = self.get_variable(
                variable_pool, input_var.node_id, input_var.variable_name
            )

        # Execute the code
        try:
            exec_globals = {}
            exec(self.data.code, exec_globals)
            main_func = exec_globals.get("main")
            if not main_func:
                raise ValueError("No 'main' function defined in the code")

            result = main_func(**input_args)

            if not isinstance(result, dict):
                raise ValueError("The 'main' function must return a dictionary")

            # Prepare output
            output = {}
            for output_var in self.data.output_variables:
                if output_var.variable_name in result:
                    output[output_var.variable_name] = result[output_var.variable_name]
                else:
                    raise ValueError(
                        f"Output variable '{output_var.variable_name}' not found in the result"
                    )

            yield NodeRunCompletedEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                outputs=output,
                complete_output=self.data.complete_output,
                is_print=self.data.print_complete,
            )
        except Exception as e:
            raise RuntimeError(f"Error executing {self.data.title} code: {str(e)}")
