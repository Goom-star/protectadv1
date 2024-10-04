from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from routes.users import router as user_router
from routes.tasks import router as task_router  # Import the tasks router
from database import connect_db, disconnect_db
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost:3000",  # Allow requests from your React frontend
    "http://127.0.0.1:3000"   # Allow requests from the localhost (alternate IP)
]

# Allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api")  # Include the user router
app.include_router(task_router, prefix="/api")  # Include the task router

@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()
    