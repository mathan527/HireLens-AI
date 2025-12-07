# 🔍 HireLens AI - AI Resume Analyzer & Job Matcher

A complete production-ready web application that analyzes resumes using AI/NLP, calculates ATS scores, extracts skills, and matches resumes with job descriptions.

![HireLens AI](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Usage Guide](#usage-guide)
- [AI Integration](#ai-integration)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### 🔐 User Authentication
- JWT-based secure authentication
- Email/password registration and login
- Password hashing with bcrypt
- Protected routes with token validation

### 📄 Resume Analysis
- **PDF Parsing**: Extract text from PDF resumes using pdfplumber and PyMuPDF
- **NLP Skill Extraction**: Identify technical skills, soft skills, and tools using spaCy
- **ATS Score Calculation**: Comprehensive 0-100 score based on:
  - Keyword density (40%)
  - Resume formatting (20%)
  - Action verbs usage (15%)
  - Experience relevance (15%)
  - Skill match (10%)

### 🎯 Job Matching Engine
- Compare resume with job descriptions
- Cosine similarity-based matching
- TF-IDF vectorization
- Return match percentage and missing skills

### 🤖 AI Resume Feedback
- Integration with OpenAI GPT or Google Gemini
- Personalized improvement suggestions
- Rewritten bullet points with action verbs
- Recruiter-style feedback summary

### 📊 Interactive Dashboard
- Visual ATS score display with Chart.js
- Skills breakdown by category
- Job match visualization
- Progress tracking

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Server**: Uvicorn (ASGI)
- **Database**: SQLite (easily switchable to PostgreSQL)
- **ORM**: SQLAlchemy
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt

### AI & NLP
- **NLP**: spaCy (en_core_web_sm)
- **PDF Processing**: pdfplumber, PyMuPDF
- **AI APIs**: OpenAI GPT-3.5 or Google Gemini
- **ML**: scikit-learn (TF-IDF, cosine similarity)
- **Embeddings**: sentence-transformers

### Frontend
- **Pure HTML5**
- **Pure CSS3** (Custom responsive design)
- **Vanilla JavaScript** (ES6+)
- **Visualization**: Chart.js

---

## 📁 Project Structure

```
HireLens AI/
│
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── auth.py                 # Authentication logic (JWT)
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy models
│   ├── schema.py               # Pydantic schemas
│   ├── resume.py               # Resume API routes
│   ├── jobs.py                 # Job matching API routes
│   │
│   └── utils/
│       ├── pdf_parser.py       # PDF text extraction
│       ├── skill_extractor.py  # NLP skill extraction
│       ├── ats_scorer.py       # ATS score calculation
│       ├── matcher.py          # Job matching algorithm
│       └── ai_feedback.py      # AI feedback generation
│
├── frontend/
│   ├── index.html              # Landing page
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── dashboard.html          # Main dashboard
│   │
│   ├── css/
│   │   └── style.css           # Complete styling
│   │
│   └── js/
│       ├── main.js             # Utility functions
│       ├── auth.js             # Authentication logic
│       └── dashboard.js        # Dashboard functionality
│
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore file
└── README.md                   # This file
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Git**

### Step 1: Clone Repository

```powershell
git clone <your-repo-url>
cd "HireLens AI"
```

### Step 2: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
# Install Python packages
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

---

## ⚙️ Configuration

### 1. Create Environment File

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

### 2. Edit `.env` File

Open `.env` and configure:

```env
# Database (SQLite by default)
DATABASE_URL=sqlite:///./hirelens.db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Provider (choose: "openai" or "gemini")
AI_PROVIDER=gemini

# OpenAI API Key (if using OpenAI)
OPENAI_API_KEY=your-openai-api-key-here

# Gemini API Key (if using Gemini)
GEMINI_API_KEY=your-gemini-api-key-here

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### 3. Get AI API Keys

#### Option A: Google Gemini (Recommended - Free tier available)
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy to `.env` as `GEMINI_API_KEY`

#### Option B: OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy to `.env` as `OPENAI_API_KEY`

### 4. Database Setup (Optional)

**For PostgreSQL** (production):

```env
DATABASE_URL=postgresql://username:password@localhost:5432/hirelens
```

Install PostgreSQL driver:
```powershell
pip install psycopg2-binary
```

---

## 🏃 Running the Application

### Start Backend Server

```powershell
# Navigate to backend directory
cd backend

# Run with Python
python main.py

# OR run with Uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: **http://localhost:8000**

### Open Frontend

#### Option 1: Simple HTTP Server (Recommended)

```powershell
# Navigate to frontend directory
cd ..\frontend

# Start Python HTTP server
python -m http.server 3000
```

Open browser: **http://localhost:3000**

#### Option 2: Open Directly

Open `frontend/index.html` in your browser.

**Note**: CORS is enabled in the backend for `http://localhost:3000` and file protocol.

---

## 📚 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
```
POST /api/register          # Register new user
POST /api/login             # Login user
GET  /api/me                # Get current user
```

#### Resume
```
POST /api/resume/upload     # Upload and analyze resume
GET  /api/resume/list       # Get all user resumes
GET  /api/resume/{id}       # Get specific resume
POST /api/resume/analyze/{id} # Re-analyze resume
DELETE /api/resume/{id}     # Delete resume
```

#### Jobs
```
POST /api/jobs/create       # Create job posting
GET  /api/jobs/list         # List all jobs
POST /api/jobs/match        # Match resume with job
GET  /api/jobs/matches/{resume_id} # Get job matches
```

#### Dashboard
```
GET /api/dashboard          # Get dashboard data
```

---

## 📖 Usage Guide

### 1. Register Account
1. Open the application
2. Click "Get Started" or "Register"
3. Enter email and password (min 6 characters)
4. Click "Create Account"

### 2. Login
1. Click "Login"
2. Enter credentials
3. You'll be redirected to the dashboard

### 3. Upload Resume
1. On the dashboard, click "Choose PDF File"
2. Select your resume (PDF format only)
3. Click "Upload & Analyze"
4. Wait for analysis (10-30 seconds)

### 4. View Results
- **ATS Score**: See your overall score out of 100
- **Skills**: View extracted technical skills, soft skills, and tools
- **Score Breakdown**: Detailed component scores
- **Charts**: Visual representation of your data

### 5. Match with Job
1. Scroll to "Job Matching" section
2. Paste a job description
3. Click "Calculate Match"
4. View:
   - Match percentage
   - Matched skills
   - Missing skills
   - AI feedback (if API key configured)

---

## 🤖 AI Integration

### Using Gemini (Google)

```python
# In .env
AI_PROVIDER=gemini
GEMINI_API_KEY=your-key-here
```

**Pros:**
- Free tier available
- Fast responses
- Good quality feedback

### Using OpenAI

```python
# In .env
AI_PROVIDER=openai
OPENAI_API_KEY=your-key-here
```

**Pros:**
- High-quality responses
- Well-documented
- Industry standard

### Fallback Mode

If no API key is configured, the system provides **default feedback** based on rule-based analysis.

---

## 🐛 Troubleshooting

### Issue: "Import 'spacy' could not be resolved"

**Solution:**
```powershell
python -m spacy download en_core_web_sm
```

### Issue: "Database locked" error

**Solution:**
Close all connections to the database or use PostgreSQL instead of SQLite.

### Issue: CORS errors in browser

**Solution:**
Ensure you're running frontend on `http://localhost:3000` or update CORS settings in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    ...
)
```

### Issue: PDF parsing fails

**Solution:**
Ensure PDF has selectable text (not scanned image). Try both parsing methods implemented.

### Issue: AI feedback not showing

**Solutions:**
1. Check API key is correct in `.env`
2. Verify `AI_PROVIDER` is set correctly
3. Check API quota/credits
4. System will fallback to default feedback

---

## 🔒 Security Notes

### For Production Deployment:

1. **Change SECRET_KEY**: Generate a strong random key
   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Use HTTPS**: Deploy behind reverse proxy (nginx/Apache)

3. **Update CORS**: Specify exact origins instead of `"*"`

4. **Environment Variables**: Never commit `.env` file

5. **Database**: Use PostgreSQL instead of SQLite

6. **Rate Limiting**: Add rate limiting middleware

---

## 📊 Performance

- **Resume Upload**: 2-5 seconds
- **ATS Scoring**: < 1 second
- **Job Matching**: 1-3 seconds
- **AI Feedback**: 3-10 seconds (depends on API)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🎯 Roadmap

- [ ] Resume templates
- [ ] Cover letter generation
- [ ] Multiple file format support
- [ ] Email notifications
- [ ] Resume versioning
- [ ] Advanced analytics
- [ ] LinkedIn integration
- [ ] Bulk job matching

---

## 💡 Tips for Best Results

### Resume Optimization Tips:

1. **Use Action Verbs**: Start bullet points with strong verbs (Developed, Implemented, Led)
2. **Quantify Achievements**: Include numbers and metrics (Increased by 30%)
3. **Keywords**: Include relevant technical skills and tools
4. **Format**: Use clear sections (Experience, Education, Skills)
5. **Length**: Keep it 1-2 pages (400-2000 words optimal)

### ATS Score Improvement:

- **80-100**: Excellent - Ready to apply
- **70-79**: Good - Minor tweaks needed
- **60-69**: Fair - Review missing skills
- **Below 60**: Needs significant work

---

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Email: support@hirelens.ai (example)
- Documentation: Check `/docs` endpoint

---

## 🙏 Acknowledgments

- **spaCy** for NLP capabilities
- **FastAPI** for the excellent framework
- **Chart.js** for visualizations
- **OpenAI/Google** for AI APIs

---

## ⭐ Star this project

If you find HireLens AI helpful, please give it a star on GitHub!

---

**Built with ❤️ by AI Engineers for Job Seekers**

*Last Updated: December 2025*
