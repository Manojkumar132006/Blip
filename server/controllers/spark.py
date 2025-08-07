```
"""
Spark Controller - Enhanced with state, triggers, and sync
"""
from typing import List, Optional
from models.spark import Spark
from config.database import sparks as sparks_collection
from bson import ObjectId
import logging
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
                spark["id"] = str(spark["_id"])
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
            spark = await Spark.get(spark_id)
            return spark
        except Exception as e:
            logger.error(f"Error fetching spark: {str(e)}")
            raise Exception(f"Database error: {str(e)}")


    @staticmethod
    async def create_spark(spark_data: dict) -> Spark:
        try:
            spark_data.pop('id', None)
            spark_data["status"] = "scheduled"
            spark = Spark(**spark_data)
            await spark.save()

            # Fetch the cluster and group associated with the spark
            # Assuming spark_data contains cluster_id and group_id
            from controllers.cluster import ClusterController
            from controllers.group import GroupController
            cluster = await ClusterController.get_cluster(spark_data["cluster"])
            group = await GroupController.get_group(spark_data["group"])

            # Generate updated calendar data
            from services.calendar import CalendarService
            # Generate spark calendar event and update calendars using CalendarService
            # Generate spark calendar event and check for conflicts
            spark = Spark(**spark_data)

            # Check for conflicts with user calendars
            # from controllers.user import UserController
            # for user_id in spark.members:
            #     user = await UserController.get_current_user_profile(user_id)
            #     if user:
            #         if CalendarService.has_spark_conflict(user.calendar, spark):
            #             raise ValueError(f"User {user.name} has a scheduling conflict.")

            await CalendarService.update_cluster_calendar_with_spark(cluster, spark)
            await CalendarService.update_group_calendar_with_spark(group, spark)

            return Spark(**spark_data)
        except Exception as e:
            logger.error(f"Error creating spark: {str(e)}")
            raise Exception(f"Failed to create spark: {str(e)}")

    @staticmethod
    async def update_spark(spark_id: str, spark_data: dict) -> Optional[Spark]:
        try:
            spark = await Spark.get(spark_id)
            if not spark:
                return None

            # Validate state transition
            if "status" in spark_data:
                if spark_data["status"] not in SparkController.STATES:
                    raise ValueError("Invalid status")

            # Update the spark object with the new data
            for key, value in spark_data.items():
                setattr(spark, key, value)

            await spark.update()

            # If the members list has been updated, update the user calendars
            #if "members" in spark_data:
            #    # Fetch the cluster and group associated with the spark
            #    # Assuming spark_data contains cluster_id and group_id
            #    from controllers.cluster import ClusterController
            #    from controllers.group import GroupController
            #    cluster = await ClusterController.get_cluster(updated["cluster"])
            #    group = await GroupController.get_group(updated["group"])

            #    # Generate updated calendar data
            #    from services.calendar import CalendarService
            #    cluster_calendar = CalendarService.cluster_to_ics(cluster)
            #    group_calendar = CalendarService.group_to_ics(group)

            #    # Update the calendar attributes
            #    from config.database import clusters as clusters_collection
            #    from config.database import groups as groups_collection
            #    from bson import ObjectId
            #    await clusters_collection.update_one(
            #        {"_id": ObjectId(cluster._id)},
            #        {"$set": {"calendar": cluster_calendar}}
            #    )
            #    await groups_collection.update_one(
            #        {"_id": ObjectId(group._id)},
            #        {"$set": {"calendar": group_calendar}}
            #    )

            #    # Update user calendars
            #    from controllers.user import UserController
            #    spark = Spark(**updated)
            #    # Update user calendars
            #    from controllers.user import UserController
            #    for user_id in spark_data["members"]:
            #        user = await UserController.get_current_user_profile(user_id)
            #        if user:
            #            await CalendarService.update_user_calendar_with_spark(user, spark)

            return spark
        except Exception as e:
            logger.error(f"Error updating spark: {str(e)}")
            raise Exception(f"Failed to update spark: {str(e)}")

    @staticmethod
    async def delete_spark(spark_id: str) -> bool:
        try:
            spark = await Spark.get(spark_id)
            if not spark:
                return False

            deleted_count = await spark.delete()
            return deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting spark: {str(e)}")
            raise Exception(f"Failed to delete spark: {str(e)}")

```