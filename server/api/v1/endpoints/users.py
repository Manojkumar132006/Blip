"""
Users API - CRUD
"""
from fastapi import APIRouter, HTTPException, Depends
from models.user import User
from utils.auth import get_current_user
from config.database import users as users_collection
from typing import List

router = APIRouter()

@router.get("/me", response_model=User)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    try:
        user = await users_collection.find_one({"_id": current_user.user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/", response_model=List[User])
async def list_users():
    try:
        cursor = users_collection.find()
        users = await cursor.to_list(length=100)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
