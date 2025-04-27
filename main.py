from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from validator import validate_Solution, validate_Ques
from typing import List
import uvicorn
import os
from services.health_service import HealthService
import requests
import asyncio
from fastapi.middleware.cors import CORSMiddleware

# const app = express()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

usersDB = {}

health_service = HealthService()

@app.on_event("startup")
async def startup_event():
    await asyncio.sleep(5)
    asyncio.create_task(health_service.keep_alive())


class USER(BaseModel):
    name : str
    age : int

class TWEET(BaseModel):
    tasks : List[str]

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint that returns the application status
    """
    return await health_service.health_check()


@app.post("/register")
def reg_user(user: USER):
    usersDB[user.name] = user.age
    return {"message": "hello", "data": user.dict()}

@app.post("/gen-tweet")
def get_tweet(data: TWEET): 
    return {"tweet" : gen_tweet(data)}
    

if __name__ == "__main__":
    # Get port from environment variable or use a default
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)