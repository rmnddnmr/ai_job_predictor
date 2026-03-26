import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1. Get URL from environment, fallback to 127.0.0.1 if not found
# Using 127.0.0.1 is more reliable than 'localhost' in many Python environments
MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL environment variable is missing")

# Initialize the client
client = AsyncIOMotorClient(MONGO_URL)

database = client["job_predictor"]

user_collection = database["users"]
history_collection = database["history"]

# Quick connection test (Optional but recommended)
async def test_connection():
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
