from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# ============================================
# USER SCHEMAS
# ============================================

class UserRegister(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=6, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# ============================================
# RESUME SCHEMAS
# ============================================

class ResumeUpload(BaseModel):
    filename: str
    raw_text: str

class ResumeAnalysis(BaseModel):
    id: int
    filename: str
    raw_text: str
    extracted_skills: List[str]
    technical_skills: List[str]
    soft_skills: List[str]
    tools: List[str]
    ats_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class SkillsExtracted(BaseModel):
    all_skills: List[str]
    technical_skills: List[str]
    soft_skills: List[str]
    tools: List[str]

# ============================================
# JOB SCHEMAS
# ============================================

class JobCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str = Field(..., min_length=10, max_length=50000)
    required_skills: Optional[List[str]] = Field(default=[], max_length=100)

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    required_skills: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class JobMatchRequest(BaseModel):
    resume_id: int = Field(..., gt=0)
    job_description: str = Field(..., min_length=10, max_length=50000)
    job_title: Optional[str] = Field(default="Target Position", max_length=500)

class JobMatchResponse(BaseModel):
    match_percentage: float
    missing_skills: List[str]
    matched_skills: List[str]
    ai_feedback: Optional[str] = None

# ============================================
# DASHBOARD SCHEMAS
# ============================================

class DashboardData(BaseModel):
    user: UserResponse
    latest_resume: Optional[ResumeAnalysis] = None
    total_resumes: int
    average_ats_score: float
    recent_matches: List[Dict[str, Any]]

# ============================================
# AI FEEDBACK SCHEMA
# ============================================

class AIFeedback(BaseModel):
    ats_score: float
    missing_skills: List[str]
    improvements: List[str]
    rewritten_bullets: List[str]
    recruiter_summary: str
