from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import json

from database import get_db
from auth import get_current_user
from models import User, Resume, Job, JobMatch
from schema import ResumeAnalysis, JobMatchRequest, JobMatchResponse
from utils.pdf_parser import parse_pdf, clean_text
from utils.skill_extractor import extract_skills
from utils.ats_scorer import calculate_ats_score
from utils.matcher import calculate_match_score
from utils.ai_feedback import get_ai_feedback

router = APIRouter(prefix="/api/resume", tags=["Resume"])

@router.post("/upload", response_model=ResumeAnalysis)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload and analyze resume
    
    - Extracts text from PDF
    - Extracts skills using NLP
    - Calculates ATS score
    - Stores in database
    """
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    try:
        # Validate file size (max 10MB)
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large. Maximum size is 10MB."
            )
        
        # Read file content
        content = await file.read()
        
        # Extract text from PDF (run in thread pool to avoid blocking)
        import asyncio
        loop = asyncio.get_event_loop()
        raw_text = await loop.run_in_executor(None, parse_pdf, content)
        cleaned_text = clean_text(raw_text)
        
        if len(cleaned_text) < 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resume text is too short. Please upload a complete resume."
            )
        
        # Extract skills
        skills_data = extract_skills(cleaned_text)
        
        # Calculate ATS score
        ats_result = calculate_ats_score(cleaned_text)
        
        # Create resume record
        new_resume = Resume(
            user_id=current_user.id,
            filename=file.filename,
            raw_text=cleaned_text,
            extracted_skills=skills_data["all_skills"],
            technical_skills=skills_data["technical_skills"],
            soft_skills=skills_data["soft_skills"],
            tools=skills_data["tools"],
            ats_score=ats_result["overall_score"]
        )
        
        db.add(new_resume)
        db.commit()
        db.refresh(new_resume)
        
        return new_resume
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        import traceback
        print(f"Resume processing error: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing resume. Please ensure the PDF is valid and contains readable text."
        )

@router.get("/list", response_model=List[ResumeAnalysis])
def get_user_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all resumes for current user"""
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    return resumes

@router.get("/{resume_id}", response_model=ResumeAnalysis)
def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific resume by ID"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    return resume

@router.post("/analyze/{resume_id}")
def analyze_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Re-analyze existing resume and update ATS score"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Recalculate everything
    skills_data = extract_skills(resume.raw_text)
    ats_result = calculate_ats_score(resume.raw_text)
    
    # Update resume
    resume.extracted_skills = skills_data["all_skills"]
    resume.technical_skills = skills_data["technical_skills"]
    resume.soft_skills = skills_data["soft_skills"]
    resume.tools = skills_data["tools"]
    resume.ats_score = ats_result["overall_score"]
    
    db.commit()
    db.refresh(resume)
    
    return {
        "message": "Resume re-analyzed successfully",
        "resume": resume,
        "ats_breakdown": ats_result
    }

@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a resume"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    db.delete(resume)
    db.commit()
    
    return {"message": "Resume deleted successfully"}
