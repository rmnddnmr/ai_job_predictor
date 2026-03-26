from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = "mongodb://localhost:27017"

if not MONGO_URL:
    raise ValueError("MONGO_URL not set")

client = AsyncIOMotorClient(MONGO_URL)

database = client["job_predictor"]

user_collection = database["users"]
history_collection = database["history"]
