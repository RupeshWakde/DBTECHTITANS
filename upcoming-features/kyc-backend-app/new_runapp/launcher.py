#!/usr/bin/env python3
"""
KYC API Application Launcher
A simple launcher that reads configuration and runs the application
"""

import json
import sys
import os
from pathlib import Path

def load_config():
    """Load configuration from config.json"""
    config_path = Path(__file__).parent / "config.json"
    
    if not config_path.exists():
        print("❌ Configuration file not found: config.json")
        return None
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing configuration file: {e}")
        return None
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return None

def print_usage():
    """Print usage information"""
    print("🎯 KYC API Application Launcher")
    print("=" * 50)
    print("Usage:")
    print("  python launcher.py [environment] [options]")
    print("")
    print("Environments:")
    print("  dev, development    - Development mode")
    print("  prod, production    - Production mode")
    print("  test, testing       - Testing mode")
    print("")
    print("Options:")
    print("  --help, -h          - Show this help")
    print("  --config            - Show current configuration")
    print("")
    print("Examples:")
    print("  python launcher.py dev")
    print("  python launcher.py production")
    print("  python launcher.py test --config")

def show_config(config):
    """Show current configuration"""
    print("📋 Current Configuration:")
    print("=" * 50)
    
    for env_name, env_config in config["environments"].items():
        print(f"\n{env_name.upper()}:")
        for key, value in env_config.items():
            print(f"  {key}: {value}")

def build_command(env_config, args):
    """Build the command to run the application"""
    cmd = ["python", "run_app.py"]
    
    # Add configuration from environment
    if env_config.get("host"):
        cmd.extend(["--host", env_config["host"]])
    
    if env_config.get("port"):
        cmd.extend(["--port", str(env_config["port"])])
    
    if env_config.get("workers"):
        cmd.extend(["--workers", str(env_config["workers"])])
    
    if env_config.get("dev_mode"):
        cmd.append("--dev")
    
    if env_config.get("health_check"):
        cmd.append("--health-check")
    
    # Add any additional arguments
    cmd.extend(args)
    
    return cmd

def main():
    """Main launcher function"""
    # Load configuration
    config = load_config()
    if not config:
        sys.exit(1)
    
    # Parse arguments
    args = sys.argv[1:]
    
    if not args or "--help" in args or "-h" in args:
        print_usage()
        return
    
    if "--config" in args:
        show_config(config)
        return
    
    # Determine environment
    env_name = args[0].lower()
    remaining_args = args[1:]
    
    # Map environment names
    env_mapping = {
        "dev": "development",
        "development": "development",
        "prod": "production", 
        "production": "production",
        "test": "testing",
        "testing": "testing"
    }
    
    if env_name not in env_mapping:
        print(f"❌ Unknown environment: {env_name}")
        print("Available environments: dev, production, test")
        sys.exit(1)
    
    env_key = env_mapping[env_name]
    env_config = config["environments"].get(env_key)
    
    if not env_config:
        print(f"❌ Environment configuration not found: {env_key}")
        sys.exit(1)
    
    print(f"🚀 Launching KYC API in {env_key} mode...")
    print(f"📍 Host: {env_config.get('host', '0.0.0.0')}")
    print(f"🔌 Port: {env_config.get('port', 8000)}")
    print(f"🔄 Dev Mode: {env_config.get('dev_mode', False)}")
    print(f"👥 Workers: {env_config.get('workers', 1)}")
    print(f"🏥 Health Check: {env_config.get('health_check', False)}")
    print()
    
    # Build and execute command
    cmd = build_command(env_config, remaining_args)
    
    print(f"Executing: {' '.join(cmd)}")
    print()
    
    # Change to parent directory
    parent_dir = Path(__file__).parent.parent
    os.chdir(parent_dir)
    
    # Run the command
    try:
        import subprocess
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Application failed with exit code: {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 