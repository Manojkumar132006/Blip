"""
Clusters API - CRUD
"""
from fastapi import APIRouter, HTTPException
from models.cluster import Cluster
from controllers import ClusterController
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Cluster])
async def list_clusters():
    try:
        clusters = await ClusterController.list_clusters()
        return clusters
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{cluster_id}", response_model=Cluster)
async def get_cluster(cluster_id: str):
    try:
        cluster = await ClusterController.get_cluster(cluster_id)
        if not cluster:
            raise HTTPException(status_code=404, detail="Cluster not found")
        return cluster
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/", response_model=Cluster)
async def create_cluster(cluster: Cluster):
    try:
        cluster_dict = cluster.dict(by_alias=True)
        created_cluster = await ClusterController.create_cluster(cluster_dict)
        return created_cluster
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create cluster: {str(e)}")
