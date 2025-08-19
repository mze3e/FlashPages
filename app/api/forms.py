"""API routes for handling form submissions"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
import json
from datetime import datetime

from ..models import FormSubmission, get_db

router = APIRouter()

@router.post("/submit")
async def submit_form(request: Request, db: Session = Depends(get_db)):
    """Handle form submissions from modal dialogs"""
    try:
        # Get form data
        form_data = await request.form()
        form_dict = dict(form_data)
        
        # Get form type and page URL from request
        form_type = form_dict.pop('form_type', 'contact')
        page_url = str(request.url).replace('/api/forms/submit', '')
        
        # Create form submission record
        submission = FormSubmission(
            form_type=form_type,
            email=form_dict.get('email'),
            name=form_dict.get('name'),
            subject=form_dict.get('subject'),
            message=form_dict.get('message'),
            phone=form_dict.get('phone'),
            company=form_dict.get('company'),
            data=json.dumps(form_dict),  # Store all form data as JSON
            page_url=page_url,
            created_at=datetime.utcnow()
        )
        
        db.add(submission)
        db.commit()
        
        return {
            "status": "success",
            "message": "Form submitted successfully!",
            "id": submission.id
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit form: {str(e)}")

@router.get("/submissions/{form_type}")
async def get_submissions(form_type: str, db: Session = Depends(get_db)):
    """Get form submissions by type (for CMS admin)"""
    try:
        submissions = db.query(FormSubmission).filter(
            FormSubmission.form_type == form_type
        ).order_by(FormSubmission.created_at.desc()).limit(100).all()
        
        return {
            "status": "success",
            "submissions": [
                {
                    "id": s.id,
                    "email": s.email,
                    "name": s.name,
                    "subject": s.subject,
                    "message": s.message,
                    "phone": s.phone,
                    "company": s.company,
                    "created_at": s.created_at.isoformat(),
                    "page_url": s.page_url
                }
                for s in submissions
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get submissions: {str(e)}")

@router.get("/submissions")
async def get_all_submissions(db: Session = Depends(get_db)):
    """Get all form submissions (for CMS admin)"""
    try:
        submissions = db.query(FormSubmission).order_by(
            FormSubmission.created_at.desc()
        ).limit(200).all()
        
        return {
            "status": "success",
            "submissions": [
                {
                    "id": s.id,
                    "form_type": s.form_type,
                    "email": s.email,
                    "name": s.name,
                    "subject": s.subject,
                    "message": s.message[:100] + "..." if s.message and len(s.message) > 100 else s.message,
                    "created_at": s.created_at.isoformat(),
                    "page_url": s.page_url
                }
                for s in submissions
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get submissions: {str(e)}")

@router.delete("/submissions/{submission_id}")
async def delete_submission(submission_id: int, db: Session = Depends(get_db)):
    """Delete a form submission"""
    try:
        submission = db.query(FormSubmission).filter(FormSubmission.id == submission_id).first()
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")
        
        db.delete(submission)
        db.commit()
        
        return {"status": "success", "message": "Submission deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete submission: {str(e)}")