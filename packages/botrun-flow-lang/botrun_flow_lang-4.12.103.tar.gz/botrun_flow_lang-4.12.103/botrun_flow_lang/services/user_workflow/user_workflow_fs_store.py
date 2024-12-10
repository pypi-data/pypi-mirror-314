from typing import Union, List, Tuple
from google.cloud.exceptions import GoogleCloudError
from botrun_flow_lang.constants import USER_WORKFLOW_STORE_NAME
from botrun_flow_lang.services.user_workflow.user_workflow import UserWorkflow
from botrun_flow_lang.services.base.firestore_base import FirestoreBase
from google.cloud import firestore


class UserWorkflowFsStore(FirestoreBase):
    def __init__(self, env_name: str):
        super().__init__(f"{env_name}-{USER_WORKFLOW_STORE_NAME}")

    async def get_user_workflow(self, workflow_id: str) -> Union[UserWorkflow, None]:
        doc_ref = self.collection.document(workflow_id)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return UserWorkflow(**data)
        else:
            print(f">============Getting user workflow {workflow_id} not exists")
            return None

    async def set_user_workflow(self, user_workflow: UserWorkflow):
        try:
            doc_ref = self.collection.document(user_workflow.id)
            doc_ref.set(user_workflow.model_dump())
            return True, user_workflow
        except GoogleCloudError as e:
            print(f"Error setting user workflow {user_workflow.id}: {e}")
            return False, None

    async def delete_user_workflow(self, workflow_id: str):
        try:
            doc_ref = self.collection.document(workflow_id)
            doc_ref.delete()
            return True
        except GoogleCloudError as e:
            print(f"Error deleting user workflow {workflow_id}: {e}")
            return False

    async def get_user_workflows(
        self, user_id: str, offset: int = 0, limit: int = 20
    ) -> Tuple[List[UserWorkflow], str]:
        try:
            query = (
                self.collection.where(
                    filter=firestore.FieldFilter("user_id", "==", user_id)
                )
                .offset(offset)
                .limit(limit)
            )

            docs = query.stream()
            workflows = [UserWorkflow(**doc.to_dict()) for doc in docs]
            return workflows, ""
        except GoogleCloudError as e:
            print(f"Error getting user workflows for user {user_id}: {e}")
            return [], str(e)
