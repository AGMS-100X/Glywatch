#!/usr/bin/env python3
"""
Manual GlyWatch Setup
This script guides you through setting up GlyWatch manually
"""

import os
import subprocess
import sys

def check_prerequisites():
    """Check if prerequisites are installed"""
    print("🔍 Checking Prerequisites...")
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js not working")
            return False
    except:
        print("❌ Node.js not found")
        return False
    
    # Check npm
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ npm: {result.stdout.strip()}")
        else:
            print("❌ npm not working")
            return False
    except:
        print("❌ npm not found")
        return False
    
    return True

def setup_nightscout_manual():
    """Set up Nightscout manually"""
    print("\n📥 Setting up Nightscout...")
    
    nightscout_dir = "./nightscout"
    
    # Clone Nightscout if not exists
    if not os.path.exists(nightscout_dir):
        print("📥 Cloning Nightscout repository...")
        try:
            subprocess.run(["git", "clone", "https://github.com/nightscout/cgm-remote-monitor.git", "nightscout"], check=True)
            print("✅ Nightscout cloned successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to clone Nightscout: {e}")
            return False
    else:
        print("✅ Nightscout directory already exists")
    
    # Install dependencies manually
    print("\n📦 Installing Nightscout dependencies...")
    print("   This may take a few minutes...")
    
    try:
        # Use shell=True for Windows
        result = subprocess.run("npm install", cwd=nightscout_dir, shell=True, check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("\n🔧 Manual npm install:")
        print(f"   cd {nightscout_dir}")
        print("   npm install")
        return False
    
    # Create environment file
    env_file_path = f"{nightscout_dir}/.env"
    
    if not os.path.exists(env_file_path):
        print("\n📋 Creating .env file...")
        env_content = """# Nightscout Configuration for GlyWatch
# Database Configuration
MONGO_CONNECTION=postgresql://postgres:$Glywatch@2103@db.kkxlmjfmjrtgiqyomzks.supabase.co:5432/postgres

# API Configuration
API_SECRET=glywatch_secret_123

# Display Settings
DISPLAY_UNITS=mg/dl

# Enabled Features
ENABLE=careportal basal dbsize rawbg iob maker cob bwp cage sage boluscalc pushover treatmentnotify loop pump profile food openaps bage iage weight heartrate

# Server Configuration
PORT=1337
HOSTNAME=0.0.0.0

# Optional: Authentication
AUTH_DEFAULT_ROLES=readable

# Optional: Timezone
TIME_FORMAT=12
"""
        
        with open(env_file_path, "w") as f:
            f.write(env_content)
        
        print("✅ Created .env file with your Supabase connection")
    else:
        print("✅ .env file already exists")
    
    return True

def main():
    print("🌙 Manual GlyWatch Setup")
    print("This will guide you through setting up GlyWatch step by step")
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met")
        print("Please install Node.js and npm first:")
        print("1. Go to https://nodejs.org/")
        print("2. Download and install Node.js LTS")
        print("3. Restart your terminal")
        print("4. Run this script again")
        return
    
    # Set up Nightscout
    if not setup_nightscout_manual():
        print("\n❌ Nightscout setup failed")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Start Nightscout:")
    print("   cd nightscout")
    print("   npm start")
    print("\n2. Start GlyWatch API (in a new terminal):")
    print("   cd glywatch-fullstack/backend")
    print("   python main.py")
    print("\n3. Test the connection:")
    print("   curl http://localhost:1337/api/v1/status.json")
    print("   curl http://localhost:8000/health")

if __name__ == "__main__":
    main() 