"""
Event-driven trigger system for Sparks and Routines
"""
import asyncio
from datetime import datetime, timezone
import pytz
from typing import Callable, Dict, Any
from controllers.spark import SparkController
from controllers.routine import RoutineController

class TriggerService:
    def __init__(self):
        self.triggers: Dict[str, Callable] = {}
        self.active = False

    def register(self, event_type: str, callback: Callable):
        self.triggers[event_type] = callback

    async def check_time_triggers(self):
        """Check for time-based triggers (Sparks, Routines)"""
        now_utc = datetime.now(timezone.utc)
        
        # Check Sparks
        sparks = await SparkController.list_sparks()
        for spark in sparks:
            if spark.status == "scheduled" and spark.start_time <= now_utc.isoformat():
                await self.fire("spark:start", spark)

        # Check Routines (simplified daily for now)
        routines = await RoutineController.list_routines()
        for routine in routines:
            if routine.status == "active":
                # Parse time-only start_time
                start_time = datetime.fromisoformat(f"2025-01-01T{routine.start_time}")
                now_local = datetime.now(pytz.timezone("UTC"))  # TODO: user tz
                if start_time.hour == now_local.hour and start_time.minute == now_local.minute:
                    await self.fire("routine:start", routine)

    async def fire(self, event_type: str, payload: Any):
        if event_type in self.triggers:
            await self.triggers[event_type](payload)

    async def start(self):
        self.active = True
        while self.active:
            await self.check_time_triggers()
            await asyncio.sleep(60)  # Check every minute

    def stop(self):
        self.active = False
