import unittest
import asyncio
from botrun_flow_lang.models.nodes.base_node import NodeType
from botrun_flow_lang.models.nodes.start_node import StartNode, StartNodeData
from botrun_flow_lang.models.nodes.event import NodeRunCompletedEvent
import uuid


class TestStartNode(unittest.TestCase):
    def test_start_node_data_creation(self):
        start_node = StartNodeData(title="Test Start")

        self.assertEqual(start_node.type, NodeType.START)
        self.assertEqual(start_node.title, "Test Start")

        # Test that id is a string and can be parsed as a valid UUID
        self.assertIsInstance(start_node.id, str)
        self.assertTrue(uuid.UUID(start_node.id, version=4))

    async def async_test_start_node_run(self):
        start_node = StartNode(data=StartNodeData(title="Test Start"))
        variable_pool = {"user_input": "Hello, world!"}

        async for event in start_node.run(variable_pool):
            self.assertIsInstance(event, NodeRunCompletedEvent)
            self.assertEqual(event.outputs, {"user_input": "Hello, world!"})

    def test_start_node_run(self):
        asyncio.run(self.async_test_start_node_run())


if __name__ == "__main__":
    unittest.main()
