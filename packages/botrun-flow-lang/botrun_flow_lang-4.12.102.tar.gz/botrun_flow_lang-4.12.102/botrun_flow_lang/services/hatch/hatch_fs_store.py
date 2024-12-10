from typing import Union, List, Tuple
from google.cloud.exceptions import GoogleCloudError
from botrun_flow_lang.constants import HATCH_STORE_NAME
from botrun_flow_lang.services.hatch.hatch import Hatch
from botrun_flow_lang.services.base.firestore_base import FirestoreBase
from google.cloud import firestore


class HatchFsStore(FirestoreBase):
    def __init__(self, env_name: str):
        super().__init__(f"{env_name}-{HATCH_STORE_NAME}")

    async def get_hatch(self, item_id: str) -> Union[Hatch, None]:
        doc_ref = self.collection.document(item_id)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return Hatch(**data)
        else:
            print(f">============Getting hatch {item_id} not exists")
            return None

    async def set_hatch(self, item: Hatch):
        try:
            doc_ref = self.collection.document(str(item.id))
            doc_ref.set(item.model_dump())
            return True, item
        except GoogleCloudError as e:
            print(f"Error setting hatch {item.id}: {e}")
            return False, None

    async def delete_hatch(self, item_id: str):
        try:
            doc_ref = self.collection.document(item_id)
            doc_ref.delete()
            return True
        except GoogleCloudError as e:
            print(f"Error deleting hatch {item_id}: {e}")
            return False

    async def get_hatches(
        self, user_id: str, offset: int = 0, limit: int = 20
    ) -> Tuple[List[Hatch], str]:
        try:
            query = (
                self.collection.where(
                    filter=firestore.FieldFilter("user_id", "==", user_id)
                )
                .order_by("name")
                .offset(offset)
                .limit(limit)
            )

            docs = query.stream()
            hatches = [Hatch(**doc.to_dict()) for doc in docs]
            return hatches, ""
        except GoogleCloudError as e:
            import traceback

            traceback.print_exc()
            print(f"Error getting hatches for user {user_id}: {e}")
            return [], f"Error getting hatches for user {user_id}: {e}"
        except Exception as e:
            import traceback

            traceback.print_exc()
            print(f"Error getting hatches for user {user_id}: {e}")
            return [], f"Error getting hatches for user {user_id}: {e}"

    async def get_default_hatch(self, user_id: str) -> Union[Hatch, None]:
        try:
            query = (
                self.collection.where(
                    filter=firestore.FieldFilter("user_id", "==", user_id)
                )
                .where(filter=firestore.FieldFilter("is_default", "==", True))
                .limit(1)
            )
            docs = query.stream()
            for doc in docs:
                return Hatch(**doc.to_dict())
            return None
        except GoogleCloudError as e:
            print(f"Error getting default hatch for user {user_id}: {e}")
            return None

    async def set_default_hatch(self, user_id: str, hatch_id: str) -> Tuple[bool, str]:
        try:
            # 获取当前的默认 hatch
            current_default = await self.get_default_hatch(user_id)

            # 获取要设置为默认的 hatch
            new_default = await self.get_hatch(hatch_id)
            if not new_default or new_default.user_id != user_id:
                return (
                    False,
                    f"Hatch with id {hatch_id} not found or does not belong to user {user_id}",
                )

            # 更新当前默认 hatch（如果存在）
            if current_default and current_default.id != hatch_id:
                current_default.is_default = False
                success, _ = await self.set_hatch(current_default)
                if not success:
                    return (
                        False,
                        f"Failed to update current default hatch {current_default.id}",
                    )

            # 设置新的默认 hatch
            new_default.is_default = True
            success, _ = await self.set_hatch(new_default)
            if not success:
                return False, f"Failed to set hatch {hatch_id} as default"

            return (
                True,
                f"Successfully set hatch {hatch_id} as default for user {user_id}",
            )
        except Exception as e:
            print(f"Error setting default hatch: {e}")
            return False, f"An error occurred: {str(e)}"
