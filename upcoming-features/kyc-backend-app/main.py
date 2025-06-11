#!/usr/bin/env python3
"""
KYC API Application - AWS Version
This is a FastAPI-based backend application for handling KYC (Know Your Customer) processes.
Configured to use AWS PostgreSQL (RDS) and S3 storage.
"""

import os
import sys
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import shutil
from typing import List, Optional, Dict
from datetime import datetime
import random
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Set environment to AWS
os.environ["ENV"] = "aws"

# Add parent directory to path for imports
sys.path.append('..')

# AWS environment imports
from database import get_db, init_db, get_engine
from models import User, KycDocument, KycCase, KycDetail, KycStatus
from storage import storage
from secrets import get_database_url
from config import get_settings

# File upload configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB in bytes
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx', '.mp4', '.avi', '.mov', '.webm', '.mkv'}

app = FastAPI(
    title="KYC API - AWS Version",
    description="KYC API configured for AWS PostgreSQL and S3",
    version="2.0.0"
)

# CORS configuration for AWS - Let nginx handle CORS
cors_origins = ["*"]  # Allow all origins for now

# Simplified CORS middleware - let nginx handle the headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    """Initialize database on startup"""
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")

@app.middleware("http")
async def add_cors_headers(request, call_next):
    """Add CORS headers to all responses - simplified approach"""
    response = await call_next(request)
    
        
    # Always add CORS headers
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "false"


    # Log CORS requests for debugging
    origin = request.headers.get("origin", "unknown")
    print(f"🌐 DEBUG: CORS request from {origin} to {request.method} {request.url.path}")
    
    # Let nginx handle CORS headers, just log the request
    return response

@app.get("/cors-test")
@app.head("/cors-test")
async def cors_test():
    """Test endpoint to verify CORS is working"""
    return {
        "message": "CORS is working!",
        "timestamp": datetime.utcnow().isoformat(),
        "allowed_origins": cors_origins,
        "status": "success"
    }

# Mock data arrays for document extraction
aadhaar_front_mocks = [
    {"name": "Rahul Sharma", "dob": "1988-05-23", "gender": "Male", "aadhar_number": "234567890123"},
    {"name": "Priya Singh", "dob": "1992-11-10", "gender": "Female", "aadhar_number": "345678901234"},
    {"name": "Amit Patel", "dob": "1985-03-15", "gender": "Male", "aadhar_number": "456789012345"},
    {"name": "Sneha Reddy", "dob": "1990-07-19", "gender": "Female", "aadhar_number": "567890123456"},
    {"name": "Vikram Desai", "dob": "1979-12-01", "gender": "Male", "aadhar_number": "678901234567"},
    {"name": "Anjali Mehta", "dob": "1995-04-22", "gender": "Female", "aadhar_number": "789012345678"},
    {"name": "Rohit Verma", "dob": "1983-09-30", "gender": "Male", "aadhar_number": "890123456789"},
    {"name": "Kavita Joshi", "dob": "1987-06-14", "gender": "Female", "aadhar_number": "901234567890"},
    {"name": "Suresh Kumar", "dob": "1975-01-05", "gender": "Male", "aadhar_number": "123456780912"},
    {"name": "Meena Gupta", "dob": "1991-08-27", "gender": "Female", "aadhar_number": "234567801923"}
]

aadhaar_back_mocks = [
    {"address": "Flat 12B, Green Residency, Baner Road, Pune, Maharashtra", "pincode": "411045"},
    {"address": "23, Rose Villa, Sector 17, Chandigarh", "pincode": "160017"},
    {"address": "B-45, Lake View, Salt Lake, Kolkata, West Bengal", "pincode": "700064"},
    {"address": "Plot 8, MG Road, Bengaluru, Karnataka", "pincode": "560001"},
    {"address": "H.No. 123, Lajpat Nagar, New Delhi", "pincode": "110024"},
    {"address": "501, Palm Heights, Andheri East, Mumbai", "pincode": "400069"},
    {"address": "7, Lotus Enclave, Banjara Hills, Hyderabad", "pincode": "500034"},
    {"address": "C-22, Ashok Nagar, Chennai, Tamil Nadu", "pincode": "600083"},
    {"address": "D-9, Alkapuri, Vadodara, Gujarat", "pincode": "390007"},
    {"address": "A-1, Civil Lines, Jaipur, Rajasthan", "pincode": "302006"}
]

pancard_mocks = [
    {"name": "Rahul Sharma", "pan_number": "FMPPK1234L"},
    {"name": "Priya Singh", "pan_number": "BNZPS1234K"},
    {"name": "Amit Patel", "pan_number": "AKLPJ2345M"},
    {"name": "Sneha Reddy", "pan_number": "QWERT5678Z"},
    {"name": "Vikram Desai", "pan_number": "ZXCVB6789N"},
    {"name": "Anjali Mehta", "pan_number": "LKJHG3456B"},
    {"name": "Rohit Verma", "pan_number": "POIUY4321V"},
    {"name": "Kavita Joshi", "pan_number": "MNBVC0987X"},
    {"name": "Suresh Kumar", "pan_number": "ASDFG7654C"},
    {"name": "Meena Gupta", "pan_number": "GHJKL8765D"}
]

