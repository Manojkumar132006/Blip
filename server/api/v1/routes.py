"""
Main API v1 Router
"""
from fastapi import APIRouter
from api.v1.endpoints import clusters, groups, sparks, routines, users, ui

api_router = APIRouter(prefix="/v1")

api_router.include_router(clusters.router, prefix="/clusters", tags=["clusters"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(sparks.router, prefix="/sparks", tags=["sparks"])
api_router.include_router(routines.router, prefix="/routines", tags=["routines"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(ui.router, tags=["ui"])  # /api/v1/ui
