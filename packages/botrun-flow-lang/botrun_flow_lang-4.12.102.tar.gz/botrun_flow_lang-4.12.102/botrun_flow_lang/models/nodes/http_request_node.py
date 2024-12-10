from enum import Enum
from typing import Dict, Any, AsyncGenerator, Optional, List
from pydantic import BaseModel, Field, field_validator
import aiohttp
import json

from botrun_flow_lang.models.nodes.base_node import BaseNode, BaseNodeData, NodeType
from botrun_flow_lang.models.variable import InputVariable, OutputVariable
from botrun_flow_lang.models.nodes.event import (
    NodeEvent,
    NodeRunCompletedEvent,
)


class AuthorizationType(str, Enum):
    NONE = "none"
    API_KEY = "api-key"


class ApiKeyType(str, Enum):
    BEARER = "bearer"
    BASIC = "basic"
    CUSTOM = "custom"


class BodyType(str, Enum):
    NONE = "none"
    JSON = "json"
    FORM_DATA = "form-data"
    X_WWW_FORM_URLENCODED = "x-www-form-urlencoded"
    RAW = "raw"
    BINARY = "binary"


class HttpMethod(str, Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


class AuthorizationConfig(BaseModel):
    api_key: str
    type: ApiKeyType


class Authorization(BaseModel):
    type: AuthorizationType = AuthorizationType.NONE
    config: Optional[AuthorizationConfig] = None


class Body(BaseModel):
    type: BodyType = BodyType.NONE
    data: Any = None


class Timeout(BaseModel):
    total: float = 30.0


class HttpRequestNodeData(BaseNodeData):
    type: NodeType = NodeType.HTTP_REQUEST
    authorization: Authorization = Field(default_factory=Authorization)
    body: Body = Field(default_factory=Body)
    headers: str = ""
    method: HttpMethod = HttpMethod.GET
    params: str = ""
    timeout: Timeout = Field(default_factory=Timeout)
    url: str
    input_variables: List[InputVariable] = Field(default_factory=list)
    output_variables: List[OutputVariable] = Field(
        default_factory=lambda: [
            OutputVariable(variable_name="status_code"),
            OutputVariable(variable_name="body"),
            OutputVariable(variable_name="headers"),
        ]
    )

    @field_validator("output_variables")
    def validate_output_variables(cls, v):
        required_vars = {"status_code", "body", "headers"}
        actual_vars = {ov.variable_name for ov in v}
        assert required_vars.issubset(
            actual_vars
        ), f"HttpRequestNode must have output variables: {required_vars}"
        return v


class HttpRequestNode(BaseNode):
    data: HttpRequestNodeData

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        try:
            headers = self._parse_headers(variable_pool)
            params = self._parse_params(variable_pool)
            body = self._prepare_body(variable_pool)

            url = self.replace_variables(self.data.url, variable_pool)
            print(f"[HttpRequestNode]url: {url}")
            print(f"[HttpRequestNode]params: {params}")

            timeout = aiohttp.ClientTimeout(total=self.data.timeout.total)

            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.request(
                    method=self.data.method.value,
                    url=url,
                    headers=headers,
                    params=params,
                    data=body,
                ) as response:
                    status_code = response.status
                    response_body = await response.text()
                    response_headers = dict(response.headers)

            yield NodeRunCompletedEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                outputs={
                    "status_code": status_code,
                    "body": response_body,
                    "headers": response_headers,
                },
                complete_output=self.data.complete_output,
                is_print=self.data.print_complete,
            )
        except Exception as e:
            print(f"Error executing HTTP request: url: {url}, params: {params}")
            print(f"http request exception: {str(e)}")
            # print(f"params: {params}")
            # import traceback

            # traceback.print_exc()
            yield NodeRunCompletedEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                outputs={
                    "status_code": "",
                    "body": f"Error executing HTTP request: {str(e)}",
                    "headers": {},
                },
                complete_output=self.data.complete_output,
                is_print=self.data.print_complete,
            )

            # raise RuntimeError(f"Error executing HTTP request: {str(e)}")

    def _parse_headers(self, variable_pool: Dict[str, Dict[str, Any]]) -> dict:
        headers = {}
        if self.data.headers:
            for line in self.data.headers.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    headers[key.strip()] = self.replace_variables(
                        value.strip(), variable_pool
                    )

        if self.data.authorization.type == AuthorizationType.API_KEY:
            if self.data.authorization.config:
                api_key = self.replace_variables(
                    self.data.authorization.config.api_key, variable_pool
                )
                if self.data.authorization.config.type == ApiKeyType.BEARER:
                    headers["Authorization"] = f"Bearer {api_key}"
                elif self.data.authorization.config.type == ApiKeyType.BASIC:
                    headers["Authorization"] = f"Basic {api_key}"
                elif self.data.authorization.config.type == ApiKeyType.CUSTOM:
                    headers["Authorization"] = api_key
        if self.data.body.type == BodyType.JSON:
            headers["Content-Type"] = "application/json"
        return headers

    def _parse_params(self, variable_pool: Dict[str, Dict[str, Any]]) -> dict:
        params = {}
        if self.data.params:
            for line in self.data.params.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    params[key.strip()] = self.replace_variables(
                        value.strip(), variable_pool
                    )
        return params

    def _prepare_body(self, variable_pool: Dict[str, Dict[str, Any]]) -> Any:
        if self.data.body.type == BodyType.NONE:
            return None
        elif self.data.body.type == BodyType.JSON:
            new_data = {}
            for key, value in self.data.body.data.items():
                if isinstance(value, str):
                    new_data[key] = self.replace_variables(value, variable_pool)
                else:
                    new_data[key] = value
            return json.dumps(new_data)  # 將字典轉換為 JSON 字符串
        elif self.data.body.type == BodyType.FORM_DATA:
            return aiohttp.FormData(
                {
                    k: self.replace_variables(v, variable_pool)
                    for k, v in self.data.body.data.items()
                }
            )
        elif self.data.body.type == BodyType.X_WWW_FORM_URLENCODED:
            return aiohttp.FormData(
                {
                    k: self.replace_variables(v, variable_pool)
                    for k, v in self.data.body.data.items()
                },
                quote_fields=False,
            )
        elif self.data.body.type == BodyType.RAW:
            return self.replace_variables(self.data.body.data, variable_pool)
        elif self.data.body.type == BodyType.BINARY:
            # Implement binary data handling if needed
            raise NotImplementedError("Binary body type is not implemented")