passport_mocks = [
    {"name": "Rahul Sharma", "passport_number": "M1234567", "address": "22, Lotus Apartments, Andheri West, Mumbai, Maharashtra, 400053"},
    {"name": "Priya Singh", "passport_number": "N2345678", "address": "14, Sunrise Towers, Powai, Mumbai, Maharashtra, 400076"},
    {"name": "Amit Patel", "passport_number": "P3456789", "address": "8, Green Park, South Delhi, 110016"},
    {"name": "Sneha Reddy", "passport_number": "Q4567890", "address": "33, Lake Gardens, Kolkata, 700045"},
    {"name": "Vikram Desai", "passport_number": "R5678901", "address": "55, Residency Road, Bengaluru, 560025"},
    {"name": "Anjali Mehta", "passport_number": "S6789012", "address": "12, Marine Drive, Kochi, 682031"},
    {"name": "Rohit Verma", "passport_number": "T7890123", "address": "7, Civil Lines, Jaipur, 302006"},
    {"name": "Kavita Joshi", "passport_number": "U8901234", "address": "19, Sector 21, Chandigarh, 160022"},
    {"name": "Suresh Kumar", "passport_number": "V9012345", "address": "2, MG Road, Pune, 411001"},
    {"name": "Meena Gupta", "passport_number": "W0123456", "address": "101, City Center, Ahmedabad, 380009"}
]

def mock_extract_aadhaar_front_info():
    return random.choice(aadhaar_front_mocks)

def mock_extract_aadhaar_back_info():
    return random.choice(aadhaar_back_mocks)

def mock_extract_pancard_info(name=None):
    if name:
        # Find the mock with the same name, else random
        for rec in pancard_mocks:
            if rec["name"] == name:
                return rec.copy()
        rec = random.choice(pancard_mocks)
        rec = rec.copy()
        rec["name"] = name
        return rec
    else:
        return random.choice(pancard_mocks).copy()

def mock_extract_passport_info(name=None):
    if name:
        for rec in passport_mocks:
            if rec["name"] == name:
                return rec.copy()
        rec = random.choice(passport_mocks)
        rec = rec.copy()
        rec["name"] = name
        return rec
    else:
        return random.choice(passport_mocks).copy()

def validate_file_upload(file: UploadFile):
    """Validate file upload size and type"""
    print(f"🔍 DEBUG: Validating file: {file.filename}")
    print(f"📊 DEBUG: File size: {file.size} bytes, Max allowed: {MAX_FILE_SIZE} bytes")
    
    # Check file size
    if file.size and file.size > MAX_FILE_SIZE:
        print(f"❌ DEBUG: File too large: {file.size} > {MAX_FILE_SIZE}")
        raise HTTPException(
            status_code=413, 
            detail=f"File too large. Maximum size allowed is {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    print(f"✅ DEBUG: File size validation passed")
    
    # Check file extension
    if file.filename:
        file_ext = os.path.splitext(file.filename)[1].lower()
        print(f"📁 DEBUG: File extension: {file_ext}")
        print(f"📋 DEBUG: Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}")
        
        if file_ext not in ALLOWED_EXTENSIONS:
            print(f"❌ DEBUG: File type not allowed: {file_ext}")
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        print(f"✅ DEBUG: File extension validation passed")
    else:
        print(f"⚠️  DEBUG: No filename provided")
    
    # Check content type for additional validation
    if file.content_type:
        print(f"📄 DEBUG: Content type: {file.content_type}")
        # Allow common video and image content types
        allowed_content_types = {
            'image/jpeg', 'image/jpg', 'image/png', 'application/pdf',
            'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'video/mp4', 'video/avi', 'video/quicktime', 'video/webm', 'video/x-matroska'
        }
        
        if file.content_type not in allowed_content_types:
            print(f"⚠️  DEBUG: Content type not in allowed list: {file.content_type}")
            # Don't fail here, just log a warning
        else:
            print(f"✅ DEBUG: Content type validation passed")
    
    print(f"✅ DEBUG: File validation completed successfully")

# Pydantic models
class UserRegistrationRequest(BaseModel):
    email: EmailStr
    phone: str
    password: str
    emailVerified: bool
    phoneVerified: bool
    securityQuestions: Optional[List[str]] = []
    kyc_case_id: int

class KycDetailsRequest(BaseModel):
    kyc_case_id: int
    name: str
    dob: str
    gender: str
    address: str
    father_name: str
    pan_number: str
    aadhar_number: str
    email: str
    phone: str
    occupation: str
    source_of_funds: str
    business_type: str
    is_pep: bool = False
    pep_details: str = ''
    annual_income: str = ''
    purpose_of_account: str = ''
    nationality: str = ''
    marital_status: str = ''
    nominee_name: str = ''
    nominee_relation: str = ''
    nominee_contact: str = ''

class KycScreenData(BaseModel):
    case: dict
    details: Optional[dict]
    documents: List[dict]
    status: Optional[dict]

class KycStepProgress(BaseModel):
    id: str
    status: str  # 'pending', 'completed'

class KycProgressResponse(BaseModel):
    steps: list
    current_step: str

class CustomerOut(BaseModel):
    kyc_details_id: int
    kyc_case_id: int
    name: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    environment: str
    timestamp: str
    database: str
    s3: str

# API Endpoints
@app.get("/health", response_model=HealthResponse)
@app.head("/health")
async def health_check():
    """Health check endpoint with AWS service status"""
    try:
        # Test database connection
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    try:
        # Test S3 connection
        storage.test_connection()
        s3_status = "connected"
    except Exception as e:
        s3_status = f"error: {str(e)}"
    
    return HealthResponse(
        status="healthy",
        environment="aws",
        timestamp=datetime.utcnow().isoformat(),
        database=db_status,
        s3=s3_status
    )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "KYC API - AWS Version",
        "version": "2.0.0",
        "environment": "aws",
        "database": "PostgreSQL (RDS)",
        "storage": "S3",
        "endpoints": {
            "health": "/health",
            "register": "/register",
            "kyc_register": "/kyc/register",
            "kyc_upload": "/kyc/upload",
            "kyc_case": "/kyc/case",
            "kyc_details": "/kyc/details",
            "kyc_screen_data": "/kyc/screen-data/{case_id}",
            "kyc_progress": "/kyc/progress/{case_id}",
            "customers": "/customers",
            "docs": "/docs"
        }
    }

