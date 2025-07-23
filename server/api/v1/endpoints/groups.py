"""
Groups API - CRUD
"""
from fastapi import APIRouter, HTTPException
from models.group import Group
from config.database import groups as groups_collection
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Group])
async def list_groups():
    try:
        cursor = groups_collection.find()
        groups = await cursor.to_list(length=100)
        return groups
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/", response_model=Group)
async def create_group(group: Group):
    try:
        group_dict = group.dict(by_alias=True)
        result = await groups_collection.insert_one(group_dict)
        return group
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create group: {str(e)}")
