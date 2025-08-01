#!/usr/bin/env python3
"""
Complete GlyWatch System Setup Script
This script sets up the entire GlyWatch system with local Nightscout and Supabase
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

def print_step(step_num, title):
    print(f"\n{'='*60}")
    print(f"Step {step_num}: {title}")
    print(f"{'='*60}")

def run_command(command, description, cwd=None):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}")
    print(f"   Running: {command}")
    
    try:
        result = subprocess.run(
            command.split(),
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"   ✅ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed: {e.stderr}")
        return False

def install_python_dependencies():
    """Install required Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    dependencies = [
        "fastapi",
        "uvicorn",
        "requests",
        "supabase",
        "postgrest"
    ]
    
    for dep in dependencies:
        try:
            __import__(dep.replace("-", "_"))
            print(f"   ✅ {dep} already installed")
        except ImportError:
            print(f"   📦 Installing {dep}...")
            if not run_command(f"pip install {dep}", f"Installing {dep}"):
                return False
    
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print_step(1, "Checking Dependencies")
    
    # Install Python dependencies first
    if not install_python_dependencies():
        print("❌ Failed to install Python dependencies")
        return False
    
    # Check Node.js
    print("\n🔧 Checking Node.js...")
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        print(f"   ✅ Node.js version: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js is not installed or not in PATH")
        print("   Please install Node.js from: https://nodejs.org/")
        print("   After installation, restart your terminal and try again")
        return False
    
    # Check npm
    print("\n🔧 Checking npm...")
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, check=True)
        print(f"   ✅ npm version: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm is not installed or not in PATH")
        print("   Please install Node.js (which includes npm) from: https://nodejs.org/")
        print("   After installation, restart your terminal and try again")
        return False
    
    return True

def setup_nightscout():
    """Set up Nightscout locally"""
    print_step(2, "Setting up Nightscout")
    
    nightscout_dir = "./nightscout"
    
    # Clone Nightscout if not exists
    if not os.path.exists(nightscout_dir):
        print("📥 Cloning Nightscout repository...")
        if not run_command("git clone https://github.com/nightscout/cgm-remote-monitor.git nightscout", "Cloning Nightscout"):
            return False
    
    # Install dependencies
    if not run_command("npm install", "Installing Nightscout dependencies", cwd=nightscout_dir):
        return False
    
    # Create environment file using the correct template
    env_file_path = f"{nightscout_dir}/.env"
    
    # Check if .env already exists
    if os.path.exists(env_file_path):
        print("✅ .env file already exists")
    else:
        # Copy the example template from docs directory
        template_path = f"{nightscout_dir}/docs/example-template.env"
        
        if os.path.exists(template_path):
            print("📋 Using Nightscout's example template...")
            # Copy the template file
            if not run_command(f"cp {template_path} {env_file_path}", "Copying example template"):
                return False
            
            # Read the template and modify it for GlyWatch
            with open(env_file_path, "r") as f:
                env_content = f.read()
            
            # Update the template for GlyWatch with Supabase
            env_content = env_content.replace(
                "CUSTOMCONNSTR_mongo=mongodb://....",
                "MONGO_CONNECTION=postgresql://postgres:$Glywatch@2103@db.kkxlmjfmjrtgiqyomzks.supabase.co:5432/postgres"
            )
            
            # Update other settings for GlyWatch
            env_content = env_content.replace(
                "API_SECRET=1234567890abc",
                "API_SECRET=glywatch_secret_123"
            )
            
            env_content = env_content.replace(
                'DISPLAY_UNITS="mmol"',
                'DISPLAY_UNITS="mg/dl"'
            )
            
            env_content = env_content.replace(
                'ENABLE="devicestatus rawbg upbat careportal iob profile cage bage avg cob basal treatments sage boluscalc pump openaps iage speech"',
                'ENABLE="careportal basal dbsize rawbg iob maker cob bwp cage sage boluscalc pushover treatmentnotify loop pump profile food openaps bage iage weight heartrate"'
            )
            
            # Add GlyWatch-specific settings
            env_content += """
# GlyWatch Specific Settings
AUTH_DEFAULT_ROLES=readable
TIME_FORMAT=12
"""
            
            # Write the updated content
            with open(env_file_path, "w") as f:
                f.write(env_content)
            
            print("✅ Created .env file from Nightscout template")
            print("   Note: Update the MONGO_CONNECTION with your Supabase PostgreSQL connection string")
        else:
            print("❌ Example template not found, creating basic .env file...")
            # Create a basic .env file as fallback
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
            
            print("✅ Created basic .env file")
            print("   Note: Update the MONGO_CONNECTION with your Supabase PostgreSQL connection string")
    
    return True

