from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
from pydantic import BaseModel
from services.nightscout_manager import (
    create_nightscout_for_user,
    start_user_nightscout,
    get_user_nightscout_config,
    update_user_nightscout_config,
    delete_user_nightscout
)

router = APIRouter(prefix="/users", tags=["User Management"])

class UserRegistration(BaseModel):
    user_id: str
    user_email: str
    cgm_type: Optional[str] = None
    cgm_device_id: Optional[str] = None

class UserNightscoutConfig(BaseModel):
    nightscout_url: Optional[str] = None
    api_secret: Optional[str] = None
    cgm_type: Optional[str] = None
    cgm_device_id: Optional[str] = None

@router.post("/register")
async def register_user(user_data: UserRegistration):
    """Register a new user and create their Nightscout instance"""
    try:
        result = create_nightscout_for_user(user_data.user_id, user_data.user_email)
        
        if result["success"]:
            return {
                "success": True,
                "message": "User registered successfully",
                "user_id": user_data.user_id,
                "nightscout_url": result["nightscout_url"],
                "api_secret": result["api_secret"],
                "next_steps": [
                    "1. Start your Nightscout instance",
                    "2. Configure your CGM device",
                    "3. Set up data upload to Nightscout"
                ]
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register user: {str(e)}")

@router.post("/{user_id}/start-nightscout")
async def start_user_nightscout_instance(user_id: str):
    """Start Nightscout instance for a specific user"""
    try:
        result = start_user_nightscout(user_id)
        
        if result["success"]:
            return {
                "success": True,
                "message": "Nightscout instance started",
                "user_id": user_id,
                "process_id": result.get("process_id")
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start Nightscout: {str(e)}")

@router.get("/{user_id}/nightscout-config")
async def get_user_nightscout_configuration(user_id: str):
    """Get Nightscout configuration for a user"""
    try:
        result = get_user_nightscout_config(user_id)
        
        if result["success"]:
            return {
                "success": True,
                "user_id": user_id,
                "nightscout_url": result["nightscout_url"],
                "api_secret": result["api_secret"],
                "created_at": result["created_at"]
            }
        else:
            raise HTTPException(status_code=404, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user config: {str(e)}")

@router.put("/{user_id}/nightscout-config")
async def update_user_nightscout_configuration(user_id: str, config: UserNightscoutConfig):
    """Update Nightscout configuration for a user"""
    try:
        config_data = config.dict(exclude_unset=True)
        result = update_user_nightscout_config(user_id, config_data)
        
        if result["success"]:
            return {
                "success": True,
                "message": "User configuration updated",
                "user_id": user_id
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user config: {str(e)}")

@router.delete("/{user_id}/nightscout")
async def delete_user_nightscout_instance(user_id: str):
    """Delete Nightscout instance for a user"""
    try:
        result = delete_user_nightscout(user_id)
        
        if result["success"]:
            return {
                "success": True,
                "message": "User Nightscout instance deleted",
                "user_id": user_id
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete Nightscout: {str(e)}")

@router.get("/{user_id}/status")
async def get_user_status(user_id: str):
    """Get comprehensive status for a user"""
    try:
        # Get Nightscout config
        config_result = get_user_nightscout_config(user_id)
        
        if config_result["success"]:
            return {
                "success": True,
                "user_id": user_id,
                "nightscout_configured": True,
                "nightscout_url": config_result["nightscout_url"],
                "status": "active",
                "created_at": config_result["created_at"]
            }
        else:
            return {
                "success": True,
                "user_id": user_id,
                "nightscout_configured": False,
                "status": "not_configured",
                "message": "User needs to register first"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user status: {str(e)}") 