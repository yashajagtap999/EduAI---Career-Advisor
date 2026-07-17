import os
import sys
import json
import uuid
import tempfile
from typing import List, Optional
from pydantic import BaseModel

from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Cookie, Response, Request
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Ensure the parent directory is on the path for package resolutions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables explicitly on startup
from dotenv import load_dotenv
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, ".env")
load_dotenv(env_path)

from backend.database.database import (
    init_db, register_user, login_user, user_exists, save_progress, get_progress,
    log_scan, get_dashboard_data, get_user_scans, get_latest_scan, get_latest_scan_full
)
from backend.api.parser import extract_resume_text
from backend.api.skill_extractor import extract_skills
from backend.api.analyzer import analyze_resume, JOB_SKILLS, _is_match
from backend.api.builder import enhance_resume
from backend.api.recommender import recommend_courses, generate_roadmap, generate_skill_roadmap
from backend.api.student_advisor import get_fields_of_study, get_colleges_for_field, get_four_year_roadmap
from backend.api.export import export_resume_pdf, export_roadmap_pdf
from backend.models.job_predictor import predict_job_role
from backend.api.mentor_engine import get_mentor_response
from backend.api.internship_engine import search_adzuna_internships

# Initialize SQLite database
init_db()

app = FastAPI(title="EduAI API", description="SaaS Backend API for EduAI Career platform")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app|http://localhost.*|http://127\.0\.0\.1.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache for generated resume PDFs
resume_pdf_cache = {}

# Pydantic Schemas
class RegisterRequest(BaseModel):
    username: str
    password: str
    full_name: str

class LoginRequest(BaseModel):
    username: str
    password: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage]

class OptimizeResumeRequest(BaseModel):
    username: str
    resume_text: str
    missing_skills: List[str]
    job_role: str

class InternshipRecommendRequest(BaseModel):
    skills: List[str]
    cgpa: float
    location: str
    branch: str

# Helper to verify session cookie
def get_logged_in_user(username: Optional[str] = Cookie(None)):
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return username

# ── AUTH ENDPOINTS ──

@app.post("/api/auth/register")
def api_register(req: RegisterRequest):
    success, msg = register_user(req.username, req.password, req.full_name)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"success": True, "message": msg}

@app.post("/api/auth/login")
def api_login(req: LoginRequest, response: Response):
    # Check if user exists in database first
    if not user_exists(req.username):
        raise HTTPException(status_code=400, detail="Account does not exist. Please register/create an account first.")
        
    success, full_name = login_user(req.username, req.password)
    if not success:
        raise HTTPException(status_code=400, detail="Incorrect password. Please try again.")
    
    # Set username session cookie
    response.set_cookie(key="username", value=req.username, max_age=86400, httponly=False)
    response.set_cookie(key="full_name", value=full_name, max_age=86400, httponly=False)
    return {
        "success": True, 
        "username": req.username, 
        "full_name": full_name, 
        "message": "Login successful!"
    }

@app.post("/api/auth/logout")
def api_logout(response: Response):
    response.delete_cookie("username")
    response.delete_cookie("full_name")
    return {"success": True, "message": "Logged out successfully!"}

@app.get("/api/auth/session")
def api_session(username: Optional[str] = Cookie(None), full_name: Optional[str] = Cookie(None)):
    if not username:
        return {"logged_in": False}
    return {
        "logged_in": True,
        "username": username,
        "full_name": full_name
    }

# ── DASHBOARD ENDPOINTS ──

@app.get("/api/dashboard/stats")
def api_dashboard_stats(username: str = Depends(get_logged_in_user)):
    latest_scan = get_latest_scan_full(username)
    if not latest_scan:
        return {
            "has_scan": False,
            "ats_score": 0,
            "skills_count": 0,
            "predicted_role": "Not Predicted",
            "readiness": 0,
            "skills": []
        }
    
    ats = latest_scan["ats_score"]
    job_role = latest_scan["predicted_role"]
    skills = latest_scan.get("skills", [])
    readiness = int((ats * 0.5) + (min(len(skills)*10, 100) * 0.5))
    
    return {
        "has_scan": True,
        "ats_score": ats,
        "skills_count": len(skills),
        "predicted_role": job_role,
        "readiness": readiness,
        "skills": skills,
        "suggestions": latest_scan.get("suggestions", [])
    }

