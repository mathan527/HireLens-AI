from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple
import numpy as np
from utils.skill_extractor import extract_skills

def calculate_match_score(resume_text: str, job_description: str) -> Dict:
    """
    Calculate job match score using cosine similarity and skill matching
    
    Args:
        resume_text: Resume content
        job_description: Job description content
        
    Returns:
        Dictionary with match percentage, matched skills, and missing skills
    """
    
    # Extract skills from both texts
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    
    # Convert skill lists to sets for comparison
    resume_all_skills = set([s.lower() for s in resume_skills["all_skills"]])
    job_all_skills = set([s.lower() for s in job_skills["all_skills"]])
    
    resume_technical = set([s.lower() for s in resume_skills["technical_skills"]])
    job_technical = set([s.lower() for s in job_skills["technical_skills"]])
    
    # Calculate skill-based match
    matched_skills = resume_all_skills & job_all_skills
    missing_skills = job_all_skills - resume_all_skills
    
    matched_technical = resume_technical & job_technical
    missing_technical = job_technical - resume_technical
    
    # Skill match percentage (weighted more for technical skills)
    if job_all_skills:
        skill_match_rate = len(matched_skills) / len(job_all_skills)
    else:
        skill_match_rate = 0.5  # Default if no skills in job description
    
    if job_technical:
        technical_match_rate = len(matched_technical) / len(job_technical)
    else:
        technical_match_rate = 0.5
    
    # Calculate cosine similarity using TF-IDF
    # Use try-except to handle edge cases
    cosine_sim = 0.5  # Default fallback
    try:
        # Ensure texts are not empty
        if len(resume_text.strip()) > 10 and len(job_description.strip()) > 10:
            vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=500,
                min_df=1,
                max_df=0.95
            )
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except Exception as e:
        print(f"TF-IDF calculation warning: {e}")
        # Continue with default cosine_sim value
    
    # Calculate weighted match score
    # 40% skill match, 30% technical match, 30% cosine similarity
    final_match = (
        skill_match_rate * 0.40 +
        technical_match_rate * 0.30 +
        cosine_sim * 0.30
    ) * 100
    
    # Prepare results
    result = {
        "match_percentage": round(final_match, 2),
        "matched_skills": sorted(list(matched_skills)),
        "missing_skills": sorted(list(missing_skills)),
        "matched_technical_skills": sorted(list(matched_technical)),
        "missing_technical_skills": sorted(list(missing_technical)),
        "cosine_similarity": round(cosine_sim * 100, 2)
    }
    
    return result

def rank_resumes(resumes: List[str], job_description: str) -> List[Tuple[int, float]]:
    """
    Rank multiple resumes against a job description
    
    Args:
        resumes: List of resume texts
        job_description: Job description text
        
    Returns:
        List of tuples (resume_index, match_score) sorted by score descending
    """
    scores = []
    
    for idx, resume in enumerate(resumes):
        match_result = calculate_match_score(resume, job_description)
        scores.append((idx, match_result["match_percentage"]))
    
    # Sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)
    
    return scores

def get_match_interpretation(score: float) -> str:
    """Get interpretation of match score"""
    if score >= 80:
        return "Excellent Match - You're a strong candidate for this position"
    elif score >= 70:
        return "Good Match - Your profile aligns well with the job requirements"
    elif score >= 60:
        return "Fair Match - You meet some of the job requirements"
    elif score >= 50:
        return "Moderate Match - Consider developing additional skills"
    else:
        return "Low Match - Significant skill gap exists for this position"
