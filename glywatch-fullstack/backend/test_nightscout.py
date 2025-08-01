#!/usr/bin/env python3
"""
Test script for Nightscout connection
Run this script to test your Nightscout configuration
"""

import os
import sys
from services.nightscout import test_nightscout_connection, get_latest_glucose, get_device_status
from config import nightscout_config

def test_connection():
    """Test the Nightscout connection"""
    print("🔍 Testing Nightscout Connection...")
    print("=" * 50)
    
    # Check configuration
    config_status = nightscout_config.get_config_status()
    print(f"📋 Configuration Status:")
    print(f"   Base URL: {config_status['base_url']}")
    print(f"   API Secret Configured: {config_status['api_secret_configured']}")
    print(f"   Timeout: {config_status['timeout']} seconds")
    print(f"   Properly Configured: {config_status['is_configured']}")
    print()
    
    if not config_status['is_configured']:
        print("❌ Configuration Error:")
        print("   Please set NIGHTSCOUT_URL environment variable to your Nightscout instance URL")
        print("   Example: export NIGHTSCOUT_URL=https://your-nightscout.herokuapp.com")
        return False
    
    # Test connection
    result = test_nightscout_connection()
    
    if result['connected']:
        print("✅ Connection Successful!")
        print(f"   Nightscout Version: {result.get('nightscout_version', 'unknown')}")
        print(f"   Server Time: {result.get('server_time', 'unknown')}")
        print()
        
        # Test getting latest glucose
        print("🔬 Testing Glucose Data Retrieval...")
        glucose_result = get_latest_glucose("test_patient")
        if 'error' not in glucose_result:
            print("✅ Glucose Data Retrieved Successfully!")
            print(f"   Glucose: {glucose_result.get('glucose', 'N/A')} mg/dL")
            print(f"   Trend: {glucose_result.get('trend', 'N/A')}")
            print(f"   Status: {glucose_result.get('status', 'N/A')}")
        else:
            print(f"⚠️  Glucose Data Error: {glucose_result['error']}")
        
        print()
        
        # Test device status
        print("📱 Testing Device Status...")
        device_result = get_device_status("test_patient")
        if 'error' not in device_result:
            print("✅ Device Status Retrieved Successfully!")
            print(f"   Device Connected: {device_result.get('device_connected', False)}")
            print(f"   Device Name: {device_result.get('device_name', 'N/A')}")
        else:
            print(f"⚠️  Device Status Error: {device_result['error']}")
        
        return True
    else:
        print("❌ Connection Failed!")
        print(f"   Status: {result['status']}")
        print(f"   Error: {result['error']}")
        print()
        print("🔧 Troubleshooting Tips:")
        print("   1. Check if your Nightscout URL is correct")
        print("   2. Verify your Nightscout instance is running")
        print("   3. Check if API secret is required and correctly set")
        print("   4. Ensure your Nightscout instance allows API access")
        return False

def main():
    """Main function"""
    print("🌙 Nightscout Connection Test")
    print("=" * 50)
    print()
    
    success = test_connection()
    
    print()
    print("=" * 50)
    if success:
        print("🎉 All tests completed successfully!")
        print("   Your Nightscout integration is working properly.")
    else:
        print("💥 Tests failed. Please check your configuration.")
    
    print()
    print("📚 Next Steps:")
    print("   1. If tests passed, your API is ready to use")
    print("   2. If tests failed, fix the configuration and run again")
    print("   3. Start your FastAPI server: python main.py")
    print("   4. Test the API endpoints at http://localhost:8000/docs")

if __name__ == "__main__":
    main() 