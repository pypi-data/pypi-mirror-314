from pydantic import BaseModel
from typing import Dict, Any, List, Optional


class NodeEvent(BaseModel):
    """
    node_type 就是 NodeType的值，但是不能直接使用 NodeType 因為會circular import
    """

    node_id: str
    node_type: str
    node_title: str
    is_print: bool = False


class NodeRunStartedEvent(NodeEvent):
    pass


class NodeRunCompletedEvent(NodeEvent):
    outputs: Dict[str, Any]
    complete_output: Optional[str] = None


class NodeRunStreamEvent(NodeEvent):
    chunk: str


class NodeRunFailedEvent(NodeEvent):
    error: str


class WorkflowRunStartedEvent(BaseModel):
    pass


class WorkflowRunCompletedEvent(BaseModel):
    outputs: Dict[str, Any]
    execution_times: List[str] = []


class WorkflowRunFailedEvent(BaseModel):
    error: str