def setup_supabase():
    """Guide user through Supabase setup"""
    print_step(3, "Setting up Supabase")
    
    print("📋 Supabase Setup Instructions:")
    print("1. Go to https://supabase.com")
    print("2. Create a new project")
    print("3. Go to Settings → Database")
    print("4. Copy your PostgreSQL connection string")
    print("5. Update the Nightscout .env file with your connection string")
    print("6. Go to SQL Editor and run the contents of supabase_tables.sql")
    
    input("\nPress Enter when you've completed the Supabase setup...")
    return True

def setup_glywatch():
    """Set up GlyWatch backend"""
    print_step(4, "Setting up GlyWatch Backend")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Run environment setup
    print("\n🔧 Setting up environment variables...")
    if not run_command("python setup_env.py", "Running environment setup"):
        return False
    
    return True

def test_system():
    """Test the complete system"""
    print_step(5, "Testing the System")
    
    # Start Nightscout
    print("🚀 Starting Nightscout...")
    nightscout_process = subprocess.Popen(
        ["npm", "start"],
        cwd="./nightscout",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for Nightscout to start
    print("⏳ Waiting for Nightscout to start...")
    time.sleep(15)  # Increased wait time
    
    # Test Nightscout connection
    try:
        response = requests.get("http://localhost:1337/api/v1/status.json", timeout=15)
        if response.status_code == 200:
            print("✅ Nightscout is running")
        else:
            print("⚠️  Nightscout responded but status check failed")
    except:
        print("❌ Nightscout is not responding")
        print("   This might be due to database connection issues")
        print("   Make sure to update the .env file with your Supabase connection string")
        return False
    
    # Start GlyWatch API
    print("🚀 Starting GlyWatch API...")
    glywatch_process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for GlyWatch to start
    print("⏳ Waiting for GlyWatch API to start...")
    time.sleep(5)
    
    # Test GlyWatch API
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("✅ GlyWatch API is running")
        else:
            print("⚠️  GlyWatch API responded but health check failed")
    except:
        print("❌ GlyWatch API is not responding")
        return False
    
    # Test connections
    print("\n🔍 Testing connections...")
    if not run_command("python test_nightscout.py", "Testing Nightscout connection"):
        return False
    
    print("\n🎉 System is ready!")
    print("\n📋 Next Steps:")
    print("1. Visit http://localhost:8000/docs for API documentation")
    print("2. Visit http://localhost:1337 for Nightscout web interface")
    print("3. Test user registration: POST /users/register")
    print("4. Test glucose data: GET /cgm/latest/{user_id}")
    
    return True

def main():
    """Main setup function"""
    print("🌙 GlyWatch Complete System Setup")
    print("This will set up GlyWatch with local Nightscout and Supabase")
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Setup failed. Please install missing dependencies.")
        return
    
    # Setup Nightscout
    if not setup_nightscout():
        print("\n❌ Nightscout setup failed.")
        return
    
    # Setup Supabase
    if not setup_supabase():
        print("\n❌ Supabase setup failed.")
        return
    
    # Setup GlyWatch
    if not setup_glywatch():
        print("\n❌ GlyWatch setup failed.")
        return
    
    # Test system
    if not test_system():
        print("\n❌ System test failed.")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n📚 Documentation:")
    print("- Complete Setup Guide: COMPLETE_SETUP_GUIDE.md")
    print("- API Documentation: http://localhost:8000/docs")
    print("- Nightscout Interface: http://localhost:1337")

if __name__ == "__main__":
    main() 