import unittest
from botrun_flow_lang.models.nodes.base_node import NodeType
from botrun_flow_lang.models.nodes.llm_node import LLMNodeData, LLMModelConfig
import uuid


class TestLLMNode(unittest.TestCase):
    def test_llm_node_data_creation(self):
        model_config = LLMModelConfig(
            completion_params={
                "frequency_penalty": 0,
                "max_tokens": 512,
                "presence_penalty": 0,
                "temperature": 0.7,
                "top_p": 1,
            },
            mode="chat",
            name="gpt-3.5-turbo",
            provider="openai",
        )

        llm_node = LLMNodeData(
            title="LLM 2",
            model=model_config,
            prompt_template=[
                {
                    "role": "system",
                    "text": "<Task>\nDo a general overview style summary to the following text. Use the same language as text to be summarized. \n<Text to be summarized>\n{{#1711526002155.input#}}\n<Summary>",
                }
            ],
            context={"enabled": False, "variable_selector": []},
            variables=[],
            vision={},
        )

        self.assertEqual(llm_node.type, NodeType.LLM)
        self.assertEqual(llm_node.title, "LLM 2")
        self.assertEqual(llm_node.model.name, "gpt-3.5-turbo")
        self.assertEqual(llm_node.model.provider, "openai")
        self.assertEqual(len(llm_node.prompt_template), 1)
        self.assertEqual(llm_node.context["enabled"], False)
        self.assertEqual(llm_node.input_variables, [])
        self.assertEqual(llm_node.output_variables, [])
        self.assertEqual(llm_node.vision, {})

        # Test that id is a string and can be parsed as a valid UUID
        self.assertIsInstance(llm_node.id, str)
        self.assertTrue(uuid.UUID(llm_node.id, version=4))


if __name__ == "__main__":
    unittest.main()
