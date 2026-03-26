from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from utils.user import User,UserLogin,PredictionInput
from services.predictor import predict_future_roles
from utils.database import user_collection as user_table,history_collection as history_table


app = FastAPI(
    title="AI Career Evolution & Future Job Predictor",
    description="Predicts future careers based on evolving skills using AI",
    version="1.0.0"
)

# 🔹 Enable CORS (for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Root endpoint
@app.get("/")
def home():
    return {
        "message": "🚀 AI Career Predictor API is running",
        "docs": "/docs"
    }

#register user
@app.post("/register")
async def register_user(user:User):
    user_dict =user.dict()
    user_dict["role"]="user"
    result = await user_table.insert_one(user_dict)
    if result.inserted_id:
        return{"message":"User registered successfully"}
    else:
        return{"message":"failed to register"}

#login user
@app.post("/login")
async def login_user(user: UserLogin):
    user_dict = user.dict()
    result = await user_table.find_one(user_dict)  
    if result:
        return {
            "message": "Login successful",
            "role": result.get("role", "N/A"),
            "user_id": str(result["_id"])
        }
    else:
        return {"message": "Invalid credentials"}

@app.post("/predict")
async def predict(prediction_input: PredictionInput):
    user_id = prediction_input.user_id
    skills = prediction_input.skills

    # Generate predictions
    predictions = predict_future_roles(skills)  # returns a list of prediction dicts

    # Save to MongoDB
    doc = {
        "user_id": user_id,
        "skills": skills,
        "predictions": predictions
    }

    result = await history_table.insert_one(doc)
    if result.inserted_id:
        return {"predictions": predictions}
    else:
        return {"message": "Failed to save prediction"}



# 🔹 Get Prediction History for a User
@app.get("/history/{user_id}")
async def get_history(user_id: str):
    history_cursor = history_table.find({"user_id": user_id})
    history_list = await history_cursor.to_list(length=None)

    # Convert ObjectId to string for JSON serialization
    for record in history_list:
        if "_id" in record:
            record["_id"] = str(record["_id"])

    return {"user_id": user_id, "history": history_list}

@app.get("/users")
async def get_users():
    users_cursor = user_table.find({})
    users_list = await users_cursor.to_list(length=None)

    # Convert ObjectId to string for JSON serialization
    for user in users_list:
        if "_id" in user:
            user["_id"] = str(user["_id"])

    return {"users": users_list}
        
