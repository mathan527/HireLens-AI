import spacy
import re
from typing import Dict, List, Set
from collections import Counter
from functools import lru_cache

# Load spaCy model (download with: python -m spacy download en_core_web_sm)
# Use singleton pattern to load model once
_nlp_model = None

def get_nlp_model():
    """Get or load spaCy model (singleton pattern)"""
    global _nlp_model
    if _nlp_model is None:
        try:
            _nlp_model = spacy.load("en_core_web_sm")
        except OSError:
            print("⚠️  Downloading spaCy model...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            _nlp_model = spacy.load("en_core_web_sm")
    return _nlp_model

# Comprehensive skill databases
TECHNICAL_SKILLS = {
    # Programming Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
    'go', 'rust', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash', 'powershell', 'sql',
    
    # Web Technologies
    'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express', 'django', 'flask', 'fastapi',
    'spring', 'asp.net', 'laravel', 'rails', 'jquery', 'bootstrap', 'tailwind', 'sass', 'webpack',
    
    # Databases
    'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server', 'sqlite', 'cassandra',
    'dynamodb', 'elasticsearch', 'firebase', 'mariadb', 'neo4j',
    
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github', 'ci/cd',
    'terraform', 'ansible', 'chef', 'puppet', 'circleci', 'travis ci',
    
    # AI/ML
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'opencv', 'nlp',
    'machine learning', 'deep learning', 'neural networks', 'computer vision', 'data science',
    
    # Tools & Platforms
    'git', 'linux', 'unix', 'windows', 'macos', 'jira', 'confluence', 'slack', 'notion',
    'figma', 'adobe', 'photoshop', 'illustrator', 'sketch', 'invision',
    
    # Methodologies
    'agile', 'scrum', 'kanban', 'devops', 'microservices', 'rest api', 'graphql', 'soap',
    'tdd', 'bdd', 'oauth', 'jwt', 'websocket', 'grpc'
}

SOFT_SKILLS = {
    'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
    'time management', 'adaptability', 'creativity', 'collaboration', 'analytical',
    'decision making', 'interpersonal', 'presentation', 'negotiation', 'conflict resolution',
    'emotional intelligence', 'mentoring', 'coaching', 'strategic thinking', 'innovation',
    'customer service', 'attention to detail', 'multitasking', 'organization', 'self-motivated'
}

TOOLS = {
    'vscode', 'visual studio', 'intellij', 'pycharm', 'eclipse', 'sublime', 'atom',
    'postman', 'insomnia', 'swagger', 'tableau', 'power bi', 'excel', 'word', 'powerpoint',
    'trello', 'asana', 'monday', 'salesforce', 'hubspot', 'google analytics', 'mixpanel',
    'amplitude', 'segment', 'datadog', 'new relic', 'splunk', 'grafana', 'prometheus'
}

def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extract technical skills, soft skills, and tools from resume text
    
    Args:
        text: Resume text
        
    Returns:
        Dictionary with categorized skills
    """
    # Validate input
    if not text or not isinstance(text, str):
        return {
            "all_skills": [],
            "technical_skills": [],
            "soft_skills": [],
            "tools": []
        }
    
    text_lower = text.lower()
    
    # Extract technical skills
    technical_found = set()
    for skill in TECHNICAL_SKILLS:
        # Use word boundaries for better matching
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            technical_found.add(skill.title())
    
    # Extract soft skills
    soft_found = set()
    for skill in SOFT_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            soft_found.add(skill.title())
    
    # Extract tools
    tools_found = set()
    for tool in TOOLS:
        pattern = r'\b' + re.escape(tool) + r'\b'
        if re.search(pattern, text_lower):
            tools_found.add(tool.title())
    
    # Use spaCy for additional entity extraction (with length limit)
    nlp = get_nlp_model()
    doc = nlp(text[:100000])  # Limit text length for spaCy
    
    # Extract noun chunks as potential skills
    noun_chunks = [chunk.text.lower() for chunk in doc.noun_chunks]
    
    # Add common programming patterns
    programming_patterns = [
        r'\b(object[- ]oriented programming|oop)\b',
        r'\b(functional programming)\b',
        r'\b(data structures?)\b',
        r'\b(algorithms?)\b',
        r'\b(design patterns?)\b',
        r'\b(api development)\b',
        r'\b(database design)\b',
        r'\b(ui/ux)\b',
        r'\b(front[- ]end|frontend)\b',
        r'\b(back[- ]end|backend)\b',
        r'\b(full[- ]stack|fullstack)\b',
    ]
    
    for pattern in programming_patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            technical_found.add(match.title())
    
    # Combine all skills
    all_skills = list(technical_found | soft_found | tools_found)
    
    return {
        "all_skills": sorted(all_skills),
        "technical_skills": sorted(list(technical_found)),
        "soft_skills": sorted(list(soft_found)),
        "tools": sorted(list(tools_found))
    }

def extract_keywords(text: str) -> List[str]:
    """Extract important keywords using spaCy NLP"""
    if not text or not isinstance(text, str) or len(text.strip()) < 10:
        return []
    
    nlp = get_nlp_model()
    doc = nlp(text[:100000])
    
    # Extract nouns and proper nouns
    keywords = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and len(token.text) > 2:
            keywords.append(token.text.lower())
    
    # Get most common keywords
    keyword_freq = Counter(keywords)
    top_keywords = [word for word, freq in keyword_freq.most_common(50)]
    
    return top_keywords

def count_action_verbs(text: str) -> int:
    """Count action verbs commonly used in strong resumes"""
    action_verbs = {
        'achieved', 'improved', 'developed', 'created', 'designed', 'implemented', 'managed',
        'led', 'coordinated', 'executed', 'launched', 'established', 'initiated', 'built',
        'streamlined', 'optimized', 'increased', 'reduced', 'enhanced', 'transformed',
        'delivered', 'spearheaded', 'pioneered', 'orchestrated', 'facilitated', 'generated',
        'resolved', 'accelerated', 'maximized', 'strengthened', 'collaborated', 'conducted',
        'analyzed', 'evaluated', 'strategized', 'formulated', 'demonstrated', 'exceeded'
    }
    
    text_lower = text.lower()
    count = 0
    for verb in action_verbs:
        count += len(re.findall(r'\b' + verb + r'\b', text_lower))
    
    return count
