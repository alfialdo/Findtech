import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from supabase import Client, create_client

from src.logger import setup_logger

load_dotenv()
logger = setup_logger(__name__)


class SupabaseManager:
    def __init__(self) -> None:
        self.url: str = os.environ.get("SUPABASE_URL", "")
        self.key: str = os.environ.get("SUPABASE_KEY", "")

        if not self.url or not self.key:
            raise ValueError(
                "SUPABASE Credentials not initialized in environment vars!"
            )

        self.client: Client = create_client(self.url, self.key)

    def insert_bulk_from_dict(self, table_name: str, data: List[Dict[str, Any]]) -> Any:
        try:
            response = self.client.table(table_name).insert(data).execute()
            return response
        except Exception as e:
            print(f"Error inserting into {table_name}: {e}")
            raise e

    def table(self, table_name: str) -> Any:
        return self.client.table(table_name)
