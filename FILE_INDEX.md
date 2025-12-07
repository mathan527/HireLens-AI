# 📑 HireLens AI - Complete File Index

Quick reference guide to all project files and their purposes.

---

## 📄 Documentation Files (Read These First!)

| File | Purpose | Priority |
|------|---------|----------|
| `README.md` | Complete project documentation | ⭐⭐⭐ Must Read |
| `QUICKSTART.md` | 5-minute setup guide | ⭐⭐⭐ Start Here |
| `PROJECT_SUMMARY.md` | High-level project overview | ⭐⭐ Overview |
| `DEVELOPER_GUIDE.md` | Deep dive for developers | ⭐⭐ For Devs |
| `API_TESTING.md` | API testing examples | ⭐ Testing |
| `FILE_INDEX.md` | This file | ⭐ Reference |

---

## ⚙️ Configuration Files

| File | Purpose | Edit Required |
|------|---------|---------------|
| `.env` | Environment variables | ✅ Yes - Add API keys |
| `.env.example` | Environment template | ❌ No - Reference only |
| `requirements.txt` | Python dependencies | ❌ No - Unless adding packages |
| `.gitignore` | Git ignore rules | ❌ No - Already configured |

---

## 🚀 Startup Scripts

| File | Purpose | When to Use |
|------|---------|-------------|
| `setup.ps1` | Automated project setup | ✅ Run first time |
| `start.ps1` | Start backend server | ✅ Every time |
| `start-frontend.ps1` | Start frontend server | ✅ Every time |

**Usage:**
```powershell
# First time only
.\setup.ps1

# Then every time you work:
# Terminal 1:
.\start.ps1

# Terminal 2:
.\start-frontend.ps1
```

---

## 🔧 Backend Files

### Main Application Files

| File | Lines | Purpose |
|------|-------|---------|
| `backend/main.py` | ~180 | FastAPI app entry point, routes, CORS |
| `backend/auth.py` | ~120 | JWT authentication logic |
| `backend/database.py` | ~40 | Database configuration, session management |
| `backend/models.py` | ~80 | SQLAlchemy database models |
| `backend/schema.py` | ~120 | Pydantic validation schemas |
| `backend/resume.py` | ~170 | Resume upload and analysis routes |
| `backend/jobs.py` | ~140 | Job matching routes |

### Utility Modules

| File | Lines | Purpose |
|------|-------|---------|
| `backend/utils/pdf_parser.py` | ~80 | PDF text extraction (dual method) |
| `backend/utils/skill_extractor.py` | ~180 | NLP skill extraction using spaCy |
| `backend/utils/ats_scorer.py` | ~160 | ATS score calculation algorithm |
| `backend/utils/matcher.py` | ~120 | Job matching with TF-IDF |
| `backend/utils/ai_feedback.py` | ~160 | AI feedback generation (OpenAI/Gemini) |

**Total Backend: ~1,550 lines**

---

## 🎨 Frontend Files

### HTML Pages

| File | Lines | Purpose |
|------|-------|---------|
| `frontend/index.html` | ~180 | Landing page with hero, features, CTA |
| `frontend/login.html` | ~90 | User login page |
| `frontend/register.html` | ~100 | User registration page |
| `frontend/dashboard.html` | ~220 | Main application dashboard |

**Total HTML: ~590 lines**

### CSS Styling

| File | Lines | Purpose |
|------|-------|---------|
| `frontend/css/style.css` | ~650 | Complete responsive styling |

**Features:**
- CSS variables for theming
- Responsive design (mobile-first)
- Component-based structure
- Smooth animations
- Modern color scheme

### JavaScript Files

| File | Lines | Purpose |
|------|-------|---------|
| `frontend/js/main.js` | ~90 | Utility functions, API calls, auth helpers |
| `frontend/js/auth.js` | ~100 | Login and registration logic |
| `frontend/js/dashboard.js` | ~360 | Dashboard functionality, charts, matching |

**Total JavaScript: ~550 lines**

---

## 📊 Total Project Statistics

```
Backend:         ~1,550 lines (Python)
Frontend HTML:   ~590 lines
Frontend CSS:    ~650 lines
Frontend JS:     ~550 lines
Documentation:   ~3,000 lines (Markdown)
─────────────────────────────────
Total:           ~6,340 lines of code
Total Files:     31 files
```

---

## 🗂️ Directory Structure

```
HireLens AI/
│
├── 📚 Documentation (6 files)
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── PROJECT_SUMMARY.md
│   ├── DEVELOPER_GUIDE.md
│   ├── API_TESTING.md
│   └── FILE_INDEX.md
│
├── ⚙️ Configuration (4 files)
│   ├── .env
│   ├── .env.example
│   ├── requirements.txt
│   └── .gitignore
│
├── 🚀 Scripts (3 files)
│   ├── setup.ps1
│   ├── start.ps1
│   └── start-frontend.ps1
│
├── 🔧 Backend/ (12 files)
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   ├── schema.py
│   ├── resume.py
│   ├── jobs.py
│   │
│   └── utils/
│       ├── pdf_parser.py
│       ├── skill_extractor.py
│       ├── ats_scorer.py
│       ├── matcher.py
│       └── ai_feedback.py
│
└── 🎨 Frontend/ (7 files)
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    │
    ├── css/
    │   └── style.css
    │
    └── js/
        ├── main.js
        ├── auth.js
        └── dashboard.js
```

---

## 🎯 Files by Feature

