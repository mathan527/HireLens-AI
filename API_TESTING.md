# API Testing Guide - HireLens AI

This guide helps you test the API endpoints using PowerShell, curl, or any API client.

## Base URL
```
http://localhost:8000
```

---

## 1. AUTHENTICATION

### Register New User
```powershell
$body = @{
    email = "test@example.com"
    password = "test123456"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/register" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Login
```powershell
$body = @{
    email = "test@example.com"
    password = "test123456"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/login" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

# Store token for subsequent requests
$token = $response.access_token
```

### Get Current User
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/me" `
    -Method Get `
    -Headers $headers
```

---

## 2. RESUME UPLOAD

### Upload Resume (PDF)
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

# Prepare file
$filePath = "C:\path\to\your\resume.pdf"
$boundary = [System.Guid]::NewGuid().ToString()
$fileName = [System.IO.Path]::GetFileName($filePath)

# Create multipart form data
$bodyLines = @(
    "--$boundary",
    "Content-Disposition: form-data; name=`"file`"; filename=`"$fileName`"",
    "Content-Type: application/pdf",
    "",
    [System.IO.File]::ReadAllBytes($filePath),
    "--$boundary--"
)

Invoke-RestMethod -Uri "http://localhost:8000/api/resume/upload" `
    -Method Post `
    -Headers $headers `
    -ContentType "multipart/form-data; boundary=$boundary" `
    -Body $bodyLines
```

### List User Resumes
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/resume/list" `
    -Method Get `
    -Headers $headers
```

### Get Specific Resume
```powershell
$resumeId = 1
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/resume/$resumeId" `
    -Method Get `
    -Headers $headers
```

### Delete Resume
```powershell
$resumeId = 1
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/resume/$resumeId" `
    -Method Delete `
    -Headers $headers
```

---

## 3. JOB MATCHING

### Match Resume with Job
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

$body = @{
    resume_id = 1
    job_title = "Senior Software Engineer"
    job_description = @"
We are seeking a Senior Software Engineer with 5+ years of experience.
Required skills: Python, FastAPI, React, PostgreSQL, Docker, AWS.
Experience with AI/ML is a plus.
"@
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/jobs/match" `
    -Method Post `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $body
```

### Create Job Posting
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

$body = @{
    title = "Full Stack Developer"
    description = "Looking for a full stack developer with React and Node.js experience"
    required_skills = @("React", "Node.js", "MongoDB", "JavaScript")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/jobs/create" `
    -Method Post `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $body
```

### List All Jobs
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/jobs/list" `
    -Method Get `
    -Headers $headers
```

---

## 4. DASHBOARD

### Get Dashboard Data
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/dashboard" `
    -Method Get `
    -Headers $headers
```

---

## 5. HEALTH CHECK

### Check API Health
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```

---

## CURL Examples (Cross-platform)

### Register
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456"}'
```

### Upload Resume
```bash
curl -X POST http://localhost:8000/api/resume/upload \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@/path/to/resume.pdf"
```

### Match Job
```bash
curl -X POST http://localhost:8000/api/jobs/match \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_title": "Software Engineer",
    "job_description": "Looking for Python developer with FastAPI experience"
  }'
```

---

## Testing with Postman

1. Import this collection into Postman
2. Set up environment variable:
   - `base_url`: http://localhost:8000
   - `token`: (will be set after login)

3. Collection structure:
   ```
   HireLens AI
   ├── Auth
   │   ├── Register
   │   ├── Login
   │   └── Get Current User
   ├── Resume
   │   ├── Upload Resume
   │   ├── List Resumes
   │   ├── Get Resume
   │   └── Delete Resume
   ├── Jobs
   │   ├── Create Job
   │   ├── List Jobs
   │   └── Match Job
   └── Dashboard
       └── Get Dashboard Data
   ```

---

## Expected Response Codes

- `200 OK`: Successful GET/DELETE
- `201 Created`: Successful POST (creation)
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing/invalid token
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## Response Examples

### Successful Login
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Resume Analysis
```json
{
  "id": 1,
  "filename": "resume.pdf",
  "raw_text": "John Doe\nSoftware Engineer...",
  "extracted_skills": ["Python", "FastAPI", "React"],
  "technical_skills": ["Python", "FastAPI"],
  "soft_skills": ["Leadership", "Communication"],
  "tools": ["Git", "Docker"],
  "ats_score": 85.5,
  "created_at": "2025-12-07T10:30:00"
}
```

### Job Match
```json
{
  "match_percentage": 78.5,
  "missing_skills": ["AWS", "Kubernetes"],
  "matched_skills": ["Python", "FastAPI", "Docker"],
  "ai_feedback": "Your resume is a good match..."
}
```

---

## Interactive API Documentation

Visit these URLs when server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API testing interfaces.

---

## Troubleshooting

### 401 Unauthorized
- Token expired (tokens last 30 minutes)
- Re-login to get new token

### 400 Bad Request
- Check request body format
- Ensure all required fields are present

### 500 Internal Server Error
- Check server logs
- Verify database connection
- Ensure all dependencies are installed

---

## Complete Test Flow

1. Register user
2. Login and save token
3. Upload resume
4. View resume analysis
5. Match with job description
6. View AI feedback
7. Check dashboard

This tests all major features!
