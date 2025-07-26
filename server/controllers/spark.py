"""
Spark Controller - Handles all business logic for Spark model
"""
from typing import List, Optional
from models.spark import Spark
from config.database import sparks as sparks_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class SparkController:
    @staticmethod
    async def list_sparks() -> List[Spark]:
        """List all sparks"""
        try:
            cursor = sparks_collection.find()
            sparks = await cursor.to_list(length=100)
            # Convert ObjectId to string for JSON serialization
            for spark in sparks:
                spark["_id"] = str(spark["_id"])
            return [Spark(**spark) for spark in sparks]
        except Exception as e:
            logger.error(f"Error listing sparks: {str(e)}")
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def get_spark(spark_id: str) -> Optional[Spark]:
        """Get a specific spark by ID"""
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
        """Create a new spark"""
        try:
            # Remove _id if present in input
            spark_data.pop('_id', None)
            result = await sparks_collection.insert_one(spark_data)
            spark_data["_id"] = str(result.inserted_id)
            return Spark(**spark_data)
        except Exception as e:
            logger.error(f"Error creating spark: {str(e)}")
            raise Exception(f"Failed to create spark: {str(e)}")

    @staticmethod
    async def update_spark(spark_id: str, spark_data: dict) -> Optional[Spark]:
        """Update an existing spark"""
        try:
            spark_data.pop('_id', None)  # Ensure _id is not updated
            result = await sparks_collection.update_one(
                {"_id": ObjectId(spark_id)},
                {"$set": spark_data}
            )
            if result.matched_count == 0:
                return None
            
            updated_spark = await sparks_collection.find_one({"_id": ObjectId(spark_id)})
            updated_spark["_id"] = str(updated_spark["_id"])
            return Spark(**updated_spark)
        except Exception as e:
            logger.error(f"Error updating spark: {str(e)}")
            raise Exception(f"Failed to update spark: {str(e)}")

    @staticmethod
    async def delete_spark(spark_id: str) -> bool:
        """Delete a spark"""
        try:
            result = await sparks_collection.delete_one({"_id": ObjectId(spark_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting spark: {str(e)}")
            raise Exception(f"Failed to delete spark: {str(e)}")
