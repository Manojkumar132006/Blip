"""
Sparks API - CRUD
"""
from fastapi import APIRouter, HTTPException
from models.spark import Spark
from controllers import SparkController
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Spark])
async def list_sparks():
    try:
        sparks = await SparkController.list_sparks()
        return sparks
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
async def create_spark(spark: Spark):
    try:
        spark_dict = spark.dict(by_alias=True)
        created_spark = await SparkController.create_spark(spark_dict)
        return created_spark
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create spark: {str(e)}")
