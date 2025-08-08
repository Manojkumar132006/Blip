"""
Calendar integration service
"""
from typing import Dict
import ics

class CalendarService:
    @staticmethod
    def spark_to_ics(spark, calendar: ics.Calendar = None) -> str:
        event = ics.Event()
        event.name = spark.name
        event.begin = spark.start_time
        event.end = spark.end_time
        event.description = spark.description or ""
        if calendar is None:
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
    # def has_spark_conflict(user_calendar: str, spark) -> bool:
    #     import ics
    #     from datetime import datetime, timezone
    #     if not user_calendar:
    #         return False

    #     calendar = ics.Calendar(user_calendar)
    #     for event in calendar.events:
    #         # Convert event begin and end to UTC aware datetime objects
    #         if isinstance(event.begin, datetime) and event.begin.tzinfo is None:
    #             event_begin = event.begin.replace(tzinfo=timezone.utc)
    #         else:
    #             event_begin = event.begin
                
    #         if isinstance(event.end, datetime) and event.end.tzinfo is None:
    #             event_end = event.end.replace(tzinfo=timezone.utc)
    #         else:
    #             event_end = event.end
            
    #         spark_start = spark.start_time
    #         spark_end = spark.end_time

    #         # Compare the datetimes directly
    #         if spark_start < event_end and spark_end > event_begin:
    #             return True

    #     return False

    @staticmethod
    def routine_to_ics(routine, calendar: ics.Calendar = None) -> str:
        # Create recurring event
        event = ics.Event()
        event.name = routine.name
        event.begin = f"2025-01-01T{routine.start_time}"
        event.end = f"2025-01-01T{routine.end_time}"
        event.description = routine.description or ""
        event.make_all_day()
        # Add recurrence rule (simplified)
        event.rrule = f"FREQ=DAILY;UNTIL=20260101T000000"
        if calendar is None:
            calendar = ics.Calendar()
        calendar.events.add(event)
        return str(calendar)
