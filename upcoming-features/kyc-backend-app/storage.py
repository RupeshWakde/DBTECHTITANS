import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile, HTTPException
from config import get_settings
import os
from typing import Optional

settings = get_settings()

class S3Storage:
    def __init__(self):
        # Initialize S3 client with session token for temporary credentials
        # Use us-west-2 region specifically for S3 operations
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            region_name='us-west-2'  # S3 bucket is in us-west-2
        )
        # Use the specific bucket name
        self.bucket_name = "dbdtcckycbucket"

    async def upload_file(self, file: UploadFile, kyc_case_id: int, doc_type: str) -> str:
        """Upload a file to S3 and return the S3 URL"""
        print(f"☁️  DEBUG: Starting S3 upload for case {kyc_case_id}, type {doc_type}")
        print(f"📁 DEBUG: File: {file.filename}, Size: {file.size}, Content-Type: {file.content_type}")
        
        if settings.ENV == "local":
            print(f"💾 DEBUG: Using local storage for development")
            # For local development, save to local filesystem
            return await self._save_local(file, kyc_case_id, doc_type)
        
        # Use uploads/ folder structure in S3
        s3_key = f"uploads/kyc/{kyc_case_id}/{doc_type}/{file.filename}"
        print(f"🗂️  DEBUG: S3 key: {s3_key}")
        
        try:
            print(f"📖 DEBUG: Reading file content")
            # Read file content
            file_content = await file.read()
            print(f"✅ DEBUG: File content read successfully, size: {len(file_content)} bytes")
            
            print(f"☁️  DEBUG: Uploading to S3 bucket: {self.bucket_name}")
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content
            )
            print(f"✅ DEBUG: File uploaded to S3 successfully")
            
            # Generate S3 URL
            s3_url = f"s3://{self.bucket_name}/{s3_key}"
            print(f"🔗 DEBUG: Generated S3 URL: {s3_url}")
            return s3_url
            
        except NoCredentialsError as e:
            print(f"❌ DEBUG: AWS credentials not found: {e}")
            raise HTTPException(status_code=500, detail="AWS credentials not found")
        except Exception as e:
            print(f"❌ DEBUG: S3 upload failed: {e}")
            print(f"❌ DEBUG: Exception type: {type(e).__name__}")
            import traceback
            print(f"❌ DEBUG: Full traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")
        finally:
            print(f"🧹 DEBUG: Closing file")
            await file.close()

    async def _save_local(self, file: UploadFile, kyc_case_id: int, doc_type: str) -> str:
        """Save file locally for development environment"""
        print(f"💾 DEBUG: Starting local file save for case {kyc_case_id}, type {doc_type}")
        
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        print(f"📁 DEBUG: Created upload directory: {upload_dir}")
        
        file_path = os.path.join(upload_dir, f"{kyc_case_id}_{doc_type}_{file.filename}")
        print(f"📄 DEBUG: Local file path: {file_path}")
        
        try:
            # Save file
            print(f"📖 DEBUG: Reading file content for local save")
            content = await file.read()
            print(f"✅ DEBUG: File content read, size: {len(content)} bytes")
            
            print(f"💾 DEBUG: Writing file to local storage")
            with open(file_path, "wb") as buffer:
                buffer.write(content)
            print(f"✅ DEBUG: File saved locally successfully")
            
            return file_path
        except Exception as e:
            print(f"❌ DEBUG: Local file save failed: {e}")
            print(f"❌ DEBUG: Exception type: {type(e).__name__}")
            import traceback
            print(f"❌ DEBUG: Full traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Local file save failed: {str(e)}")

    def get_file_url(self, s3_key: str) -> Optional[str]:
        """Generate a pre-signed URL for file download"""
        if settings.ENV == "local":
            return None
            
        try:
            # If the s3_key doesn't start with uploads/, add it
            if not s3_key.startswith("uploads/"):
                s3_key = f"uploads/{s3_key}"
                
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=3600  # URL expires in 1 hour
            )
            return url
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate download URL: {str(e)}")

    def test_connection(self):
        """Test S3 connection"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except Exception as e:
            print(f"S3 connection test failed: {e}")
            return False

# Create a singleton instance
storage = S3Storage() 