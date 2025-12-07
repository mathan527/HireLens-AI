from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from auth import get_current_user
from models import User, Resume, Job, JobMatch
from schema import JobCreate, JobResponse, JobMatchRequest, JobMatchResponse
from utils.matcher import calculate_match_score, get_match_interpretation
from utils.ai_feedback import get_ai_feedback

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.post("/create", response_model=JobResponse)
def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new job posting (for testing/demo purposes)"""
    
    new_job = Job(
        title=job_data.title,
        description=job_data.description,
        required_skills=job_data.required_skills
    )
    
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    return new_job

@router.get("/list", response_model=List[JobResponse])
def get_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all available jobs"""
    jobs = db.query(Job).all()
    return jobs

@router.post("/match", response_model=JobMatchResponse)
def match_job(
    match_request: JobMatchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Match a resume with a job description
    
    - Calculates match percentage using cosine similarity
    - Identifies missing skills
    - Provides AI-powered feedback
    """
    
    # Get resume
    resume = db.query(Resume).filter(
        Resume.id == match_request.resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    try:
        # Validate job description length
        if len(match_request.job_description.strip()) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Job description is too short. Minimum 10 characters required."
            )
        
        # Calculate match score
        match_result = calculate_match_score(
            resume.raw_text,
            match_request.job_description
        )
        
        # Get AI feedback
        try:
            ai_feedback = get_ai_feedback(
                resume_text=resume.raw_text[:3000],
                extracted_skills=resume.extracted_skills,
                job_description=match_request.job_description,
                missing_skills=match_result["missing_skills"]
            )
            
            feedback_text = f"""
ATS Score: {ai_feedback['ats_score']}/100

Key Improvements:
{chr(10).join('• ' + imp for imp in ai_feedback['improvements'])}

Suggested Bullet Points:
{chr(10).join('• ' + bullet for bullet in ai_feedback['rewritten_bullets'])}

Recruiter Summary:
{ai_feedback['recruiter_summary']}
            """
        except Exception as e:
            print(f"AI Feedback Error: {e}")
            feedback_text = f"""
Match Interpretation: {get_match_interpretation(match_result['match_percentage'])}

Technical Skills Matched: {len(match_result['matched_technical_skills'])}
Technical Skills Missing: {len(match_result['missing_technical_skills'])}

Focus on acquiring: {', '.join(match_result['missing_technical_skills'][:5])}
            """
        
        # Store match result (optional - for job matching history)
        # You could create a Job entry if needed
        
        response = JobMatchResponse(
            match_percentage=match_result["match_percentage"],
            missing_skills=match_result["missing_skills"],
            matched_skills=match_result["matched_skills"],
            ai_feedback=feedback_text
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error matching job: {str(e)}"
        )

@router.get("/matches/{resume_id}")
def get_resume_matches(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all job matches for a specific resume"""
    
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    matches = db.query(JobMatch).filter(JobMatch.resume_id == resume_id).all()
    
    return {
        "resume_id": resume_id,
        "total_matches": len(matches),
        "matches": matches
    }
