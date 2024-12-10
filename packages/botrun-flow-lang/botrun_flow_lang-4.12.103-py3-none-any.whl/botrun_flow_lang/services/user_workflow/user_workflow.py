from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid
from botrun_flow_lang.models.workflow_config import WorkflowConfig


class UserWorkflow(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    workflow_config_yaml: str
