from functools import wraps
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Header
from api.v1.routes import api_router as v1_router
import os
# Assume you have a way to validate API keys (e.g., against a database)
# For demonstration, let's use a simple in-memory set of valid keys
VALID_API_KEYS = {os.getenv("API_KEY")}  # Replace with your actual keys and storage

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return True

router = APIRouter(dependencies=[Depends(verify_api_key)])
router.include_router(v1_router)