from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from services.nightscout import (
    get_latest_glucose, 
    get_glucose_history, 
    get_device_status, 
    get_treatments,
    test_nightscout_connection
)
from services.supabase_service import (
    test_supabase_connection,
    get_latest_glucose_from_db,
    get_glucose_history_from_db
)

router = APIRouter(prefix="/cgm", tags=["Continuous Glucose Monitoring"])

@router.get("/test-connection")
async def test_nightscout_connection_endpoint():
    """Test the connection to Nightscout"""
    return test_nightscout_connection()

@router.get("/test-db-connection")
async def test_supabase_connection_endpoint():
    """Test the connection to Supabase database"""
    return test_supabase_connection()

@router.get("/test-all-connections")
async def test_all_connections():
    """Test connections to both Nightscout and Supabase"""
    nightscout_result = test_nightscout_connection()
    supabase_result = test_supabase_connection()
    
    return {
        "nightscout": nightscout_result,
        "supabase": supabase_result,
        "all_working": nightscout_result.get("connected", False) and supabase_result.get("connected", False)
    }

@router.get("/latest/{patient_id}")
def latest_glucose(patient_id: str):
    """Get the latest glucose reading for a specific patient from Nightscout and store in database"""
    return get_latest_glucose(patient_id)

@router.get("/latest-db/{patient_id}")
def latest_glucose_from_db(patient_id: str):
    """Get the latest glucose reading for a specific patient from database"""
    return get_latest_glucose_from_db(patient_id)

@router.get("/readings")
async def get_glucose_readings():
    # TODO: Implement actual CGM data retrieval
    return {
        "readings": [
            {"timestamp": "2024-01-01T10:00:00", "glucose": 120, "trend": "stable"},
            {"timestamp": "2024-01-01T10:05:00", "glucose": 125, "trend": "rising"},
            {"timestamp": "2024-01-01T10:10:00", "glucose": 130, "trend": "rising"}
        ]
    }

@router.get("/current")
async def get_current_reading():
    # TODO: Implement current glucose reading
    return {
        "timestamp": "2024-01-01T10:15:00",
        "glucose": 135,
        "trend": "rising",
        "status": "normal"
    }

@router.get("/history/{patient_id}")
async def get_glucose_history_endpoint(patient_id: str, hours: int = 24):
    """Get glucose history for a specific patient from Nightscout and store in database"""
    return get_glucose_history(patient_id, hours)

@router.get("/history-db/{patient_id}")
async def get_glucose_history_from_db_endpoint(patient_id: str, hours: int = 24):
    """Get glucose history for a specific patient from database"""
    return get_glucose_history_from_db(patient_id, hours)

@router.get("/history")
async def get_glucose_history_general(days: int = 7):
    # TODO: Implement historical data retrieval
    return {
        "period": f"Last {days} days",
        "average": 125,
        "min": 80,
        "max": 180,
        "readings_count": 1008  # 7 days * 24 hours * 6 readings per hour
    }

@router.post("/calibrate")
async def calibrate_sensor():
    # TODO: Implement sensor calibration
    return {"message": "Sensor calibration initiated"}

@router.get("/device-status/{patient_id}")
async def get_device_status_endpoint(patient_id: str):
    """Get device status for a specific patient from Nightscout and store in database"""
    return get_device_status(patient_id)

@router.get("/device-status")
async def get_device_status_general():
    # TODO: Implement device status check
    return {
        "device_connected": True,
        "battery_level": 85,
        "signal_strength": "strong",
        "last_communication": "2024-01-01T10:15:00"
    }

@router.get("/treatments/{patient_id}")
async def get_treatments_endpoint(patient_id: str, hours: int = 24):
    """Get treatments (insulin, carbs, etc.) for a specific patient from Nightscout and store in database"""
    return get_treatments(patient_id, hours) 