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
