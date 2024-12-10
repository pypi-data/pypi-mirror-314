from typing import Union
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import firestore

load_dotenv()


class FirestoreBase:
    def __init__(self, collection_name: str):
        google_service_account_key_path = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS_FOR_FASTAPI",
            "/app/keys/scoop-386004-d22d99a7afd9.json",
        )
        credentials = service_account.Credentials.from_service_account_file(
            google_service_account_key_path,
            scopes=["https://www.googleapis.com/auth/datastore"],
        )

        self.db = firestore.Client(credentials=credentials)
        self.collection = self.db.collection(collection_name)
