
from pydantic import BaseModel, EmailStr  


class User(BaseModel):
    name: str
    email: EmailStr
    password: str

# User login model
class UserLogin(BaseModel):  
    email: EmailStr
    password: str

# Prediction input model
class PredictionInput(BaseModel):  
    user_id: str
    skills: list[str]

