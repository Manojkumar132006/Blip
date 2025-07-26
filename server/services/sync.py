"""
Sync service for multi-device consistency
"""
import datetime
import asyncio
import hashlib
from typing import List
from models.spark import Spark
from models.routine import Routine

class SyncService:
    def __init__(self, api_client):
        self.api_client = api_client
        self.offline_queue = []
        self.sync_interval = 900  # 15 mins
        self.active = False

    def compute_hash(self, obj: dict) -> str:
        return hashlib.md5(str(sorted(obj.items())).encode()).hexdigest()

    async def push_local_changes(self):
        # Simulate sync with Supabase
        pass

    async def pull_remote_updates(self):
        # Simulate fetch from Supabase
        pass

    async def start_sync_loop(self):
        self.active = True
        while self.active:
            await self.push_local_changes()
            await self.pull_remote_updates()
            await asyncio.sleep(self.sync_interval)

    def queue_offline_action(self, action: dict):
        self.offline_queue.append({**action, "timestamp": datetime.now().isoformat()})
