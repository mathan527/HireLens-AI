from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import os

from database import get_db, init_db
from auth import (
    get_password_hash, 
    authenticate_user, 
    create_access_token, 
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from models import User, Resume
from schema import (
    UserRegister, 
    UserLogin, 
    Token, 
    UserResponse,
    DashboardData
)

# Import routers
from resume import router as resume_router
from jobs import router as jobs_router

# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

# Initialize FastAPI app
app = FastAPI(
    title="HireLens AI",
    description="AI Resume Analyzer & Job Matcher",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# CORS Configuration
# In production, replace with your actual frontend domain
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()
    print("🚀 HireLens AI API is running!")
    print("📚 API Documentation: http://localhost:8000/docs")

# Include routers
app.include_router(resume_router)
app.include_router(jobs_router)

# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.post("/api/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - Email must be unique
    - Password is hashed using bcrypt
    """
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.post("/api/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return JWT token
    
    - Token expires after 30 minutes (configurable)
    - Token must be sent in Authorization header as Bearer token
    """
    
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return current_user

# ============================================
# DASHBOARD ROUTE
# ============================================

@app.get("/api/dashboard", response_model=DashboardData)
def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get dashboard data for current user
    
    Returns:
    - User information
    - Latest resume analysis
    - Total resumes uploaded
    - Average ATS score
    - Recent job matches
    """
    from sqlalchemy import func, desc
    
    # Optimized query: Get count and average in single query
    stats = db.query(
        func.count(Resume.id).label('total'),
        func.avg(Resume.ats_score).label('avg_score')
    ).filter(Resume.user_id == current_user.id).first()
    
    total_resumes = stats.total or 0
    avg_ats_score = round(float(stats.avg_score or 0), 2)
    
    # Get latest resume only if exists (optimized query)
    latest_resume = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).order_by(desc(Resume.created_at)).first()
    
    # Get recent matches (placeholder - expand as needed)
    recent_matches = []
    
    return DashboardData(
        user=current_user,
        latest_resume=latest_resume,
        total_resumes=total_resumes,
        average_ats_score=avg_ats_score,
        recent_matches=recent_matches
    )

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/")
def root():
    """Root endpoint - API health check"""
    return {
        "message": "HireLens AI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# ============================================
# SERVE FRONTEND (Optional - for development)
# ============================================

# Uncomment to serve frontend from FastAPI
# app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
