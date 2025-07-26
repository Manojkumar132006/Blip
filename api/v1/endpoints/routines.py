"""
Routines API - CRUD
"""
from fastapi import APIRouter, HTTPException
from models.routine import Routine
from controllers import RoutineController
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Routine])
async def list_routines():
    try:
        routines = await RoutineController.list_routines()
        return routines
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{routine_id}", response_model=Routine)
async def get_routine(routine_id: str):
    try:
        routine = await RoutineController.get_routine(routine_id)
        if not routine:
            raise HTTPException(status_code=404, detail="Routine not found")
        return routine
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/", response_model=Routine)
async def create_routine(routine: Routine):
    try:
        routine_dict = routine.dict(by_alias=True)
        created_routine = await RoutineController.create_routine(routine_dict)
        return created_routine
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create routine: {str(e)}")
