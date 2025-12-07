# 🔧 Developer Guide - HireLens AI

A comprehensive guide for developers who want to understand, modify, or extend HireLens AI.

---

## 📚 Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Backend Deep Dive](#backend-deep-dive)
3. [Frontend Deep Dive](#frontend-deep-dive)
4. [Adding New Features](#adding-new-features)
5. [Customization Guide](#customization-guide)
6. [Best Practices](#best-practices)

---

## 🏗️ Architecture Overview

### System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   HTML      │  │     CSS     │  │  JavaScript │        │
│  │  Structure  │  │   Styling   │  │    Logic    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│         │                │                │                  │
│         └────────────────┴────────────────┘                 │
│                         │                                    │
│                    Fetch API                                 │
│                         │                                    │
└─────────────────────────┼────────────────────────────────────┘
                          │
                     HTTP/JSON
                          │
┌─────────────────────────┼────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              API Routes Layer                        │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │    │
│  │  │   Auth   │  │  Resume  │  │   Jobs   │          │    │
│  │  └──────────┘  └──────────┘  └──────────┘          │    │
│  └──────────────────────┬──────────────────────────────┘    │
│                         │                                    │
│  ┌──────────────────────┴──────────────────────────────┐    │
│  │           Business Logic Layer                       │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────┐   │    │
│  │  │ PDF Parser   │  │   NLP/AI     │  │ Matcher │   │    │
│  │  └──────────────┘  └──────────────┘  └─────────┘   │    │
│  └──────────────────────┬──────────────────────────────┘    │
│                         │                                    │
│  ┌──────────────────────┴──────────────────────────────┐    │
│  │              Data Access Layer                       │    │
│  │           SQLAlchemy ORM + Database                  │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                          │
                    External APIs
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
   OpenAI API                          Gemini API
```

---

## 🔙 Backend Deep Dive

### File Organization

```python
# main.py - Application entry point
# Purpose: Configure FastAPI app, include routers, CORS, startup events

# Key components:
app = FastAPI(...)  # Create app instance
app.add_middleware(CORSMiddleware, ...)  # CORS config
app.include_router(resume_router)  # Include routes
```

### Database Layer (`database.py`, `models.py`)

```python
# models.py - SQLAlchemy Models
# Define database schema using SQLAlchemy ORM

class User(Base):
    # Represents users table
    # Relationships: One-to-Many with Resume
    
class Resume(Base):
    # Represents resumes table
    # Relationships: Many-to-One with User
    #                One-to-Many with JobMatch

# Benefits:
# - Automatic schema creation
# - Type safety
# - Easy querying
# - Relationship management
```

### Authentication Flow (`auth.py`)

```python
# JWT Authentication Flow:
1. User registers → Password hashed with bcrypt
2. User logs in → Credentials verified
3. Generate JWT token → Contains user email + expiration
4. Return token to client → Stored in localStorage
5. Client sends token in Authorization header
6. Server validates token → Extracts user info
7. Grants access to protected routes

# Key functions:
get_password_hash()      # Hash password
verify_password()        # Verify password
create_access_token()    # Generate JWT
decode_token()           # Validate JWT
get_current_user()       # Dependency for protected routes
```

### Resume Processing Pipeline

```python
# resume.py - Resume upload endpoint
1. Receive PDF file
2. Validate file type
3. Extract text using pdf_parser.py
4. Clean and normalize text
5. Extract skills using skill_extractor.py
6. Calculate ATS score using ats_scorer.py
7. Store in database
8. Return analysis results

# Key utilities:
pdf_parser.py        # PDF → Text extraction
skill_extractor.py   # Text → Skills extraction
ats_scorer.py        # Resume → ATS score
```

### NLP Pipeline (`skill_extractor.py`)

```python
# Skill Extraction Process:
1. Load spaCy model (en_core_web_sm)
2. Define skill databases (technical, soft, tools)
3. Text preprocessing:
   - Convert to lowercase
   - Tokenization
4. Pattern matching:
   - Regex for known skills
   - Word boundary matching
5. NLP analysis:
   - Part-of-speech tagging
   - Named entity recognition
   - Noun chunk extraction
6. Categorization:
   - Technical skills
   - Soft skills
   - Tools and frameworks
7. Return structured data

# Skill databases contain:
- 50+ programming languages
- 30+ frameworks
- 20+ databases
- 25+ soft skills
- 30+ tools
```

### ATS Scoring Algorithm (`ats_scorer.py`)

```python
# Scoring Components:

1. Keyword Density (40%):
   - Important sections present
   - Relevant keywords count
   - Technical skills presence
   
2. Formatting (20%):
   - Email present
   - Phone number present
   - Dates formatted correctly
   - Bullet points used
   - Appropriate length
   
3. Action Verbs (15%):
   - Count of strong action verbs
   - Developed, Implemented, Led, etc.
   
4. Experience Relevance (15%):
   - Quantifiable achievements
   - Numbers and metrics present
   
5. Skill Match (10%):
   - Match with job description
   - Cosine similarity

# Final score: Weighted average (0-100)
```

### Job Matching Engine (`matcher.py`)

```python
# Matching Algorithm:

1. Text Preprocessing:
   - Clean both resume and job description
   
2. Feature Extraction:
   - Extract skills from both
   - Convert to skill sets
   
3. TF-IDF Vectorization:
   - Convert text to numerical vectors
   - Weight by term frequency and inverse document frequency
   
4. Similarity Calculation:
   - Cosine similarity between vectors
   - Skill overlap percentage
   
5. Weighted Score:
   - 40% skill match rate
   - 30% technical skill match
   - 30% cosine similarity
   
6. Missing Skills Analysis:
   - Set difference: job_skills - resume_skills

# Result: Match percentage + detailed breakdown
```

### AI Integration (`ai_feedback.py`)

```python
# AI Provider Abstraction:

def get_ai_feedback():
    if AI_PROVIDER == "openai":
        return get_openai_feedback()
    elif AI_PROVIDER == "gemini":
        return get_gemini_feedback()
    else:
        return get_default_feedback()

# Prompt Engineering:
- Clear role definition: "You are a professional ATS evaluator"
- Structured input: Resume + Skills + Job Description
- JSON output format required
- Specific task breakdown

# Response Parsing:
- Extract JSON from markdown code blocks
- Validate structure
- Fallback to default if parsing fails
```

---

## 🎨 Frontend Deep Dive

### Page Structure

```javascript
// index.html - Landing page
- Hero section with CTA
- Features showcase
- How it works
- Call to action
- Footer

// login.html & register.html - Authentication
- Form handling
- Validation
- API integration
- Error display
- Redirect on success

// dashboard.html - Main application
- Navigation with user info
- Stats cards (overview)
- Resume upload section
- ATS score display
- Skills visualization
- Job matching
- AI feedback display
- Charts and graphs
```

### JavaScript Architecture

```javascript
// main.js - Utility functions
- API_BASE_URL configuration
- getAuthToken() - Token management
- isAuthenticated() - Auth check
- requireAuth() - Route protection
- apiCall() - Centralized API calls
- showLoading() - Loading states
- showError/showSuccess() - User feedback

// auth.js - Authentication logic
- Login form handler
- Register form handler
- Password validation
- Token storage
- Redirect logic

// dashboard.js - Core functionality
- initDashboard() - Initialize on load
- loadDashboardData() - Fetch user data
- handleResumeUpload() - File upload
- displayResumeData() - Show results
- createScoreChart() - Chart.js integration
- displaySkills() - Skill categorization
- handleJobMatch() - Job matching
- displayMatchResults() - Show match
```

### State Management

```javascript
// Global state variables
let currentResume = null;  // Currently displayed resume
let currentSkills = {      // Extracted skills
    all: [],
    technical: [],
    soft: [],
    tools: []
};

// Local storage
localStorage.setItem('authToken', token);
localStorage.setItem('userEmail', email);

// Token management
- Stored after login
- Sent with every API request
- Cleared on logout
- Checked before protected operations
```

### API Communication

```javascript
// Fetch API pattern
async function apiCall(endpoint, options) {
    const token = getAuthToken();
    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        {
            ...options,
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                ...options.headers
            }
        }
    );
    
    // Handle 401 - Auto logout
    if (response.status === 401) {
        logout();
    }
    
    return await response.json();
}
```

### Chart.js Integration

```javascript
// Score Doughnut Chart
new Chart(ctx, {
    type: 'doughnut',
    data: {
        datasets: [{
            data: [score, 100 - score],
            backgroundColor: [color, '#e5e7eb']
        }]
    },
    options: {
        cutout: '80%',  // Donut style
        responsive: true
    }
});

// Skills Bar Chart
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Technical', 'Soft', 'Tools'],
        datasets: [{
            data: [techCount, softCount, toolsCount],
            backgroundColor: [color1, color2, color3]
        }]
    }
});
```

### CSS Architecture

```css
/* CSS Variables for theming */
:root {
    --primary-color: #6366f1;
    --spacing-md: 1.5rem;
    /* Easy to customize */
}

