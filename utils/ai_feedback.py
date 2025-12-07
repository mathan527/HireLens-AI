import os
import json
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

# Determine which AI provider to use
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()

def get_ai_feedback(resume_text: str, extracted_skills: List[str], 
                   job_description: str = "", missing_skills: List[str] = None) -> Dict:
    """
    Get AI-powered resume feedback using OpenAI or Gemini
    
    Args:
        resume_text: Resume content
        extracted_skills: List of extracted skills
        job_description: Target job description
        missing_skills: List of missing skills
        
    Returns:
        Dictionary with AI feedback
    """
    
    if missing_skills is None:
        missing_skills = []
    
    # Construct the prompt
    prompt = f"""You are a professional ATS resume evaluator and recruiter with 10+ years of experience.

Analyze this resume text:
{resume_text[:3000]}

Extracted Skills:
{', '.join(extracted_skills[:30])}

Target Job Description:
{job_description[:2000] if job_description else "General professional resume evaluation"}

Missing Skills:
{', '.join(missing_skills[:20]) if missing_skills else "None identified"}

Provide a detailed analysis in JSON format with the following structure:
{{
    "ats_score": <number 0-100>,
    "missing_skills": [<list of critical missing skills>],
    "improvements": [
        "5 specific improvements to increase ATS ranking"
    ],
    "rewritten_bullets": [
        "3 rewritten bullet points using strong action verbs and quantifiable metrics"
    ],
    "recruiter_summary": "A 2-3 sentence summary of the candidate's profile and fit for the role"
}}

Focus on:
1. ATS optimization techniques
2. Quantifiable achievements
3. Action verb usage
4. Keyword optimization
5. Skill gaps

Return ONLY valid JSON, no additional text."""

    try:
        if AI_PROVIDER == "openai":
            return get_openai_feedback(prompt)
        elif AI_PROVIDER == "gemini":
            return get_gemini_feedback(prompt)
        else:
            return get_default_feedback(extracted_skills, missing_skills)
    except Exception as e:
        print(f"AI Feedback Error: {e}")
        return get_default_feedback(extracted_skills, missing_skills)

def get_openai_feedback(prompt: str) -> Dict:
    """Get feedback using OpenAI API"""
    try:
        import openai
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found")
        
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert ATS resume evaluator. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        feedback_text = response.choices[0].message.content.strip()
        
        # Extract JSON from response
        feedback_json = extract_json(feedback_text)
        return feedback_json
        
    except Exception as e:
        print(f"OpenAI Error: {e}")
        raise

def get_gemini_feedback(prompt: str) -> Dict:
    """Get feedback using Google Gemini API"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key not found")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(prompt)
        feedback_text = response.text.strip()
        
        # Extract JSON from response
        feedback_json = extract_json(feedback_text)
        return feedback_json
        
    except Exception as e:
        print(f"Gemini Error: {e}")
        raise

def extract_json(text: str) -> Dict:
    """Extract JSON from AI response text"""
    # Try to find JSON in markdown code blocks
    import re
    
    # Look for JSON in code blocks
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        text = json_match.group(1)
    else:
        # Look for JSON without code blocks
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            text = json_match.group(0)
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # If parsing fails, return default structure
        raise ValueError("Could not parse AI response as JSON")

def get_default_feedback(extracted_skills: List[str], missing_skills: List[str]) -> Dict:
    """Provide default feedback when AI is unavailable"""
    return {
        "ats_score": 70,
        "missing_skills": missing_skills[:10] if missing_skills else [],
        "improvements": [
            "Add quantifiable achievements with specific metrics (e.g., 'Increased sales by 25%')",
            "Use strong action verbs at the start of each bullet point (e.g., 'Developed', 'Led', 'Implemented')",
            "Include relevant technical skills and tools mentioned in the job description",
            "Optimize your resume format for ATS by using standard section headings",
            "Add a professional summary highlighting your key qualifications and career objectives"
        ],
        "rewritten_bullets": [
            "Developed and implemented scalable web applications using React and Node.js, resulting in 40% faster page load times",
            "Led a cross-functional team of 5 developers to deliver a mission-critical project 2 weeks ahead of schedule",
            "Optimized database queries and reduced server response time by 35%, improving overall system performance"
        ],
        "recruiter_summary": f"Candidate demonstrates strong technical skills including {', '.join(extracted_skills[:5])}. To improve chances, focus on quantifying achievements and addressing skill gaps in {', '.join(missing_skills[:3]) if missing_skills else 'emerging technologies'}. Overall profile shows good potential with room for optimization."
    }
