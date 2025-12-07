"""
HireLens AI - Database Initialization Utility
Run this script to initialize the database and create sample data
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from database import engine, SessionLocal, init_db
from models import User, Job
from auth import get_password_hash
from datetime import datetime

def create_sample_jobs():
    """Create sample job postings for testing"""
    db = SessionLocal()
    
    sample_jobs = [
        {
            "title": "Senior Full Stack Developer",
            "description": """
We are seeking a Senior Full Stack Developer with 5+ years of experience.

Required Skills:
- Python, JavaScript, TypeScript
- React, Node.js, Express
- PostgreSQL, MongoDB
- AWS, Docker, Kubernetes
- Git, CI/CD

Responsibilities:
- Develop scalable web applications
- Lead technical architecture decisions
- Mentor junior developers
- Collaborate with cross-functional teams

Nice to have:
- Experience with microservices
- Knowledge of GraphQL
- Agile/Scrum methodology
            """,
            "required_skills": [
                "Python", "JavaScript", "TypeScript", "React", "Node.js",
                "PostgreSQL", "MongoDB", "AWS", "Docker", "Kubernetes"
            ]
        },
        {
            "title": "Data Scientist",
            "description": """
Looking for a Data Scientist to join our AI/ML team.

Required Skills:
- Python, R, SQL
- Machine Learning, Deep Learning
- TensorFlow, PyTorch, scikit-learn
- Pandas, NumPy, Matplotlib
- Statistics, Data Analysis

Responsibilities:
- Build and deploy ML models
- Analyze large datasets
- Develop predictive algorithms
- Present findings to stakeholders

Preferred:
- PhD in related field
- Experience with NLP
- Big Data technologies (Spark, Hadoop)
            """,
            "required_skills": [
                "Python", "R", "SQL", "Machine Learning", "TensorFlow",
                "PyTorch", "Pandas", "NumPy", "Data Analysis"
            ]
        },
        {
            "title": "Frontend Developer",
            "description": """
Seeking a talented Frontend Developer for web application development.

Required Skills:
- HTML5, CSS3, JavaScript
- React or Vue.js
- Responsive design
- CSS frameworks (Tailwind, Bootstrap)
- Git version control

Responsibilities:
- Build user interfaces
- Implement responsive designs
- Optimize web performance
- Collaborate with designers and backend team

Nice to have:
- TypeScript experience
- Testing frameworks (Jest, Cypress)
- UI/UX design skills
            """,
            "required_skills": [
                "HTML", "CSS", "JavaScript", "React", "Vue",
                "Responsive Design", "Git"
            ]
        }
    ]
    
    print("Creating sample job postings...")
    
    for job_data in sample_jobs:
        # Check if job already exists
        existing = db.query(Job).filter(Job.title == job_data["title"]).first()
        if not existing:
            job = Job(**job_data)
            db.add(job)
            print(f"  ✓ Created: {job_data['title']}")
        else:
            print(f"  ⚠ Skipped (exists): {job_data['title']}")
    
    db.commit()
    db.close()
    print("✅ Sample jobs created successfully!")

def create_test_user():
    """Create a test user for development"""
    db = SessionLocal()
    
    test_email = "test@hirelens.ai"
    
    # Check if user already exists
    existing = db.query(User).filter(User.email == test_email).first()
    
    if existing:
        print(f"⚠️  Test user already exists: {test_email}")
    else:
        test_user = User(
            email=test_email,
            password_hash=get_password_hash("test123456")
        )
        db.add(test_user)
        db.commit()
        print(f"✅ Test user created: {test_email}")
        print(f"   Password: test123456")
    
    db.close()

def main():
    """Main initialization function"""
    print("=" * 60)
    print("    HireLens AI - Database Initialization")
    print("=" * 60)
    print()
    
    # Initialize database
    print("Step 1: Initializing database...")
    try:
        init_db()
        print("✅ Database initialized!")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return
    
    print()
    
    # Create test user
    print("Step 2: Creating test user...")
    try:
        create_test_user()
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
    
    print()
    
    # Create sample jobs
    print("Step 3: Creating sample job postings...")
    try:
        create_sample_jobs()
    except Exception as e:
        print(f"❌ Error creating sample jobs: {e}")
    
    print()
    print("=" * 60)
    print("    Initialization Complete!")
    print("=" * 60)
    print()
    print("📝 Test Credentials:")
    print("   Email: test@hirelens.ai")
    print("   Password: test123456")
    print()
    print("🚀 Next Steps:")
    print("   1. Start backend: .\\start.ps1")
    print("   2. Start frontend: .\\start-frontend.ps1")
    print("   3. Open browser: http://localhost:3000")
    print("   4. Login with test credentials")
    print()

if __name__ == "__main__":
    main()
