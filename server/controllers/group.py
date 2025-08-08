"""
Group Controller - Handles all business logic for Group model
"""
from typing import List, Optional
from models.group import Group
from config.database import groups as groups_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class GroupController:
    @staticmethod
    async def list_groups() -> List[Group]:
        """List all groups"""
        try:
            cursor = groups_collection.find()
            groups = await cursor.to_list(length=100)
            # Convert ObjectId to string for JSON serialization
            for group in groups:
                group["_id"] = str(group["_id"])
            return [Group(**group) for group in groups]
        except Exception as e:
            logger.error(f"Error listing groups: {str(e)}")
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def get_group(group_id: str) -> Optional[Group]:
        """Get a specific group by ID"""
        try:
            group = await Group.get(group_id)
            return group
        except Exception as e:
            logger.error(f"Error fetching group: {str(e)}")
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def create_group(group_data: dict) -> Group:
        """Create a new group"""
        try:
            # Remove _id if present in input
            group_data.pop('_id', None)
            group = Group(**group_data)
            await group.save()
            return group
        except Exception as e:
            logger.error(f"Error creating group: {str(e)}")
            raise Exception(f"Failed to create group: {str(e)}")

    @staticmethod
    async def update_group(group_id: str, group_data: dict) -> Optional[Group]:
        """Update an existing group"""
        try:
            group = await Group.get(group_id)
            if not group:
                return None

            # Update the group object with the new data
            for key, value in group_data.items():
                setattr(group, key, value)

            await group.update()
            return group
        except Exception as e:
            logger.error(f"Error updating group: {str(e)}")
            raise Exception(f"Failed to update group: {str(e)}")

    @staticmethod
    async def delete_group(group_id: str) -> bool:
        """Delete a group"""
        try:
            group = await Group.get(group_id)
            if not group:
                return False
            deleted_count = await group.delete()
            return deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting group: {str(e)}")
            raise Exception(f"Failed to delete group: {str(e)}")