@app.get("/api/dashboard/charts")
def api_dashboard_charts(username: str = Depends(get_logged_in_user)):
    latest_scan = get_latest_scan_full(username)
    scans_history = get_user_scans(username)
    
    # 1. Radar Chart Data
    radar_cats = ["Technical", "Communication", "Problem Solving", "Tools", "Domain", "Soft Skills"]
    if not latest_scan:
        radar_vals = [0] * 6
    else:
        ats = latest_scan["ats_score"]
        skill_count = len(latest_scan.get("skills", []))
        radar_vals = [
            min(100, skill_count * 12),
            min(100, int(ats * 0.85)),
            min(100, int((ats + skill_count*6)/2)),
            min(100, skill_count * 10),
            min(100, ats),
            min(100, 60 + skill_count*2)
        ]
        
    # 2. History Chart Data
    history_data = []
    for i, row in enumerate(scans_history):
        # row: (id, ats_score, predicted_role, timestamp)
        history_data.append({
            "scan": f"#{i+1}",
            "score": row[1],
            "role": row[2],
            "date": row[3][:10] if row[3] else ""
        })
        
    # 3. Top Career Suggestions
    suggestions = []
    if latest_scan:
        job_role = latest_scan["predicted_role"]
        mapping = {
            "Data Science": [("Data Scientist", 95, "Best match based on your resume"), ("Machine Learning Engineer", 88, "Strong alignment with detected skills"), ("AI Engineer", 82, "Recommended growth path")],
            "Software Engineer": [("Software Engineer", 95, "Best match based on your resume"), ("Backend Developer", 88, "Strong alignment with detected skills"), ("Full Stack Developer", 82, "Recommended growth path")],
            "Data Analyst": [("Data Analyst", 95, "Best match based on your resume"), ("Business Analyst", 88, "Strong alignment with detected skills"), ("BI Developer", 82, "Recommended growth path")],
            "Web Designing": [("Frontend Developer", 95, "Best match based on your resume"), ("UI/UX Engineer", 88, "Strong alignment with detected skills"), ("Full Stack Developer", 82, "Recommended growth path")],
            "Python Developer": [("Python Developer", 95, "Best match based on your resume"), ("Backend Engineer", 88, "Strong alignment with detected skills"), ("Data Engineer", 82, "Recommended growth path")],
            "Java Developer": [("Java Developer", 95, "Best match based on your resume"), ("Backend Engineer", 88, "Strong alignment with detected skills"), ("Software Architect", 82, "Recommended growth path")],
            "DevOps Engineer": [("DevOps Engineer", 95, "Best match based on your resume"), ("Cloud Architect", 88, "Strong alignment with detected skills"), ("SRE", 82, "Recommended growth path")],
        }
        if job_role in mapping:
            roles = mapping[job_role]
        elif "Developer" in job_role or "Engineer" in job_role:
            roles = [(job_role, 95, "Best match based on your resume"), (f"Senior {job_role}", 88, "Strong alignment with detected skills"), (f"Lead {job_role}", 82, "Recommended growth path")]
        else:
            roles = [(job_role, 95, "Best match based on your resume"), (f"{job_role} Specialist", 88, "Strong alignment with detected skills"), (f"{job_role} Manager", 82, "Recommended growth path")]
            
        for r_title, r_pct, r_desc in roles:
            suggestions.append({"title": r_title, "match": r_pct, "description": r_desc})

    return {
        "radar": {"categories": radar_cats, "values": radar_vals},
        "history": history_data,
        "career_suggestions": suggestions
    }

