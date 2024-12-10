from typing import Dict, Any, List, Union
import uuid
from pydantic import BaseModel, field_validator, Field
import yaml
from botrun_flow_lang.models.botrun_app import BotrunApp, BotrunAppMode
from botrun_flow_lang.models.nodes.code_node import CodeNodeData
from botrun_flow_lang.models.nodes.http_request_node import HttpRequestNodeData
from botrun_flow_lang.models.nodes.iteration_node import IterationNodeData
from botrun_flow_lang.models.nodes.perplexity_node import PerplexityNodeData
from botrun_flow_lang.models.nodes.vertex_ai_search_node import VertexAiSearchNodeData
from botrun_flow_lang.models.workflow import WorkflowData, Workflow, WorkflowItem
from botrun_flow_lang.models.nodes.start_node import StartNodeData
from botrun_flow_lang.models.nodes.llm_node import LLMNodeData
from botrun_flow_lang.models.nodes.end_node import EndNodeData
from botrun_flow_lang.models.nodes.answer_node import AnswerNodeData
from botrun_flow_lang.models.nodes.search_and_scrape_node import SearchAndScrapeNodeData
from botrun_flow_lang.models.nodes.base_node import NodeType, BaseNodeData

NodeData = Union[
    StartNodeData,
    LLMNodeData,
    EndNodeData,
    AnswerNodeData,
    CodeNodeData,
    HttpRequestNodeData,
    IterationNodeData,
    SearchAndScrapeNodeData,
    PerplexityNodeData,
]


class WorkflowConfig(BaseModel):
    botrun_app: BotrunApp
    workflow: WorkflowData

    @field_validator("workflow")
    def validate_workflow(cls, v, values):
        if "botrun_app" not in values.data:
            raise ValueError("botrun_app must be provided")

        botrun_app = values.data["botrun_app"]
        nodes = v.nodes

        if not nodes:
            raise ValueError("Workflow must have at least one node")

        if botrun_app.mode == BotrunAppMode.WORKFLOW:
            if not cls._ends_with_node_type(nodes, EndNodeData):
                raise ValueError("Workflow mode must end with an EndNode")
        elif botrun_app.mode == BotrunAppMode.CHATBOT:
            if not cls._ends_with_node_type(nodes, AnswerNodeData):
                raise ValueError("Chatbot mode must end with an AnswerNode")

        return v

    @classmethod
    def _ends_with_node_type(cls, nodes, node_type):
        if isinstance(nodes[-1], list):
            return cls._ends_with_node_type(nodes[-1], node_type)
        return isinstance(nodes[-1], node_type)

    def to_yaml(self) -> str:
        return yaml.dump(
            self.model_dump(mode="json"),
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "WorkflowConfig":
        data = yaml.safe_load(yaml_str)
        botrun_app = BotrunApp(**data["botrun_app"])

        nodes = cls._parse_nodes(data["workflow"]["nodes"])
        workflow = WorkflowData(nodes=nodes)
        return cls(botrun_app=botrun_app, workflow=workflow)

    @staticmethod
    def _parse_nodes(
        node_data_list: List[Union[Dict, List]]
    ) -> List[Union[NodeData, List]]:
        nodes = []
        for item in node_data_list:
            if isinstance(item, list):
                nodes.append(
                    [WorkflowConfig._create_node(item[0])]
                    + WorkflowConfig._parse_nodes(item[1:])
                )
            else:
                nodes.append(WorkflowConfig._create_node(item))
        return nodes

    @staticmethod
    def _create_node(node_data: Dict[str, Any]) -> NodeData:
        node_type = NodeType(node_data["type"])
        if node_type == NodeType.START:
            return StartNodeData(**node_data)
        elif node_type == NodeType.LLM:
            return LLMNodeData(**node_data)
        elif node_type == NodeType.END:
            return EndNodeData(**node_data)
        elif node_type == NodeType.ANSWER:
            return AnswerNodeData(**node_data)
        elif node_type == NodeType.CODE:
            return CodeNodeData(**node_data)
        elif node_type == NodeType.HTTP_REQUEST:
            return HttpRequestNodeData(**node_data)
        elif node_type == NodeType.ITERATION:
            return IterationNodeData(**node_data)
        elif node_type == NodeType.SEARCH_AND_SCRAPE:
            return SearchAndScrapeNodeData(**node_data)
        elif node_type == NodeType.VERTEX_AI_SEARCH:
            return VertexAiSearchNodeData(**node_data)
        elif node_type == NodeType.PERPLEXITY:
            return PerplexityNodeData(**node_data)
        else:
            raise ValueError(f"Unknown node type: {node_type}")

    def to_workflow(self) -> Workflow:
        return Workflow.from_workflow_data(self.workflow)
