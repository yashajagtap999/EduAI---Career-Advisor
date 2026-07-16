# Job role → required skills mapping (Supporting Full Kaggle Job Market)
JOB_SKILLS = {
    # Tech / Developer Roles
    "Data Science": ["python", "machine learning", "ml", "statistics", "pandas", "numpy", "sql", "scikit-learn", "data visualization", "r"],
    "Java Developer": ["java", "spring boot", "hibernate", "rest api", "maven", "microservices", "sql", "junit"],
    "Python Developer": ["python", "django", "flask", "fastapi", "rest api", "git", "linux", "sql", "docker"],
    "Web Designing": ["html", "css", "javascript", "react", "photoshop", "figma", "ui/ux", "frontend", "tailwind", "bootstrap"],
    "DotNet Developer": ["c#", ".net", "asp.net", "sql server", "mvc", "entity framework", "web api"],
    "SAP Developer": ["sap", "abap", "erp", "hana", "business objects", "fiori", "basis"],
    "Blockchain": ["solidity", "smart contracts", "ethereum", "cryptography", "web3", "hyperledger", "rust", "ipfs"],
    
    # Data & Architecture
    "Database": ["sql", "mysql", "postgresql", "oracle", "nosql", "pl/sql", "mongodb", "database design", "indexing"],
    "Hadoop": ["hadoop", "spark", "big data", "hive", "scala", "kafka", "pyspark", "mapreduce", "zookeeper"],
    "ETL Developer": ["etl", "informatica", "data warehousing", "sql", "talend", "data pipeline", "airflow", "ssis"],
    
    # QA & Infrastructure
    "DevOps Engineer": ["aws", "docker", "kubernetes", "jenkins", "linux", "ci/cd", "terraform", "ansible", "cloud", "monitoring"],
    "Network Security Engineer": ["cybersecurity", "firewalls", "cisco", "linux", "cloud security", "penetration testing", "siem", "vpn"],
    "Automation Testing": ["selenium", "testing", "qa", "java", "cucumber", "testng", "api testing", "automation"],
    "Testing": ["manual testing", "qa", "test cases", "jira", "agile", "sdlc", "bug tracking", "black box testing"],
    
    # Engineering & Traditional
    "Mechanical Engineer": ["cad", "autocad", "solidworks", "manufacturing", "thermodynamics", "mechanical design", "ansys", "materials"],
    "Civil Engineer": ["autocad", "structural design", "construction", "project management", "surveying", "revit", "staad pro"],
    "Electrical Engineering": ["circuit design", "matlab", "plc", "autocad", "control systems", "embedded systems", "vlsi", "fpga"],
    
    # Business & Operations
    "HR": ["recruitment", "onboarding", "employee relations", "payroll", "performance management", "talent acquisition", "training", "hrms"],
    "Sales": ["b2b", "lead generation", "crm", "negotiation", "salesforce", "communication", "marketing", "business development"],
    "Operations Manager": ["supply chain", "process improvement", "budgeting", "project management", "logistics", "lean", "six sigma", "operations"],
    "Business Analyst": ["agile", "sql", "jira", "stakeholder management", "visio", "requirements gathering", "uml", "documentation", "tableau"],
    "PMO": ["project management", "pmp", "agile", "risk management", "scrum", "budgeting", "governance", "ms project", "planning"],
    
    # Misc Fields
    "Advocate": ["litigation", "legal research", "drafting", "corporate law", "compliance", "arbitration", "contract law", "intellectual property"],
    "Arts": ["illustration", "graphic design", "painting", "creativity", "adobe photoshop", "indesign", "sketching", "digital art"],
    "Health and fitness": ["nutrition", "personal training", "wellness", "anatomy", "cpr", "fitness coaching", "physiology", "yoga"],
    "General / Entry-Level": ["microsoft office", "communication", "teamwork", "problem solving", "time management", "learning agility"]
}


def _is_match(required, user_skill):
    """Helper for fuzzy/substring matching to handle plurals and minor variations."""
    r = required.lower()
    u = user_skill.lower()
    # Direct match or substring
    if r in u or u in r:
        return True
    # Handle simple pluralization (s/es)
    if r.endswith('s') and r[:-1] in u: return True
    if u.endswith('s') and u[:-1] in r: return True
    return False


