#!/usr/bin/env python3
"""
Helper script to set up Nightscout and Supabase environment variables
"""

import os
import sys

def setup_environment():
    """Interactive setup for Nightscout and Supabase environment variables"""
    print("🌙 GlyWatch Environment Setup")
    print("=" * 50)
    print()
    
    # Get Nightscout URL
    print("Step 1: Nightscout Configuration")
    print("-" * 35)
    current_url = os.getenv("NIGHTSCOUT_URL", "")
    if current_url and current_url != "https://your-nightscout-instance.herokuapp.com":
        print(f"Current Nightscout URL: {current_url}")
        change = input("Do you want to change it? (y/N): ").lower().strip()
        if change != 'y':
            nightscout_url = current_url
        else:
            nightscout_url = input("Enter your Nightscout URL: ").strip()
    else:
        print("Example: https://your-nightscout.herokuapp.com")
        nightscout_url = input("Enter your Nightscout URL: ").strip()
    
    if not nightscout_url:
        print("❌ Nightscout URL is required!")
        return False
    
    # Get Nightscout API Secret
    print()
    current_secret = os.getenv("NIGHTSCOUT_API_SECRET", "")
    if current_secret:
        print("Nightscout API Secret is already set")
        change = input("Do you want to change it? (y/N): ").lower().strip()
        if change != 'y':
            api_secret = current_secret
        else:
            api_secret = input("Enter your Nightscout API Secret (or press Enter to skip): ").strip()
    else:
        print("Note: Only needed if your Nightscout requires authentication")
        api_secret = input("Enter your Nightscout API Secret (or press Enter to skip): ").strip()
    
    # Get Nightscout Timeout
    current_timeout = os.getenv("NIGHTSCOUT_TIMEOUT", "30")
    print(f"Current Nightscout timeout: {current_timeout} seconds")
    change = input("Do you want to change it? (y/N): ").lower().strip()
    if change == 'y':
        timeout = input("Enter timeout in seconds (default: 30): ").strip()
        if not timeout:
            timeout = "30"
    else:
        timeout = current_timeout
    
    # Get Supabase URL
    print()
    print("Step 2: Supabase Configuration")
    print("-" * 35)
    current_supabase_url = os.getenv("SUPABASE_URL", "")
    if current_supabase_url:
        print(f"Current Supabase URL: {current_supabase_url}")
        change = input("Do you want to change it? (y/N): ").lower().strip()
        if change != 'y':
            supabase_url = current_supabase_url
        else:
            supabase_url = input("Enter your Supabase URL: ").strip()
    else:
        print("Example: https://your-project.supabase.co")
        supabase_url = input("Enter your Supabase URL: ").strip()
    
    if not supabase_url:
        print("⚠️  Supabase URL is optional but recommended for data persistence")
        supabase_url = ""
    
    # Get Supabase Anon Key
    current_supabase_key = os.getenv("SUPABASE_ANON_KEY", "")
    if current_supabase_key:
        print("Supabase Anon Key is already set")
        change = input("Do you want to change it? (y/N): ").lower().strip()
        if change != 'y':
            supabase_key = current_supabase_key
        else:
            supabase_key = input("Enter your Supabase Anon Key: ").strip()
    else:
        supabase_key = input("Enter your Supabase Anon Key: ").strip()
    
    # Get Supabase Service Key (optional)
    current_service_key = os.getenv("SUPABASE_SERVICE_KEY", "")
    if current_service_key:
        print("Supabase Service Key is already set")
        change = input("Do you want to change it? (y/N): ").lower().strip()
        if change != 'y':
            supabase_service_key = current_service_key
        else:
            supabase_service_key = input("Enter your Supabase Service Key (optional): ").strip()
    else:
        supabase_service_key = input("Enter your Supabase Service Key (optional): ").strip()
    
    # Create .env file content
    env_content = f"""# Nightscout Configuration
NIGHTSCOUT_URL={nightscout_url}
NIGHTSCOUT_API_SECRET={api_secret}
NIGHTSCOUT_TIMEOUT={timeout}

# Supabase Configuration
SUPABASE_URL={supabase_url}
SUPABASE_ANON_KEY={supabase_key}
SUPABASE_SERVICE_KEY={supabase_service_key}
"""
    
    # Write to .env file
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print()
        print("✅ Environment variables saved to .env file")
        print()
        print("📋 Configuration Summary:")
        print(f"   Nightscout URL: {nightscout_url}")
        print(f"   Nightscout API Secret: {'Set' if api_secret else 'Not set'}")
        print(f"   Nightscout Timeout: {timeout} seconds")
        print(f"   Supabase URL: {supabase_url or 'Not set'}")
        print(f"   Supabase Anon Key: {'Set' if supabase_key else 'Not set'}")
        print(f"   Supabase Service Key: {'Set' if supabase_service_key else 'Not set'}")
        print()
        print("🚀 Next steps:")
        print("   1. Set up Supabase tables: Run the SQL in supabase_tables.sql")
        print("   2. Test connections: python test_nightscout.py")
        print("   3. Test all endpoints: python test_all_endpoints.py")
        print("   4. Start server: python main.py")
        print("   5. Visit: http://localhost:8000/docs")
        return True
        
    except Exception as e:
        print(f"❌ Error saving .env file: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage: python setup_env.py")
        print("This script will help you set up Nightscout and Supabase environment variables.")
        return
    
    success = setup_environment()
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 