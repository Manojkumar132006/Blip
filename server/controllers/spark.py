"""
Spark Controller - Enhanced with state, triggers, and sync
"""
from typing import List, Optional
from models.spark import Spark
from config.database import sparks as sparks_collection
from bson import ObjectId
import logging
from services.sync import SyncService
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class SparkController:
    STATES = ["created", "scheduled", "active", "expired", "completed", "cancelled"]

    @staticmethod
    async def list_sparks() -> List[Spark]:
        try:
            cursor = sparks_collection.find()
            sparks = await cursor.to_list(length=100)
            for spark in sparks:
                spark["_id"] = str(spark["_id"])
                # Auto-expire
                if spark["end_time"] < datetime.now(timezone.utc).isoformat() and spark["status"] == "active":
                    spark["status"] = "expired"
                    await sparks_collection.update_one(
                        {"_id": ObjectId(spark["_id"])},
                        {"$set": {"status": "expired"}}
                    )
            return [Spark(**spark) for spark in sparks]
        except Exception as e:
            logger.error(f"Error listing sparks: {str(e)}")
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def get_spark(spark_id: str) -> Optional[Spark]:
        try:
            spark = await sparks_collection.find_one({"_id": ObjectId(spark_id)})
            if not spark:
                return None
            spark["_id"] = str(spark["_id"])
            return Spark(**spark)
        except Exception as e:
            logger.error(f"Error fetching spark: {str(e)}")
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def create_spark(spark_data: dict) -> Spark:
        try:
            spark_data.pop('_id', None)
            spark_data["status"] = "scheduled"
            result = await sparks_collection.insert_one(spark_data)
            spark_data["_id"] = str(result.inserted_id)
            # Sync
            await SyncService.push_local_changes()
            return Spark(**spark_data)
        except Exception as e:
            logger.error(f"Error creating spark: {str(e)}")
            raise Exception(f"Failed to create spark: {str(e)}")

    @staticmethod
    async def update_spark(spark_id: str, spark_data: dict) -> Optional[Spark]:
        try:
            spark_data.pop('_id', None)
            # Validate state transition
            current = await sparks_collection.find_one({"_id": ObjectId(spark_id)})
            if current and "status" in spark_data:
                if spark_data["status"] not in SparkController.STATES:
                    raise ValueError("Invalid status")
            result = await sparks_collection.update_one(
                {"_id": ObjectId(spark_id)},
                {"$set": spark_data}
            )
            if result.matched_count == 0:
                return None
            updated = await sparks_collection.find_one({"_id": ObjectId(spark_id)})
            updated["_id"] = str(updated["_id"])
            return Spark(**updated)
        except Exception as e:
            logger.error(f"Error updating spark: {str(e)}")
            raise Exception(f"Failed to update spark: {str(e)}")

    @staticmethod
    async def delete_spark(spark_id: str) -> bool:
        try:
            result = await sparks_collection.delete_one({"_id": ObjectId(spark_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting spark: {str(e)}")
            raise Exception(f"Failed to delete spark: {str(e)}")
