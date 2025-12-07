# 🚀 Quick Start Guide - HireLens AI

## ⚡ Fastest Way to Get Started (5 minutes)

### Prerequisites
- Python 3.8 or higher
- Internet connection (for downloading dependencies)

---

## 🎯 Quick Setup (Automated)

### Step 1: Run Setup Script
Open PowerShell in the project directory and run:

```powershell
.\setup.ps1
```

This will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Download NLP models
- ✅ Create configuration file

### Step 2: Configure API Key (Optional but Recommended)

1. Open `.env` file
2. Add your API key:

**For Gemini (Free tier available):**
```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your-key-here
```
Get key: https://makersuite.google.com/app/apikey

**For OpenAI:**
```env
AI_PROVIDER=openai
OPENAI_API_KEY=your-key-here
```
Get key: https://platform.openai.com/api-keys

> **Note:** Without API key, system will provide default feedback

### Step 3: Start Backend

```powershell
.\start.ps1
```

### Step 4: Start Frontend (New Terminal)

```powershell
.\start-frontend.ps1
```

### Step 5: Open Application

Open browser: **http://localhost:3000**

---

## 📖 Manual Setup (If Scripts Don't Work)

### 1. Create Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Configure Environment
```powershell
Copy-Item .env.example .env
# Edit .env with your API keys
```

### 4. Start Backend
```powershell
cd backend
python main.py
```

### 5. Start Frontend (New Terminal)
```powershell
cd frontend
python -m http.server 3000
```

---

## 🎮 Using the Application

### 1️⃣ Register Account
1. Click "Get Started"
2. Enter email and password
3. Click "Create Account"

### 2️⃣ Login
1. Use your credentials
2. You'll be redirected to dashboard

### 3️⃣ Upload Resume
1. Click "Choose PDF File"
2. Select your resume
3. Click "Upload & Analyze"
4. Wait 10-30 seconds

### 4️⃣ View Results
- **ATS Score**: Overall score out of 100
- **Skills**: Extracted skills by category
- **Charts**: Visual data representation

### 5️⃣ Match with Job
1. Paste job description
2. Click "Calculate Match"
3. View match percentage and missing skills
4. Get AI-powered feedback

---

## 🔧 Troubleshooting

### Backend won't start?
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Try running directly
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend shows CORS errors?
- Make sure backend is running
- Frontend should be on `http://localhost:3000`

### "Module not found" errors?
```powershell
pip install -r requirements.txt --force-reinstall
```

### spaCy model error?
```powershell
python -m spacy download en_core_web_sm
```

---

## 📍 Important URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 💡 Tips

### Best Resume Practices:
- Use PDF format only
- Include clear sections (Experience, Skills, Education)
- Use action verbs (Developed, Implemented, Led)
- Add quantifiable achievements
- Keep it 1-2 pages

### For Better ATS Scores:
- Include relevant keywords
- Use standard section headings
- Add contact information
- List technical skills
- Include dates and metrics

---

## 🆘 Need Help?

1. Check `README.md` for detailed documentation
2. Visit API docs: http://localhost:8000/docs
3. Check logs in terminal for errors

---

## 📊 What to Expect

### Performance:
- Resume upload: 2-5 seconds
- ATS scoring: < 1 second
- Job matching: 1-3 seconds
- AI feedback: 3-10 seconds

### ATS Score Guide:
- **80-100**: Excellent ✅
- **70-79**: Good 👍
- **60-69**: Fair ⚠️
- **Below 60**: Needs work ❌

---

## 🎉 You're All Set!

Start optimizing your resume and landing your dream job! 🚀

For detailed documentation, see `README.md`
