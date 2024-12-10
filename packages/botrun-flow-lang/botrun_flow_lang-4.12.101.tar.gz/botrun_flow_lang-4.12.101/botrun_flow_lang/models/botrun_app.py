from pydantic import BaseModel
import yaml
from enum import Enum


class BotrunAppMode(str, Enum):
    CHATBOT = "chatbot"
    WORKFLOW = "workflow"


class BotrunApp(BaseModel):
    name: str
    description: str
    mode: BotrunAppMode

    def to_yaml(self) -> str:
        return yaml.dump(self.model_dump(mode="json"))

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "BotrunApp":
        data = yaml.safe_load(yaml_str)
        return cls(**data)
