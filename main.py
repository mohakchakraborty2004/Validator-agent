from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from validator import validate_Solution, validate_Ques
from typing import List
import uvicorn
import os
# from services.health_service import HealthService
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

# health_service = HealthService()

# @app.on_event("startup")
# async def startup_event():
#     await asyncio.sleep(5)
#     asyncio.create_task(health_service.keep_alive())


class ProblemValidationRequest(BaseModel):
    ques: str

class SolutionValidationRequest(BaseModel):
    ques: str
    solution_code: str
    language: str 

# @app.get("/api/health")
# async def health_check():
#     """
#     Health check endpoint that returns the application status
#     """
#     return await health_service.health_check()


@app.post("/validateQuest")
def validate(validator: ProblemValidationRequest):
    return validate_Ques(validator)

@app.post("/checkSolution")
def solnCheck(data: SolutionValidationRequest): 
    return validate_Solution(data)
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)