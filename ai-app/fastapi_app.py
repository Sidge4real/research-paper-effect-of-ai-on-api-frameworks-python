from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import asyncio
from transformers import pipeline

# Load environment variables
load_dotenv()

# MongoDB connection
try:
    client = AsyncIOMotorClient(os.getenv('MONGODB_URI'))
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB")
except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
    raise

# App instance
app = FastAPI()
db = client.get_database('researchDB').fastapi

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Post(BaseModel):
    title: str
    content: str
    author: Optional[str] = None

class SummarizeRequest(BaseModel):
    text: str

# Routes: CRUD
@app.get("/posts")
async def get_posts(page: int = 1):
    posts = await db.find().skip((page-1)*10).limit(10).to_list(length=1000)
    return [{**post, '_id': str(post['_id'])} for post in posts]

@app.get("/posts/{id}")
async def get_post(id: str):
    try:
        object_id = ObjectId(id)
        post = await db.find_one({'_id': object_id})
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return {**post, '_id': str(post['_id'])}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

@app.post("/posts")
async def create_post(post: Post):
    result = await db.insert_one(post.dict())
    return {'_id': str(result.inserted_id)}

@app.put("/posts/{id}")
async def update_post(id: str, post: Post):
    try:
        object_id = ObjectId(id)
        result = await db.update_one({'_id': object_id}, {'$set': post.dict()})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Post not found")
        return {'message': 'Post updated successfully'}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

@app.delete("/posts/{id}")
async def delete_post(id: str):
    try:
        object_id = ObjectId(id)
        result = await db.delete_one({'_id': object_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Post not found")
        return {'message': 'Post deleted successfully'}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

# Load summarizer model (lightweight)
try:
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    test_summary = summarizer("Dit is een testtekst om de samenvatting te testen.")
    print("✅ AI-model geladen en getest succesvol")
except Exception as e:
    print("❌ Fout bij laden AI-model:", e)
    summarizer = None

# AI route: text summarization
@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    if not summarizer:
        raise HTTPException(status_code=503, detail="AI model not loaded")
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")

    try:
        result = await asyncio.to_thread(
            summarizer,
            request.text,
            max_length=150,
            min_length=40,
            do_sample=False
        )
        return {"summary": result[0]['summary_text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during summarization: {str(e)}")

# Uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
