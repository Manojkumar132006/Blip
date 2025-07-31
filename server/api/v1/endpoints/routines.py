"""
Routines API - CRUD
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from models.routine import Routine
from controllers.routine import RoutineController
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Routine])
async def list_routines():
    try:
        return await RoutineController.list_routines()
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
async def create_routine(request: Request):
    """Create a new routine"""
    try:
        routine_data = await request.json()
        return await RoutineController.create_routine(routine_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/{routine_id}", response_model=Routine)
async def update_routine(routine_id: str, request: Request):
    """Update an existing routine"""
    try:
        routine_data = await request.json()
        updated_routine = await RoutineController.update_routine(routine_id, routine_data)
        if not updated_routine:
            raise HTTPException(status_code=404, detail="Routine not found")
        return updated_routine
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/{routine_id}")
async def delete_routine(routine_id: str):
    """Delete a routine"""
    try:
        deleted = await RoutineController.delete_routine(routine_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Routine not found")
        return {"detail": "Routine deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
