"""
Groups API - CRUD
"""
from fastapi import APIRouter, HTTPException, Request
from models.group import Group
from controllers.group import GroupController
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Group])
async def list_groups():
    try:
        return await GroupController.list_groups()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{group_id}", response_model=Group)
async def get_group(group_id: str):
    try:
        group = await GroupController.get_group(group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        return group
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/", response_model=Group)
async def create_group(request: Request):
    """Create a new group"""
    try:
        group_data = await request.json()
        return await GroupController.create_group(group_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/{group_id}", response_model=Group)
async def update_group(group_id: str, request: Request):
    """Update an existing group"""
    try:
        group_data = await request.json()
        updated_group = await GroupController.update_group(group_id, group_data)
        if not updated_group:
            raise HTTPException(status_code=404, detail="Group not found")
        return updated_group
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/{group_id}")
async def delete_group(group_id: str):
    """Delete a group"""
    try:
        deleted = await GroupController.delete_group(group_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Group not found")
        return {"detail": "Group deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
