"""
Blip Backend Entry Point
FastAPI + Socket.IO integrated server
"""
import os
import socketio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api.routes import router as api_router
from sockets.manager import sio

load_dotenv()

# Initialize FastAPI
app = FastAPI(title="Blip API", version="1.0.0")

# CORS - restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API router
app.include_router(api_router, prefix="/api")

# Attach Socket.IO middleware
app.mount("/", socketio.ASGIApp(sio))

@app.get("/")
def root():
    return {"message": "Welcome to Blip — Real-time, privacy-first social networking"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
