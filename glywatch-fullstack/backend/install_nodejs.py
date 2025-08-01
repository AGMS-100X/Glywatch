#!/usr/bin/env python3
"""
Node.js Installer Helper for Windows
"""

import subprocess
import sys
import webbrowser
import os

def check_nodejs():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js is already installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm is already installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    return False

def install_nodejs():
    """Guide user to install Node.js"""
    print("🔧 Node.js Installation Guide")
    print("=" * 50)
    
    print("\n📋 Steps to install Node.js:")
    print("1. Go to https://nodejs.org/")
    print("2. Download the LTS version (recommended)")
    print("3. Run the installer")
    print("4. Follow the installation wizard")
    print("5. Restart your terminal/command prompt")
    print("6. Run this script again")
    
    # Open the Node.js download page
    print("\n🌐 Opening Node.js download page...")
    try:
        webbrowser.open("https://nodejs.org/")
    except:
        print("   Please manually visit: https://nodejs.org/")
    
    print("\n📝 After installing Node.js:")
    print("   - Close this terminal/command prompt")
    print("   - Open a new terminal/command prompt")
    print("   - Navigate back to this directory")
    print("   - Run: python setup_complete_system.py")

def main():
    print("🚀 Node.js Installation Helper")
    print("This will help you install Node.js for GlyWatch setup")
    
    if check_nodejs():
        print("\n🎉 Node.js is already installed!")
        print("You can now run: python setup_complete_system.py")
        return
    
    print("\n❌ Node.js is not installed")
    install_nodejs()
    
    input("\nPress Enter when you've installed Node.js and restarted your terminal...")
    
    # Check again after user confirms installation
    if check_nodejs():
        print("\n🎉 Node.js installation successful!")
        print("You can now run: python setup_complete_system.py")
    else:
        print("\n❌ Node.js is still not found")
        print("Please make sure to:")
        print("1. Install Node.js from https://nodejs.org/")
        print("2. Restart your terminal/command prompt")
        print("3. Try running this script again")

if __name__ == "__main__":
    main() 