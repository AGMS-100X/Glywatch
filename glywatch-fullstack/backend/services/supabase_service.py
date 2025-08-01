from supabase import create_client, Client
from typing import Dict, List, Optional
from datetime import datetime
import logging
from config import supabase_config

logger = logging.getLogger(__name__)

class SupabaseService:
    def __init__(self):
        self.client: Optional[Client] = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Supabase client"""
        if supabase_config.is_configured():
            try:
                self.client = create_client(supabase_config.url, supabase_config.key)
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                self.client = None
        else:
            logger.warning("Supabase not configured - data will not be persisted")
            self.client = None
    
    def test_connection(self) -> Dict:
        """Test the connection to Supabase"""
        if not self.client:
            return {
                "connected": False,
                "status": "not_configured",
                "error": "Supabase not configured"
            }
        
        try:
            # Test connection by querying a simple table
            response = self.client.table("glucose_readings").select("count", count="exact").limit(1).execute()
            return {
                "connected": True,
                "status": "success",
                "message": "Successfully connected to Supabase"
            }
        except Exception as e:
            return {
                "connected": False,
                "status": "connection_error",
                "error": f"Failed to connect to Supabase: {str(e)}"
            }
    
    def store_glucose_reading(self, patient_id: str, reading_data: Dict) -> Dict:
        """Store glucose reading in Supabase"""
        if not self.client:
            return {"error": "Supabase not configured"}
        
        try:
            data = {
                "patient_id": patient_id,
                "glucose": reading_data.get("glucose", 0),
                "timestamp": reading_data.get("timestamp", ""),
                "trend": reading_data.get("trend", "unknown"),
                "status": reading_data.get("status", "unknown"),
                "raw": reading_data.get("raw", 0),
                "filtered": reading_data.get("filtered", 0),
                "noise": reading_data.get("noise", 0),
                "created_at": datetime.utcnow().isoformat()
            }
            
            response = self.client.table("glucose_readings").insert(data).execute()
            
            if response.data:
                return {
                    "success": True,
                    "id": response.data[0].get("id"),
                    "message": "Glucose reading stored successfully"
                }
            else:
                return {"error": "Failed to store glucose reading"}
                
        except Exception as e:
            logger.error(f"Failed to store glucose reading: {e}")
            return {"error": f"Failed to store glucose reading: {str(e)}"}
    
    def store_device_status(self, patient_id: str, status_data: Dict) -> Dict:
        """Store device status in Supabase"""
        if not self.client:
            return {"error": "Supabase not configured"}
        
        try:
            data = {
                "patient_id": patient_id,
                "device_connected": status_data.get("device_connected", False),
                "battery_level": status_data.get("battery_level", 0),
                "signal_strength": status_data.get("signal_strength", "unknown"),
                "device_name": status_data.get("device_name", "unknown"),
                "last_communication": status_data.get("last_communication", ""),
                "pump_status": status_data.get("pump_status", {}),
                "loop_status": status_data.get("loop_status", {}),
                "created_at": datetime.utcnow().isoformat()
            }
            
            response = self.client.table("device_status").insert(data).execute()
            
            if response.data:
                return {
                    "success": True,
                    "id": response.data[0].get("id"),
                    "message": "Device status stored successfully"
                }
            else:
                return {"error": "Failed to store device status"}
                
        except Exception as e:
            logger.error(f"Failed to store device status: {e}")
            return {"error": f"Failed to store device status: {str(e)}"}
    
    def store_treatment(self, patient_id: str, treatment_data: Dict) -> Dict:
        """Store treatment in Supabase"""
        if not self.client:
            return {"error": "Supabase not configured"}
        
        try:
            data = {
                "patient_id": patient_id,
                "treatment_type": treatment_data.get("eventType", "unknown"),
                "timestamp": treatment_data.get("created_at", ""),
                "insulin": treatment_data.get("insulin", 0),
                "carbs": treatment_data.get("carbs", 0),
                "notes": treatment_data.get("notes", ""),
                "entered_by": treatment_data.get("enteredBy", ""),
                "raw_data": treatment_data,
                "created_at": datetime.utcnow().isoformat()
            }
            
            response = self.client.table("treatments").insert(data).execute()
            
            if response.data:
                return {
                    "success": True,
                    "id": response.data[0].get("id"),
                    "message": "Treatment stored successfully"
                }
            else:
                return {"error": "Failed to store treatment"}
                
        except Exception as e:
            logger.error(f"Failed to store treatment: {e}")
            return {"error": f"Failed to store treatment: {str(e)}"}
    
    def get_glucose_history(self, patient_id: str, hours: int = 24) -> Dict:
        """Get glucose history from Supabase"""
        if not self.client:
            return {"error": "Supabase not configured"}
        
        try:
            # Calculate time range
            from datetime import timedelta
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=hours)
            
            response = self.client.table("glucose_readings")\
                .select("*")\
                .eq("patient_id", patient_id)\
                .gte("created_at", start_time.isoformat())\
                .lte("created_at", end_time.isoformat())\
                .order("created_at", desc=True)\
                .execute()
            
            return {
                "patient_id": patient_id,
                "readings": response.data,
                "period_hours": hours,
                "total_readings": len(response.data)
            }
                
        except Exception as e:
            logger.error(f"Failed to get glucose history: {e}")
            return {"error": f"Failed to get glucose history: {str(e)}"}
    
    def get_latest_glucose(self, patient_id: str) -> Dict:
        """Get latest glucose reading from Supabase"""
        if not self.client:
            return {"error": "Supabase not configured"}
        
        try:
            response = self.client.table("glucose_readings")\
                .select("*")\
                .eq("patient_id", patient_id)\
                .order("created_at", desc=True)\
                .limit(1)\
                .execute()
            
            if response.data:
                reading = response.data[0]
                return {
                    "patient_id": patient_id,
                    "glucose": reading.get("glucose", 0),
                    "timestamp": reading.get("timestamp", ""),
                    "trend": reading.get("trend", "unknown"),
                    "status": reading.get("status", "unknown"),
                    "raw": reading.get("raw", 0),
                    "filtered": reading.get("filtered", 0),
                    "noise": reading.get("noise", 0)
                }
            else:
                return {
                    "patient_id": patient_id,
                    "error": "No glucose data available"
                }
                
        except Exception as e:
            logger.error(f"Failed to get latest glucose: {e}")
            return {"error": f"Failed to get latest glucose: {str(e)}"}

# Create a global instance
supabase_service = SupabaseService()

def test_supabase_connection() -> Dict:
    """Test connection to Supabase"""
    return supabase_service.test_connection()

def store_glucose_reading(patient_id: str, reading_data: Dict) -> Dict:
    """Store glucose reading in Supabase"""
    return supabase_service.store_glucose_reading(patient_id, reading_data)

def store_device_status(patient_id: str, status_data: Dict) -> Dict:
    """Store device status in Supabase"""
    return supabase_service.store_device_status(patient_id, status_data)

def store_treatment(patient_id: str, treatment_data: Dict) -> Dict:
    """Store treatment in Supabase"""
    return supabase_service.store_treatment(patient_id, treatment_data)

def get_glucose_history_from_db(patient_id: str, hours: int = 24) -> Dict:
    """Get glucose history from Supabase"""
    return supabase_service.get_glucose_history(patient_id, hours)

def get_latest_glucose_from_db(patient_id: str) -> Dict:
    """Get latest glucose reading from Supabase"""
    return supabase_service.get_latest_glucose(patient_id) 