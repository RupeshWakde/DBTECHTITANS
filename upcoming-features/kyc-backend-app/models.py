from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    kyc_details = relationship('KycDetail', back_populates='user', uselist=False)
    kyc_status = relationship('KycStatus', back_populates='user', uselist=False)

class KycDocument(Base):
    __tablename__ = 'kyc_documents'
    id = Column(Integer, primary_key=True, index=True)
    kyc_case_id = Column(Integer, ForeignKey('kyc_cases.id'))
    doc_type = Column(String, nullable=False)  # e.g., 'aadhar-front', 'aadhar-back', 'pancard', etc.
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    kyc_case = relationship('KycCase', back_populates='kyc_documents')

class KycDetail(Base):
    __tablename__ = 'kyc_details'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    kyc_case_id = Column(Integer, ForeignKey('kyc_cases.id'))
    name = Column(String)
    dob = Column(String)
    gender = Column(String)
    address = Column(Text)
    father_name = Column(String)
    pan_number = Column(String)
    aadhar_number = Column(String)
    email = Column(String)
    phone = Column(String)
    occupation = Column(String)
    source_of_funds = Column(String)
    business_type = Column(String)
    is_pep = Column(Boolean, default=False)
    pep_details = Column(String)
    annual_income = Column(String)
    purpose_of_account = Column(String)
    nationality = Column(String)
    marital_status = Column(String)
    nominee_name = Column(String)
    nominee_relation = Column(String)
    nominee_contact = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='kyc_details')

class KycStatus(Base):
    __tablename__ = 'kyc_status'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String, default='pending')  # e.g., 'pending', 'submitted', 'approved', 'rejected'
    kyc_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship('User', back_populates='kyc_status')

class KycCase(Base):
    __tablename__ = 'kyc_cases'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String, default='initiated')  # initiated, in_progress, submitted, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationships
    kyc_documents = relationship('KycDocument', back_populates='kyc_case') 