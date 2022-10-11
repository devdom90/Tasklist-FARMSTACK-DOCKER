from bson import ObjectId                             #-----IMPORT ObjectId TO HANDLE MONGODB _Id MODEL-----
from bson.errors import InvalidId                     #-----HANDLING OBJECT_ID EXCEPTIONS-----
from fastapi import HTTPException                     #-----HANDLING EXCEPTIONS(ERROR)-----
from .db import tasks_collection, user_collection     #-----IMPORT COLLECTIONS FROM DB-----
from .models import Task                              #-----IMPORT MODELS-----


#-----CREATING NEW USER IN DB-----

async def create_user(user):
    user = dict(user)
    document = await user_collection.find_one({"username": user["username"]})
    if document:
        raise HTTPException(status_code=409, detail="User already exists")
    await user_collection.insert_one(user)
    
    
#-----CREATING NEW TASK IN DB BY USER-----

async def creating_task(task, user):
    document = dict(task, **{"username": user["username"]})
    print(document)
    await tasks_collection.insert_one(document)
    
    
#-----UPDATING TASK STATUS IN DB BY CHANGING THE "done" PROPERTY-----

async def updating_task(id, user):
    try:
        document = await tasks_collection.find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=422, detail="Invalid ID")
    if not document:
        raise HTTPException(status_code=404, detail="ID not found")
    if user["username"] != document["username"]:
        raise HTTPException(status_code=403, detail="User not allowed to change Item")
    new_value = not document["done"]
    updated_task = await tasks_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": {"done": new_value}}
        ) 
    return updated_task


#-----DELETE TASK IN DB BY USER-----

async def deleted_task(id, user):
    try:
        document = await tasks_collection.find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=422, detail="Invalid ID")
    if not document:
        raise HTTPException(status_code=404, detail="ID not found")
    if user["username"] != document["username"]:
        raise HTTPException(status_code=403, detail="User not allowed to delete Item")
    document = await tasks_collection.find_one_and_delete({"_id": ObjectId(id)})
    return document


#-----FETCH TASKLIST DATA FROM DB BY USER-----

async def fetch_tasks_by_user(user):
    tasks = []
    cursor = tasks_collection.find({"username": {"$eq": user["username"]}})
    async for document in cursor:
        print(document["_id"])
        get_task = Task(**document)
        tasks.append(get_task)
    return tasks

    
    