@app.post("/register")
def register_user(data: UserRegistrationRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user exists by email or phone
        existing_user = db.query(User).filter(
            (User.email == data.email) | (User.phone == data.phone)
        ).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create new user (without email_verified and phone_verified fields)
        user = User(
            email=data.email,
            phone=data.phone,
            password_hash=data.password,  # In production, hash this
            created_at=datetime.utcnow()
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {
            "success": True,
            "message": "User registered successfully",
            "user_id": user.id,
            "email": user.email,
            "phone": user.phone
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/kyc/register")
def register_user_kyc(data: UserRegistrationRequest, db: Session = Depends(get_db)):
    """Register a new user or update existing user (KYC endpoint)"""
    try:
        print(f"🔍 DEBUG: Registration request for kyc_case_id: {data.kyc_case_id}")
        print(f"🔍 DEBUG: Email: {data.email}, Phone: {data.phone}")
        
        # Check if user exists by email or phone
        existing_user = db.query(User).filter(
            (User.email == data.email) | (User.phone == data.phone)
        ).first()
        
        if existing_user:
            print(f"✅ DEBUG: Found existing user with ID: {existing_user.id}")
            # Update existing user
            existing_user.email = data.email
            existing_user.phone = data.phone
            existing_user.password_hash = data.password  # In production, hash this
            # Note: updated_at field doesn't exist in the database schema
            
            db.commit()
            db.refresh(existing_user)
            user = existing_user
        else:
            print(f"✅ DEBUG: Creating new user")
            # Create new user (without email_verified and phone_verified fields)
            user = User(
                email=data.email,
                phone=data.phone,
                password_hash=data.password,  # In production, hash this
                created_at=datetime.utcnow()
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"✅ DEBUG: New user created with ID: {user.id}")
        
        # Link user to KYC case
        print(f"🔍 DEBUG: Looking for KYC case with ID: {data.kyc_case_id}")
        kyc_case = db.query(KycCase).filter(KycCase.id == data.kyc_case_id).first()
        if kyc_case:
            print(f"✅ DEBUG: Found KYC case {data.kyc_case_id}")
            print(f"🔍 DEBUG: KYC case user_id before update: {kyc_case.user_id}")
            kyc_case.user_id = user.id
            db.commit()
            print(f"✅ DEBUG: Updated KYC case user_id to: {kyc_case.user_id}")
            
            # Create or update KYC details with registration information
            kyc_details = db.query(KycDetail).filter(KycDetail.kyc_case_id == data.kyc_case_id).first()
            if kyc_details:
                # Update existing KYC details with email and phone
                kyc_details.email = data.email
                kyc_details.phone = data.phone
                db.commit()
                print(f"✅ DEBUG: Updated existing KYC details with registration info")
            else:
                # Create new KYC details with email and phone
                kyc_details = KycDetail(
                    kyc_case_id=data.kyc_case_id,
                    email=data.email,
                    phone=data.phone
                )
                db.add(kyc_details)
                db.commit()
                print(f"✅ DEBUG: Created new KYC details with registration info")
        else:
            print(f"❌ DEBUG: KYC case {data.kyc_case_id} not found!")
        
        return {
            "success": True,
            "message": "User registered successfully" if not existing_user else "User updated successfully",
            "user_id": user.id,
            "email": user.email,
            "phone": user.phone
        }
        
    except Exception as e:
        print(f"❌ DEBUG: Registration error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/kyc/upload")
async def upload_document(
    kyc_case_id: int = Form(...),
    doc_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload KYC document and extract information"""
    try:
        print(f"🔍 DEBUG: Uploading document for case_id: {kyc_case_id}, type: {doc_type}")
        print(f"📁 DEBUG: File details - Name: {file.filename}, Size: {file.size}, Content-Type: {file.content_type}")
        
        # Validate kyc_case_id exists
        print(f"🔍 DEBUG: Validating KYC case {kyc_case_id}")
        kyc_case = db.query(KycCase).filter(KycCase.id == kyc_case_id).first()
        if not kyc_case:
            print(f"❌ DEBUG: KYC case {kyc_case_id} not found")
            raise HTTPException(status_code=404, detail=f"KYC case {kyc_case_id} not found")
        print(f"✅ DEBUG: KYC case {kyc_case_id} validated")

        # Validate file upload
        print(f"🔍 DEBUG: Validating file upload")
        try:
            validate_file_upload(file)
            print(f"✅ DEBUG: File validation passed")
        except Exception as validation_error:
            print(f"❌ DEBUG: File validation failed: {validation_error}")
            raise validation_error

        # File storage based on environment
        print(f"🔍 DEBUG: Environment: {get_settings().ENV}")
        if get_settings().ENV == "aws":
            print(f"☁️  DEBUG: Using S3 storage for AWS")
            try:
                # Use S3 storage for AWS Lambda
                file_path = await storage.upload_file(file, kyc_case_id, doc_type)
                print(f"✅ DEBUG: File uploaded to S3: {file_path}")
            except Exception as s3_error:
                print(f"❌ DEBUG: S3 upload failed: {s3_error}")
                raise s3_error
        else:
            print(f"💾 DEBUG: Using local file storage")
            try:
                # Use local file storage for local development
                upload_dir = "uploads"
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, f"{kyc_case_id}_{doc_type}_{file.filename}")
                
                # Reset file position to beginning
                await file.seek(0)
                
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                print(f"✅ DEBUG: File saved locally: {file_path}")
            except Exception as local_error:
                print(f"❌ DEBUG: Local file save failed: {local_error}")
                raise local_error

        # Save or update metadata to DB
        print(f"💾 DEBUG: Saving document metadata to database")
        try:
            existing_doc = db.query(KycDocument).filter(
                KycDocument.kyc_case_id == kyc_case_id, 
                KycDocument.doc_type == doc_type
            ).first()
            
            if existing_doc:
                print(f"🔄 DEBUG: Updating existing document record")
                existing_doc.file_path = file_path
                existing_doc.uploaded_at = datetime.utcnow()
                db.commit()
                doc = existing_doc
            else:
                print(f"🆕 DEBUG: Creating new document record")
                doc = KycDocument(
                    kyc_case_id=kyc_case_id, 
                    doc_type=doc_type, 
                    file_path=file_path,
                    uploaded_at=datetime.utcnow()
                )
                db.add(doc)
                db.commit()
                db.refresh(doc)
            print(f"✅ DEBUG: Document metadata saved successfully")
        except Exception as db_error:
            print(f"❌ DEBUG: Database save failed: {db_error}")
            raise db_error

        # Mock extraction logic - same as original main.py
        print(f"🔍 DEBUG: Processing document type: {doc_type}")
        if doc_type == "aadhar_front":
            print(f"🆔 DEBUG: Extracting Aadhar front information")
            extracted = mock_extract_aadhaar_front_info()
            details = db.query(KycDetail).filter(KycDetail.kyc_case_id == kyc_case_id).first()
            if details:
                for k, v in extracted.items():
                    if v:
                        setattr(details, k, v)
                db.commit()
                print(f"✅ DEBUG: Updated existing KYC details with Aadhar front info")
            else:
                details = KycDetail(kyc_case_id=kyc_case_id, **{k: v for k, v in extracted.items() if v})
                db.add(details)
                db.commit()
                print(f"✅ DEBUG: Created new KYC details with Aadhar front info")
                
        elif doc_type == "aadhar_back":
            print(f"🆔 DEBUG: Extracting Aadhar back information")
            extracted = mock_extract_aadhaar_back_info()
            details = db.query(KycDetail).filter(KycDetail.kyc_case_id == kyc_case_id).first()
            if details:
                for k, v in extracted.items():
                    if v:
                        if k == "address":
                            details.address = v
                        elif k == "pincode":
                            if details.address:
                                details.address += f", {v}"
                            else:
                                details.address = v
                db.commit()
                print(f"✅ DEBUG: Updated existing KYC details with Aadhar back info")
            else:
                address = extracted.get("address", "")
                pincode = extracted.get("pincode", "")
                full_address = f"{address}, {pincode}" if address and pincode else address or pincode
                details = KycDetail(kyc_case_id=kyc_case_id, address=full_address)
                db.add(details)
                db.commit()
                print(f"✅ DEBUG: Created new KYC details with Aadhar back info")
                
        elif doc_type == "pancard":
            print(f"🆔 DEBUG: Extracting PAN card information")
            details = db.query(KycDetail).filter(KycDetail.kyc_case_id == kyc_case_id).first()
            name = details.name if details and details.name else None
            extracted = mock_extract_pancard_info(name)
            if details:
                for k, v in extracted.items():
                    if v:
                        setattr(details, k, v)
                db.commit()
                print(f"✅ DEBUG: Updated existing KYC details with PAN info")
            else:
                details = KycDetail(kyc_case_id=kyc_case_id, **{k: v for k, v in extracted.items() if v})
                db.add(details)
                db.commit()
                print(f"✅ DEBUG: Created new KYC details with PAN info")
                
        elif doc_type == "passport":
            print(f"🆔 DEBUG: Extracting Passport information")
            details = db.query(KycDetail).filter(KycDetail.kyc_case_id == kyc_case_id).first()
            name = details.name if details and details.name else None
            extracted = mock_extract_passport_info(name)
            if details:
                for k, v in extracted.items():
                    if v:
                        if k == "address":
                            details.address = v
                        else:
                            setattr(details, k, v)
                db.commit()
                print(f"✅ DEBUG: Updated existing KYC details with Passport info")
            else:
                details = KycDetail(kyc_case_id=kyc_case_id, **{k: v for k, v in extracted.items() if v})
                db.add(details)
                db.commit()
                print(f"✅ DEBUG: Created new KYC details with Passport info")
        elif doc_type == "video":
            print(f"🎥 DEBUG: Video upload - no extraction needed")
            # For video uploads, we don't need to extract information
            pass
        else:
            print(f"⚠️  DEBUG: Unknown document type: {doc_type} - no extraction performed")

        print(f"✅ DEBUG: Upload completed successfully")
        return {
            "success": True,
            "message": "Document uploaded successfully",
            "doc_id": doc.id,
            "file_path": file_path,
            "kyc_case_id": kyc_case_id
        }
        
    except Exception as e:
        print(f"❌ DEBUG: Upload failed: {e}")
        print(f"❌ DEBUG: Exception type: {type(e).__name__}")
        import traceback
        print(f"❌ DEBUG: Full traceback: {traceback.format_exc()}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/kyc/case")
def create_kyc_case(db: Session = Depends(get_db)):
    """Create a new KYC case"""
    try:
        # Find the max id in KycCase
        max_case = db.query(KycCase).order_by(KycCase.id.desc()).first()
        new_case_id = (max_case.id + 1) if max_case else 1
        
        # Create new KYC case
        kyc_case = KycCase(
            id=new_case_id,
            status="initiated",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(kyc_case)
        db.commit()
        db.refresh(kyc_case)
        
        return {
            "success": True,
            "message": "KYC case created successfully",
            "kyc_case_id": kyc_case.id,
            "status": kyc_case.status
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create KYC case: {str(e)}")

@app.post("/kyc/details")
def save_kyc_details(data: KycDetailsRequest, db: Session = Depends(get_db)):
    """Save KYC details"""
    try:
        print(f"🔍 DEBUG: Received KYC details for case_id: {data.kyc_case_id}")
        
        # Check if a record with the same kyc_case_id exists
        existing_details = db.query(KycDetail).filter(
            KycDetail.kyc_case_id == data.kyc_case_id
        ).first()
        
        if existing_details:
            # Update existing record
            for field, value in data.dict().items():
                if field != 'kyc_case_id':
                    setattr(existing_details, field, value)
            # Note: updated_at field doesn't exist in the database
            db.commit()
            db.refresh(existing_details)
            details = existing_details
        else:
            # Create new record
            details = KycDetail(**data.dict())
            db.add(details)
            db.commit()
            db.refresh(details)
        
        # Mark KYC as submitted in both KycCase and KycStatus
        kyc_case = db.query(KycCase).filter(KycCase.id == data.kyc_case_id).first()
        if kyc_case:
            print(f"🔍 DEBUG: Found KYC case, updating status to 'submitted'")
            # Update KycCase status
            kyc_case.status = 'submitted'
            
            # Update KycStatus
            if kyc_case.user_id:
                kyc_status = db.query(KycStatus).filter(KycStatus.user_id == kyc_case.user_id).first()
                if kyc_status:
                    print(f"🔍 DEBUG: Updating existing KYC status to 'submitted'")
                    kyc_status.status = 'submitted'
                    kyc_status.kyc_id = str(data.kyc_case_id)
                else:
                    print(f"🔍 DEBUG: Creating new KYC status record with 'submitted'")
                    kyc_status = KycStatus(user_id=kyc_case.user_id, status='submitted', kyc_id=str(data.kyc_case_id))
                    db.add(kyc_status)
                
                db.commit()
                print(f"🔍 DEBUG: Database committed successfully")
            else:
                print(f"⚠️ DEBUG: No user_id in KYC case, cannot update KycStatus")
        else:
            print(f"❌ DEBUG: KYC case not found for case_id: {data.kyc_case_id}")
        
        return {
            "success": True,
            "message": "KYC details saved successfully",
            "kyc_details_id": details.id,
            "kyc_case_id": details.kyc_case_id
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ DEBUG: Error saving KYC details: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save KYC details: {str(e)}")

@app.get("/kyc/screen-data/{case_id}", response_model=KycScreenData)
def get_kyc_screen_data(case_id: int, db: Session = Depends(get_db)):
    """Get KYC screen data for a case"""
    try:
        print(f"🔍 DEBUG: Getting screen data for case_id: {case_id}")
        
        # Convert SQLAlchemy objects to dictionaries safely
        def to_dict(obj):
            if obj is None:
                return None
            return {
                column.name: getattr(obj, column.name)
                for column in obj.__table__.columns
            }
        
        # Get KYC case
        kyc_case = db.query(KycCase).filter(KycCase.id == case_id).first()
        if not kyc_case:
            print(f"❌ DEBUG: KYC case {case_id} not found")
            raise HTTPException(status_code=404, detail="KYC case not found")
        
        print(f"✅ DEBUG: Found KYC case {case_id}")
        print(f"🔍 DEBUG: KYC case user_id: {kyc_case.user_id}")
        print(f"🔍 DEBUG: KYC case status: {kyc_case.status}")
        
        # Get KYC details
        kyc_details = db.query(KycDetail).filter(KycDetail.kyc_case_id == case_id).first()
        if kyc_details:
            print(f"✅ DEBUG: Found KYC details for case {case_id}")
            details_data = to_dict(kyc_details)
        else:
            print(f"❌ DEBUG: No KYC details found for case {case_id}, getting auto-populated details")
            # Get auto-populated details from documents and registration
            auto_details = get_auto_populated_kyc_details(case_id, db)
            if auto_details:
                print(f"✅ DEBUG: Found auto-populated details for case {case_id}")
                details_data = auto_details
            else:
                print(f"❌ DEBUG: No auto-populated details found for case {case_id}")
                details_data = None
        
        # Get documents
        documents = db.query(KycDocument).filter(KycDocument.kyc_case_id == case_id).all()
        print(f"🔍 DEBUG: Found {len(documents)} documents for case {case_id}")
        
        # Get status (only if user_id exists)
        kyc_status = None
        if kyc_case.user_id:
            kyc_status = db.query(KycStatus).filter(KycStatus.user_id == kyc_case.user_id).first()
            if kyc_status:
                print(f"✅ DEBUG: Found KYC status for user {kyc_case.user_id}")
            else:
                print(f"❌ DEBUG: No KYC status found for user {kyc_case.user_id}")
        else:
            print(f"❌ DEBUG: No user_id in KYC case, cannot check status")
        
        return KycScreenData(
            case={
                "id": kyc_case.id,
                "status": kyc_case.status,
                "created_at": kyc_case.created_at.isoformat() if kyc_case.created_at else None,
                "updated_at": kyc_case.updated_at.isoformat() if kyc_case.updated_at else None
            },
            details=details_data,
            documents=[{
                "id": doc.id,
                "doc_type": doc.doc_type,
                "file_path": doc.file_path,
                "uploaded_at": doc.uploaded_at.isoformat() if doc.uploaded_at else None
            } for doc in documents],
            status=to_dict(kyc_status)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ DEBUG: Error in screen-data endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get screen data: {str(e)}")

@app.get("/kyc/progress/{case_id}", response_model=KycProgressResponse)
def get_kyc_progress(case_id: int, db: Session = Depends(get_db)):
    """Get KYC progress for a case"""
    try:
        print(f"🔍 DEBUG: Checking progress for case_id: {case_id}")
        
        # Define the steps in order with correct names and status
        steps = [
            {"id": "registration", "name": "Registration", "status": "pending"},
            {"id": "aadhar_upload", "name": "Aadhar Upload", "status": "pending"},
            {"id": "pan_upload", "name": "PAN Upload", "status": "pending"},
            {"id": "passport_upload", "name": "Passport Upload", "status": "pending"},
            {"id": "photo_upload", "name": "Photo Upload", "status": "pending"},
            {"id": "selfie_upload", "name": "Selfie Upload", "status": "pending"},
            {"id": "video_upload", "name": "Video Upload", "status": "pending"},
            {"id": "review", "name": "Review", "status": "pending"},
            {"id": "kyc_submitted", "name": "KYC Submitted", "status": "pending"}
        ]
        
        # Check case exists
        kyc_case = db.query(KycCase).filter(KycCase.id == case_id).first()
        if not kyc_case:
            print(f"❌ DEBUG: KYC case {case_id} not found")
            raise HTTPException(status_code=404, detail="KYC case not found")
        
        print(f"✅ DEBUG: Found KYC case {case_id}")
        print(f"🔍 DEBUG: KYC case user_id: {kyc_case.user_id}")
        print(f"🔍 DEBUG: KYC case status: {kyc_case.status}")
        
        # Check if user is registered (has user_id)
        if kyc_case.user_id:
            print(f"✅ DEBUG: User is registered, user_id: {kyc_case.user_id}")
            steps[0]["status"] = "completed"
        else:
            print(f"❌ DEBUG: No user_id found in KYC case")
        
        # Check document uploads
        documents = db.query(KycDocument).filter(KycDocument.kyc_case_id == case_id).all()
        uploaded_doc_types = [doc.doc_type.lower() for doc in documents]
        print(f"🔍 DEBUG: Uploaded documents: {uploaded_doc_types}")
        
        # Update document step statuses
        # Check for aadhar uploads (both front and back)
        aadhar_docs = [doc for doc in uploaded_doc_types if 'aadhar' in doc or 'aadhaar' in doc]
        if len(aadhar_docs) >= 2:  # Both front and back uploaded
            steps[1]["status"] = "completed"
            print(f"✅ DEBUG: Aadhar upload completed (found {len(aadhar_docs)} aadhar documents)")
        elif len(aadhar_docs) == 1:
            print(f"⚠️ DEBUG: Only {len(aadhar_docs)} aadhar document found, need both front and back")
        else:
            print(f"❌ DEBUG: No aadhar documents found")
            
        # Check for PAN upload
        pan_docs = [doc for doc in uploaded_doc_types if 'pan' in doc]
        if len(pan_docs) >= 1:
            steps[2]["status"] = "completed"
            print(f"✅ DEBUG: PAN upload completed (found {len(pan_docs)} PAN documents)")
        else:
            print(f"❌ DEBUG: No PAN documents found")
            
        # Check for Passport upload
        passport_docs = [doc for doc in uploaded_doc_types if 'passport' in doc]
        if len(passport_docs) >= 1:
            steps[3]["status"] = "completed"
            print(f"✅ DEBUG: Passport upload completed (found {len(passport_docs)} passport documents)")
        else:
            print(f"❌ DEBUG: No passport documents found")
            
        # Check for Photo upload
        photo_docs = [doc for doc in uploaded_doc_types if 'photo' in doc]
        if len(photo_docs) >= 1:
            steps[4]["status"] = "completed"
            print(f"✅ DEBUG: Photo upload completed (found {len(photo_docs)} photo documents)")
        else:
            print(f"❌ DEBUG: No photo documents found")
            
        # Check for Selfie upload
        selfie_docs = [doc for doc in uploaded_doc_types if 'selfie' in doc]
        if len(selfie_docs) >= 1:
            steps[5]["status"] = "completed"
            print(f"✅ DEBUG: Selfie upload completed (found {len(selfie_docs)} selfie documents)")
        else:
            print(f"❌ DEBUG: No selfie documents found")
            
        # Check for Video upload
        video_docs = [doc for doc in uploaded_doc_types if 'video' in doc]
        if len(video_docs) >= 1:
            steps[6]["status"] = "completed"
            print(f"✅ DEBUG: Video upload completed (found {len(video_docs)} video documents)")
        else:
            print(f"❌ DEBUG: No video documents found")
        
        # Check details submission - this should not mark review as completed
        details = db.query(KycDetail).filter(KycDetail.kyc_case_id == case_id).first()
        if details:
            print(f"✅ DEBUG: KYC details exist")
        else:
            print(f"❌ DEBUG: No KYC details found")
        
        # Check if KYC is submitted (case status) - this determines both review and kyc_submitted
        if kyc_case.status and kyc_case.status.lower() in ["submitted", "approved", "rejected"]:
            steps[7]["status"] = "completed"  # Review step completed
            steps[8]["status"] = "completed"  # KYC submitted
            print(f"✅ DEBUG: KYC submitted with status: {kyc_case.status}")
        else:
            print(f"❌ DEBUG: KYC not submitted, status: {kyc_case.status}")
            # Review step should only be completed when KYC is actually submitted
            steps[7]["status"] = "pending"  # Review step pending until KYC is submitted
        
        # Determine current step
        current_step = "registration"
        for i, step in enumerate(steps):
            if step["status"] == "pending":
                current_step = step["id"]
                break
            elif step["status"] == "completed":
                current_step = step["id"]
        
        print(f"🎯 DEBUG: Current step: {current_step}")
        print(f"📊 DEBUG: Final steps status: {[step['id'] + ':' + step['status'] for step in steps]}")
        
        return KycProgressResponse(
            steps=steps,
            current_step=current_step
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ DEBUG: Error in progress endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get progress: {str(e)}")

@app.get("/customers", response_model=List[CustomerOut])
@app.head("/customers")
def list_customers(db: Session = Depends(get_db)):
    """List all customers with KYC details"""
    try:
        # Get all KYC details with related information
        kyc_details = db.query(KycDetail).all()
        
        customers = []
        for detail in kyc_details:
            # Get KYC case
            kyc_case = db.query(KycCase).filter(KycCase.id == detail.kyc_case_id).first()
            
            # Get KYC status (only if user_id exists)
            kyc_status = None
            if kyc_case and kyc_case.user_id:
                kyc_status = db.query(KycStatus).filter(KycStatus.user_id == kyc_case.user_id).first()
            
            customers.append(CustomerOut(
                kyc_details_id=detail.id,
                kyc_case_id=kyc_case.id,
                name=detail.name,
                email=detail.email,
                status=kyc_status.status if kyc_status else "unknown"
            ))
        
        return customers
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list customers: {str(e)}")

def extract_aadhar_info(documents, db):
    """Extract information from Aadhar documents using mock data"""
    aadhar_info = {}
    
    # Check if we have both front and back aadhar documents
    aadhar_front_docs = [doc for doc in documents if 'aadhar' in doc.doc_type.lower() and 'front' in doc.doc_type.lower()]
    aadhar_back_docs = [doc for doc in documents if 'aadhar' in doc.doc_type.lower() and 'back' in doc.doc_type.lower()]
    
    if aadhar_front_docs:
        # Extract from aadhar front
        front_info = mock_extract_aadhaar_front_info()
        aadhar_info.update(front_info)
        print(f"✅ DEBUG: Extracted Aadhar front info: {front_info}")
    
    if aadhar_back_docs:
        # Extract from aadhar back
        back_info = mock_extract_aadhaar_back_info()
        address = back_info.get("address", "")
        pincode = back_info.get("pincode", "")
        full_address = f"{address}, {pincode}" if address and pincode else address or pincode
        aadhar_info["address"] = full_address
        print(f"✅ DEBUG: Extracted Aadhar back info: {back_info}")
    
    return aadhar_info

def extract_pan_info(documents, db):
    """Extract information from PAN document using mock data"""
    pan_info = {}
    
    pan_docs = [doc for doc in documents if 'pan' in doc.doc_type.lower()]
    
    if pan_docs:
        # Get existing name from aadhar if available
        existing_details = db.query(KycDetail).filter(KycDetail.kyc_case_id == pan_docs[0].kyc_case_id).first()
        name = existing_details.name if existing_details and existing_details.name else None
        
        extracted = mock_extract_pancard_info(name)
        pan_info.update(extracted)
        print(f"✅ DEBUG: Extracted PAN info: {extracted}")
    
    return pan_info

def extract_passport_info(documents, db):
    """Extract information from Passport document using mock data"""
    passport_info = {}
    
    passport_docs = [doc for doc in documents if 'passport' in doc.doc_type.lower()]
    
    if passport_docs:
        # Get existing name from aadhar if available
        existing_details = db.query(KycDetail).filter(KycDetail.kyc_case_id == passport_docs[0].kyc_case_id).first()
        name = existing_details.name if existing_details and existing_details.name else None
        
        extracted = mock_extract_passport_info(name)
        passport_info.update(extracted)
        print(f"✅ DEBUG: Extracted Passport info: {extracted}")
    
    return passport_info

def get_user_info_from_registration(kyc_case, db):
    """Get user information from registration"""
    user_info = {}
    
    if kyc_case.user_id:
        user = db.query(User).filter(User.id == kyc_case.user_id).first()
        if user:
            user_info.update({
                'email': user.email,
                'phone': user.phone
            })
    
    return user_info

def get_auto_populated_kyc_details(case_id: int, db: Session):
    """Get auto-populated KYC details from uploaded documents and registration"""
    try:
        # Get KYC case
        kyc_case = db.query(KycCase).filter(KycCase.id == case_id).first()
        if not kyc_case:
            return None
        
        # Get all documents for this case
        documents = db.query(KycDocument).filter(KycDocument.kyc_case_id == case_id).all()
        
        # Extract information from different sources
        user_info = get_user_info_from_registration(kyc_case, db)
        aadhar_info = extract_aadhar_info(documents, db)
        pan_info = extract_pan_info(documents, db)
        passport_info = extract_passport_info(documents, db)
        
        # Merge all information (user info takes precedence for email/phone)
        auto_details = {}
        auto_details.update(aadhar_info)
        auto_details.update(pan_info)
        auto_details.update(passport_info)
        auto_details.update(user_info)  # User info overrides extracted info for email/phone
        
        # Add default values for required fields
        auto_details.update({
            'occupation': 'Not specified',
            'source_of_funds': 'Not specified',
            'business_type': 'Not specified',
            'is_pep': False,
            'pep_details': '',
            'annual_income': 'Not specified',
            'purpose_of_account': 'Personal',
            'marital_status': 'Not specified',
            'nominee_name': '',
            'nominee_relation': '',
            'nominee_contact': ''
        })
        
        return auto_details
        
    except Exception as e:
        print(f"Error getting auto-populated details: {e}")
        return None

@app.get("/kyc/auto-details/{case_id}")
def get_auto_populated_details(case_id: int, db: Session = Depends(get_db)):
    """Get auto-populated KYC details from uploaded documents and registration"""
    try:
        print(f"🔍 DEBUG: Getting auto-populated details for case_id: {case_id}")
        
        auto_details = get_auto_populated_kyc_details(case_id, db)
        
        if auto_details:
            print(f"✅ DEBUG: Auto-populated details found for case {case_id}")
            return {
                "success": True,
                "message": "Auto-populated details retrieved successfully",
                "kyc_case_id": case_id,
                "details": auto_details
            }
        else:
            print(f"❌ DEBUG: No auto-populated details found for case {case_id}")
            raise HTTPException(status_code=404, detail="No auto-populated details found")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ DEBUG: Error getting auto-populated details: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get auto-populated details: {str(e)}")

# Add a specific endpoint to serve files (as a fallback)
@app.get("/files/{file_path:path}")
async def get_file(file_path: str):
    # Handle S3 URLs regardless of environment
    if file_path.startswith("s3://"):
        # Extract the S3 key from the file path
        s3_key = file_path.replace("s3://", "").split("/", 1)[1]
        
        # Generate pre-signed URL for S3
        try:
            download_url = storage.get_file_url(s3_key)
            if download_url:
                return {"download_url": download_url}
            else:
                raise HTTPException(status_code=404, detail="File not found in S3")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error accessing file: {str(e)}")
    
    # Handle local files based on environment
    if ENV == "aws":
        # For AWS Lambda, try to convert local path to S3 key
        s3_key = file_path
        
        # Generate pre-signed URL for S3
        try:
            download_url = storage.get_file_url(s3_key)
            if download_url:
                return {"download_url": download_url}
            else:
                raise HTTPException(status_code=404, detail="File not found in S3")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error accessing file: {str(e)}")
    else:
        # For local development, serve files from local filesystem
        file_location = os.path.join("uploads", file_path)
        if not os.path.exists(file_location):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Determine content type based on file extension
        content_type = None
        if file_path.lower().endswith('.webm'):
            content_type = 'video/webm'
        elif file_path.lower().endswith('.mp4'):
            content_type = 'video/mp4'
        elif file_path.lower().endswith(('.jpg', '.jpeg')):
            content_type = 'image/jpeg'
        elif file_path.lower().endswith('.png'):
            content_type = 'image/png'
        elif file_path.lower().endswith('.pdf'):
            content_type = 'application/pdf'
        
        return FileResponse(
            file_location,
            media_type=content_type,
            headers={
                'Accept-Ranges': 'bytes',
                'Cache-Control': 'public, max-age=3600'
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
 