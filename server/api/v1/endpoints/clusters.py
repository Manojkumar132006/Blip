"""
Clusters API - CRUD
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from models.cluster import Cluster
from controllers.cluster import ClusterController
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=List[Cluster])
async def list_clusters():
    try:
        return await ClusterController.list_clusters()
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
async def create_cluster(request: Request):
    """Create a new cluster"""
    try:
        cluster_data = await request.json()
        return await ClusterController.create_cluster(cluster_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/{cluster_id}", response_model=Cluster)
async def update_cluster(cluster_id: str, request: Request):
    """Update an existing cluster"""
    try:
        cluster_data = await request.json()
        updated_cluster = await ClusterController.update_cluster(cluster_id, cluster_data)
        if not updated_cluster:
            raise HTTPException(status_code=404, detail="Cluster not found")
        return updated_cluster
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/{cluster_id}")
async def delete_cluster(cluster_id: str):
    """Delete a cluster"""
    try:
        deleted = await ClusterController.delete_cluster(cluster_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Cluster not found")
        return {"detail": "Cluster deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