### Authentication Feature
- `backend/auth.py` - JWT logic
- `backend/main.py` - Login/register routes
- `frontend/login.html` - Login UI
- `frontend/register.html` - Register UI
- `frontend/js/auth.js` - Auth JavaScript

### Resume Analysis Feature
- `backend/resume.py` - Resume routes
- `backend/utils/pdf_parser.py` - PDF processing
- `backend/utils/skill_extractor.py` - NLP analysis
- `backend/utils/ats_scorer.py` - Score calculation
- `frontend/dashboard.html` - Upload UI
- `frontend/js/dashboard.js` - Upload logic

### Job Matching Feature
- `backend/jobs.py` - Matching routes
- `backend/utils/matcher.py` - Matching algorithm
- `backend/utils/ai_feedback.py` - AI integration
- `frontend/dashboard.html` - Matching UI
- `frontend/js/dashboard.js` - Matching logic

### Database Feature
- `backend/database.py` - DB setup
- `backend/models.py` - Table definitions
- `backend/schema.py` - Validation schemas

### UI/UX Feature
- `frontend/index.html` - Landing page
- `frontend/css/style.css` - All styling
- `frontend/js/main.js` - Utilities
- Chart.js (CDN) - Visualizations

---

## 🔍 Quick File Lookup

### Need to modify...

**Colors/Styling?**
→ `frontend/css/style.css` (lines 9-25 for color variables)

**API endpoints?**
→ `backend/main.py`, `backend/resume.py`, `backend/jobs.py`

**Database schema?**
→ `backend/models.py`

**Skill detection?**
→ `backend/utils/skill_extractor.py` (lines 16-60 for skill lists)

**ATS scoring logic?**
→ `backend/utils/ats_scorer.py` (lines 90-160 for weights)

**AI prompts?**
→ `backend/utils/ai_feedback.py` (lines 25-55 for prompt)

**Frontend logic?**
→ `frontend/js/dashboard.js` (main functionality)

**Authentication?**
→ `backend/auth.py` (backend), `frontend/js/auth.js` (frontend)

---

## 📝 File Modification Guide

### When to Edit Each File

**Never Edit:**
- `.env.example` (template only)
- `requirements.txt` (unless adding packages)
- Documentation files (unless contributing)

**Edit Once (Setup):**
- `.env` (add your API keys)

**Edit for Customization:**
- `frontend/css/style.css` (colors, styling)
- `backend/utils/skill_extractor.py` (add skills)
- `backend/utils/ats_scorer.py` (adjust weights)
- `backend/utils/ai_feedback.py` (modify prompts)

**Edit for Features:**
- `backend/main.py` (new routes)
- `backend/models.py` (new tables)
- `frontend/dashboard.html` (new UI)
- `frontend/js/dashboard.js` (new logic)

---

## 🔧 Maintenance Checklist

### Regular Updates
- [ ] Update dependencies: `pip install --upgrade -r requirements.txt`
- [ ] Check for security updates
- [ ] Review and rotate API keys
- [ ] Backup database
- [ ] Review logs for errors

### Before Deployment
- [ ] Change `SECRET_KEY` in `.env`
- [ ] Update `DATABASE_URL` for production
- [ ] Configure CORS for production domain
- [ ] Set up SSL/HTTPS
- [ ] Enable production logging

---

## 🆘 Troubleshooting by File

**Error: "Module not found"**
→ Check `requirements.txt`, run `pip install -r requirements.txt`

**Error: "Database locked"**
→ Check `backend/database.py`, consider PostgreSQL

**Error: "PDF parsing failed"**
→ Check `backend/utils/pdf_parser.py`, verify PDF format

**Error: "Skills not detected"**
→ Check `backend/utils/skill_extractor.py`, add missing skills

**Error: "CORS policy blocked"**
→ Check `backend/main.py`, update CORS origins

**Error: "Token expired"**
→ Check `backend/auth.py`, adjust `ACCESS_TOKEN_EXPIRE_MINUTES`

**UI not updating?**
→ Check browser console, verify `frontend/js/dashboard.js`

**Styling issues?**
→ Check `frontend/css/style.css`, clear cache

---

## 📖 Reading Order for New Developers

1. **QUICKSTART.md** - Get it running (15 min)
2. **README.md** - Understand the project (30 min)
3. **PROJECT_SUMMARY.md** - See the big picture (15 min)
4. **backend/main.py** - Entry point (10 min)
5. **frontend/dashboard.html** - Main UI (10 min)
6. **DEVELOPER_GUIDE.md** - Deep dive (45 min)
7. **Experiment!** - Make changes, break things, learn!

---

## 🎓 Learning Path

**Beginner:**
1. Run the application
2. Test all features
3. Read documentation
4. Modify CSS styling

**Intermediate:**
1. Add new skills to database
2. Adjust ATS scoring weights
3. Customize AI prompts
4. Add UI components

**Advanced:**
1. Add new API endpoints
2. Implement new algorithms
3. Integrate new services
4. Optimize performance

---

## 📞 Getting Help

**File-specific issues:**
- Check comments in the file
- Read DEVELOPER_GUIDE.md
- Check API documentation: `/docs`

**General issues:**
- Check QUICKSTART.md troubleshooting
- Review README.md
- Check server logs

**Contributing:**
- Follow code structure
- Add comments
- Update documentation
- Test thoroughly

---

**Last Updated:** December 2025
**Project Version:** 1.0.0
**Total Files:** 31
**Total Lines:** ~6,340

---

*This index helps you navigate the entire project efficiently! 🚀*
