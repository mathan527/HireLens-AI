import re
from typing import Dict
from utils.skill_extractor import extract_skills, extract_keywords, count_action_verbs

def calculate_ats_score(resume_text: str, job_description: str = "") -> Dict[str, float]:
    """
    Calculate ATS score based on multiple factors
    
    Score Breakdown:
    - Keyword density (40%)
    - Resume formatting (20%)
    - Action verbs usage (15%)
    - Experience relevance (15%)
    - Skill match with job (10%)
    
    Args:
        resume_text: Extracted resume text
        job_description: Optional job description for better scoring
        
    Returns:
        Dictionary with overall score and component scores
    """
    
    # Extract skills and keywords
    skills_data = extract_skills(resume_text)
    all_skills = skills_data["all_skills"]
    technical_skills = skills_data["technical_skills"]
    
    # Initialize scores
    scores = {
        "keyword_density": 0.0,
        "formatting": 0.0,
        "action_verbs": 0.0,
        "experience": 0.0,
        "skill_match": 0.0
    }
    
    # ====================================
    # 1. KEYWORD DENSITY (40%)
    # ====================================
    # Check for important sections and keywords
    text_lower = resume_text.lower()
    
    important_sections = [
        'experience', 'education', 'skills', 'projects', 'certifications',
        'summary', 'objective', 'achievements', 'work history'
    ]
    sections_found = sum(1 for section in important_sections if section in text_lower)
    section_score = min(sections_found / 6 * 100, 100)  # Max 100%
    
    # Check keyword density (number of relevant keywords)
    keywords = extract_keywords(resume_text)
    keyword_score = min(len(keywords) / 30 * 100, 100)  # Target: 30+ keywords
    
    # Technical skills presence
    tech_skill_score = min(len(technical_skills) / 10 * 100, 100)  # Target: 10+ skills
    
    scores["keyword_density"] = (section_score + keyword_score + tech_skill_score) / 3
    
    # ====================================
    # 2. RESUME FORMATTING (20%)
    # ====================================
    formatting_score = 0
    
    # Check for email
    if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
        formatting_score += 20
    
    # Check for phone number
    if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', resume_text):
        formatting_score += 20
    
    # Check for dates (experience timeline)
    date_patterns = [
        r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b',
        r'\b\d{4}\s*[-–]\s*\d{4}\b',
        r'\b\d{4}\s*[-–]\s*present\b'
    ]
    dates_found = any(re.search(pattern, text_lower) for pattern in date_patterns)
    if dates_found:
        formatting_score += 20
    
    # Check for bullet points or structured content
    bullet_indicators = ['•', '●', '▪', '■', '-', '*']
    has_bullets = any(indicator in resume_text for indicator in bullet_indicators)
    if has_bullets:
        formatting_score += 20
    
    # Check for reasonable length (400-2000 words)
    word_count = len(resume_text.split())
    if 400 <= word_count <= 2000:
        formatting_score += 20
    elif word_count > 300:
        formatting_score += 10
    
    scores["formatting"] = formatting_score
    
    # ====================================
    # 3. ACTION VERBS USAGE (15%)
    # ====================================
    action_verb_count = count_action_verbs(resume_text)
    # Target: 15+ action verbs for strong resume
    scores["action_verbs"] = min(action_verb_count / 15 * 100, 100)
    
    # ====================================
    # 4. EXPERIENCE RELEVANCE (15%)
    # ====================================
    experience_score = 0
    
    # Check for quantifiable achievements (numbers in text)
    numbers = re.findall(r'\b\d+[%$kKmM]?\b', resume_text)
    if len(numbers) >= 5:
        experience_score += 50
    elif len(numbers) >= 2:
        experience_score += 25
    
    # Check for experience indicators
    experience_keywords = ['developed', 'managed', 'led', 'implemented', 'designed', 
                          'created', 'improved', 'increased', 'reduced', 'achieved']
    exp_count = sum(1 for keyword in experience_keywords if keyword in text_lower)
    experience_score += min(exp_count / 5 * 50, 50)
    
    scores["experience"] = experience_score
    
    # ====================================
    # 5. SKILL MATCH WITH JOB (10%)
    # ====================================
    if job_description:
        job_skills = extract_skills(job_description)
        job_all_skills = set([s.lower() for s in job_skills["all_skills"]])
        resume_all_skills = set([s.lower() for s in all_skills])
        
        if job_all_skills:
            matched_skills = resume_all_skills & job_all_skills
            match_ratio = len(matched_skills) / len(job_all_skills)
            scores["skill_match"] = match_ratio * 100
        else:
            scores["skill_match"] = 50  # Default if no job description
    else:
        # Default score if no job description provided
        scores["skill_match"] = 50
    
    # ====================================
    # CALCULATE FINAL WEIGHTED SCORE
    # ====================================
    weights = {
        "keyword_density": 0.40,
        "formatting": 0.20,
        "action_verbs": 0.15,
        "experience": 0.15,
        "skill_match": 0.10
    }
    
    final_score = sum(scores[key] * weights[key] for key in scores)
    
    return {
        "overall_score": round(final_score, 2),
        "keyword_density": round(scores["keyword_density"], 2),
        "formatting": round(scores["formatting"], 2),
        "action_verbs": round(scores["action_verbs"], 2),
        "experience": round(scores["experience"], 2),
        "skill_match": round(scores["skill_match"], 2)
    }

def get_score_interpretation(score: float) -> str:
    """Get interpretation of ATS score"""
    if score >= 80:
        return "Excellent - Your resume is highly optimized for ATS systems"
    elif score >= 70:
        return "Good - Your resume should pass most ATS systems"
    elif score >= 60:
        return "Fair - Your resume needs some improvements"
    elif score >= 50:
        return "Poor - Your resume may not pass ATS screening"
    else:
        return "Critical - Your resume needs significant improvements"
