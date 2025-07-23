"""
Sparks API - CRUD
"""
from fastapi import APIRouter, HTTPException
from models.spark import Spark
from config.database import sparks as sparks_collection
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Spark])
async def list_sparks():
    try:
        cursor = sparks_collection.find()
        sparks = await cursor.to_list(length=100)
        return sparks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/", response_model=Spark)
async def create_spark(spark: Spark):
    try:
        spark_dict = spark.dict(by_alias=True)
        result = await sparks_collection.insert_one(spark_dict)
        # Emit via Socket.IO (placeholder)
        return spark
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create spark: {str(e)}")
