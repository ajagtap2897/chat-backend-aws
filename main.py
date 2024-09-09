from datetime import datetime
import json
import os
from pathlib import Path
import uuid
from fastapi import FastAPI, HTTPException, status, Depends
from typing import List
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from models.user_model import CreateUser, ResponseUser, User
from uuid import UUID, uuid4
from models.message_model import CreateMessageRequest, Message
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv() 



client = AsyncIOMotorClient(os.environ.get("MONGO_URI"))
db = client.chatty_chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = Path(__file__).resolve().parent / "static"

app.mount("/static", StaticFiles(directory=static_path), name="static")

def get_user_collection():
    return db.user

def get_message_collection():
    return db.message


@app.get("/chat-list/{user_id}")
async def getChatList(user_id: str, messages=Depends(get_message_collection), users = Depends(get_user_collection)):
    messageList = await messages.find({'$or': [{ "sender": user_id },{ "receiver": user_id }]}).to_list(None)
    
    related_ids = set()
    for message in messageList:
        if message['sender'] == user_id:
            related_ids.add(message['receiver'])
        elif message['receiver'] == user_id:
            related_ids.add(message['sender'])

    related_users = await users.find({'_id': {'$in': list(related_ids)}}).to_list(None)
    
    result = []
    for related_user in related_users:
        last_message = await messages.find({'$or': [{ 'sender': user_id, 'receiver': related_user['_id'] },{ 'sender': related_user['_id'], 'receiver': user_id }]}).sort('timestamp', -1).limit(1).to_list(None)
        
        result.append({
            'user': related_user,
            'last_message': last_message[0]
        })
    
    return result

@app.get("/chat-history/{user_id}/{contact_id}")
async def getChatList(user_id: str, contact_id: str, messages=Depends(get_message_collection), users = Depends(get_user_collection)):
    messageList = await messages.find({'$or': [{ 'sender': user_id, 'receiver': contact_id },{ 'sender': contact_id, 'receiver': user_id }]}).to_list(None)

    contactUser = await users.find({'_id': contact_id}).to_list(None)
    print("Size: " + str(len(contactUser)))
    return {
        "contactUser": contactUser[0],
        "messageList": messageList
    }

@app.post("/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
async def create_message(message: CreateMessageRequest, messages=Depends(get_message_collection)):
    newMessage = {
        "_id": str(uuid.uuid4()),  # Set the custom UUID as the _id
        "content": message.content,
        "created_at": str(datetime.now()),
        "sender": message.sender,
        "receiver": message.receiver,
    }
    
    result = await db.message.insert_one(newMessage)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    return newMessage

@app.get("/users/{email}")
async def get_user(email: str, users=Depends(get_user_collection)):
    user  = await users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=400, detail="Email already registered")
    responseUser = ResponseUser(
            id=user['_id'],
            name=user['name'],
            email=user['email'],
            profile_pic=user['profile_pic']
        )
    return responseUser

@app.get("/users/", response_model=List[ResponseUser])
async def get_users(users=Depends(get_user_collection)):
    users = await users.find().to_list(None)
    userList = []
    for user in users:
        responseUser = ResponseUser(
            id=user['_id'],
            name=user['name'],
            email=user['email'],
            profile_pic=user['profile_pic']
        )
        userList.append(responseUser)
    return userList

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, users=Depends(get_user_collection)):
    if await users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    id = str(uuid.uuid4())
    new_user_model = {
        "_id": id,
        "name": user.name,
        "email": user.email,
        "profile_pic": id + ".jpg",
        "password": "1234567"
    }
    new_user = await users.insert_one(new_user_model)
    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user_model.pop('password')
    return new_user_model