#!/usr/bin/env python3
"""
Setup script for PostgreSQL environment variables
"""

import os

def setup_postgres_environment():
    """Setup environment variables for PostgreSQL connection"""
    print("🔧 Setting up PostgreSQL environment variables...")
    
    # Database configuration
    os.environ['ENV'] = 'local'
    os.environ['DB_USERNAME'] = 'kycapp'
    os.environ['DB_PASSWORD'] = 'kycapp123'
    os.environ['DB_HOST'] = 'database-1-instance-1.c3iikqyyi0uu.us-east-2.rds.amazonaws.com'
    os.environ['DB_PORT'] = '5432'
    os.environ['DB_NAME'] = 'kycdb'
    
    # AWS configuration
    os.environ['AWS_REGION'] = 'us-east-2'
    os.environ['S3_BUCKET_NAME'] = 'dbdtcckycbucket'
    
    # Clear any expired AWS credentials
    if 'AWS_ACCESS_KEY_ID' in os.environ:
        del os.environ['AWS_ACCESS_KEY_ID']
    if 'AWS_SECRET_ACCESS_KEY' in os.environ:
        del os.environ['AWS_SECRET_ACCESS_KEY']
    if 'AWS_SESSION_TOKEN' in os.environ:
        del os.environ['AWS_SESSION_TOKEN']
    
    print("✅ Environment variables set:")
    print(f"  - ENV: {os.getenv('ENV')}")
    print(f"  - DB_HOST: {os.getenv('DB_HOST')}")
    print(f"  - DB_NAME: {os.getenv('DB_NAME')}")
    print(f"  - DB_USER: {os.getenv('DB_USERNAME')}")
    print(f"  - AWS_REGION: {os.getenv('AWS_REGION')}")
    print("  - AWS credentials: Cleared (using direct PostgreSQL connection)")

if __name__ == "__main__":
    setup_postgres_environment()
    print("\n🚀 You can now run:")
    print("  python test_postgres_connection.py  # Test connection")
    print("  python run_local_postgres.py        # Run application") 