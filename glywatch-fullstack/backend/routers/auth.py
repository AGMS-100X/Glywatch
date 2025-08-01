from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import jwt
import os
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Secret key for JWT (in production, use environment variable)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"

class LoginRequest(BaseModel):
    role: str
    username: str
    password: str

class RegisterRequest(BaseModel):
    role: str
    username: str
    email: str
    password: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login")
async def login(data: LoginRequest):
    # Validate role
    if data.role not in ["individual", "camp"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be 'individual' or 'camp'")
    
    # Different authentication logic based on role
    if data.role == "individual":
        # Individual user authentication
        if data.username == "patient" and data.password == "password":
            token = create_access_token(
                data={"sub": data.username, "role": data.role},
                expires_delta=timedelta(hours=24)
            )
            return {
                "message": "Login successful",
                "role": data.role,
                "token": token,
                "user_type": "patient",
                "redirect_to": "/dashboard"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials for individual user")
    
    elif data.role == "camp":
        # Camp/caregiver authentication
        if data.username == "caregiver" and data.password == "password":
            token = create_access_token(
                data={"sub": data.username, "role": data.role},
                expires_delta=timedelta(hours=24)
            )
            return {
                "message": "Login successful",
                "role": data.role,
                "token": token,
                "user_type": "caregiver",
                "redirect_to": "/caregiver"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials for camp user")

@router.post("/register")
async def register(data: RegisterRequest):
    # Validate role
    if data.role not in ["individual", "camp"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be 'individual' or 'camp'")
    
    # TODO: Implement actual user registration with database
    # For now, just return success
    return {
        "message": f"User registered successfully as {data.role}",
        "username": data.username,
        "role": data.role
    }

@router.get("/profile")
async def get_profile():
    # TODO: Implement profile retrieval with JWT token validation
    return {"message": "Profile endpoint"}

@router.post("/logout")
async def logout():
    return {"message": "Logout successful"} 