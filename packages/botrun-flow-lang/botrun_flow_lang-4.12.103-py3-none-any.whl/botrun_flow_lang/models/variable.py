from pydantic import BaseModel, Field
from typing import Optional


class InputVariable(BaseModel):
    node_id: str
    variable_name: str


class OutputVariable(BaseModel):
    variable_name: str