# 🔥 Skill Gap
def get_skill_gap(user_skills, job_role):
    required_skills = JOB_SKILLS.get(job_role, [])
    user_skills_lower = [s.lower() for s in user_skills]

    missing = []
    for req in required_skills:
        if not any(_is_match(req, us) for us in user_skills_lower):
            missing.append(req)
    return missing


# 🔥 ATS Score
def calculate_ats_score(text, user_skills, job_role):
    """
    Calculates a highly accurate ATS score based on multiple parameters:
    1. Skill Keyword Match (60% weight)
    2. Section Completeness (20% weight) - checks for Education, Experience, Skills
    3. Contact Info & Links (10% weight) - checks for Email, Phone, LinkedIn, GitHub
    4. Formatting & Professional Quality (10% weight) - checks for Action Verbs and Word Count
    """
    import re
    required_skills = JOB_SKILLS.get(job_role, [])
    text_lower = text.lower()
    
    # ── 1. SKILL MATCH (60%) ──
    skill_score = 0
    if required_skills:
        user_skills_lower = [s.lower() for s in user_skills]
        matched = 0
        for req in required_skills:
            if any(_is_match(req, us) for us in user_skills_lower):
                matched += 1
        skill_score = (matched / len(required_skills)) * 60
    else:
        skill_score = 30 # Default baseline if no required skills are mapped
        
    # ── 2. SECTION COMPLETENESS (20%) ──
    # Checks for presence of main resume sections
    section_score = 0
    sections = {
        "education": ["education", "academic", "degree", "university", "college", "school"],
        "experience": ["experience", "employment", "work history", "professional history", "job history", "internship", "projects"],
        "skills": ["skills", "technical skills", "expertise", "competencies", "technologies"]
    }
    
    for section, keywords in sections.items():
        if any(kw in text_lower for kw in keywords):
            section_score += 6.67 # approx 20 / 3
            
    # ── 3. CONTACT INFO & LINKS (10%) ──
    contact_score = 0
    if "@" in text_lower or "email" in text_lower:
        contact_score += 2.5
    if "phone" in text_lower or "contact" in text_lower or re.search(r'\+?\d[\d -]{8,12}\d', text_lower):
        contact_score += 2.5
    if "linkedin.com" in text_lower or "linkedin" in text_lower:
        contact_score += 2.5
    if "github.com" in text_lower or "github" in text_lower or "portfolio" in text_lower or "website" in text_lower:
        contact_score += 2.5
        
    # ── 4. FORMATTING & PROFESSIONAL QUALITY (10%) ──
    quality_score = 0
    action_verbs = ["managed", "designed", "developed", "implemented", "achieved", "led", "created", "built", "optimized", "increased", "conducted", "spearheaded", "formulated", "leveraged"]
    verbs_found = sum(1 for verb in action_verbs if verb in text_lower)
    if verbs_found >= 5:
        quality_score += 5
    elif verbs_found >= 2:
        quality_score += 2.5
        
    word_count = len(text.split())
    if 200 <= word_count <= 1000:
        quality_score += 5
    elif 100 <= word_count <= 1500:
        quality_score += 2.5

    total_score = skill_score + section_score + contact_score + quality_score
    return round(min(max(total_score, 10.0), 100.0), 2)


def analyze_resume(text, job_role):
    """
    Main entry point for resume analysis.
    Returns: (score, missing_skills, improvement_tips)
    """
    from backend.api.skill_extractor import extract_skills
    user_skills = list(extract_skills(text))
    
    score = calculate_ats_score(text, user_skills, job_role)
    missing = get_skill_gap(user_skills, job_role)
    
    tips = []
    if score < 50:
        tips.append("Your resume matches less than 50% of the required skills. Focus on adding core technical keywords.")
    elif score < 80:
        tips.append("Good start, but you can improve your score by mentioning specific frameworks or tools like " + ", ".join(missing[:2]))
    else:
        tips.append("Excellent! Your resume is highly optimized for this role.")
        
    if "education" not in text.lower():
        tips.append("Education section seems missing or unparseable. Ensure it is clearly labeled.")
    if "experience" not in text.lower() and "internship" not in text.lower():
        tips.append("Professional experience or internships are crucial. Try to include a dedicated section.")

    return score, missing, tips
