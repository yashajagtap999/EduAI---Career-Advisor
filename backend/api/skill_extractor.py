import re

# Optional NLP model
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

# Comprehensive Skills Database (Technical, Management, Tools)
SKILLS_DB = [
    # Programming Languages
    "python", "java", "c++", "c#", "ruby", "javascript", "typescript", "golang", "rust", "php", "swift", "kotlin", "sql", "r", "sas", "matlab",
    # Data Science & AI
    "data science", "machine learning", "deep learning", "natural language processing", "nlp", "computer vision", "statistics",
    "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "tensorflow", "keras", "pytorch", "transformers", "opencv", "big data",
    "hadoop", "spark", "hive", "kafka", "tableau", "power bi", "looker", "data visualization", "predictive modeling", "clustering",
    # Web Development
    "html", "css", "react", "angular", "vue", "next.js", "bootstrap", "tailwind", "node.js", "express", "django", "flask", "fastapi",
    "spring boot", "hibernate", "asp.net", "laravel", "wordpress", "rest api", "graphql", "websockets", "microservices",
    # Cloud & DevOps
    "aws", "amazon web services", "azure", "gcp", "google cloud platform", "docker", "kubernetes", "jenkins", "terraform", "ansible",
    "git", "github", "gitlab", "bitbucket", "ci/cd", "devops", "linux", "bash", "shell", "powershell", "nginx", "apache", "prometheus", "grafana",
    # Database
    "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "sqlite", "oracle", "snowflake", "cassandra", "firebase",
    # Software Engineering & Soft Skills
    "agile", "scrum", "kanban", "sdlc", "testing", "unit testing", "integration testing", "selenium", "jira", "confluence",
    "communication", "teamwork", "problem solving", "leadership", "project management", "time management", "analytical",
    # Other domains
    "blockchain", "crypto", "smart contracts", "solidity", "cybersecurity", "networking", "iot", "robotics", "embedded systems",
    "mobile development", "android", "ios", "flutter", "react native", "ui/ux", "figma", "adobe xd", "photoshop", "illustrator"
]

def extract_skills(text):
    text_lower = text.lower()
    found_skills = set()

    for skill in SKILLS_DB:
        # Use word boundaries to avoid matching substrings within words (e.g., 'cat' in 'category')
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return list(found_skills)