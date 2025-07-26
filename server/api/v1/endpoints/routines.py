"""
Routines API - CRUD
"""
from fastapi import APIRouter, HTTPException
from models.routine import Routine
from config.database import routines as routines_collection
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Routine])
async def list_routines():
    try:
        cursor = routines_collection.find()
        routines = await cursor.to_list(length=100)
        return routines
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/", response_model=Routine)
async def create_routine(routine: Routine):
    try:
        routine_dict = routine.dict(by_alias=True)
        result = await routines_collection.insert_one(routine_dict)
        return routine
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create routine: {str(e)}")
