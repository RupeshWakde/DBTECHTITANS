import boto3
import json
import os
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Dict, Optional


def get_secret() -> Dict[str, str]:
    """
    Get database credentials from AWS Secrets Manager
    """
    secret_name = "rds!cluster-cbb2d3bf-4194-454c-9b9b-1094e7916326"
    region_name = "us-east-2"

    # Check if we have AWS credentials
    if not (os.getenv('AWS_ACCESS_KEY_ID') or os.getenv('AWS_PROFILE')):
        print("⚠️  AWS credentials not found. Using direct PostgreSQL connection.")
        return get_direct_credentials()

    # Create a Secrets Manager client
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except (ClientError, NoCredentialsError) as e:
        # Check for specific error types
        error_code = getattr(e, 'response', {}).get('Error', {}).get('Code', 'Unknown')
        if error_code == 'ExpiredTokenException':
            print("⚠️  AWS session token has expired. Using direct PostgreSQL connection.")
        else:
            print(f"⚠️  Could not access AWS Secrets Manager: {e}")
        print("Using direct PostgreSQL connection.")
        return get_direct_credentials()

    secret = get_secret_value_response['SecretString']
    
    # Parse the JSON secret string
    try:
        secret_dict = json.loads(secret)
        return secret_dict
    except json.JSONDecodeError as e:
        print(f"⚠️  Failed to parse secret JSON: {e}")
        return get_direct_credentials()


def get_direct_credentials() -> Dict[str, str]:
    """
    Get direct PostgreSQL credentials for AWS RDS
    """
    return {
        'username': os.getenv('DB_USERNAME', 'kycapp'),
        'password': os.getenv('DB_PASSWORD', 'kycapp123'),
        'host': os.getenv('DB_HOST', 'database-1-instance-1.c3iikqyyi0uu.us-east-2.rds.amazonaws.com'),
        'port': os.getenv('DB_PORT', '5432'),
        'dbname': os.getenv('DB_NAME', 'kycdb')
    }


def get_database_url() -> str:
    """
    Construct DATABASE_URL - always use AWS PostgreSQL
    """
    try:
        secret = get_secret()
        
        # Extract database connection details from secret
        username = secret.get('username', 'kycapp')
        password = secret.get('password', '')
        host = secret.get('host', 'database-1-instance-1.c3iikqyyi0uu.us-east-2.rds.amazonaws.com')
        port = secret.get('port', '5432')
        dbname = secret.get('dbname', 'kycdb')
        
        # Construct PostgreSQL connection string
        database_url = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
        
        print(f"Constructed PostgreSQL URL: postgresql://{username}:***@{host}:{port}/{dbname}")
        
        return database_url
        
    except Exception as e:
        print(f"Error getting database URL from secrets: {e}")
        # Fallback to environment variable or direct construction
        fallback_url = os.getenv('DATABASE_URL', '')
        if fallback_url:
            print(f"Using fallback DATABASE_URL from environment")
            return fallback_url
        else:
            # Construct from environment variables
            username = os.getenv('DB_USERNAME', 'kycapp')
            password = os.getenv('DB_PASSWORD', 'kycapp123')
            host = os.getenv('DB_HOST', 'database-1-instance-1.c3iikqyyi0uu.us-east-2.rds.amazonaws.com')
            port = os.getenv('DB_PORT', '5432')
            dbname = os.getenv('DB_NAME', 'kycdb')
            
            direct_url = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
            print(f"Using direct PostgreSQL URL: postgresql://{username}:***@{host}:{port}/{dbname}")
            return direct_url


def get_secret_value(key: str) -> Optional[str]:
    """
    Get a specific value from the secret
    """
    try:
        secret = get_secret()
        return secret.get(key)
    except Exception as e:
        print(f"Error getting secret value for {key}: {e}")
        return None 