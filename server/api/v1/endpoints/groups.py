"""
Groups API - CRUD
"""
from fastapi import APIRouter, HTTPException
from models.group import Group
from controllers import GroupController
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Group])
async def list_groups():
    try:
        groups = await GroupController.list_groups()
        return groups
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
async def create_group(group: Group):
    try:
        group_dict = group.dict(by_alias=True)
        created_group = await GroupController.create_group(group_dict)
        return created_group
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create group: {str(e)}")