@app.get("/api/dashboard/roadmap")
def api_dashboard_roadmap(role: str, username: str = Depends(get_logged_in_user)):
    # 1. Fetch latest scan to calculate personal placement readiness metrics
    latest_scan = get_latest_scan_full(username)
    
    # Defaults
    resume_score = 0
    skills_score = 0
    projects_score = 60
    coding_score = 60
    communication_score = 65
    
    # Map the dropdown sub-specialties to the corresponding core roadmaps
    role_mapping = {
        # CSE / IT / Software mappings
        "Software Developer": "Software Developer",
        "Full Stack Developer": "Software Developer",
        "Frontend Developer": "Software Developer",
        "Backend Developer": "Software Developer",
        "Mobile App Developer": "Software Developer",
        "Blockchain Developer": "Software Developer",
        "UI/UX Designer": "Software Developer",
        
        "Machine Learning Engineer": "Machine Learning Engineer",
        "Artificial Intelligence Engineer": "Machine Learning Engineer",
        
        "Cloud & DevOps Engineer": "Cloud & DevOps Engineer",
        "Cybersecurity Specialist": "Cybersecurity Specialist",
        "Ethical Hacker": "Cybersecurity Specialist",
        
        "Data Scientist": "Data Scientist",
        "Data Analyst": "Data Scientist",
        
        "Data Engineer": "Data Engineer",
        "Database Administrator": "Data Engineer",
        
        # ENTC Mappings
        "Embedded Systems & IoT Engineer": "Embedded Systems & IoT Engineer",
        "VLSI Design Engineer": "Embedded Systems & IoT Engineer",
        "Electronics Design Engineer": "Embedded Systems & IoT Engineer",
        "Telecommunication Engineer": "Embedded Systems & IoT Engineer",
        
        # Mechanical Mappings
        "Design & CAD Engineer": "Design & CAD Engineer",
        "Automotive Engineer": "Design & CAD Engineer",
        "Aerospace Engineer": "Design & CAD Engineer",
        
        "Robotics & Automation Engineer": "Robotics & Automation Engineer",
        "Mechatronics Engineer": "Robotics & Automation Engineer",
        
        "Thermal Engineer": "Thermal Engineer",
        "Manufacturing & Production Engineer": "Thermal Engineer",
        
        # Electrical Mappings
        "Power & Control Systems Engineer": "Power & Control Systems Engineer",
        "Electrical Design Engineer": "Power & Control Systems Engineer",
        "Control Systems Engineer": "Power & Control Systems Engineer",
        
        # Civil Mappings
        "Structural Design Engineer": "Structural Design Engineer",
        "Civil Site Engineer": "Structural Design Engineer",
        "Construction Project Manager": "Structural Design Engineer",
        "Geotechnical Engineer": "Structural Design Engineer",
        
        # Chemical Mappings
        "Process & Chemical Engineer": "Process & Chemical Engineer",
        "Petroleum Engineer": "Process & Chemical Engineer",
        "Materials Engineer": "Process & Chemical Engineer"
    }

    mapped_role = role_mapping.get(role, "Software Developer")
    
    # Customize keyword filters based on category of role to make readiness score branch-aware!
    role_lower = mapped_role.lower()
    
    if any(branch in role_lower for branch in ["mechanical", "design & cad", "robotics", "thermal"]):
        proj_kws = ["solidworks", "ansys", "cad", "design project", "fea", "cfd", "catia", "fusion 360", "prototype"]
        code_kws = ["matlab", "python", "g-code", "cnc", "thermodynamics", "labview", "materials science", "simulink"]
    elif any(branch in role_lower for branch in ["electrical", "power & control"]):
        proj_kws = ["circuit design", "pcb", "simulation", "etap", "multisim", "proteus", "power systems", "major project"]
        code_kws = ["matlab", "simulink", "plc", "scada", "vlsi", "fpga", "verilog", "vhdl"]
    elif any(branch in role_lower for branch in ["civil", "structural"]):
        proj_kws = ["autocad", "revit", "staad pro", "etabs", "site survey", "concrete construction", "gis", "estimation"]
        code_kws = ["structural analysis", "surveying", "geotechnical", "hydraulics", "project management"]
    elif any(branch in role_lower for branch in ["chemical", "process"]):
        proj_kws = ["aspen plus", "hysys", "process control", "reactor design", "mass transfer", "heat exchanger", "simulation"]
        code_kws = ["matlab", "fluid mechanics", "thermodynamics", "chemistry", "material balance"]
    elif any(branch in role_lower for branch in ["embedded", "iot", "entc"]):
        proj_kws = ["arduino", "raspberry pi", "esp32", "pcb design", "embedded c", "microcontroller", "oscilloscope"]
        code_kws = ["matlab", "verilog", "vhdl", "c", "c++", "rtos", "arm cortex", "signal processing"]
    else: # Default: CSE / IT / Data Science / ML Roles
        proj_kws = ["github", "git", "project", "portfolio", "docker", "kubernetes", "aws", "gcp", "django", "react", "node"]
        code_kws = ["python", "java", "c++", "data structures", "algorithms", "sql", "pytorch", "tensorflow", "javascript"]

    if latest_scan:
        resume_score = latest_scan["ats_score"]
        
        # Calculate skills score based on count of keywords matched
        skills = latest_scan.get("skills", [])
        skills_count = len(skills)
        skills_score = min(100, skills_count * 8)
        
        # Check text details for customized projects, coding, and communication indicators
        skills_lower = [s.lower() for s in skills]
        
        # Projects Check
        if any(kw in skills_lower for kw in proj_kws):
            projects_score = 92
        elif skills_count > 5:
            projects_score = 80
            
        # Coding/Simulation Check
        if any(kw in skills_lower for kw in code_kws):
            coding_score = 85
        elif skills_count > 6:
            coding_score = 75
            
        # Communication Check
        if any(kw in skills_lower for kw in ["leadership", "agile", "scrum", "communication", "team", "mentoring", "presentation"]):
            communication_score = 80
        elif skills_count > 4:
            communication_score = 70
            
    # Calculate Overall Weighted Readiness Score
    overall_score = int((resume_score * 0.25) + (skills_score * 0.25) + (projects_score * 0.20) + (coding_score * 0.20) + (communication_score * 0.10))
    
    # Ensure realistic minimum bounds if scanned
    if latest_scan and overall_score < 40:
        overall_score = 45

    readiness = {
        "resume": resume_score,
        "skills": skills_score,
        "projects": projects_score,
        "coding": coding_score,
        "communication": communication_score,
        "overall": overall_score
    }
    
    # 2. Generate personalized roadmap semesters 4, 5, 6, 7, 8
    roadmaps = {
        "Machine Learning Engineer": [
            {"semester": "Semester 4", "title": "Programming & Data Structures Foundations", "details": "Master core Python OOP, Algorithmic Analysis (Big O), and basic SQLite schemas. Set up GitHub portfolio."},
            {"semester": "Semester 5", "title": "Mathematical Modeling & Data Analysis", "details": "Study Calculus, Linear Algebra, Probability, Pandas, NumPy, and Scikit-Learn regression models."},
            {"semester": "Semester 6", "title": "Deep Learning & Neural Networks", "details": "Learn PyTorch/TensorFlow, MLP, CNNs for computer vision, RNNs/Transformers for NLP, and model evaluation."},
            {"semester": "Semester 7", "title": "MLOps & Pipeline Orchestration", "details": "Learn Docker, Kubernetes, MLflow for tracking models, CI/CD pipelines, and cloud training on AWS/GCP."},
            {"semester": "Semester 8", "title": "Placement Prep & Capstone Project", "details": "Build a full-scale LLM or computer vision application, solve DSA mock tests, and practice system design interviews."}
        ],
        "Software Developer": [
            {"semester": "Semester 4", "title": "Object-Oriented Programming & Databases", "details": "Master Java, C++, DBMS design, and SQL query optimization. Write clean OOP packages."},
            {"semester": "Semester 5", "title": "Full Stack Web Technologies", "details": "Learn HTML, CSS, JavaScript, ES6, React.js, and Node.js backend APIs. Build simple CRUD tools."},
            {"semester": "Semester 6", "title": "Advanced Algorithmic DSA", "details": "Study Trees, Graphs, Dynamic Programming, and practice solving LeetCode Medium problems daily."},
            {"semester": "Semester 7", "title": "Cloud Platforms & DevOps Pipelines", "details": "Deploy apps to AWS/GCP, build Docker containers, write GitHub Actions workflows, and monitor applications."},
            {"semester": "Semester 8", "title": "Interview Simulation & Portfolio Project", "details": "Complete a distributed full stack portfolio project, review System Design basics, and run mock interviews."}
        ],
        "Cloud & DevOps Engineer": [
            {"semester": "Semester 4", "title": "Linux Systems, Bash & Networking", "details": "Master Linux CLI commands, write shell scripts, understand TCP/IP networking, and practice git basics."},
            {"semester": "Semester 5", "title": "Cloud Provider Core (AWS/Azure)", "details": "Learn computing instances, VPC/VNet subnets, IAM policies, and basic relational storage configurations."},
            {"semester": "Semester 6", "title": "Containerization & Infrastructure as Code", "details": "Master Docker container creation and build declarative cloud configurations with Terraform."},
            {"semester": "Semester 7", "title": "CI/CD & Kubernetes Orchestration", "details": "Build automated pipelines with GitHub Actions/Jenkins. Deploy scalable microservices to Kubernetes clusters."},
            {"semester": "Semester 8", "title": "Site Reliability & Mock Audits", "details": "Implement monitoring (Prometheus/Grafana), logging dashboards, run chaos testing simulations, and mock interviews."}
        ],
        "Cybersecurity Specialist": [
            {"semester": "Semester 4", "title": "Network Protocols & OS Auditing", "details": "Understand routing, packet structures, cryptography math, and windows/linux host hardening protocols."},
            {"semester": "Semester 5", "title": "Penetration Testing Tools & OWASP", "details": "Practice vulnerability auditing using Kali Linux, Nmap, Burp Suite, Metasploit, and secure coding."},
            {"semester": "Semester 6", "title": "Threat Intel & SIEM Logs", "details": "Learn log aggregation, threat intelligence feeds, Splunk dashboard configuration, and network capture analysis."},
            {"semester": "Semester 7", "title": "Cloud & Enterprise Compliance", "details": "Audit AWS/Azure access control compliance with ISO 27001, SOC2 checklists, and data privacy rules."},
            {"semester": "Semester 8", "title": "Incident Response & Simulation", "details": "Practice digital forensics steps, complete malware analysis mock labs, and run incident simulations."}
        ],
        "Data Scientist": [
            {"semester": "Semester 4", "title": "Python Programming & SQL Databases", "details": "Master Pandas, NumPy, relational databases, and advanced SQL querying. Build data cleaning scripts."},
            {"semester": "Semester 5", "title": "Applied Statistics & A/B testing", "details": "Study hypothesis testing, ANOVA, linear regression, Tableau dashboard design, and seaborn plots."},
            {"semester": "Semester 6", "title": "Supervised & Unsupervised Machine Learning", "details": "Learn Scikit-Learn algorithms (trees, clustering, SVMs), validation metrics, and feature engineering."},
            {"semester": "Semester 7", "title": "Big Data Infrastructures & NLP", "details": "Learn Hadoop, Apache Spark, NoSQL data storage, and TF-IDF/NLTK for text processing."},
            {"semester": "Semester 8", "title": "Business Case Analysis & Projects", "details": "Prepare analytical case studies, complete a capstone EDA portfolio project, and solve SQL coding tests."}
        ],
        "Data Engineer": [
            {"semester": "Semester 4", "title": "Data Schemas & Database Optimization", "details": "Master advanced SQL, database index normalization, constraints, and relational schema designs."},
            {"semester": "Semester 5", "title": "ETL/ELT Pipeline Foundations", "details": "Learn Python scripting, data serialization formats (JSON, Parquet), and Apache Airflow pipelines."},
            {"semester": "Semester 6", "title": "Distributed Big Data Systems", "details": "Learn Apache Spark, Hadoop HDFS, Kafka streaming, and Snowflake/Redshift data warehousing."},
            {"semester": "Semester 7", "title": "Cloud Data Lakes & MLOps Infrastructure", "details": "Build AWS S3 data lakes, set up IAM access policies, run Dockerized ETL tasks, and monitor jobs."},
            {"semester": "Semester 8", "title": "Data Engineering Capstone", "details": "Build a real-time data streaming pipeline, solve SQL query optimization challenges, and complete mock interviews."}
        ],
        "Embedded Systems & IoT Engineer": [
            {"semester": "Semester 4", "title": "Circuits & C Language Breadboarding", "details": "Study analog and digital circuits, write low-level C firmware, and build sensor circuits on Arduino/ESP32."},
            {"semester": "Semester 5", "title": "ARM Architecture & Interfacing", "details": "Interface ARM Cortex-M microcontrollers with registers, ADC converters, and communication links (SPI/I2C)."},
            {"semester": "Semester 6", "title": "Real-Time Systems & PCB Layouts", "details": "Learn RTOS tasks scheduler systems (FreeRTOS) and design multi-layer PCBs using Altium or Eagle CAD."},
            {"semester": "Semester 7", "title": "IoT Protocols & Wireless Nodes", "details": "Send sensor packets over MQTT, HTTP, and BLE webservice interfaces. Write energy-efficient firmware."},
            {"semester": "Semester 8", "title": "Firmware Testing & Prototype Review", "details": "Verify signals using oscilloscopes, write peripheral integration tests, and present your hardware portfolio."}
        ],
        "Design & CAD Engineer": [
            {"semester": "Semester 4", "title": "Strength of Materials & AutoCAD", "details": "Understand mechanical stress, strain, shear diagrams, and build 2D engineering blueprints in AutoCAD."},
            {"semester": "Semester 5", "title": "3D CAD Solid/Surface Modeling", "details": "Create complex component designs, part assemblies, and structural layout configurations in SolidWorks/CATIA."},
            {"semester": "Semester 6", "title": "Finite Element Analysis (FEA) Stress Analysis", "details": "Perform mesh generation, define constraints, and analyze stress, thermal, and load simulations in ANSYS."},
            {"semester": "Semester 7", "title": "Design for Manufacturing & CNC", "details": "Learn DFM parameters, sheet metal manufacturing constraints, material selection keys, and CNC G-code programming."},
            {"semester": "Semester 8", "title": "Geometric Dimensioning & Tolerancing (GD&T)", "details": "Add precision engineering tolerancing, construct a detailed CAD design project, and prepare a design portfolio."}
        ],
        "Robotics & Automation Engineer": [
            {"semester": "Semester 4", "title": "Kinematics & Microcontrollers", "details": "Analyze mechanism displacements, write C++/Python controller code, and interface sensors with ESP32/Arduino boards."},
            {"semester": "Semester 5", "title": "Control Systems & MATLAB Modeling", "details": "Model system transfer functions, run PID controller stabilization, and simulate feedbacks using MATLAB/Simulink."},
            {"semester": "Semester 6", "title": "Robot Kinematics & ROS Simulation", "details": "Study DH parameters for robot arms, trajectory planning, and simulate navigation tasks in ROS Gazebo."},
            {"semester": "Semester 7", "title": "Industrial PLCs & SCADA Panels", "details": "Write ladder logic scripts, program industrial PLCs, and build SCADA factory telemetry monitoring dashboards."},
            {"semester": "Semester 8", "title": "Autonomous Navigation & SLAM Project", "details": "Build a wheeled robot prototype using LiDAR, simulate SLAM mapping navigation, and mock hardware reviews."}
        ],
        "Thermal Engineer": [
            {"semester": "Semester 4", "title": "Fluid Mechanics & Fluid Dynamics", "details": "Study fluid behaviors, flow control systems, dimensional analysis, and basic mechanical design blueprints."},
            {"semester": "Semester 5", "title": "Advanced Thermodynamics & Heat Transfer", "details": "Model heat exchanges, design conduction and radiation panels, and analyze internal combustion cycles."},
            {"semester": "Semester 6", "title": "Computational Fluid Dynamics (CFD)", "details": "Construct finite volume meshes and perform simulation models of fluids/gas behaviors using ANSYS Fluent."},
            {"semester": "Semester 7", "title": "Refrigeration, HVAC & Power Plants", "details": "Understand air conditioning cycles, duct layouts, steam/gas turbines, and solar-thermal installations."},
            {"semester": "Semester 8", "title": "Thermal System Design Capstone Project", "details": "Design an industrial cooling unit or shell-and-tube heat exchanger, run mock stress calculation tests."}
        ],
        "Power & Control Systems Engineer": [
            {"semester": "Semester 4", "title": "Network Analysis & MATLAB Circuits", "details": "Master circuit loop theorems, AC waveforms, transients, and simulate network circuits using MATLAB."},
            {"semester": "Semester 5", "title": "Electrical Machinery & Transformers", "details": "Understand working principles, equivalent circuits, and tests of induction/synchronous motors & power transformers."},
            {"semester": "Semester 6", "title": "Control System Design & ETAP Analysis", "details": "Model loop stability, design compensators, and perform power flow / short circuit studies in ETAP software."},
            {"semester": "Semester 7", "title": "Smart Grids & Substation Relays", "details": "Learn electrical protection schemes, digital relays, smart grid architectures, and solar/wind inverter grids."},
            {"semester": "Semester 8", "title": "Substation Layout Capstone Project", "details": "Design a complete transmission substation layout, perform load calculations, and review mock site plans."}
        ],
        "Structural Design Engineer": [
            {"semester": "Semester 4", "title": "Fluid Mechanics & Concrete technology", "details": "Learn concrete mix designs, fluid hydraulics, and draw basic CAD site layout plans."},
            {"semester": "Semester 5", "title": "Structural Mechanics & Steel Designs", "details": "Learn axial stress load distributions, steel structural design parameters, and AutoCAD structural drafting."},
            {"semester": "Semester 6", "title": "RCC Building Analysis & STAAD Pro", "details": "Perform structural calculations, design RCC slabs/columns, and model multi-story frames in STAAD Pro / ETABS."},
            {"semester": "Semester 7", "title": "Geotechnical & Soil Foundations", "details": "Calculate foundation load bearings, retaining wall stresses, and use GIS software for mapping elevations."},
            {"semester": "Semester 8", "title": "Earthquake Design & Project Estimating", "details": "Design seismic-resistant elements, draft quantities / cost estimates, and prepare 3D Revit models."}
        ],
        "Process & Chemical Engineer": [
            {"semester": "Semester 4", "title": "Mass & Energy Material Balances", "details": "Perform mass flow balances on multi-unit operations, draw piping diagrams, and study industrial chemistry."},
            {"semester": "Semester 5", "title": "Thermodynamics & Heat Transfer", "details": "Model thermodynamic states, design heat exchangers, and solve heat conduction / convection equations."},
            {"semester": "Semester 6", "title": "Separation Processes & Aspen Simulation", "details": "Analyze distillation column mass transfers, gas absorption columns, and model processes in Aspen Plus/HYSYS."},
            {"semester": "Semester 7", "title": "Reaction Kinetics & Process Controls", "details": "Design chemical reactors, configure PID control feedback loops, and perform plant safety audits."},
            {"semester": "Semester 8", "title": "Refinery Plant Design Capstone", "details": "Draft a complete plant process design layout, write HAZOP safety reviews, and perform cost estimation."}
        ]
    }
    
    roadmap_list = roadmaps.get(mapped_role, roadmaps["Software Developer"])
    
    return {
        "role": role,
        "readiness": readiness,
        "roadmap": roadmap_list
    }

