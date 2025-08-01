import os
from typing import Optional

class NightscoutConfig:
    """Configuration for Nightscout connection"""
    
    def __init__(self):
        self.base_url = os.getenv("NIGHTSCOUT_URL", "https://your-nightscout-instance.herokuapp.com")
        self.api_secret = os.getenv("NIGHTSCOUT_API_SECRET", "")
        self.timeout = int(os.getenv("NIGHTSCOUT_TIMEOUT", "30"))
    
    def is_configured(self) -> bool:
        """Check if Nightscout is properly configured"""
        return (
            self.base_url != "https://your-nightscout-instance.herokuapp.com" and
            self.base_url.startswith(("http://", "https://"))
        )
    
    def get_config_status(self) -> dict:
        """Get configuration status"""
        return {
            "base_url": self.base_url,
            "api_secret_configured": bool(self.api_secret),
            "timeout": self.timeout,
            "is_configured": self.is_configured()
        }

class SupabaseConfig:
    """Configuration for Supabase connection"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL", "")
        self.key = os.getenv("SUPABASE_ANON_KEY", "")
        self.service_key = os.getenv("SUPABASE_SERVICE_KEY", "")
    
    def is_configured(self) -> bool:
        """Check if Supabase is properly configured"""
        return bool(self.url and self.key)
    
    def get_config_status(self) -> dict:
        """Get configuration status"""
        return {
            "url": self.url,
            "anon_key_configured": bool(self.key),
            "service_key_configured": bool(self.service_key),
            "is_configured": self.is_configured()
        }

# Global configuration instances
nightscout_config = NightscoutConfig()
supabase_config = SupabaseConfig() 