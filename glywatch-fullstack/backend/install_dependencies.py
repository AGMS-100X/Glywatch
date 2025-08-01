#!/usr/bin/env python3
"""
Quick dependency installer for GlyWatch setup
"""

import subprocess
import sys

def install_dependencies():
    print("📦 Installing GlyWatch dependencies...")
    
    # Install from requirements.txt
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

if __name__ == "__main__":
    print("🚀 GlyWatch Dependency Installer")
    print("This will install all required Python packages...")
    
    if install_dependencies():
        print("\n🎉 Dependencies installed! You can now run:")
        print("   python setup_complete_system.py")
    else:
        print("\n❌ Installation failed. Please check your Python environment.") 