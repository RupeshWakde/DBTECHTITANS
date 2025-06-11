#!/usr/bin/env python3
"""
Database Secrets Retrieval Script
This script retrieves database credentials in plaintext from AWS Secrets Manager
and environment variables for the KYC API application.
"""

import boto3
import json
import os
import sys
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Dict, Optional
from datetime import datetime


def get_aws_secret() -> Dict[str, str]:
    """
    Get database credentials from AWS Secrets Manager
    Returns the secret as a dictionary
    """
    secret_name = "rds!cluster-cbb2d3bf-4194-454c-9b9b-1094e7916326"
    region_name = "us-east-2"

    print(f"🔍 Attempting to retrieve secret: {secret_name}")
    print(f"🌍 AWS Region: {region_name}")

    # Check if we have AWS credentials
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_session_token = os.getenv('AWS_SESSION_TOKEN')
    aws_profile = os.getenv('AWS_PROFILE')

    if not (aws_access_key or aws_profile):
        print("⚠️  AWS credentials not found in environment variables")
        print("   Available AWS environment variables:")
        print(f"   - AWS_ACCESS_KEY_ID: {'Set' if aws_access_key else 'Not set'}")
        print(f"   - AWS_SECRET_ACCESS_KEY: {'Set' if aws_secret_key else 'Not set'}")
        print(f"   - AWS_SESSION_TOKEN: {'Set' if aws_session_token else 'Not set'}")
        print(f"   - AWS_PROFILE: {'Set' if aws_profile else 'Not set'}")
        return {}

    # Create a Secrets Manager client
    try:
        if aws_profile:
            session = boto3.session.Session(profile_name=aws_profile)
        else:
            session = boto3.session.Session()
            
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        print("✅ AWS Secrets Manager client created successfully")
        
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        
        print("✅ Secret retrieved successfully from AWS Secrets Manager")
        
    except (ClientError, NoCredentialsError) as e:
        error_code = getattr(e, 'response', {}).get('Error', {}).get('Code', 'Unknown')
        print(f"❌ Error accessing AWS Secrets Manager:")
        print(f"   Error Code: {error_code}")
        print(f"   Error Message: {str(e)}")
        
        if error_code == 'ExpiredTokenException':
            print("   💡 AWS session token has expired")
        elif error_code == 'AccessDeniedException':
            print("   💡 Access denied - check your AWS permissions")
        elif error_code == 'ResourceNotFoundException':
            print("   💡 Secret not found - check the secret name")
        
        return {}

    secret = get_secret_value_response['SecretString']
    
    # Parse the JSON secret string
    try:
        secret_dict = json.loads(secret)
        print("✅ Secret JSON parsed successfully")
        return secret_dict
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse secret JSON: {e}")
        return {}


def get_environment_credentials() -> Dict[str, str]:
    """
    Get database credentials from environment variables
    Returns the credentials as a dictionary
    """
    print("🔍 Retrieving credentials from environment variables...")
    
    credentials = {
        'username': os.getenv('DB_USERNAME', 'kycapp'),
        'password': os.getenv('DB_PASSWORD', 'kycapp123'),
        'host': os.getenv('DB_HOST', 'database-1-instance-1.c3iikqyyi0uu.us-east-2.rds.amazonaws.com'),
        'port': os.getenv('DB_PORT', '5432'),
        'dbname': os.getenv('DB_NAME', 'kycdb')
    }
    
    print("✅ Environment credentials retrieved")
    return credentials


def get_database_url(credentials: Dict[str, str]) -> str:
    """
    Construct DATABASE_URL from credentials
    """
    username = credentials.get('username', '')
    password = credentials.get('password', '')
    host = credentials.get('host', '')
    port = credentials.get('port', '5432')
    dbname = credentials.get('dbname', '')
    
    database_url = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
    return database_url


def display_credentials(credentials: Dict[str, str], source: str):
    """
    Display credentials in a formatted way
    """
    print(f"\n{'='*60}")
    print(f"📋 DATABASE CREDENTIALS ({source.upper()})")
    print(f"{'='*60}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    for key, value in credentials.items():
        if key == 'password':
            print(f"{key:12}: {'*' * len(value)} ({len(value)} characters)")
        else:
            print(f"{key:12}: {value}")
    
    # Construct and display database URL
    db_url = get_database_url(credentials)
    masked_url = db_url.replace(credentials.get('password', ''), '*' * len(credentials.get('password', '')))
    print(f"{'='*60}")
    print(f"Database URL: {masked_url}")
    print(f"{'='*60}")


def display_plaintext_credentials(credentials: Dict[str, str], source: str):
    """
    Display credentials in plaintext (use with caution)
    """
    print(f"\n{'='*60}")
    print(f"🔓 PLAINTEXT DATABASE CREDENTIALS ({source.upper()})")
    print(f"{'='*60}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    for key, value in credentials.items():
        print(f"{key:12}: {value}")
    
    # Construct and display database URL
    db_url = get_database_url(credentials)
    print(f"{'='*60}")
    print(f"Database URL: {db_url}")
    print(f"{'='*60}")


def main():
    """
    Main function to retrieve and display database secrets
    """
    print("🚀 Database Secrets Retrieval Script")
    print("=" * 50)
    
    # Try to get secrets from AWS Secrets Manager first
    aws_secrets = get_aws_secret()
    
    if aws_secrets:
        print("\n✅ Successfully retrieved secrets from AWS Secrets Manager")
        display_credentials(aws_secrets, "AWS Secrets Manager")
        
        # Ask user if they want to see plaintext
        response = input("\n🔓 Do you want to see the credentials in plaintext? (y/N): ")
        if response.lower() in ['y', 'yes']:
            display_plaintext_credentials(aws_secrets, "AWS Secrets Manager")
    else:
        print("\n⚠️  Could not retrieve secrets from AWS Secrets Manager")
        print("   Falling back to environment variables...")
        
        # Get credentials from environment variables
        env_credentials = get_environment_credentials()
        
        if env_credentials:
            print("\n✅ Successfully retrieved credentials from environment variables")
            display_credentials(env_credentials, "Environment Variables")
            
            # Ask user if they want to see plaintext
            response = input("\n🔓 Do you want to see the credentials in plaintext? (y/N): ")
            if response.lower() in ['y', 'yes']:
                display_plaintext_credentials(env_credentials, "Environment Variables")
        else:
            print("\n❌ Could not retrieve credentials from any source")
            sys.exit(1)
    
    print("\n✅ Script completed successfully")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Script interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 