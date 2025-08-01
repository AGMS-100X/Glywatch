import os
import subprocess
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime
import logging
from config import supabase_config

logger = logging.getLogger(__name__)

class NightscoutManager:
    def __init__(self):
        self.nightscout_base_path = os.getenv("NIGHTSCOUT_BASE_PATH", "./nightscout-instances")
        self.supabase_url = supabase_config.url
        self.supabase_key = supabase_config.key
        
    def create_nightscout_for_user(self, user_id: str, user_email: str) -> Dict:
        """Create a new Nightscout instance for a user"""
        try:
            # Create user-specific directory
            user_instance_path = f"{self.nightscout_base_path}/{user_id}"
            os.makedirs(user_instance_path, exist_ok=True)
            
            # Generate unique API secret for this user
            api_secret = self._generate_api_secret(user_id)
            
            # Create environment file for this user
            env_content = self._create_env_file(user_id, api_secret)
            
            with open(f"{user_instance_path}/.env", "w") as f:
                f.write(env_content)
            
            # Store user configuration in Supabase
            self._store_user_config(user_id, user_email, api_secret)
            
            return {
                "success": True,
                "user_id": user_id,
                "nightscout_url": f"http://localhost:1337/{user_id}",
                "api_secret": api_secret,
                "instance_path": user_instance_path
            }
            
        except Exception as e:
            logger.error(f"Failed to create Nightscout for user {user_id}: {e}")
            return {
                "success": False,
                "error": f"Failed to create Nightscout instance: {str(e)}"
            }
    
    def start_user_nightscout(self, user_id: str) -> Dict:
        """Start Nightscout instance for a specific user"""
        try:
            user_instance_path = f"{self.nightscout_base_path}/{user_id}"
            
            if not os.path.exists(user_instance_path):
                return {
                    "success": False,
                    "error": "User Nightscout instance not found"
                }
            
            # Start Nightscout process
            process = subprocess.Popen(
                ["npm", "start"],
                cwd=user_instance_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            return {
                "success": True,
                "user_id": user_id,
                "process_id": process.pid,
                "message": "Nightscout instance started"
            }
            
        except Exception as e:
            logger.error(f"Failed to start Nightscout for user {user_id}: {e}")
            return {
                "success": False,
                "error": f"Failed to start Nightscout instance: {str(e)}"
            }
    
    def get_user_nightscout_config(self, user_id: str) -> Dict:
        """Get Nightscout configuration for a user"""
        try:
            # Query Supabase for user config
            response = requests.get(
                f"{self.supabase_url}/rest/v1/user_nightscout_config",
                headers={
                    "apikey": self.supabase_key,
                    "Authorization": f"Bearer {self.supabase_key}"
                },
                params={"user_id": f"eq.{user_id}"}
            )
            
            if response.status_code == 200 and response.json():
                config = response.json()[0]
                return {
                    "success": True,
                    "user_id": user_id,
                    "nightscout_url": config.get("nightscout_url"),
                    "api_secret": config.get("api_secret"),
                    "created_at": config.get("created_at")
                }
            else:
                return {
                    "success": False,
                    "error": "User configuration not found"
                }
                
        except Exception as e:
            logger.error(f"Failed to get user config for {user_id}: {e}")
            return {
                "success": False,
                "error": f"Failed to get user configuration: {str(e)}"
            }
    
    def update_user_nightscout_config(self, user_id: str, config_data: Dict) -> Dict:
        """Update Nightscout configuration for a user"""
        try:
            response = requests.patch(
                f"{self.supabase_url}/rest/v1/user_nightscout_config",
                headers={
                    "apikey": self.supabase_key,
                    "Authorization": f"Bearer {self.supabase_key}",
                    "Content-Type": "application/json"
                },
                params={"user_id": f"eq.{user_id}"},
                json=config_data
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "User configuration updated"
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to update configuration: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Failed to update user config for {user_id}: {e}")
            return {
                "success": False,
                "error": f"Failed to update user configuration: {str(e)}"
            }
    
    def delete_user_nightscout(self, user_id: str) -> Dict:
        """Delete Nightscout instance for a user"""
        try:
            user_instance_path = f"{self.nightscout_base_path}/{user_id}"
            
            if os.path.exists(user_instance_path):
                import shutil
                shutil.rmtree(user_instance_path)
            
            # Remove from Supabase
            response = requests.delete(
                f"{self.supabase_url}/rest/v1/user_nightscout_config",
                headers={
                    "apikey": self.supabase_key,
                    "Authorization": f"Bearer {self.supabase_key}"
                },
                params={"user_id": f"eq.{user_id}"}
            )
            
            return {
                "success": True,
                "message": "User Nightscout instance deleted"
            }
            
        except Exception as e:
            logger.error(f"Failed to delete Nightscout for user {user_id}: {e}")
            return {
                "success": False,
                "error": f"Failed to delete Nightscout instance: {str(e)}"
            }
    
    def _generate_api_secret(self, user_id: str) -> str:
        """Generate unique API secret for user"""
        import secrets
        return f"glywatch_{user_id}_{secrets.token_hex(16)}"
    
    def _create_env_file(self, user_id: str, api_secret: str) -> str:
        """Create environment file content for user"""
        return f"""# Nightscout Configuration for User {user_id}
MONGO_CONNECTION=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
API_SECRET={api_secret}
DISPLAY_UNITS=mg/dl
ENABLE=careportal basal dbsize rawbg iob maker cob bwp cage sage boluscalc pushover treatmentnotify loop pump profile food openaps bage iage weight heartrate
PORT=1337
"""
    
    def _store_user_config(self, user_id: str, user_email: str, api_secret: str) -> bool:
        """Store user configuration in Supabase"""
        try:
            data = {
                "user_id": user_id,
                "user_email": user_email,
                "nightscout_url": f"http://localhost:1337/{user_id}",
                "api_secret": api_secret,
                "created_at": datetime.utcnow().isoformat(),
                "status": "active"
            }
            
            response = requests.post(
                f"{self.supabase_url}/rest/v1/user_nightscout_config",
                headers={
                    "apikey": self.supabase_key,
                    "Authorization": f"Bearer {self.supabase_key}",
                    "Content-Type": "application/json"
                },
                json=data
            )
            
            return response.status_code == 201
            
        except Exception as e:
            logger.error(f"Failed to store user config: {e}")
            return False

# Create global instance
nightscout_manager = NightscoutManager()

def create_nightscout_for_user(user_id: str, user_email: str) -> Dict:
    """Create Nightscout instance for a user"""
    return nightscout_manager.create_nightscout_for_user(user_id, user_email)

def start_user_nightscout(user_id: str) -> Dict:
    """Start Nightscout instance for a user"""
    return nightscout_manager.start_user_nightscout(user_id)

def get_user_nightscout_config(user_id: str) -> Dict:
    """Get Nightscout configuration for a user"""
    return nightscout_manager.get_user_nightscout_config(user_id)

def update_user_nightscout_config(user_id: str, config_data: Dict) -> Dict:
    """Update Nightscout configuration for a user"""
    return nightscout_manager.update_user_nightscout_config(user_id, config_data)

def delete_user_nightscout(user_id: str) -> Dict:
    """Delete Nightscout instance for a user"""
    return nightscout_manager.delete_user_nightscout(user_id) 