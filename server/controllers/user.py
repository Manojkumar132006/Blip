"""
User Controller - Handles all business logic for User model
"""
from typing import List, Optional
from models.user import User
from config.database import users as users_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class UserController:
    @staticmethod
    async def get_current_user_profile(user_id: str) -> Optional[User]:
        """Get current user profile by ID"""
        try:
            user = await users_collection.find_one({"_id": ObjectId(user_id)})
            if not user:
                return None
            # Convert ObjectId to string for JSON serialization
            user["_id"] = str(user["_id"])
            return User(**user)
        except Exception as e:
            logger.error(f"Error fetching user profile: {str(e)}")
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def list_users() -> List[User]:
        """List all users"""
        try:
            cursor = users_collection.find()
            users = cursor.limit(100)
            # Convert ObjectId to string for JSON serialization
            for user in users:
                user["_id"] = str(user["_id"])
            return [User(**user) for user in users]
        except Exception as e:
            logger.error(f"Error listing users: {str(e)}")
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def create_user(user_data: dict) -> User:
        """Create a new user"""
        try:
            # Remove _id if present in input
            user_data.pop('_id', None)
            result = await users_collection.insert_one(user_data)
            user_data["_id"] = str(result.inserted_id)
            return User(**user_data)
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise Exception(f"Failed to create user: {str(e)}")

    @staticmethod
    async def update_user(user_id: str, user_data: dict) -> Optional[User]:
        """Update an existing user"""
        try:
            user_data.pop('_id', None)  # Ensure _id is not updated
            result = await users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": user_data}
            )
            if result.matched_count == 0:
                return None
            
            updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
            updated_user["_id"] = str(updated_user["_id"])
            return User(**updated_user)
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            raise Exception(f"Failed to update user: {str(e)}")

    @staticmethod
    async def delete_user(user_id: str) -> bool:
        """Delete a user"""
        try:
            result = await users_collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            raise Exception(f"Failed to delete user: {str(e)}")
