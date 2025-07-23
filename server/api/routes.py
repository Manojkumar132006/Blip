"""
Main API Router (Legacy for backward compatibility)
"""
from fastapi import APIRouter
from api.v1.routes import api_router as v1_router

router = APIRouter()

# Redirect root API to v1
router.include_router(v1_router)
