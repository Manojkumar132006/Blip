"""
JWT Authentication Utilities
"""
import jwt
import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request
from pydantic import BaseModel
from config.database import db

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

class TokenData(BaseModel):
    user_id: str

def create_access_token(user_id: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return TokenData(user_id=user_id)
    except jwt.PyJWTError:
        return None

def get_current_user(token: str = Depends(lambda x: x.headers.get("authorization", "").replace("Bearer ", ""))):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

# For Socket.IO
async def authenticate_socket(sid, environ):
    query = environ.get("QUERY_STRING", "")
    if "token=" not in query:
        return False
    token = query.split("token=")[1].split("&")[0]
    user = verify_token(token)
    if not user:
        return False
    # Attach user to session
    sio = environ["sio"]
    sio.user_id = user.user_id
    return True
