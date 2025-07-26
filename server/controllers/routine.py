"""
Routine Controller - Handles all business logic for Routine model
"""
from typing import List, Optional
from models.routine import Routine
from config.database import routines as routines_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class RoutineController:
    @staticmethod
    async def list_routines() -> List[Routine]:
        """List all routines"""
        try:
            cursor = routines_collection.find()
            routines = await cursor.to_list(length=100)
            # Convert ObjectId to string for JSON serialization
            for routine in routines:
                routine["_id"] = str(routine["_id"])
            return [Routine(**routine) for routine in routines]
        except Exception as e:
            logger.error(f"Error listing routines: {str(e)}")
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def get_routine(routine_id: str) -> Optional[Routine]:
        """Get a specific routine by ID"""
        try:
            routine = await routines_collection.find_one({"_id": ObjectId(routine_id)})
            if not routine:
                return None
            routine["_id"] = str(routine["_id"])
            return Routine(**routine)
        except Exception as e:
            logger.error(f"Error fetching routine: {str(e)}")
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def create_routine(routine_data: dict) -> Routine:
        """Create a new routine"""
        try:
            # Remove _id if present in input
            routine_data.pop('_id', None)
            result = await routines_collection.insert_one(routine_data)
            routine_data["_id"] = str(result.inserted_id)
            return Routine(**routine_data)
        except Exception as e:
            logger.error(f"Error creating routine: {str(e)}")
            raise Exception(f"Failed to create routine: {str(e)}")

    @staticmethod
    async def update_routine(routine_id: str, routine_data: dict) -> Optional[Routine]:
        """Update an existing routine"""
        try:
            routine_data.pop('_id', None)  # Ensure _id is not updated
            result = await routines_collection.update_one(
                {"_id": ObjectId(routine_id)},
                {"$set": routine_data}
            )
            if result.matched_count == 0:
                return None
            
            updated_routine = await routines_collection.find_one({"_id": ObjectId(routine_id)})
            updated_routine["_id"] = str(updated_routine["_id"])
            return Routine(**updated_routine)
        except Exception as e:
            logger.error(f"Error updating routine: {str(e)}")
            raise Exception(f"Failed to update routine: {str(e)}")

    @staticmethod
    async def delete_routine(routine_id: str) -> bool:
        """Delete a routine"""
        try:
            result = await routines_collection.delete_one({"_id": ObjectId(routine_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting routine: {str(e)}")
            raise Exception(f"Failed to delete routine: {str(e)}")
