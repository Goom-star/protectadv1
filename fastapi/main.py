# # main.py

# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import sessionmaker
# from fastapi.middleware.cors import CORSMiddleware
# from .database import async_session, connect_db, disconnect_db
# from .users import create_user, login_user
# from .tasks import get_tasks_by_user, create_task
# from .schemas import UserCreate, UserLogin, TaskCreate

# # Create FastAPI instance
# app = FastAPI()

# # Allow CORS (Cross-Origin Resource Sharing) to connect frontend with backend
# origins = [
#     "http://localhost:3000",  # Frontend URL for local development
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Event handlers for database connection management
# @app.on_event("startup")
# async def startup():
#     await connect_db()

# @app.on_event("shutdown")
# async def shutdown():
#     await disconnect_db()

# # User registration endpoint
# @app.post("/api/users/create")
# async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(async_session)):
#     return await create_user(db, user)

# # User login endpoint
# @app.post("/api/users/login")
# async def login_user_endpoint(user: UserLogin, db: AsyncSession = Depends(async_session)):
#     db_user = await login_user(db, user)
#     if not db_user:
#         raise HTTPException(status_code=400, detail="Invalid username or password")
#     return db_user

# # Fetch tasks for a user by user_id
# @app.get("/api/tasks/{user_id}")
# async def get_user_tasks(user_id: int, db: AsyncSession = Depends(async_session)):
#     tasks = await get_tasks_by_user(db, user_id)
#     return {"tasks": tasks}

# # Create a new task
# @app.post("/api/tasks/create")
# async def create_task_endpoint(task: TaskCreate, db: AsyncSession = Depends(async_session)):
#     return await create_task(db, task)