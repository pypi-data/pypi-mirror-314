import os

from botrun_flow_lang.services.user_workflow.user_workflow_fs_store import (
    UserWorkflowFsStore,
)


def user_workflow_store_factory():
    env_name = os.getenv("ENV_NAME", "dev")
    return UserWorkflowFsStore(env_name)
