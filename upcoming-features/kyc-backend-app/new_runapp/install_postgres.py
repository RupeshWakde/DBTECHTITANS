#!/usr/bin/env python3
"""
PostgreSQL Driver Installer for Windows
This script helps install PostgreSQL drivers on Windows systems
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} successful")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def check_package(package_name):
    """Check if a package is installed"""
    try:
        if package_name == 'psycopg2-binary':
            import psycopg2
        elif package_name == 'psycopg2':
            import psycopg2
        elif package_name == 'psycopg':
            import psycopg
        print(f"✅ {package_name} is already installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is not installed")
        return False

def main():
    """Main installation function"""
    print("=" * 60)
    print("🐘 PostgreSQL Driver Installer for Windows")
    print("=" * 60)
    
    # Check current Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if any PostgreSQL driver is already installed
    print("\n🔍 Checking for existing PostgreSQL drivers...")
    drivers = ['psycopg2-binary', 'psycopg2', 'psycopg']
    installed_driver = None
    
    for driver in drivers:
        if check_package(driver):
            installed_driver = driver
            break
    
    if installed_driver:
        print(f"\n✅ PostgreSQL driver already installed: {installed_driver}")
        return
    
    print("\n📦 No PostgreSQL driver found. Installing...")
    
    # Try different installation methods
    installation_methods = [
        ("pip install psycopg2-binary", "Installing psycopg2-binary"),
        ("pip install psycopg2", "Installing psycopg2"),
        ("pip install psycopg", "Installing psycopg")
    ]
    
    success = False
    for cmd, description in installation_methods:
        if run_command(cmd, description):
            success = True
            break
        else:
            print("⚠️  Trying next method...")
    
    if not success:
        print("\n❌ All installation methods failed.")
        print("\n🔧 Manual installation options:")
        print("1. Install Visual Studio Build Tools:")
        print("   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
        print("   - Install C++ build tools")
        print("   - Then run: pip install psycopg2")
        print("\n2. Use conda (if available):")
        print("   conda install psycopg2")
        print("\n3. Download pre-compiled wheel:")
        print("   - Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#psycopg")
        print("   - Download appropriate wheel for your Python version")
        print("   - Install with: pip install <wheel_file>")
        print("\n4. Use alternative driver:")
        print("   pip install asyncpg  # For async support")
        print("   pip install psycopg  # Newer driver")
        return
    
    # Verify installation
    print("\n🔍 Verifying installation...")
    for driver in drivers:
        if check_package(driver):
            print(f"\n✅ Successfully installed: {driver}")
            break
    else:
        print("\n❌ Installation verification failed")

if __name__ == "__main__":
    main() 