/* Component-based structure */
.navbar { ... }
.hero { ... }
.dashboard { ... }
.dashboard-card { ... }

/* Responsive design */
@media (max-width: 768px) {
    /* Mobile styles */
}

/* Utility classes */
.btn-primary { ... }
.btn-secondary { ... }
.error-message { ... }
```

---

## 🆕 Adding New Features

### Example: Add Resume Export Feature

#### 1. Backend (Python)

```python
# In resume.py
@router.get("/export/{resume_id}/pdf")
async def export_resume_pdf(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(status_code=404)
    
    # Generate PDF using reportlab or similar
    pdf_content = generate_pdf(resume)
    
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=resume_{resume_id}.pdf"
        }
    )
```

#### 2. Frontend (JavaScript)

```javascript
// In dashboard.js
async function exportResume(resumeId) {
    try {
        const response = await fetch(
            `${API_BASE_URL}/api/resume/export/${resumeId}/pdf`,
            {
                headers: {
                    'Authorization': `Bearer ${getAuthToken()}`
                }
            }
        );
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'resume.pdf';
        a.click();
    } catch (error) {
        showError('Export failed');
    }
}
```

#### 3. UI Addition

```html
<!-- In dashboard.html -->
<button onclick="exportResume(currentResume.id)" class="btn-secondary">
    📥 Export Resume
