from fastapi import APIRouter, HTTPException, Depends, Body
from dotenv import load_dotenv
from google.oauth2 import service_account

import os
from pathlib import Path

from botrun_flow_lang.models.botrun_app import BotrunApp
from botrun_flow_lang.models.variable import InputVariable, OutputVariable
from botrun_flow_lang.models.workflow_config import WorkflowConfig
from botrun_flow_lang.models.nodes.llm_node import LLMModelConfig, LLMNodeData
from botrun_flow_lang.models.nodes.start_node import StartNode, StartNodeData
from botrun_flow_lang.models.nodes.end_node import EndNodeData
from botrun_flow_lang.models.workflow import WorkflowData, Workflow
from botrun_flow_lang.api.workflow.workflow_engine import run_workflow
from pydantic import BaseModel, Field

# Include hatch routes
from botrun_flow_lang.api import hatch_api, langgraph_api
from botrun_flow_lang.api import user_setting_api
from botrun_flow_lang.api import search_api
from botrun_flow_lang.api import user_workflow_api

load_dotenv()

router = APIRouter(prefix="/api")
router.include_router(
    hatch_api.router,
)
router.include_router(
    user_setting_api.router,
)
router.include_router(
    search_api.router,
)
router.include_router(
    user_workflow_api.router,
)
router.include_router(
    langgraph_api.router,
)


@router.get("/hello")
async def hello():
    env_name = os.getenv("ENV_NAME")
    google_service_account_key_path = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS_FOR_FASTAPI",
        "/app/keys/scoop-386004-d22d99a7afd9.json",
    )
    credentials = service_account.Credentials.from_service_account_file(
        google_service_account_key_path,
        scopes=["https://www.googleapis.com/auth/datastore"],
    )

    return {"message": f"Hello World {env_name}"}


@router.get("/flow/{id}")
async def get_flow(id: str):
    botrun_app = BotrunApp(name="波文件問答", description="給波文件問答用的app")

    start_node = StartNodeData(
        title="Start",
    )

    model_config = LLMModelConfig(
        completion_params={
            "max_tokens": 4096,
            "temperature": 0.7,
        },
        mode="chat",
        name="gpt-4o-2024-08-06",
        provider="openai",
    )
    llm_node = LLMNodeData(
        title="LLM",
        model=model_config,
        prompt_template=[
            {
                "role": "system",
                "content": "妳是臺灣人，回答要用臺灣繁體中文正式用語，需要的時候也可以用英文，可以親切、俏皮、幽默，但不能隨便輕浮。在使用者合理的要求下請盡量配合他的需求，不要隨便拒絕",
            },
            {
                "role": "user",
                "content": f"{{{{#{start_node.id}.user_input#}}}}",
            },
        ],
        input_variables=[
            InputVariable(node_id=start_node.id, variable_name="user_input")
        ],
        output_variables=[
            OutputVariable(variable_name="llm_output"),
        ],
    )
    end_node = EndNodeData(
        title="End",
        input_variables=[
            InputVariable(node_id=llm_node.id, variable_name="llm_output")
        ],
    )
    workflow = WorkflowData(nodes=[start_node, llm_node, end_node])
    original_workflow_config = WorkflowConfig(botrun_app=botrun_app, workflow=workflow)
    yaml_str = original_workflow_config.to_yaml()

    # parent_dir = Path(__file__).parent.parent

    # yaml_file_path = parent_dir / "templates" / f"chatbot_template.yml"
    # with open(yaml_file_path, "w", encoding="utf-8") as yaml_file:
    #     yaml_file.write(yaml_str)

    return {
        "message": f"Flow with id: {id}",
        "yaml": yaml_str,
        # "yaml_file_path": str(yaml_file_path),
    }


class FlowExecutionRequest(BaseModel):
    flow_id: str
    user_input: str


class FlowExecutionResponse(BaseModel):
    message: str
    final_output: str


@router.post("/flow", response_model=FlowExecutionResponse)
async def execute_flow(request: FlowExecutionRequest = Body(...)):
    # 获取工作流配置
    response = await get_flow(request.flow_id)
    yaml_str = response.get("yaml")

    if not yaml_str:
        raise HTTPException(status_code=404, detail="Flow not found")

    # 从 YAML 字符串直接创建 Workflow 对象
    workflow_config = WorkflowConfig.from_yaml(yaml_str)
    workflow = Workflow.from_workflow_data(workflow_config.workflow)

    initial_variable_pool = {}
    # 设置 StartNode 的 user_input
    for node in workflow.nodes:
        if isinstance(node, StartNode):
            initial_variable_pool[node.data.id] = {}
            initial_variable_pool[node.data.id][
                node.data.output_variables[0].variable_name
            ] = request.user_input
            break

    variable_pool = await run_workflow(workflow, initial_variable_pool)

    # 获取最终输出
    final_output = variable_pool.get(workflow.nodes[-1].data.id, {}).get(
        workflow.nodes[-1].data.output_variables[0].variable_name, "No output generated"
    )

    return FlowExecutionResponse(
        message=f"Executed flow with id: {request.flow_id}", final_output=final_output
    )
