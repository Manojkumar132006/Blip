"""
Clusters API - CRUD
"""
from fastapi import APIRouter, HTTPException
from models.cluster import Cluster
from config.database import clusters as clusters_collection
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Cluster])
async def list_clusters():
    try:
        cursor = clusters_collection.find()
        clusters = await cursor.to_list(length=100)
        return clusters
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{cluster_id}", response_model=Cluster)
async def get_cluster(cluster_id: str):
    try:
        cluster = await clusters_collection.find_one({"_id": cluster_id})
        if not cluster:
            raise HTTPException(status_code=404, detail="Cluster not found")
        return cluster
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/", response_model=Cluster)
async def create_cluster(cluster: Cluster):
    try:
        cluster_dict = cluster.dict(by_alias=True)
        result = await clusters_collection.insert_one(cluster_dict)
        return cluster
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create cluster: {str(e)}")
