"""
REST API Routes
"""
from fastapi import APIRouter, Depends
from utils.auth import get_current_user
from models import user, cluster, group, role, routine, spark

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}

# You can expand with full CRUD for each model
# Placeholder endpoints
@router.get("/me")
def get_profile(current_user: dict = Depends(get_current_user)):
    return {"user_id": current_user.user_id, "message": "Profile endpoint placeholder"}

@router.get("/clusters")
def list_clusters():
    return {"clusters": []}

@router.get("/groups")
def list_groups():
    return {"groups": []}

@router.get("/routines")
def list_routines():
    return {"routines": []}

@router.get("/sparks")
def list_sparks():
    return {"sparks": []}
