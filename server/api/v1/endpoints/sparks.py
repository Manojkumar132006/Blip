"""
Sparks API - CRUD
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from models.spark import Spark
from controllers.spark import SparkController
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Spark])
async def list_sparks():
    try:
        return await SparkController.list_sparks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{spark_id}", response_model=Spark)
async def get_spark(spark_id: str):
    try:
        spark = await SparkController.get_spark(spark_id)
        if not spark:
            raise HTTPException(status_code=404, detail="Spark not found")
        return spark
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/", response_model=Spark)
async def create_spark(request: Request):
    """Create a new spark"""
    try:
        spark_data = await request.json()
        return await SparkController.create_spark(spark_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/{spark_id}", response_model=Spark)
async def update_spark(spark_id: str, request: Request):
    """Update an existing spark"""
    try:
        spark_data = await request.json()
        updated_spark = await SparkController.update_spark(spark_id, spark_data)
        if not updated_spark:
            raise HTTPException(status_code=404, detail="Spark not found")
        return updated_spark
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/{spark_id}")
async def delete_spark(spark_id: str):
    """Delete a spark"""
    try:
        deleted = await SparkController.delete_spark(spark_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Spark not found")
        return {"detail": "Spark deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
