#!/usr/bin/env python3
"""
Script to check KYC details in the database
"""

import os
import sys

# Set environment variables
os.environ["ENV"] = "aws"
os.environ["AWS_ACCESS_KEY_ID"] = "ASIAUJ7F2IOMXUXSMLL5"
os.environ["AWS_SECRET_ACCESS_KEY"] = "M9i/vqier60Cl2/KwhRM7AslBW7XIZ/B6saa8Mtj"
os.environ["AWS_SESSION_TOKEN"] = "IQoJb3JpZ2luX2VjEMP//////////wEaCXVzLWVhc3QtMiJHMEUCIQDa9E4zEy4L0vxZ4AkMEezcNdHrFb1teSmD8kUf5vuUlgIgIsVCSvYcjpKxX3V+bGcmPSGPMzERYr5ts5d8lY6T7ocqugMInP//////////ARAAGgwyOTYyOTc4NDE1NjEiDBImw4Da7BiYAODdHyqOA7b1CV95/UhqrsrWb2VV41G7Cxc/JLcLAhIJH5W+F3Ndot1dRNd+/zKHl4NBE9Rj6kEHv76P+btsi/9UHUYMQHRf5AlGjKojIffssUPDQqyXRnafVP4N3BeDndGTMQCvrn+kaSqSoUac92mwplNJSDd6hevYxanzTNEkEphreitFo1cFgkHWYZ+Tvuga+omTNuGixLLlYy2laZi15wCbmT4A75AMQm+jMfJ7EVv0FuIz9/R2+6ZdP4dEsmgCJRO2EFE3Lw0x+5gcpwAIJe91UAx4aE+/W2pfFzL6oJlNrbAB3vMSSM1nQDOuJJeQUu40fiPXt/CtAUvNiq4wBYLeebjqhb5BzdUcJOFS6TpZouvG1gGlH7lO2Cvp1OZUgENvnfHF4r4ag55v56E5O5N0ZKrMRMZQDVlhT1oFwYQ5pFy80VkqqGFgumst82MB9BJCc3DdQYBUiy+c8DRIeusHzyrmls/gE+UOIiiUC+IwlgnytXs6bAKI4CfEp0DJuR54muAqSuTvor7xHd13GpkSMMCWmcIGOqYBsrJAuJKh2SUxlJvsexG25c0zoRtnCeCUfxZnpKpczkE6z3HegJBiTZn8pmRtj8Ii4hSv5v86Vo29rzOS1088widlzvDUtWA8941gqbH9Vt84JZHRs3lmPkyM5Eu0HgMnZxQqKdSwZMWciJ0Wr9xA9ilKUEBAlWqyOc7c/IvfUIewWTBH7RXfScount+opLvw0BmFAas+BAAGY/h+RaObp5mN8qrOoA=="
os.environ["AWS_REGION"] = "us-east-2"
os.environ["S3_BUCKET_NAME"] = "dbdtcckycbucket"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import get_database_url
from models import User, KycCase, KycDetail, KycDocument, KycStatus

def check_kyc_data():
    """Check all KYC data in the database"""
    print("🔍 Checking KYC data in database...")
    
    # Create engine
    database_url = get_database_url()
    print(f"Using database: {database_url}")
    
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check Users
        print("\n👥 USERS:")
        users = db.query(User).all()
        for user in users:
            print(f"  - User ID: {user.id}, Email: {user.email}, Phone: {user.phone}")
        
        # Check KYC Cases
        print("\n📋 KYC CASES:")
        cases = db.query(KycCase).all()
        for case in cases:
            print(f"  - Case ID: {case.id}, User ID: {case.user_id}, Status: {case.status}")
        
        # Check KYC Details
        print("\n📝 KYC DETAILS:")
        details = db.query(KycDetail).all()
        for detail in details:
            print(f"  - Detail ID: {detail.id}, Case ID: {detail.kyc_case_id}, Name: {detail.name}")
        
        # Check KYC Documents
        print("\n📄 KYC DOCUMENTS:")
        documents = db.query(KycDocument).all()
        for doc in documents:
            print(f"  - Doc ID: {doc.id}, Case ID: {doc.kyc_case_id}, Type: {doc.doc_type}")
        
        # Check KYC Status
        print("\n📊 KYC STATUS:")
        statuses = db.query(KycStatus).all()
        for status in statuses:
            print(f"  - Status ID: {status.id}, User ID: {status.user_id}, Status: {status.status}")
        
        # Check specific case 1
        print(f"\n🎯 DETAILED CHECK FOR CASE 1:")
        case_1 = db.query(KycCase).filter(KycCase.id == 1).first()
        if case_1:
            print(f"  - Case 1 exists with user_id: {case_1.user_id}")
            
            # Check details for case 1
            details_1 = db.query(KycDetail).filter(KycDetail.kyc_case_id == 1).first()
            if details_1:
                print(f"  - KYC Details found for case 1: {details_1.name}")
            else:
                print(f"  - No KYC Details found for case 1")
            
            # Check documents for case 1
            docs_1 = db.query(KycDocument).filter(KycDocument.kyc_case_id == 1).all()
            print(f"  - Documents for case 1: {len(docs_1)} documents")
            for doc in docs_1:
                print(f"    * {doc.doc_type}: {doc.file_path}")
        else:
            print(f"  - Case 1 not found")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_kyc_data() 