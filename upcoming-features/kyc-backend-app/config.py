import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Environment
    ENV: str = os.getenv("ENV", "local")
    
    # Database - Use AWS PostgreSQL for both local and AWS environments
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # AWS PostgreSQL Database Configuration
    DB_USERNAME: str = os.getenv("DB_USERNAME", "kycapp")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "kycapp123")
    DB_HOST: str = os.getenv("DB_HOST", "database-1-instance-1.c3iikqyyi0uu.us-east-2.rds.amazonaws.com")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "kycdb")
    
    # AWS Configuration (optional - will use environment variables or AWS profiles)
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_SESSION_TOKEN: str = os.getenv("AWS_SESSION_TOKEN", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-2")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "dbdtcckycbucket")
    
    # CORS Settings
    CORS_ORIGINS: list = ["http://localhost:3000"]  # Add your frontend URLs
    
    # Lambda Settings
    LAMBDA_FUNCTION_NAME: str = os.getenv("LAMBDA_FUNCTION_NAME", "kyc-api")
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()


def get_database_url() -> str:
    """
    Get database URL - always use AWS PostgreSQL
    """
    settings = get_settings()
    
    # If DATABASE_URL is explicitly set, use it
    if settings.DATABASE_URL:
        return settings.DATABASE_URL
    
    # Always use AWS PostgreSQL database
    try:
        import importlib.util
        import os
        
        # Get the path to our custom secrets.py file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        secrets_path = os.path.join(current_dir, 'secrets.py')
        
        # Load our custom secrets module
        spec = importlib.util.spec_from_file_location("custom_secrets", secrets_path)
        custom_secrets = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(custom_secrets)
        
        secret_db_url = custom_secrets.get_database_url()
        if secret_db_url:
            return secret_db_url
    except Exception as e:
        print(f"Failed to get database URL from secrets: {e}")
    
    # Fallback - construct PostgreSQL URL directly
    host = settings.DB_HOST
    username = settings.DB_USERNAME
    password = settings.DB_PASSWORD
    port = settings.DB_PORT
    dbname = settings.DB_NAME
    
    fallback_url = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
    print(f"Using PostgreSQL database URL: postgresql://{username}:***@{host}:{port}/{dbname}")
    
    return fallback_url 