import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import os
import logging
from config import nightscout_config
from services.supabase_service import (
    store_glucose_reading,
    store_device_status,
    store_treatment,
    test_supabase_connection
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NightscoutService:
    def __init__(self):
        self.base_url = os.getenv("NIGHTSCOUT_URL", "https://your-nightscout-instance.herokuapp.com")
        self.api_secret = os.getenv("NIGHTSCOUT_API_SECRET", "")
        self.timeout = 30  # 30 seconds timeout
        
    def test_connection(self) -> Dict:
        """Test the connection to Nightscout"""
        try:
            headers = {"api-secret": self.api_secret} if self.api_secret else {}
            response = requests.get(
                f"{self.base_url}/api/v1/status.json",
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            status_data = response.json()
            return {
                "connected": True,
                "status": "success",
                "nightscout_version": status_data.get("version", "unknown"),
                "server_time": status_data.get("serverTime", ""),
                "base_url": self.base_url
            }
            
        except requests.exceptions.ConnectionError:
            return {
                "connected": False,
                "status": "connection_error",
                "error": "Unable to connect to Nightscout server",
                "base_url": self.base_url
            }
        except requests.exceptions.Timeout:
            return {
                "connected": False,
                "status": "timeout",
                "error": "Connection timeout",
                "base_url": self.base_url
            }
        except requests.exceptions.HTTPError as e:
            return {
                "connected": False,
                "status": "http_error",
                "error": f"HTTP error: {e.response.status_code}",
                "base_url": self.base_url
            }
        except Exception as e:
            return {
                "connected": False,
                "status": "unknown_error",
                "error": f"Unknown error: {str(e)}",
                "base_url": self.base_url
            }
    
    def get_latest_glucose(self, patient_id: str) -> Dict:
        """Get the latest glucose reading from Nightscout and store in Supabase"""
        try:
            headers = {"api-secret": self.api_secret} if self.api_secret else {}
            response = requests.get(
                f"{self.base_url}/api/v1/entries.json",
                headers=headers,
                params={"count": 1},
                timeout=self.timeout
            )
            response.raise_for_status()
            
            entries = response.json()
            if entries:
                latest = entries[0]
                glucose_data = {
                    "patient_id": patient_id,
                    "glucose": latest.get("sgv", 0),
                    "timestamp": latest.get("dateString", ""),
                    "trend": latest.get("direction", "unknown"),
                    "status": self._get_glucose_status(latest.get("sgv", 0)),
                    "raw": latest.get("raw", 0),
                    "filtered": latest.get("filtered", 0),
                    "noise": latest.get("noise", 0)
                }
                
                # Store in Supabase
                storage_result = store_glucose_reading(patient_id, glucose_data)
                glucose_data["storage_result"] = storage_result
                
                return glucose_data
            else:
                return {
                    "patient_id": patient_id,
                    "error": "No glucose data available"
                }
                
        except requests.RequestException as e:
            logger.error(f"Failed to fetch glucose data: {str(e)}")
            return {
                "patient_id": patient_id,
                "error": f"Failed to fetch data from Nightscout: {str(e)}"
            }
    
    def get_glucose_history(self, patient_id: str, hours: int = 24) -> Dict:
        """Get glucose history from Nightscout and store in Supabase"""
        try:
            headers = {"api-secret": self.api_secret} if self.api_secret else {}
            response = requests.get(
                f"{self.base_url}/api/v1/entries.json",
                headers=headers,
                params={"count": hours * 12},  # Assuming 5-minute intervals
                timeout=self.timeout
            )
            response.raise_for_status()
            
            entries = response.json()
            readings = []
            stored_count = 0
            
            for entry in entries:
                reading_data = {
                    "timestamp": entry.get("dateString", ""),
                    "glucose": entry.get("sgv", 0),
                    "trend": entry.get("direction", "unknown"),
                    "raw": entry.get("raw", 0),
                    "filtered": entry.get("filtered", 0),
                    "noise": entry.get("noise", 0)
                }
                
                readings.append(reading_data)
                
                # Store each reading in Supabase
                storage_result = store_glucose_reading(patient_id, reading_data)
                if storage_result.get("success"):
                    stored_count += 1
            
            return {
                "patient_id": patient_id,
                "readings": readings,
                "period_hours": hours,
                "total_readings": len(readings),
                "stored_in_db": stored_count,
                "storage_status": f"Stored {stored_count}/{len(readings)} readings in database"
            }
                
        except requests.RequestException as e:
            logger.error(f"Failed to fetch glucose history: {str(e)}")
            return {
                "patient_id": patient_id,
                "error": f"Failed to fetch history from Nightscout: {str(e)}"
            }
    
    def get_device_status(self, patient_id: str) -> Dict:
        """Get device status from Nightscout and store in Supabase"""
        try:
            headers = {"api-secret": self.api_secret} if self.api_secret else {}
            response = requests.get(
                f"{self.base_url}/api/v1/devicestatus.json",
                headers=headers,
                params={"count": 1},
                timeout=self.timeout
            )
            response.raise_for_status()
            
            devices = response.json()
            if devices:
                latest_device = devices[0]
                device_data = {
                    "patient_id": patient_id,
                    "device_connected": True,
                    "battery_level": latest_device.get("battery", 0),
                    "signal_strength": "strong",  # Placeholder
                    "last_communication": latest_device.get("created_at", ""),
                    "device_name": latest_device.get("device", "unknown"),
                    "pump_status": latest_device.get("pump", {}),
                    "loop_status": latest_device.get("loop", {})
                }
                
                # Store in Supabase
                storage_result = store_device_status(patient_id, device_data)
                device_data["storage_result"] = storage_result
                
                return device_data
            else:
                return {
                    "patient_id": patient_id,
                    "device_connected": False,
                    "error": "No device status available"
                }
                
        except requests.RequestException as e:
            logger.error(f"Failed to fetch device status: {str(e)}")
            return {
                "patient_id": patient_id,
                "error": f"Failed to fetch device status: {str(e)}"
            }
    
    def get_treatments(self, patient_id: str, hours: int = 24) -> Dict:
        """Get treatments from Nightscout and store in Supabase"""
        try:
            headers = {"api-secret": self.api_secret} if self.api_secret else {}
            response = requests.get(
                f"{self.base_url}/api/v1/treatments.json",
                headers=headers,
                params={"count": hours * 4},  # Assuming treatments every 15 minutes
                timeout=self.timeout
            )
            response.raise_for_status()
            
            treatments = response.json()
            stored_count = 0
            
            for treatment in treatments:
                # Store each treatment in Supabase
                storage_result = store_treatment(patient_id, treatment)
                if storage_result.get("success"):
                    stored_count += 1
            
            return {
                "patient_id": patient_id,
                "treatments": treatments,
                "period_hours": hours,
                "total_treatments": len(treatments),
                "stored_in_db": stored_count,
                "storage_status": f"Stored {stored_count}/{len(treatments)} treatments in database"
            }
                
        except requests.RequestException as e:
            logger.error(f"Failed to fetch treatments: {str(e)}")
            return {
                "patient_id": patient_id,
                "error": f"Failed to fetch treatments from Nightscout: {str(e)}"
            }
    
    def _get_glucose_status(self, glucose: int) -> str:
        """Determine glucose status based on value"""
        if glucose < 70:
            return "low"
        elif glucose > 180:
            return "high"
        else:
            return "normal"

# Create a global instance
nightscout_service = NightscoutService()

def test_nightscout_connection() -> Dict:
    """Test connection to Nightscout"""
    return nightscout_service.test_connection()

def get_latest_glucose(patient_id: str) -> Dict:
    """Get latest glucose reading for a patient"""
    return nightscout_service.get_latest_glucose(patient_id)

def get_glucose_history(patient_id: str, hours: int = 24) -> Dict:
    """Get glucose history for a patient"""
    return nightscout_service.get_glucose_history(patient_id, hours)

def get_device_status(patient_id: str) -> Dict:
    """Get device status for a patient"""
    return nightscout_service.get_device_status(patient_id)

def get_treatments(patient_id: str, hours: int = 24) -> Dict:
    """Get treatments for a patient"""
    return nightscout_service.get_treatments(patient_id, hours) 