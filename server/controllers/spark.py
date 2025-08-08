"""
Spark Controller - Enhanced with state, triggers, and sync
"""
from typing import List, Optional
from models.spark import Spark
from config.database import sparks as sparks_collection
from bson import ObjectId
import logging
from datetime import datetime, timezone
from fastapi import HTTPException

# URL imports
import qrcode
from fastapi.responses import StreamingResponse
from io import BytesIO


logger = logging.getLogger(__name__)


class SparkController:
    STATES = ["created", "scheduled", "active",
              "expired", "completed", "cancelled"]

    @staticmethod
    async def list_sparks() -> List[Spark]:
        try:
            cursor = sparks_collection.find()
            sparks = cursor.limit(100)
            sparks = list(sparks)
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

            # Generate scan URL
            spark_id = spark_data["_id"]
            base_url = "https://yourfrontend.com/scan"
            scan_url = f"{base_url}?spark_id={spark_id}"
            spark_data["qr_url"] = scan_url

            await sparks_collection.update_one(
                {
                    "_id": ObjectId(spark_id)
                },
                {"$set": {"qr_url": scan_url}}
            )

            # Fetch the cluster and group associated with the spark
            # Assuming spark_data contains cluster_id and group_id
            from controllers.cluster import ClusterController
            from controllers.group import GroupController
            cluster = await ClusterController.get_cluster(spark_data["cluster"])
            group = await GroupController.get_group(spark_data["group"])

            # Generate updated calendar data
            from services.calendar import CalendarService
            # Generate spark calendar event and update calendars using CalendarService
            spark = Spark(**spark_data)
            await CalendarService.update_cluster_calendar_with_spark(cluster, spark)
            await CalendarService.update_group_calendar_with_spark(group, spark)

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

            # If the members list has been updated, update the user calendars
            if "members" in spark_data:
                # Fetch the cluster and group associated with the spark
                # Assuming spark_data contains cluster_id and group_id
                from controllers.cluster import ClusterController
                from controllers.group import GroupController
                cluster = await ClusterController.get_cluster(updated["cluster"])
                group = await GroupController.get_group(updated["group"])

                # Generate updated calendar data
                from services.calendar import CalendarService
                cluster_calendar = CalendarService.cluster_to_ics(cluster)
                group_calendar = CalendarService.group_to_ics(group)

                # Update the calendar attributes
                from config.database import clusters as clusters_collection
                from config.database import groups as groups_collection
                from bson import ObjectId
                await clusters_collection.update_one(
                    {"_id": ObjectId(cluster._id)},
                    {"$set": {"calendar": cluster_calendar}}
                )
                await groups_collection.update_one(
                    {"_id": ObjectId(group._id)},
                    {"$set": {"calendar": group_calendar}}
                )

                # Update user calendars
                from controllers.user import UserController
                spark = Spark(**updated)
                # Update user calendars
                from controllers.user import UserController
                for user_id in spark_data["members"]:
                    user = await UserController.get_current_user_profile(user_id)
                    if user:
                        await CalendarService.update_user_calendar_with_spark(user, spark)

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

    @staticmethod
    async def get_qr_for_spark(spark_id: str):
        try:
            spark = await sparks_collection.find_one({"_id": ObjectId(spark_id)})
            if not spark:
                raise HTTPException(status_code=404, detail="Spark not found")

            checkin_url = spark["checkin_url"]
            img = qrcode.make(checkin_url)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            return StreamingResponse(buffer, media_type="image/png")
        except Exception as e:
            logger.error(f"Error generating QR code: {str(e)}")
            raise Exception(f" Failed to generate QR code: {str(e)}")

    @staticmethod
    async def mark_user_attended(spark_id: str, user_id: str) -> Spark:
        try:
            spark = await sparks_collection.find_one({"_id": ObjectId(spark_id)})
            if not spark:
                raise HTTPException(status_code=404, detail="Spark not found")

            attended_users = spark.get("attended_users", [])
            if user_id in attended_users:
                return {"message": "User already marked as attended."}

            attended_users.append(user_id)
            await sparks_collection.update_one(
                {"_id": ObjectId(spark_id)},
                {"$set": {"attended_users": attended_users}}
            )

            return {"message": "User marked as attended.", "attended_users": attended_users}
        except Exception as e:
            logger.error(f"Error marking user attended: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Failed to mark user as attended")
