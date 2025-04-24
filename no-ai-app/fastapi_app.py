from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv
import os

class Post(BaseModel):
    title: str
    content: str
    author: Optional[str] = None

load_dotenv()

try:
    client = AsyncIOMotorClient(os.getenv('MONGODB_URI'))
    client.admin.command('ping')
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise

app = FastAPI()
db = client.get_database('researchDB').fastapi

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/posts")
async def get_posts(page: int = 1):
    posts = await db.find().skip((page-1)*10).limit(10).to_list(length=1000)
    return [{**post, '_id': str(post['_id'])} for post in posts]

@app.get("/posts/{id}")
async def get_post(id: str):
    try:
        object_id = ObjectId(id)
        if (post := await db.find_one({'_id': object_id})):
            return {**post, '_id': str(post['_id'])}
        raise HTTPException(status_code=404, detail="Post not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ID format")

@app.post("/posts")
async def create_post(post: Post):
    result = await db.insert_one(post.dict())
    return {'_id': str(result.inserted_id)}

@app.put("/posts/{id}")
async def update_post(id: str, post: Post):
    try:
        object_id = ObjectId(id)
        result = await db.update_one(
            {'_id': object_id},
            {'$set': post.dict()}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Post not found")
        return {'message': 'Post updated successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ID format")

@app.delete("/posts/{id}")
async def delete_post(id: str):
    try:
        object_id = ObjectId(id)
        result = await db.delete_one({'_id': object_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Post not found")
        return {'message': 'Post deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ID format")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)