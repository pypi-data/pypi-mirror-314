import unittest
from botrun_flow_lang.models.nodes.start_node import StartNodeData
from botrun_flow_lang.models.workflow_config import WorkflowConfig
from botrun_flow_lang.models.botrun_app import BotrunApp, BotrunAppMode
from botrun_flow_lang.models.workflow import WorkflowData
from botrun_flow_lang.models.nodes.llm_node import LLMNodeData, LLMModelConfig
from botrun_flow_lang.utils.yaml_utils import compare_yaml_with_deepdiff
from botrun_flow_lang.models.nodes.base_node import NodeType
from botrun_flow_lang.models.nodes.end_node import EndNodeData
from botrun_flow_lang.models.variable import InputVariable, OutputVariable
from botrun_flow_lang.models.nodes.answer_node import AnswerNodeData


class TestWorkflowConfig(unittest.TestCase):
    def test_to_yaml(self):
        botrun_app = BotrunApp(
            name="Test App",
            description="A test application",
            mode=BotrunAppMode.CHATBOT,
        )
        model_config = LLMModelConfig(
            completion_params={
                "max_tokens": 512,
                "temperature": 0.7,
            },
            mode="chat",
            name="gpt-3.5-turbo",
            provider="openai",
        )
        llm_node = LLMNodeData(
            title="Test LLM",
            id="idLLMNodeData",
            model=model_config,
            prompt_template=[
                {"role": "system", "text": "You are a helpful assistant."}
            ],
            input_variables=[],
            output_variables=[OutputVariable(variable_name="test_var")],
        )
        answer_node = AnswerNodeData(
            title="Answer Node",
            id="idAnswerNodeData",
            input_variables=[
                InputVariable(node_id="idLLMNodeData", variable_name="test_var")
            ],
        )
        workflow = WorkflowData(nodes=[llm_node, answer_node])
        workflow_config = WorkflowConfig(botrun_app=botrun_app, workflow=workflow)
        yaml_str = workflow_config.to_yaml()
        expected_yaml = """
botrun_app:
  name: Test App
  description: A test application
  mode: chatbot
workflow:
  nodes:
    - type: llm
      id: idLLMNodeData
      title: Test LLM
      desc: ''
      model:
        completion_params:
          max_tokens: 512
          temperature: 0.7
        mode: chat
        name: gpt-3.5-turbo
        provider: openai
      prompt_template:
        - role: system
          text: You are a helpful assistant.
      context: {}
      input_variables: []
      output_variables:
        - variable_name: test_var
      vision: {}
    - type: answer
      id: idAnswerNodeData
      title: Answer Node
      desc: ''
      input_variables:
        - node_id: idLLMNodeData
          variable_name: test_var
      output_variables:
        - variable_name: answer
"""
        diff = compare_yaml_with_deepdiff(yaml_str, expected_yaml)
        self.assertEqual(diff, {})

    def test_from_yaml(self):
        yaml_str = """
botrun_app:
  name: Test App
  description: A test application
  mode: workflow
workflow:
  nodes:
    - type: llm
      id: idLLMNodeData
      title: Test LLM
      model:
        completion_params:
          max_tokens: 512
          temperature: 0.7
        mode: chat
        name: gpt-3.5-turbo
        provider: openai
      prompt_template:
        - role: system
          text: You are a helpful assistant.
      context: {}
      input_variables: []
      output_variables:
        - variable_name: test_var
      vision: {}
    - type: end
      id: idEndNodeData
      title: End Node
      desc: ''
      input_variables:
        - node_id: idLLMNodeData
          variable_name: test_var
      output_variables:
        - variable_name: final_output
"""
        workflow_config = WorkflowConfig.from_yaml(yaml_str)
        self.assertEqual(workflow_config.botrun_app.name, "Test App")
        self.assertEqual(workflow_config.botrun_app.description, "A test application")
        self.assertEqual(workflow_config.botrun_app.mode, BotrunAppMode.WORKFLOW)
        self.assertEqual(len(workflow_config.workflow.nodes), 2)
        self.assertIsInstance(workflow_config.workflow.nodes[0], LLMNodeData)
        self.assertEqual(workflow_config.workflow.nodes[0].title, "Test LLM")
        self.assertEqual(workflow_config.workflow.nodes[0].id, "idLLMNodeData")
        self.assertEqual(len(workflow_config.workflow.nodes[0].output_variables), 1)
        self.assertEqual(
            workflow_config.workflow.nodes[0].output_variables[0].variable_name,
            "test_var",
        )

    def test_roundtrip(self):
        botrun_app = BotrunApp(
            name="Test App",
            description="A test application",
            mode=BotrunAppMode.WORKFLOW,
        )
        model_config = LLMModelConfig(
            completion_params={
                "max_tokens": 512,
                "temperature": 0.7,
            },
            mode="chat",
            name="gpt-3.5-turbo",
            provider="openai",
        )
        llm_node = LLMNodeData(
            title="Test LLM",
            id="idLLMNodeData",
            model=model_config,
            prompt_template=[
                {"role": "system", "text": "You are a helpful assistant."}
            ],
            input_variables=[],
            output_variables=[OutputVariable(variable_name="test_var")],
        )
        end_node = EndNodeData(
            title="End Node",
            id="idEndNodeData",
            input_variables=[
                InputVariable(node_id="idLLMNodeData", variable_name="test_var")
            ],
        )
        workflow = WorkflowData(nodes=[llm_node, end_node])
        original_workflow_config = WorkflowConfig(
            botrun_app=botrun_app, workflow=workflow
        )
        yaml_str = original_workflow_config.to_yaml()
        reconstructed_workflow_config = WorkflowConfig.from_yaml(yaml_str)
        self.assertEqual(original_workflow_config, reconstructed_workflow_config)

    def test_workflow_with_start_and_llm_nodes(self):
        botrun_app = BotrunApp(
            name="Test App",
            description="A test application",
            mode=BotrunAppMode.WORKFLOW,
        )

        start_node = StartNodeData(
            title="Start Node",
            id="idStartNodeData",
            input_variables=[],
            output_variables=[OutputVariable(variable_name="user_input")],
        )

        model_config = LLMModelConfig(
            completion_params={
                "max_tokens": 512,
                "temperature": 0.7,
            },
            mode="chat",
            name="gpt-3.5-turbo",
            provider="openai",
        )
        llm_node = LLMNodeData(
            title="Test LLM",
            id="idLLMNodeData",
            model=model_config,
            prompt_template=[
                {"role": "system", "text": "You are a helpful assistant."}
            ],
            input_variables=[
                InputVariable(node_id="idStartNodeData", variable_name="user_input")
            ],
            output_variables=[OutputVariable(variable_name="test_var")],
        )
        end_node = EndNodeData(
            title="End Node",
            id="idEndNodeData",
            input_variables=[
                InputVariable(node_id="idLLMNodeData", variable_name="test_var")
            ],
        )

        workflow = WorkflowData(nodes=[start_node, llm_node, end_node])
        workflow_config = WorkflowConfig(botrun_app=botrun_app, workflow=workflow)

        yaml_str = workflow_config.to_yaml()
        expected_yaml = """
botrun_app:
  name: Test App
  description: A test application
  mode: workflow
workflow:
  nodes:
    - type: start
      id: idStartNodeData
      title: Start Node
      desc: ''
      input_variables: []
      output_variables:
        - variable_name: user_input
    - type: llm
      id: idLLMNodeData
      title: Test LLM
      desc: ''
      model:
        completion_params:
          max_tokens: 512
          temperature: 0.7
        mode: chat
        name: gpt-3.5-turbo
        provider: openai
      prompt_template:
        - role: system
          text: You are a helpful assistant.
      context: {}
      input_variables:
        - node_id: idStartNodeData
          variable_name: user_input
      output_variables:
        - variable_name: test_var
      vision: {}
    - type: end
      id: idEndNodeData
      title: End Node
      desc: ''
      input_variables:
        - node_id: idLLMNodeData
          variable_name: test_var
      output_variables:
        - variable_name: final_output
"""
        diff = compare_yaml_with_deepdiff(yaml_str, expected_yaml)
        self.assertEqual(diff, {})

        # Test from_yaml
        reconstructed_workflow_config = WorkflowConfig.from_yaml(yaml_str)
        self.assertEqual(len(reconstructed_workflow_config.workflow.nodes), 3)
        self.assertIsInstance(
            reconstructed_workflow_config.workflow.nodes[0], StartNodeData
        )
        self.assertIsInstance(
            reconstructed_workflow_config.workflow.nodes[1], LLMNodeData
        )
        self.assertIsInstance(
            reconstructed_workflow_config.workflow.nodes[2], EndNodeData
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[1].title, "Test LLM"
        )

        # 在测试 from_yaml 时，检查 type 字段
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[0].type, NodeType.START
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[1].type, NodeType.LLM
        )

        # Additional from_yaml test
        self.assertEqual(reconstructed_workflow_config.botrun_app.name, "Test App")
        self.assertEqual(
            reconstructed_workflow_config.botrun_app.description, "A test application"
        )
        self.assertEqual(
            reconstructed_workflow_config.botrun_app.mode, BotrunAppMode.WORKFLOW
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[0].id, "idStartNodeData"
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[1].id, "idLLMNodeData"
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[1].model.name, "gpt-3.5-turbo"
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[1].model.provider, "openai"
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[1].model.completion_params[
                "max_tokens"
            ],
            512,
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[1].model.completion_params[
                "temperature"
            ],
            0.7,
        )

    def test_workflow_with_start_llm_and_end_nodes(self):
        botrun_app = BotrunApp(
            name="Test App",
            description="A test application",
            mode=BotrunAppMode.WORKFLOW,
        )

        start_node = StartNodeData(
            title="Start Node",
            id="idStartNodeData",
            input_variables=[],
            output_variables=[OutputVariable(variable_name="user_input")],
        )

        model_config = LLMModelConfig(
            completion_params={
                "max_tokens": 512,
                "temperature": 0.7,
            },
            mode="chat",
            name="gpt-3.5-turbo",
            provider="openai",
        )
        llm_node = LLMNodeData(
            title="Test LLM",
            id="idLLMNodeData",
            model=model_config,
            prompt_template=[
                {"role": "system", "text": "You are a helpful assistant."}
            ],
            input_variables=[
                InputVariable(node_id="idStartNodeData", variable_name="user_input")
            ],
            output_variables=[OutputVariable(variable_name="llm_output")],
        )

        end_node = EndNodeData(
            title="End Node",
            id="idEndNodeData",
            input_variables=[
                InputVariable(node_id="idLLMNodeData", variable_name="llm_output")
            ],
        )

        workflow = WorkflowData(nodes=[start_node, llm_node, end_node])
        workflow_config = WorkflowConfig(botrun_app=botrun_app, workflow=workflow)

        yaml_str = workflow_config.to_yaml()
        expected_yaml = """
botrun_app:
  name: Test App
  description: A test application
  mode: workflow
workflow:
  nodes:
    - type: start
      id: idStartNodeData
      title: Start Node
      desc: ''
      input_variables: []
      output_variables:
        - variable_name: user_input
    - type: llm
      id: idLLMNodeData
      title: Test LLM
      desc: ''
      model:
        completion_params:
          max_tokens: 512
          temperature: 0.7
        mode: chat
        name: gpt-3.5-turbo
        provider: openai
      prompt_template:
        - role: system
          text: You are a helpful assistant.
      context: {}
      input_variables:
        - node_id: idStartNodeData
          variable_name: user_input
      output_variables:
        - variable_name: llm_output
      vision: {}
    - type: end
      id: idEndNodeData
      title: End Node
      desc: ''
      input_variables:
        - node_id: idLLMNodeData
          variable_name: llm_output
      output_variables:
        - variable_name: final_output
"""
        diff = compare_yaml_with_deepdiff(yaml_str, expected_yaml)
        self.assertEqual(diff, {})

        # Test from_yaml
        reconstructed_workflow_config = WorkflowConfig.from_yaml(yaml_str)
        self.assertEqual(len(reconstructed_workflow_config.workflow.nodes), 3)
        self.assertIsInstance(
            reconstructed_workflow_config.workflow.nodes[0], StartNodeData
        )
        self.assertIsInstance(
            reconstructed_workflow_config.workflow.nodes[1], LLMNodeData
        )
        self.assertIsInstance(
            reconstructed_workflow_config.workflow.nodes[2], EndNodeData
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[0].type, NodeType.START
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[1].type, NodeType.LLM
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[2].type, NodeType.END
        )
        self.assertEqual(
            reconstructed_workflow_config.botrun_app.mode, BotrunAppMode.WORKFLOW
        )

        # Check variables
        self.assertEqual(
            len(reconstructed_workflow_config.workflow.nodes[0].output_variables), 1
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[0]
            .output_variables[0]
            .variable_name,
            "user_input",
        )

        self.assertEqual(
            len(reconstructed_workflow_config.workflow.nodes[1].input_variables), 1
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[1]
            .input_variables[0]
            .variable_name,
            "user_input",
        )
        self.assertEqual(
            len(reconstructed_workflow_config.workflow.nodes[1].output_variables), 1
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[1]
            .output_variables[0]
            .variable_name,
            "llm_output",
        )

        self.assertEqual(
            len(reconstructed_workflow_config.workflow.nodes[2].input_variables), 1
        )
        self.assertEqual(
            reconstructed_workflow_config.workflow.nodes[2]
            .input_variables[0]
            .variable_name,
            "llm_output",
        )

    def test_workflow_mode_validation(self):
        botrun_app = BotrunApp(
            name="Test App",
            description="A test application",
            mode=BotrunAppMode.WORKFLOW,
        )

        start_node = StartNodeData(
            title="Start Node",
            id="idStartNodeData",
            input_variables=[],
            output_variables=[OutputVariable(variable_name="user_input")],
        )

        llm_node = LLMNodeData(
            title="Test LLM",
            id="idLLMNodeData",
            model=LLMModelConfig(
                completion_params={
                    "max_tokens": 512,
                    "temperature": 0.7,
                },
                mode="chat",
                name="gpt-3.5-turbo",
                provider="openai",
            ),
            prompt_template=[
                {"role": "system", "text": "You are a helpful assistant."}
            ],
            input_variables=[
                InputVariable(node_id="idStartNodeData", variable_name="user_input")
            ],
            output_variables=[OutputVariable(variable_name="llm_output")],
        )

        end_node = EndNodeData(
            title="End Node",
            id="idEndNodeData",
            input_variables=[
                InputVariable(node_id="idLLMNodeData", variable_name="llm_output")
            ],
        )

        # This should work
        workflow = WorkflowData(nodes=[start_node, llm_node, end_node])
        WorkflowConfig(botrun_app=botrun_app, workflow=workflow)

        # This should fail
        answer_node = AnswerNodeData(
            title="Answer Node",
            id="idAnswerNodeData",
            input_variables=[
                InputVariable(node_id="idLLMNodeData", variable_name="llm_output")
            ],
        )
        workflow_invalid = WorkflowData(nodes=[start_node, llm_node, answer_node])
        with self.assertRaises(ValueError):
            WorkflowConfig(botrun_app=botrun_app, workflow=workflow_invalid)

    def test_chatbot_mode_validation(self):
        botrun_app = BotrunApp(
            name="Test App",
            description="A test application",
            mode=BotrunAppMode.CHATBOT,
        )

        start_node = StartNodeData(
            title="Start Node",
            id="idStartNodeData",
            input_variables=[],
            output_variables=[OutputVariable(variable_name="user_input")],
        )

        llm_node = LLMNodeData(
            title="Test LLM",
            id="idLLMNodeData",
            model=LLMModelConfig(
                completion_params={
                    "max_tokens": 512,
                    "temperature": 0.7,
                },
                mode="chat",
                name="gpt-3.5-turbo",
                provider="openai",
            ),
            prompt_template=[
                {"role": "system", "text": "You are a helpful assistant."}
            ],
            input_variables=[
                InputVariable(node_id="idStartNodeData", variable_name="user_input")
            ],
            output_variables=[OutputVariable(variable_name="llm_output")],
        )

        answer_node = AnswerNodeData(
            title="Answer Node",
            id="idAnswerNodeData",
            input_variables=[
                InputVariable(node_id="idLLMNodeData", variable_name="llm_output")
            ],
        )

        # This should work
        workflow = WorkflowData(nodes=[start_node, llm_node, answer_node])
        WorkflowConfig(botrun_app=botrun_app, workflow=workflow)

        # This should fail
        end_node = EndNodeData(
            title="End Node",
            id="idEndNodeData",
            input_variables=[
                InputVariable(node_id="idLLMNodeData", variable_name="llm_output")
            ],
        )
        workflow_invalid = WorkflowData(nodes=[start_node, llm_node, end_node])
        with self.assertRaises(ValueError):
            WorkflowConfig(botrun_app=botrun_app, workflow=workflow_invalid)


if __name__ == "__main__":
    unittest.main()
