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

            if response.data:
                logger.info(
                    f"Total inserted data to {table_name}: {len(response.data)}"
                )

            return response
        except Exception as e:
            print(f"Error inserting into {table_name}: {e}")
            raise e

    def table(self, table_name: str) -> Any:
        return self.client.table(table_name)

    def fetch_all(self, table_name: str) -> List[Dict]:
        all_rows = []
        batch_size = 1000
        start = 0

        # logger.info()
        while True:
            end = start + batch_size - 1
            response = (
                self.client.table(table_name).select("*").range(start, end).execute()
            )
            all_rows.extend(response.data)

            if len(response.data) < batch_size:
                break

            start += batch_size

        return all_rows