</button>
```

---

## 🎨 Customization Guide

### Change Color Scheme

```css
/* In style.css */
:root {
    --primary-color: #your-color;      /* Main brand color */
    --primary-dark: #darker-shade;     /* Hover states */
    --primary-light: #lighter-shade;   /* Accents */
}
```

### Modify ATS Scoring Weights

```python
# In ats_scorer.py
weights = {
    "keyword_density": 0.40,   # Change these
    "formatting": 0.20,
    "action_verbs": 0.15,
    "experience": 0.15,
    "skill_match": 0.10
}
```

### Add New Skills

```python
# In skill_extractor.py
TECHNICAL_SKILLS = {
    # Add your skills here
    'nextjs', 'remix', 'astro',  # New frameworks
    'rust', 'zig',               # New languages
}
```

### Customize AI Prompt

```python
# In ai_feedback.py
prompt = f"""
Your custom prompt here.
Make it specific to your use case.
"""
```

---

## 🌟 Best Practices

### Backend

1. **Always use type hints**
```python
def process_resume(text: str, user_id: int) -> Dict[str, Any]:
    ...
```

2. **Use Pydantic for validation**
```python
class ResumeCreate(BaseModel):
    filename: str = Field(..., min_length=1)
```

3. **Handle errors gracefully**
```python
try:
    result = risky_operation()
except SpecificError as e:
    raise HTTPException(status_code=400, detail=str(e))
```

4. **Use database sessions properly**
```python
def endpoint(db: Session = Depends(get_db)):
    # Session automatically closed after request
```

### Frontend

1. **Always check authentication**
```javascript
if (!requireAuth()) return;
```

2. **Handle loading states**
```javascript
showLoading(true);
try {
    await operation();
} finally {
    showLoading(false);
}
```

3. **Validate input**
```javascript
if (!file || file.type !== 'application/pdf') {
    showError('Invalid file');
    return;
}
```

4. **Clean up resources**
```javascript
if (window.chartInstance) {
    window.chartInstance.destroy();
}
```

### Security

1. **Never expose secrets**
```python
# ✅ Good
SECRET_KEY = os.getenv("SECRET_KEY")

# ❌ Bad
SECRET_KEY = "hardcoded-secret"
```

2. **Validate all inputs**
```python
if not resume_id or resume_id < 1:
    raise HTTPException(status_code=400)
```

3. **Use parameterized queries**
```python
# SQLAlchemy ORM automatically protects
db.query(User).filter(User.id == user_id)
```

---

## 📊 Performance Optimization

### Backend
- Use async endpoints for I/O operations
- Cache frequently accessed data
- Optimize database queries
- Use connection pooling

### Frontend
- Minimize API calls
- Cache responses when appropriate
- Lazy load images and resources
- Debounce user inputs

---

## 🧪 Testing

### Backend Unit Tests
```python
def test_skill_extraction():
    text = "Python, JavaScript, React"
    skills = extract_skills(text)
    assert "Python" in skills["technical_skills"]
```

### API Integration Tests
```python
def test_resume_upload():
    response = client.post(
        "/api/resume/upload",
        files={"file": pdf_content},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

---

## 🚀 Deployment Tips

1. **Environment Configuration**
   - Use production secret key
   - Configure production database
   - Set appropriate CORS origins

2. **Database Migration**
   - Use Alembic for migrations
   - Backup before migrating

3. **Monitoring**
   - Add logging
   - Track API usage
   - Monitor errors

4. **Scaling**
   - Use production ASGI server (Gunicorn + Uvicorn)
   - Consider load balancing
   - Cache strategies

---

**Happy coding! 🎉**
