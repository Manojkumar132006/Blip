"""
Social sharing and invite management
"""
import uuid
import datetime
from typing import Optional
from server.models.spark import Spark
from server.controllers.spark import SparkController

class SocialService:
    def __init__(self):
        self.invites = {}

    def generate_invite(self, spark_id: str, expires_in_hours: int = 24) -> str:
        code = str(uuid.uuid4())[:8]
        self.invites[code] = {
            "spark_id": spark_id,
            "expires_at": datetime.now().timestamp() + expires_in_hours * 3600
        }
        return f"https://app.example.com/join/{code}"

    async def join_spark(self, invite_code: str, user_id: str) -> Optional[Spark]:
        if invite_code not in self.invites:
            return None
        invite = self.invites[invite_code]
        if invite["expires_at"] < datetime.now().timestamp():
            del self.invites[invite_code]
            return None
        
        spark = await SparkController.get_spark(invite["spark_id"])
        if spark.spots >= spark.total_spots:
            return None
        
        # Increment spots
        await SparkController.update_spark(invite["spark_id"], {"spots": spark.spots + 1})
        return spark
