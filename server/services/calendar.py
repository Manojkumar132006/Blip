"""
Calendar integration service
"""
from typing import Dict
import ics

class CalendarService:
    @staticmethod
    def spark_to_ics(spark) -> str:
        event = ics.Event()
        event.name = spark.name
        event.begin = spark.start_time
        event.end = spark.end_time
        event.description = spark.description or ""
        calendar = ics.Calendar()
        calendar.events.add(event)
        return str(calendar)

    @staticmethod
    def cluster_to_ics(cluster) -> str:
        return cluster.calendar

    @staticmethod
    def group_to_ics(group) -> str:
        return group.calendar

    @staticmethod
    def user_to_ics(user) -> str:
        return user.calendar

    @staticmethod
    async def update_cluster_calendar_with_spark(cluster, spark) -> None:
        from config.database import clusters as clusters_collection
        from bson import ObjectId

        spark_calendar = CalendarService.spark_to_ics(spark)
        cluster_calendar = cluster.calendar if cluster.calendar else ""
        cluster_calendar += spark_calendar

        await clusters_collection.update_one(
            {"_id": ObjectId(cluster._id)},
            {"$set": {"calendar": cluster_calendar}}
        )

    @staticmethod
    async def update_group_calendar_with_spark(group, spark) -> None:
        from config.database import groups as groups_collection
        from bson import ObjectId

        spark_calendar = CalendarService.spark_to_ics(spark)
        group_calendar = group.calendar if group.calendar else ""
        group_calendar += spark_calendar

        await groups_collection.update_one(
            {"_id": ObjectId(group._id)},
            {"$set": {"calendar": group_calendar}}
        )

    @staticmethod
    async def update_cluster_calendar_with_routine(cluster, routine) -> None:
        from config.database import clusters as clusters_collection
        from bson import ObjectId

        routine_calendar = CalendarService.routine_to_ics(routine)
        cluster_calendar = cluster.calendar if cluster.calendar else ""
        cluster_calendar += routine_calendar

        await clusters_collection.update_one(
            {"_id": ObjectId(cluster._id)},
            {"$set": {"calendar": cluster_calendar}}
        )

    @staticmethod
    async def update_group_calendar_with_routine(group, routine) -> None:
        from config.database import groups as groups_collection
        from bson import ObjectId

        routine_calendar = CalendarService.routine_to_ics(routine)
        group_calendar = group.calendar if group.calendar else ""
        group_calendar += routine_calendar

        await groups_collection.update_one(
            {"_id": ObjectId(group._id)},
            {"$set": {"calendar": group_calendar}}
        )

    @staticmethod
    async def update_user_calendar_with_spark(user, spark) -> None:
        from config.database import users as users_collection
        from bson import ObjectId

        spark_calendar = CalendarService.spark_to_ics(spark)
        user_calendar = user.calendar if user.calendar else ""
        user_calendar += spark_calendar

        await users_collection.update_one(
            {"_id": ObjectId(user._id)},
            {"$set": {"calendar": user_calendar}}
        )

    @staticmethod
    def routine_to_ics(routine) -> str:
        # Create recurring event
        event = ics.Event()
        event.name = routine.name
        event.begin = f"2025-01-01T{routine.start_time}"
        event.end = f"2025-01-01T{routine.end_time}"
        event.description = routine.description or ""
        event.make_all_day()
        # Add recurrence rule (simplified)
        event.rrule = f"FREQ=DAILY;UNTIL=20260101T000000"
        calendar = ics.Calendar()
        calendar.events.add(event)
        return str(calendar)
