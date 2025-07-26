"""
Users API - CRUD
"""
from fastapi import APIRouter, HTTPException, Depends
from models.user import User
from utils.auth import get_current_user
from controllers import UserController
from typing import List

router = APIRouter()

@router.get("/me", response_model=User)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    try:
        user = await UserController.get_current_user_profile(current_user.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/", response_model=List[User])
async def list_users():
    try:
        users = await UserController.list_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
