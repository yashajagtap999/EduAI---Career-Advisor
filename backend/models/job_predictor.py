import os
import pickle

# Load trained model
try:
    model = pickle.load(open(os.path.join(os.path.dirname(__file__), "job_model.pkl"), "rb"))
    vectorizer = pickle.load(open(os.path.join(os.path.dirname(__file__), "vectorizer.pkl"), "rb"))
except Exception:
    model = None
    vectorizer = None

# ── Rule-based skill → role mapping (primary detection layer) ─────────────────
# This runs BEFORE the ML model to prevent misclassification of technical resumes.
SKILL_ROLE_RULES = [
    # Data Science / AI / ML  (highest priority)
    (["machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
      "nlp", "natural language processing", "computer vision", "data science",
      "neural network", "xgboost", "random forest", "clustering", "regression"],
     "Data Science"),

    # Data Analysis
    (["pandas", "numpy", "matplotlib", "seaborn", "power bi", "tableau",
      "data analysis", "data visualization", "statistics", "excel", "looker",
      "predictive modeling", "sql", "data analyst"],
     "Data Science"),

    # Python Developer
    (["python", "django", "flask", "fastapi", "python developer"],
     "Python Developer"),

    # Web Development
    (["html", "css", "javascript", "react", "angular", "vue", "next.js",
      "node.js", "bootstrap", "tailwind", "frontend", "backend", "fullstack",
      "web development", "web designer", "wordpress"],
     "Web Designing"),

    # Java Development
    (["java", "spring boot", "hibernate", "maven", "j2ee", "jsp"],
     "Java Developer"),

    # DevOps / Cloud
    (["aws", "docker", "kubernetes", "jenkins", "terraform", "ansible",
      "ci/cd", "devops", "cloud", "azure", "gcp", "linux", "bash"],
     "DevOps Engineer"),

    # Database
    (["mysql", "postgresql", "mongodb", "oracle", "sql server", "nosql",
      "pl/sql", "database", "snowflake", "redis"],
     "Database"),

    # .NET
    (["c#", ".net", "asp.net", "dotnet", "mvc"],
     "DotNet Developer"),

    # Blockchain
    (["solidity", "smart contracts", "ethereum", "web3", "blockchain", "crypto"],
     "Blockchain"),

    # Testing / QA
    (["selenium", "testing", "qa", "cucumber", "test automation", "manual testing", "jira"],
     "Testing"),

    # Business Analyst
    (["business analyst", "agile", "scrum", "requirements gathering",
      "stakeholder management", "visio", "bpms"],
     "Business Analyst"),

    # SAP
    (["sap", "abap", "hana", "erp", "sap fico", "sap mm"],
     "SAP Developer"),

    # Mechanical Engineering
    (["autocad", "solidworks", "catia", "ansys", "manufacturing", "cad",
      "thermodynamics", "mechanical"],
     "Mechanical Engineer"),

    # Civil Engineering
    (["structural design", "construction", "surveying", "civil", "revit", "staad", "etabs"],
     "Civil Engineer"),

    # Electrical Engineering
    (["electrical", "power systems", "substation", "transformer", "circuit design", "etap", "relays", "motor control"],
     "Electrical Engineer"),

    # Chemical Engineering
    (["chemical", "aspen", "hysys", "reactor design", "process control", "refinery", "mass balance", "fluid mechanics"],
     "Chemical Engineer"),

    # Embedded Systems & IoT
    (["embedded", "arduino", "raspberry pi", "esp32", "microcontroller", "firmware", "pcb design", "iot", "rtos"],
     "Embedded Systems & IoT Engineer"),

    # HR
    (["recruitment", "onboarding", "payroll", "hrms", "employee relations",
      "talent acquisition", "hr"],
     "HR"),

    # Sales / Marketing
    (["b2b", "lead generation", "crm", "salesforce", "negotiation",
      "digital marketing", "seo", "marketing"],
     "Sales"),
]


def _rule_based_predict(skills: list) -> str | None:
    """Return the best matching role using keyword rules. Returns None if no match."""
    skills_lower = set(s.lower() for s in skills)
    best_role = None
    best_score = 0

    for keywords, role in SKILL_ROLE_RULES:
        score = sum(1 for kw in keywords if kw in skills_lower or
                    any(kw in s for s in skills_lower))
        if score > best_score:
            best_score = score
            best_role = role

    # Only trust rule-based result if at least 1 keyword matched
    return best_role if best_score >= 1 else None


def predict_job_role(skills: list) -> list:
    """Predict the top job roles for the given skill list.
    Returns a list of tuples: [(role_name, match_percentage), ...]
    Priority:
    1. Rule-based detection (reliable for technical skills).
    2. ML model (fallback for ambiguous / non-technical profiles).
    """
    result = []
    
    # ── Step 1: Rule-based primary detection ──────────────────────────────────
    rule_role = _rule_based_predict(skills)
    if rule_role:
        result.append((rule_role, 95)) # High confidence for rule-based match
        
        if model and vectorizer:
            try:
                skills_text = " ".join(skills)
                skills_vec = vectorizer.transform([skills_text])
                probs = model.predict_proba(skills_vec)[0]
                classes = model.classes_
                top_indices = probs.argsort()[::-1][:5]
                for i in top_indices:
                    role = classes[i]
                    prob = int(probs[i] * 100)
                    if role != rule_role and role not in ["Arts", "Health and fitness"]:
                        result.append((role, prob if prob < 95 else 88))
                        if len(result) >= 3:
                            break
            except Exception:
                # Mock alternatives if ML fails
                pass
        
        # If we couldn't get alternatives from ML, add mock generic ones or just return the one
        if len(result) == 1:
            result.append(("Related Field", 85))
            result.append(("General / Entry-Level", 75))
            
        return result[:3]

    # ── Step 2: ML model fallback ──────────────────────────────────────────────
    if model and vectorizer:
        try:
            skills_text = " ".join(skills)
            skills_vec = vectorizer.transform([skills_text])
            probs = model.predict_proba(skills_vec)[0]
            classes = model.classes_
            top_indices = probs.argsort()[::-1][:3]
            return [(classes[i], int(probs[i] * 100)) for i in top_indices]
        except (AttributeError, Exception):
            try:
                prediction = model.predict(vectorizer.transform([" ".join(skills)]))[0]
                return [(prediction, 80)]
            except Exception:
                pass

    # ── Step 3: Generic fallback ───────────────────────────────────────────────
    return [("General / Entry-Level", 75)]