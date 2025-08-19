"""Database models for the CMS"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class FormSubmission(Base):
    """Model for storing form submissions from modal dialogs"""
    __tablename__ = 'form_submissions'
    
    id = Column(Integer, primary_key=True)
    form_type = Column(String(50), nullable=False)  # email_signup, contact, etc.
    email = Column(String(255))
    name = Column(String(255))
    subject = Column(String(255))
    message = Column(Text)
    phone = Column(String(50))
    company = Column(String(255))
    data = Column(Text)  # JSON for additional fields
    created_at = Column(DateTime, default=datetime.utcnow)
    page_url = Column(String(500))  # Track which page the form was submitted from
    
    def __repr__(self):
        return f"<FormSubmission {self.form_type}: {self.email}>"

class ComponentUsage(Base):
    """Track which components are used on which pages"""
    __tablename__ = 'component_usage'
    
    id = Column(Integer, primary_key=True)
    page_path = Column(String(500), nullable=False)
    component_type = Column(String(50), nullable=False)  # hero, card, cta, etc.
    component_data = Column(Text)  # JSON of component parameters
    created_at = Column(DateTime, default=datetime.utcnow)

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()