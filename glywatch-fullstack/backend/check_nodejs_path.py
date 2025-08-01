#!/usr/bin/env python3
"""
Check Node.js Installation and PATH
"""

import subprocess
import os
import sys

def check_nodejs_installation():
    """Check if Node.js is installed and accessible"""
    print("🔍 Checking Node.js Installation...")
    
    # Check common Node.js installation paths
    possible_paths = [
        r"C:\Program Files\nodejs",
        r"C:\Program Files (x86)\nodejs",
        os.path.expanduser(r"~\AppData\Roaming\npm"),
        os.path.expanduser(r"~\AppData\Local\Programs\nodejs")
    ]
    
    print("\n📁 Checking common installation paths:")
    for path in possible_paths:
        if os.path.exists(path):
            print(f"   ✅ Found: {path}")
        else:
            print(f"   ❌ Not found: {path}")
    
    # Check PATH environment variable
    print("\n🔍 Checking PATH environment variable:")
    path_dirs = os.environ.get('PATH', '').split(';')
    nodejs_in_path = False
    npm_in_path = False
    
    for dir_path in path_dirs:
        if 'nodejs' in dir_path.lower():
            print(f"   ✅ Found Node.js in PATH: {dir_path}")
            nodejs_in_path = True
        if 'npm' in dir_path.lower():
            print(f"   ✅ Found npm in PATH: {dir_path}")
            npm_in_path = True
    
    if not nodejs_in_path:
        print("   ❌ Node.js not found in PATH")
    if not npm_in_path:
        print("   ❌ npm not found in PATH")
    
    # Try to run node and npm commands
    print("\n🔧 Testing node and npm commands:")
    
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"   ✅ node command works: {result.stdout.strip()}")
        else:
            print(f"   ❌ node command failed: {result.stderr}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("   ❌ node command not found")
    
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"   ✅ npm command works: {result.stdout.strip()}")
        else:
            print(f"   ❌ npm command failed: {result.stderr}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("   ❌ npm command not found")
    
    return nodejs_in_path and npm_in_path

def fix_path_issue():
    """Provide instructions to fix PATH issues"""
    print("\n🔧 How to Fix PATH Issues:")
    print("=" * 50)
    
    print("\n📋 Option 1: Reinstall Node.js")
    print("1. Uninstall Node.js from Control Panel")
    print("2. Download Node.js from https://nodejs.org/")
    print("3. Run the installer and make sure to check 'Add to PATH'")
    print("4. Restart your computer")
    
    print("\n📋 Option 2: Manual PATH Fix")
    print("1. Press Win + R, type 'sysdm.cpl', press Enter")
    print("2. Go to 'Advanced' tab, click 'Environment Variables'")
    print("3. Under 'System Variables', find 'Path', click 'Edit'")
    print("4. Add these paths if they don't exist:")
    print("   C:\\Program Files\\nodejs\\")
    print("   %APPDATA%\\npm")
    print("5. Click OK, restart your terminal")
    
    print("\n📋 Option 3: Use Full Path")
    print("If Node.js is installed but not in PATH, you can use the full path:")
    print("   C:\\Program Files\\nodejs\\node.exe --version")
    print("   C:\\Program Files\\nodejs\\npm.cmd --version")

def main():
    print("🚀 Node.js PATH Checker")
    print("This will help diagnose Node.js installation issues")
    
    is_installed = check_nodejs_installation()
    
    if is_installed:
        print("\n🎉 Node.js is properly installed and in PATH!")
        print("You can now run: python setup_complete_system.py")
    else:
        print("\n❌ Node.js is not properly installed or not in PATH")
        fix_path_issue()
        
        print("\n📝 After fixing the PATH:")
        print("1. Close all terminal windows")
        print("2. Open a new terminal")
        print("3. Navigate to your project directory")
        print("4. Run: python setup_complete_system.py")

if __name__ == "__main__":
    main() 