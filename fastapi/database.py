from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import MetaData
from databases import Database


POSTGRES_USER = "temp"
POSTGRES_PASSWORD = "temp"
POSTGRES_DB = "advcompro"
POSTGRES_HOST = "db"


DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'

# Create an async engine to connect to the PostgreSQL database using SQLAlchemy
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Metadata and Base model declaration
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Create an async session factory for handling database transactions using SQLAlchemy
async_session = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Dependency to get an async database session using SQLAlchemy
async def get_db():
    async with async_session() as session:
        yield session

database = Database(DATABASE_URL)


async def connect_db():
   await database.connect()
   print("Database connected")


async def disconnect_db():
   await database.disconnect()
   print("Database disconnected")


# Function to insert a new user into the users table
async def insert_user(username: str, password_hash: str, email: str):
   query = """
   INSERT INTO users (username, password_hash, email)
   VALUES (:username, :password_hash, :email)
   RETURNING user_id, username, password_hash, email, created_at
   """
   values = {"username": username, "password_hash": password_hash, "email": email}
   return await database.fetch_one(query=query, values=values)


# Function to select a user by user_id from the users table
async def get_user(username: str):
   query = "SELECT * FROM users WHERE username = :username"
   return await database.fetch_one(query=query, values={"username": username})


# Function to select a user by email from the users table
async def get_user_by_email(email: str,password_hash:str):
   query = "SELECT * FROM users WHERE email = :email and password_hash = :password_hash"
   return await database.fetch_one(query=query, values={"email": email,"password_hash": password_hash})


# Function to update a user in the users table
async def update_user(user_id: int, username: str, password_hash: str, email: str):
   query = """
   UPDATE users
   SET username = :username, password_hash = :password_hash, email = :email
   WHERE user_id = :user_id
   RETURNING user_id, username, password_hash, email, created_at
   """
   values = {"user_id": user_id, "username": username, "password_hash": password_hash, "email": email}
   return await database.fetch_one(query=query, values=values)


# Function to delete a user from the users table
async def delete_user(user_id: int):
   query = "DELETE FROM users WHERE user_id = :user_id RETURNING *"
   return await database.fetch_one(query=query, values={"user_id": user_id})

# CRUD Operations for tasks

async def insert_task(title: str, description: str, due_date: str, status: str, is_important: bool):
    query = """
    INSERT INTO tasks (title, description, due_date, status, is_important)
    VALUES (:title, :description, :due_date, :status, :is_important)
    RETURNING task_id, user_id, title, description, due_date, status, is_important, created_at
    """
    values = {"title": title, "description": description, "due_date": due_date, "status": status, "is_important": is_important}
    return await database.fetch_one(query=query, values=values)

async def get_tasks_by_user(user_id: int):
    query = """
    SELECT task_id, user_id, title, description, due_date, status, is_important, created_at
    FROM tasks
    WHERE user_id = :user_id
    """
    return await database.fetch_all(query=query, values={"user_id": user_id})

async def update_task(task_id: int, title: str, description: str, due_date: str, status: str, is_important: bool):
    query = """
    UPDATE tasks
    SET title = :title, description = :description, due_date = :due_date, status = :status, is_important = :is_important
    WHERE task_id = :task_id
    RETURNING task_id, user_id, title, description, due_date, status, is_important, created_at
    """
    values = {"task_id": task_id, "title": title, "description": description, "due_date": due_date, "status": status, "is_important": is_important}
    return await database.fetch_one(query=query, values=values)

async def delete_task(task_id: int):
    query = "DELETE FROM tasks WHERE task_id = :task_id RETURNING *"
    return await database.fetch_one(query=query, values={"task_id": task_id})