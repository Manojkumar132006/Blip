from typing import List
from models.spark import Spark
from models.routine import Routine
from models.user import User
from models.cluster import Cluster
from models.group import Group
from services.calendar import CalendarService
import ics

class ItemManager:
    async def create_spark(
        self,
        name: str,
        description: str,
        start_time: str,
        end_time: str,
        cluster_ids: List[str] = None,
        group_ids: List[str] = None,
        user_ids: List[str] = None,
    ) -> Spark:
        """Creates a new spark and associates it with clusters, groups, and users."""
        spark = Spark(
            name=name,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        await spark.save()

        if cluster_ids:
            for cluster_id in cluster_ids:
                cluster = await self._get_cluster(cluster_id)
                await self.add_spark_to_cluster(cluster, spark)

        if group_ids:
            for group_id in group_ids:
                group = await self._get_group(group_id)
                await self.add_spark_to_group(group, spark)

        if user_ids:
            for user_id in user_ids:
                user = await self._get_user(user_id)
                await self.add_spark_to_user(user, spark)

        return spark

    async def create_routine(
        self,
        name: str,
        description: str,
        start_time: str,
        end_time: str,
        cluster_ids: List[str] = None,
        group_ids: List[str] = None,
        user_ids: List[str] = None,
    ) -> Routine:
        """Creates a new routine and associates it with clusters, groups, and users."""
        routine = Routine(
            name=name,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        await routine.save()

        if cluster_ids:
            for cluster_id in cluster_ids:
                cluster = await self._get_cluster(cluster_id)
                await self.add_routine_to_cluster(cluster, routine)

        if group_ids:
            for group_id in group_ids:
                group = await self._get_group(group_id)
                await self.add_routine_to_group(group, routine)

        if user_ids:
            for user_id in user_ids:
                user = await self._get_user(user_id)
                await self.add_routine_to_user(user, routine)

        return routine

    async def add_spark_to_cluster(self, cluster: Cluster, spark: Spark) -> None:
        """Adds a spark to a cluster and updates the cluster's calendar."""
        await CalendarService.update_cluster_calendar_with_spark(cluster, spark)

    async def add_spark_to_group(self, group: Group, spark: Spark) -> None:
        """Adds a spark to a group and updates the group's calendar."""
        await CalendarService.update_group_calendar_with_spark(group, spark)

    async def add_spark_to_user(self, user: User, spark: Spark) -> None:
        """Adds a spark to a user and updates the user's calendar."""
        await CalendarService.update_user_calendar_with_spark(user, spark)

    async def add_routine_to_cluster(self, cluster: Cluster, routine: Routine) -> None:
        """Adds a routine to a cluster and updates the cluster's calendar."""
        await CalendarService.update_cluster_calendar_with_routine(cluster, routine)

    async def add_routine_to_group(self, group: Group, routine: Routine) -> None:
        """Adds a routine to a group and updates the group's calendar."""
        await CalendarService.update_group_calendar_with_routine(group, routine)

    async def add_routine_to_user(self, user: User, routine: Routine) -> None:
        """Adds a routine to a user and updates the user's calendar."""
        # TODO: Implement user calendar updates for routines
        pass

    async def _get_cluster(self, cluster_id: str) -> Cluster:
        """Retrieves a cluster by ID. (Placeholder)"""
        # TODO: Implement cluster retrieval from database
        return Cluster(_id=cluster_id, name="Sample Cluster")

    async def _get_group(self, group_id: str) -> Group:
        """Retrieves a group by ID. (Placeholder)"""
        # TODO: Implement group retrieval from database
        return Group(_id=group_id, name="Sample Group")

    async def _get_user(self, user_id: str) -> User:
        """Retrieves a user by ID. (Placeholder)"""
        # TODO: Implement user retrieval from database
        return User(_id=user_id, name="Sample User", calendar="")

