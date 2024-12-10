import unittest
import asyncio
from botrun_flow_lang.models.nodes.base_node import NodeType
from botrun_flow_lang.models.nodes.answer_node import AnswerNode, AnswerNodeData
from botrun_flow_lang.models.nodes.event import (
    NodeRunStreamEvent,
    NodeRunCompletedEvent,
)
from botrun_flow_lang.models.variable import InputVariable
import uuid


class TestAnswerNode(unittest.TestCase):
    def test_answer_node_data_creation(self):
        answer_node = AnswerNodeData(title="Test Answer")

        self.assertEqual(answer_node.type, NodeType.ANSWER)
        self.assertEqual(answer_node.title, "Test Answer")

        # Test that id is a string and can be parsed as a valid UUID
        self.assertIsInstance(answer_node.id, str)
        self.assertTrue(uuid.UUID(answer_node.id, version=4))

    async def async_test_answer_node_run(self):
        answer_node = AnswerNode(
            data=AnswerNodeData(
                title="Test Answer",
                input_variables=[
                    InputVariable(node_id="idLLMNodeData", variable_name="llm_output")
                ],
            )
        )
        variable_pool = {"idLLMNodeData": {"llm_output": "Test output"}}

        async for event in answer_node.run(variable_pool):
            if isinstance(event, NodeRunStreamEvent):
                self.assertEqual(event.chunk, "Test output")
            elif isinstance(event, NodeRunCompletedEvent):
                self.assertEqual(event.outputs, {"answer": "Test output"})

    def test_answer_node_run(self):
        asyncio.run(self.async_test_answer_node_run())


if __name__ == "__main__":
    unittest.main()
