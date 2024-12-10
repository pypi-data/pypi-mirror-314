from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from botrun_flow_lang.services.user_workflow.user_workflow import UserWorkflow
from botrun_flow_lang.services.user_workflow.user_workflow_factory import (
    user_workflow_store_factory,
)
from botrun_flow_lang.services.user_workflow.user_workflow_fs_store import (
    UserWorkflowFsStore,
)

router = APIRouter()


async def get_user_workflow_store():
    return user_workflow_store_factory()


@router.post("/user_workflow", response_model=UserWorkflow)
async def create_user_workflow(
    user_workflow: UserWorkflow,
    store: UserWorkflowFsStore = Depends(get_user_workflow_store),
):
    success, created_workflow = await store.set_user_workflow(user_workflow)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create user workflow")
    return created_workflow


@router.put("/user_workflow/{workflow_id}", response_model=UserWorkflow)
async def update_user_workflow(
    workflow_id: str,
    user_workflow: UserWorkflow,
    store: UserWorkflowFsStore = Depends(get_user_workflow_store),
):
    existing_workflow = await store.get_user_workflow(workflow_id)
    if not existing_workflow:
        raise HTTPException(status_code=404, detail="User workflow not found")
    user_workflow.id = workflow_id
    success, updated_workflow = await store.set_user_workflow(user_workflow)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update user workflow")
    return updated_workflow


@router.delete("/user_workflow/{workflow_id}")
async def delete_user_workflow(
    workflow_id: str, store: UserWorkflowFsStore = Depends(get_user_workflow_store)
):
    success = await store.delete_user_workflow(workflow_id)
    if not success:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "message": f"Failed to delete user workflow {workflow_id}",
            },
        )
    return {
        "success": True,
        "message": f"User workflow {workflow_id} deleted successfully",
    }


@router.get("/user_workflow/{workflow_id}", response_model=UserWorkflow)
async def get_user_workflow(
    workflow_id: str, store: UserWorkflowFsStore = Depends(get_user_workflow_store)
):
    user_workflow = await store.get_user_workflow(workflow_id)
    if not user_workflow:
        raise HTTPException(status_code=404, detail="User workflow not found")
    return user_workflow


@router.get("/user_workflows", response_model=List[UserWorkflow])
async def get_user_workflows(
    user_id: str,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=20),
    store: UserWorkflowFsStore = Depends(get_user_workflow_store),
):
    workflows, error = await store.get_user_workflows(user_id, offset, limit)
    if error:
        raise HTTPException(status_code=500, detail=error)
    return workflows
