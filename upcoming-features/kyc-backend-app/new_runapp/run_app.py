#!/usr/bin/env python3
"""
KYC API Application Runner
This script provides a comprehensive way to run the KYC FastAPI application
with proper configuration, environment setup, and error handling.
"""

import os
import sys
import subprocess
import argparse
import signal
import time
from pathlib import Path
import uvicorn
from typing import Optional

# Add the parent directory to the Python path to import application modules
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Import application modules
try:
    from main import app
    from database import init_db, get_engine
    from config import get_settings
    from storage import storage
except ImportError as e:
    print(f"❌ Error importing application modules: {e}")
    print("Make sure you're running this script from the correct directory")
    sys.exit(1)

class KYCAppRunner:
    """Main application runner class"""
    
    def __init__(self):
        self.settings = get_settings()
        self.host = "0.0.0.0"
        self.port = 8000
        self.reload = False
        self.workers = 1
        self.process = None
        
    def setup_environment(self):
        """Setup environment variables and configuration"""
        print("🔧 Setting up environment...")
        
        # Set environment to AWS by default
        os.environ["ENV"] = "aws"
        
        # Check if we're in development mode
        if "--dev" in sys.argv or "-d" in sys.argv:
            os.environ["ENV"] = "local"
            self.reload = True
            print("🐛 Development mode enabled")
        
        print(f"✅ Environment set to: {os.environ.get('ENV', 'aws')}")
        
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        print("📦 Checking dependencies...")
        
        required_packages = [
            'fastapi',
            'uvicorn',
            'sqlalchemy',
            'pydantic',
            'boto3'
        ]
        
        # PostgreSQL driver - check for alternatives
        postgres_packages = ['psycopg2-binary', 'psycopg2', 'psycopg']
        postgres_found = False
        
        for package in postgres_packages:
            try:
                if package == 'psycopg2-binary':
                    import psycopg2
                elif package == 'psycopg2':
                    import psycopg2
                elif package == 'psycopg':
                    import psycopg
                postgres_found = True
                print(f"✅ PostgreSQL driver found: {package}")
                break
            except ImportError:
                continue
        
        if not postgres_found:
            print("⚠️  PostgreSQL driver not found. Trying alternatives...")
            print("   Available options:")
            print("   1. pip install psycopg2-binary")
            print("   2. pip install psycopg2")
            print("   3. pip install psycopg")
            print("   Note: On Windows, psycopg2-binary might fail. Try psycopg2 instead.")
            print("   Continuing without PostgreSQL driver check...")
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")
            print("Please install missing packages using: pip install -r requirements.txt")
            return False
        
        print("✅ All core dependencies are installed")
        return True
    
    def initialize_database(self):
        """Initialize the database connection"""
        print("🗄️  Initializing database...")
        
        try:
            init_db()
            print("✅ Database initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            return False
    
    def test_storage_connection(self):
        """Test storage (S3) connection"""
        print("☁️  Testing storage connection...")
        
        try:
            # Test S3 connection by trying to list buckets
            storage.test_connection()
            print("✅ Storage connection successful")
            return True
        except Exception as e:
            print(f"⚠️  Storage connection warning: {e}")
            print("Application will continue but file uploads may not work")
            return True  # Don't fail the startup for storage issues
    
    def run_health_check(self):
        """Run a health check on the application"""
        print("🏥 Running health check...")
        
        try:
            import requests
            import time
            
            # Wait a moment for the server to start
            time.sleep(2)
            
            response = requests.get(f"http://localhost:{self.port}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Health check passed: {health_data}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️  Health check warning: {e}")
            return True  # Don't fail startup for health check issues
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
        
        print("✅ Application shutdown complete")
        sys.exit(0)
    
    def run_application(self):
        """Run the FastAPI application"""
        print("🚀 Starting KYC API Application...")
        print(f"📍 Host: {self.host}")
        print(f"🔌 Port: {self.port}")
        print(f"🔄 Reload: {self.reload}")
        print(f"👥 Workers: {self.workers}")
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Run the application
            uvicorn.run(
                "main:app",
                host=self.host,
                port=self.port,
                reload=self.reload,
                workers=self.workers,
                log_level="info",
                access_log=True
            )
        except KeyboardInterrupt:
            print("\n🛑 Application stopped by user")
        except Exception as e:
            print(f"❌ Application failed to start: {e}")
            sys.exit(1)
    
    def run_with_subprocess(self):
        """Run the application using subprocess (alternative method)"""
        print("🚀 Starting KYC API Application using subprocess...")
        
        cmd = [
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", self.host,
            "--port", str(self.port),
            "--log-level", "info"
        ]
        
        if self.reload:
            cmd.append("--reload")
        
        if self.workers > 1:
            cmd.extend(["--workers", str(self.workers)])
        
        try:
            self.process = subprocess.Popen(cmd, cwd=parent_dir)
            print(f"✅ Application started with PID: {self.process.pid}")
            
            # Wait for the process
            self.process.wait()
            
        except KeyboardInterrupt:
            print("\n🛑 Stopping application...")
            if self.process:
                self.process.terminate()
                self.process.wait()
        except Exception as e:
            print(f"❌ Application failed: {e}")
            sys.exit(1)
    
    def run(self, use_subprocess=False):
        """Main run method"""
        print("=" * 60)
        print("🎯 KYC API Application Runner")
        print("=" * 60)
        
        # Setup environment
        self.setup_environment()
        
        # Check dependencies
        if not self.check_dependencies():
            sys.exit(1)
        
        # Initialize database
        if not self.initialize_database():
            print("⚠️  Continuing without database initialization...")
        
        # Test storage connection
        self.test_storage_connection()
        
        # Run the application
        if use_subprocess:
            self.run_with_subprocess()
        else:
            self.run_application()
        
        # Run health check if requested
        if "--health-check" in sys.argv:
            self.run_health_check()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="KYC API Application Runner")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--dev", "-d", action="store_true", help="Enable development mode with auto-reload")
    parser.add_argument("--workers", type=int, default=1, help="Number of worker processes")
    parser.add_argument("--subprocess", action="store_true", help="Use subprocess to run the application")
    parser.add_argument("--health-check", action="store_true", help="Run health check after startup")
    
    args = parser.parse_args()
    
    # Create runner instance
    runner = KYCAppRunner()
    runner.host = args.host
    runner.port = args.port
    runner.reload = args.dev
    runner.workers = args.workers
    
    # Run the application
    runner.run(use_subprocess=args.subprocess)

if __name__ == "__main__":
    main() 