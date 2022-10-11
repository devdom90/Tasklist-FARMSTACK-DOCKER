from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.middleware.cors import CORSMiddleware
from backend.db import user_collection
#-----IMPORT DATABASE MODELS-----
from backend.models import (
    NewTask,
    Task,
    User
)
#-----IMPORT CRUD FUNCTIONS-----
from backend.crud import (
    creating_task,
    fetch_tasks_by_user,
    create_user,
    updating_task,
    deleted_task
)


#-----INITIALIZE APPLICATION-----
app = FastAPI(
    title="Taski dein Taskmanager",
    description="Taskmanager Application with React.JS Frontend and FastAPI and MongoDB for the Backend. Application Authentication and Authorization with JWT Login",
    version="0.0.1",
    license="MIT"
)

#-----ADDING CORS MIDDLEWARE FOR DIFFERENT PLATFORMS-----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

SECRET = "secret-password"
manager = LoginManager(SECRET, "/login")

@manager.user_loader()
async def query_user(username):
    document = await user_collection.find_one({"username": username})
    return document


#-----HANDLE LOGIN AND GENERATE ACCESS_TOKEN IF LOGIN IS SUCCESSFUL-----
@app.post("/login")
async def login(data: OAuth2PasswordRequestForm= Depends()):
    username = data.username
    password = data.password    
    user = await query_user(username)
#-----HANDLE LOGIN EXCEPTIONS----    
    if not user:
        raise InvalidCredentialsException
    elif password != user["password"]:
        raise InvalidCredentialsException    
#-----GENERATE ACCESS_TOKEN-----    
    JWT_token = manager.create_access_token(data={"sub": username})
    return {"access_token": JWT_token}
    
#-----REGISTER ENDPOINT-----    
@app.post("/register")
async def new_user(user: User):
    new_user = await create_user(user)
    return new_user
    
#-----CREATE ENDPOINT FOR TASK-----    
@app.post("/create_new_task")
async def new_task(task: NewTask, user=Depends(manager)):
    await creating_task(task, user)
    return task


@app.get("/get_all_tasks/")
async def get_all_tasks(user=Depends(manager)):
    tasks = await fetch_tasks_by_user(user)
    return tasks


@app.put("/update_task/{id}")
async def update(id: str, user=Depends(manager)):
    item = await updating_task(id, user)
    return Task(**item)


    
@app.delete("/delete_task_by_user/{id}")
async def delete_task(id, user=Depends(manager)):
    item = await deleted_task(id,user)
    return Task(**item)
    