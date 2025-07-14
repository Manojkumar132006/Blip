import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.ui import router as ui_router
from .db import MongoCluster

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    MongoCluster()

app.include_router(ui_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)