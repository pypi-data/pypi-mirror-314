from pydantic import BaseModel
from typing import List, Union, Optional
import yaml
from botrun_flow_lang.models.nodes.base_node import BaseNode, NodeType
from botrun_flow_lang.models.nodes.code_node import CodeNode, CodeNodeData
from botrun_flow_lang.models.nodes.http_request_node import (
    HttpRequestNode,
    HttpRequestNodeData,
)
from botrun_flow_lang.models.nodes.llm_node import LLMNodeData, LLMNode
from botrun_flow_lang.models.nodes.perplexity_node import (
    PerplexityNode,
    PerplexityNodeData,
)
from botrun_flow_lang.models.nodes.start_node import StartNodeData, StartNode
from botrun_flow_lang.models.nodes.end_node import EndNodeData, EndNode
from botrun_flow_lang.models.nodes.answer_node import AnswerNodeData, AnswerNode
from botrun_flow_lang.models.nodes.iteration_node import (
    IterationNodeData,
    IterationNode,
)
from botrun_flow_lang.models.nodes.search_and_scrape_node import (
    SearchAndScrapeNodeData,
    SearchAndScrapeNode,
)
from botrun_flow_lang.models.nodes.vertex_ai_search_node import (
    VertexAiSearchNode,
    VertexAiSearchNodeData,
)

NodeData = Union[
    LLMNodeData,
    StartNodeData,
    EndNodeData,
    AnswerNodeData,
    CodeNodeData,
    HttpRequestNodeData,
    IterationNodeData,
    SearchAndScrapeNodeData,
    PerplexityNodeData,
    VertexAiSearchNodeData,
]
Node = Union[
    LLMNode,
    StartNode,
    EndNode,
    AnswerNode,
    CodeNode,
    HttpRequestNode,
    IterationNode,
    SearchAndScrapeNode,
    PerplexityNode,
    VertexAiSearchNode,
]


class WorkflowItem(BaseModel):
    node: Optional[Node] = None
    items: Optional[List["WorkflowItem"]] = None


class Workflow(BaseModel):
    items: List[WorkflowItem]

    @classmethod
    def from_workflow_data(cls, workflow_data: "WorkflowData") -> "Workflow":
        return cls(items=cls._create_workflow_items(workflow_data.nodes))

    @classmethod
    def _create_workflow_items(
        cls, nodes: List[Union[NodeData, List]]
    ) -> List[WorkflowItem]:
        items = []
        for node in nodes:
            if isinstance(node, list):
                iteration_node = cls._create_node(node[0])
                sub_items = cls._create_workflow_items(node[1:])
                items.append(WorkflowItem(node=iteration_node, items=sub_items))
            else:
                items.append(WorkflowItem(node=cls._create_node(node)))
        return items

    @staticmethod
    def _create_node(node_data: NodeData) -> Node:
        if isinstance(node_data, StartNodeData):
            return StartNode(data=node_data)
        elif isinstance(node_data, LLMNodeData):
            return LLMNode(data=node_data)
        elif isinstance(node_data, EndNodeData):
            return EndNode(data=node_data)
        elif isinstance(node_data, AnswerNodeData):
            return AnswerNode(data=node_data)
        elif isinstance(node_data, CodeNodeData):
            return CodeNode(data=node_data)
        elif isinstance(node_data, HttpRequestNodeData):
            return HttpRequestNode(data=node_data)
        elif isinstance(node_data, IterationNodeData):
            return IterationNode(data=node_data)
        elif isinstance(node_data, SearchAndScrapeNodeData):
            return SearchAndScrapeNode(data=node_data)
        elif isinstance(node_data, PerplexityNodeData):
            return PerplexityNode(data=node_data)
        elif isinstance(node_data, VertexAiSearchNodeData):
            return VertexAiSearchNode(data=node_data)
        else:
            raise ValueError(f"Unknown node type: {type(node_data)}")


class WorkflowData(BaseModel):
    nodes: List[Union[NodeData, List[Union[NodeData, List]]]]

    def to_yaml(self) -> str:
        return yaml.dump(self.model_dump(mode="json"))

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "WorkflowData":
        data = yaml.safe_load(yaml_str)
        return cls(**data)
