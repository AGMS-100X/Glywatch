#!/usr/bin/env python3
"""
GlyWatch Setup Without npm (Alternative Method)
This script sets up GlyWatch without requiring npm to be in PATH
"""

import os
import subprocess
import sys
import time

# Try to import requests, install if missing
try:
    import requests
except ImportError:
    print("📦 Installing requests module...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

def find_nodejs():
    """Find Node.js installation"""
    possible_paths = [
        r"C:\Program Files\nodejs\node.exe",
        r"C:\Program Files (x86)\nodejs\node.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\nodejs\node.exe")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def find_npm():
    """Find npm installation"""
    possible_paths = [
        r"C:\Program Files\nodejs\npm.cmd",
        r"C:\Program Files (x86)\nodejs\npm.cmd",
        os.path.expanduser(r"~\AppData\Local\Programs\nodejs\npm.cmd")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def run_command_with_path(command, description, cwd=None):
    """Run a command with full path if needed"""
    print(f"\n🔧 {description}")
    print(f"   Running: {command}")
    
    try:
        # Try with PATH first
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            shell=True  # Use shell=True for Windows
        )
        print(f"   ✅ Success")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Try with full path
        if "npm" in command:
            npm_path = find_npm()
            if npm_path:
                try:
                    # Replace npm with full path
                    full_command = command.replace("npm", f'"{npm_path}"')
                    result = subprocess.run(
                        full_command,
                        cwd=cwd,
                        capture_output=True,
                        text=True,
                        check=True,
                        shell=True  # Use shell=True for Windows
                    )
                    print(f"   ✅ Success (using full path)")
                    return True
                except subprocess.CalledProcessError as e:
                    print(f"   ❌ Failed: {e.stderr}")
                    return False
            else:
                print(f"   ❌ npm not found in common locations")
                return False
        else:
            print(f"   ❌ Command not found")
            return False

def setup_without_npm():
    """Set up GlyWatch without requiring npm in PATH"""
    print("🌙 GlyWatch Setup (Alternative Method)")
    print("This will set up GlyWatch without requiring npm to be in PATH")
    
    # Check if Node.js is installed
    nodejs_path = find_nodejs()
    npm_path = find_npm()
    
    if not nodejs_path:
        print("❌ Node.js not found in common locations")
        print("   Please install Node.js from https://nodejs.org/")
        return False
    
    print(f"✅ Found Node.js: {nodejs_path}")
    
    if not npm_path:
        print("❌ npm not found in common locations")
        print("   Please reinstall Node.js and make sure to check 'Add to PATH'")
        return False
    
    print(f"✅ Found npm: {npm_path}")
    
    # Set up Nightscout
    print("\n📥 Setting up Nightscout...")
    
    nightscout_dir = "./nightscout"
    
    # Clone Nightscout if not exists
    if not os.path.exists(nightscout_dir):
        print("📥 Cloning Nightscout repository...")
        if not run_command_with_path("git clone https://github.com/nightscout/cgm-remote-monitor.git nightscout", "Cloning Nightscout"):
            return False
    
    # Install dependencies using full npm path
    print("📦 Installing Nightscout dependencies...")
    npm_install_cmd = f'"{npm_path}" install'
    if not run_command_with_path(npm_install_cmd, "Installing Nightscout dependencies", cwd=nightscout_dir):
        return False
    
    # Create environment file
    env_file_path = f"{nightscout_dir}/.env"
    
    if not os.path.exists(env_file_path):
        print("📋 Creating .env file...")
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
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Start Nightscout: cd nightscout && npm start")
    print("2. Start GlyWatch API: python main.py")
    print("3. Test the connection: curl http://localhost:1337/api/v1/status.json")
    
    return True

if __name__ == "__main__":
    setup_without_npm() 