@app.post("/api/internships/recommend")
def api_internships_recommend(req: InternshipRecommendRequest, username: str = Depends(get_logged_in_user)):
    return search_adzuna_internships(req.skills, req.cgpa, req.location, req.branch)

# ── RESUME X-RAY ENDPOINTS ──

class FastAPIUploadedFileWrapper:
    def __init__(self, file_like, filename):
        self.file = file_like
        self.name = filename
    def __getattr__(self, name):
        return getattr(self.file, name)

@app.post("/api/resume/scan")
async def api_resume_scan(file: UploadFile = File(...), username: str = Depends(get_logged_in_user)):
    # Read uploaded file
    file_content = await file.read()
    
    # Save to temp file
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_content)
        tmp_path = tmp.name
        
    try:
        # Wrap the file for extract_resume_text compatibility
        with open(tmp_path, "rb") as f:
            file_wrapper = FastAPIUploadedFileWrapper(f, file.filename)
            text = extract_resume_text(file_wrapper)
            
        if not text or text == "Unsupported file format":
            raise HTTPException(status_code=400, detail="Unsupported file format or unreadable document.")
            
        skills = list(extract_skills(text))
        roles_with_scores = predict_job_role(skills)
        
        if roles_with_scores:
            job_role = roles_with_scores[0][0]
            job_match_percentage = roles_with_scores[0][1]
        else:
            job_role = "General / Entry-Level"
            job_match_percentage = 75
            
        score, missing, tips = analyze_resume(text, job_role)
        log_scan(username, score, job_role, skills, tips)
        
        # Skill gaps
        req_skills = JOB_SKILLS.get(job_role, [])
        matched_skills = []
        missing_skills = []
        for req in req_skills:
            found = False
            for us in skills:
                if _is_match(req, us):
                    matched_skills.append(us.title())
                    found = True
                    break
            if not found:
                missing_skills.append(req.title())
                
        additional_skills = []
        for us in skills:
            if not any(_is_match(req, us) for req in req_skills):
                additional_skills.append(us.title())
                
        # Mastery Plans for missing skills
        mastery_plans = {}
        for skill in missing_skills[:5]: # Cap at 5 plans to keep response fast
            roadmap_data = generate_skill_roadmap(skill)
            mastery_plans[skill] = {
                "plan": roadmap_data.get("plan", []),
                "resources": roadmap_data.get("links", {})
            }

        return {
            "success": True,
            "resume_text": text,
            "ats_score": score,
            "predicted_role": job_role,
            "match_percentage": job_match_percentage,
            "tips": tips,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "additional_skills": additional_skills,
            "mastery_plans": mastery_plans
        }
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.post("/api/resume/optimize")
def api_resume_optimize(req: OptimizeResumeRequest):
    try:
        resume_dict = enhance_resume(req.resume_text, req.missing_skills, req.job_role)
        if not isinstance(resume_dict, dict) or "name" not in resume_dict:
            raise HTTPException(status_code=400, detail="Could not optimize resume details.")
            
        pdf_bytes = export_resume_pdf(resume_dict)
        
        # Save to memory cache using a unique token
        token = str(uuid.uuid4())
        resume_pdf_cache[token] = {
            "bytes": pdf_bytes,
            "filename": f"{resume_dict.get('name','Resume').replace(' ', '_')}_ATS_Optimized.pdf"
        }
        
        return {
            "success": True,
            "resume_data": resume_dict,
            "download_token": token
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resume/download")
def api_resume_download(token: str):
    if token not in resume_pdf_cache:
        raise HTTPException(status_code=404, detail="File expired or not found.")
        
    cache = resume_pdf_cache[token]
    
    # Save temporary file to serve
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(cache["bytes"])
        tmp_path = tmp.name
        
    # Standard file responder
    response = FileResponse(tmp_path, filename=cache["filename"], media_type="application/pdf")
    return response

# ── AI MENTOR CHAT ENDPOINT ──

@app.post("/api/mentor/chat")
async def api_mentor_chat(req: Request, username: str = Depends(get_logged_in_user)):
    try:
        body = await req.json()
        message = body.get("message")
        history_list = body.get("history", [])
        
        # Retrieve user context from database
        latest_scan = get_latest_scan_full(username)
        if latest_scan:
            job_role = latest_scan["predicted_role"]
            skills = latest_scan["skills"]
            suggestions = latest_scan["suggestions"]
        else:
            job_role = "General / Entry-Level"
            skills = []
            suggestions = []
            
        # Re-arrange ChatRequest history object to tuples (role, message)
        chat_history = []
        for h in history_list:
            role = "user" if h.get("role") == "user" else "assistant"
            chat_history.append((role, h.get("content", "")))
            
        # Server Sent Events response stream generator
        async def event_generator():
            try:
                # get_mentor_response yields chunks of text
                for chunk in get_mentor_response(message, job_role, skills, "", chat_history):
                    yield f"data: {json.dumps({'text': chunk})}\n\n"
            except Exception as ex:
                yield f"data: {json.dumps({'error': str(ex)})}\n\n"
            yield "data: [DONE]\n\n"
            
        return StreamingResponse(event_generator(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request format: {e}")

# ── COLLEGE FINDER ENDPOINTS ──

@app.get("/api/college/fields")
def api_college_fields():
    return {"fields": get_fields_of_study()}

@app.get("/api/college/recommendations")
def api_college_recommendations(field: str, city: Optional[str] = None):
    raw_colleges = get_colleges_for_field(field)
    colleges = []
    for c in raw_colleges:
        # c: (name, city, description, website)
        if city and c[1].lower() != city.lower():
            continue
        colleges.append({
            "name": c[0],
            "city": c[1],
            "description": c[2],
            "website": c[3]
        })
    return {"colleges": colleges}

@app.get("/api/college/roadmap")
def api_college_roadmap(field: str, username: str = Depends(get_logged_in_user)):
    roadmap = get_four_year_roadmap(field)
    
    # Generate PDF bytes
    pdf_bytes = export_roadmap_pdf(field, {k: v["summary"] for k, v in roadmap.items()}, username)
    token = str(uuid.uuid4())
    resume_pdf_cache[token] = {
        "bytes": pdf_bytes,
        "filename": f"{field.replace(' ', '_')}_Academic_Blueprint.pdf"
    }
    
    return {
        "roadmap": roadmap,
        "download_token": token
    }

# ── PLATFORM ANALYTICS ENDPOINT ──

@app.get("/api/analytics/global")
def api_analytics_global():
    data = get_dashboard_data()
    # data keys: career_paths, scores, engagement, total_scans, avg_score
    
    paths = []
    for p in data["career_paths"]:
        paths.append({"role": p[0], "count": p[1]})
        
    scores = data["scores"]
    avg_score = data["avg_score"]
    total_scans = data["total_scans"]
    
    # ── Tech Market Size Projections (2026-2030) ──
    market_stats = {
        "years": [2026, 2027, 2028, 2029, 2030],
        "categories": {
            "AI & Machine Learning": [320, 450, 630, 900, 1300],
            "Cloud Computing": [670, 780, 910, 1060, 1250],
            "Cybersecurity": [220, 250, 290, 330, 380],
            "Data Engineering & Big Data": [180, 210, 245, 290, 340]
        }
    }
    
    return {
        "total_scans": total_scans,
        "avg_score": avg_score,
        "preparedness": "High" if avg_score >= 75 else "Medium",
        "career_paths": paths,
        "scores": scores,
        "market_projections": market_stats
    }

# ── SERVE WEB PAGES ──

# Define web page serving endpoints
pages = [
    ("index.html", "/"),
    ("login.html", "/login"),
    ("dashboard.html", "/dashboard"),
    ("profile.html", "/profile"),
    ("resume.html", "/resume"),
    ("chatbot.html", "/chatbot"),
    ("college-finder.html", "/college-finder"),
    ("analytics.html", "/analytics")
]

@app.get("/")
def get_index():
    response = FileResponse(os.path.join(base_dir, "frontend", "index.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/login")
def get_login():
    response = FileResponse(os.path.join(base_dir, "frontend", "login.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/dashboard")
def get_dashboard():
    return FileResponse(os.path.join(base_dir, "frontend", "dashboard.html"))

@app.get("/roadmap")
def get_roadmap():
    return FileResponse(os.path.join(base_dir, "frontend", "roadmap.html"))

@app.get("/internships")
def get_internships():
    response = FileResponse(os.path.join(base_dir, "frontend", "internships.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/profile")
def get_profile():
    return FileResponse(os.path.join(base_dir, "frontend", "profile.html"))

@app.get("/resume")
def get_resume():
    return FileResponse(os.path.join(base_dir, "frontend", "resume.html"))

@app.get("/chatbot")
def get_chatbot():
    return FileResponse(os.path.join(base_dir, "frontend", "chatbot.html"))

@app.get("/college-finder")
def get_college_finder():
    return FileResponse(os.path.join(base_dir, "frontend", "college-finder.html"))

@app.get("/analytics")
def get_analytics():
    return FileResponse(os.path.join(base_dir, "frontend", "analytics.html"))

# Mount Static Directories
app.mount("/css", StaticFiles(directory=os.path.join(base_dir, "frontend", "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(base_dir, "frontend", "js")), name="js")
app.mount("/assets", StaticFiles(directory=os.path.join(base_dir, "frontend", "assets")), name="assets")

# Run using uvicorn if script invoked directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
