"""
Routine Controller - Enhanced with recurrence and state
"""
from typing import List, Optional
from models.routine import Routine
from config.database import routines as routines_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class RoutineController:
    STATES = ["active", "paused", "completed", "overdue", "cancelled"]
    STEP_STATES = ["pending", "in_progress", "completed", "skipped", "failed"]

    @staticmethod
    async def list_routines() -> List[Routine]:
        try:
            cursor = routines_collection.find()
            routines = cursor.limit(100)
            for routine in routines:
                routine["_id"] = str(routine["_id"])
            return [Routine(**routine) for routine in routines]
        except Exception as e:
            logger.error(f"Error listing routines: {str(e)}")
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def get_routine(routine_id: str) -> Optional[Routine]:
        try:
            routine = await Routine.get(routine_id)
            return routine
        except Exception as e:
            logger.error(f"Error fetching routine: {str(e)}")
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def create_routine(routine_data: dict) -> Routine:
        try:
            routine_data.pop('_id', None)
            routine_data["status"] = "active"
            routine = Routine(**routine_data)
            await routine.save()

            # Fetch the cluster and group associated with the routine
            # Assuming routine_data contains cluster_id and group_id
            from controllers.cluster import ClusterController
            from controllers.group import GroupController
            cluster = await ClusterController.get_cluster(routine_data["cluster"])
            group = await GroupController.get_group(routine_data["group"])

            # Generate updated calendar data
            from services.calendar import CalendarService
            # Generate routine calendar event
            # Generate routine calendar event and update calendars using CalendarService
            routine = Routine(**routine_data)
            await CalendarService.update_cluster_calendar_with_routine(cluster, routine)
            await CalendarService.update_group_calendar_with_routine(group, routine)

            return Routine(**routine_data)
        except Exception as e:
            logger.error(f"Error creating routine: {str(e)}")
            raise Exception(f"Failed to create routine: {str(e)}")

    @staticmethod
    async def update_routine(routine_id: str, routine_data: dict) -> Optional[Routine]:
        try:
            routine = await Routine.get(routine_id)
            if not routine:
                return None

            # Update the routine object with the new data
            for key, value in routine_data.items():
                setattr(routine, key, value)

            await routine.update()
            return routine
        except Exception as e:
            logger.error(f"Error updating routine: {str(e)}")
            raise Exception(f"Failed to update routine: {str(e)}")

    @staticmethod
    async def delete_routine(routine_id: str) -> bool:
        try:
            routine = await Routine.get(routine_id)
            if not routine:
                return False
            deleted_count = await routine.delete()
            return deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting routine: {str(e)}")
            raise Exception(f"Failed to delete routine: {str(e)}")