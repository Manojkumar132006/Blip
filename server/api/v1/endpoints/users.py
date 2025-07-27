"""
Users API - CRUD
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from models.user import User
from utils.auth import get_current_user
from controllers.user import UserController
from typing import List, Optional

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

@router.post("/", response_model=User)
async def create_user(request: Request):
    """Create a new user"""
    try:
        user_data = await request.json()
        return await UserController.create_user(user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get a specific user by ID"""
    try:
        user = await UserController.get_current_user_profile(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, request: Request):
    """Update an existing user"""
    try:
        user_data = await request.json()
        updated_user = await UserController.update_user(user_id, user_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """Delete a user"""
    try:
        deleted = await UserController.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
@router.get("/", response_model=List[User])
async def list_users():
    try:
        return await UserController.list_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
