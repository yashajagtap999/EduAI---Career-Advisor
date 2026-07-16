# Student Advisor Data & Engine - India-wide College Database
from backend.api.college_data import (
    EXTENDED_CS_COLLEGES,
    EXTENDED_CORE_COLLEGES,
    EXTENDED_BBA_COLLEGES,
    EXTENDED_MED_COLLEGES,
    EXTENDED_ARTS_COLLEGES
)
def get_fields_of_study():
    return [
        "Artificial Intelligence & Machine Learning (AI/ML)",
        "Computer Science Engineering (Core)",
        "Information Technology (IT)",
        "Data Science & Analytics",
        "Electronics & Telecommunication (E&TC)",
        "Mechanical Engineering",
        "Civil Engineering",
        "Bachelor of Business Administration (BBA)",
        "Medicine / MBBS",
        "Arts & Psychology"
    ]

def get_colleges_for_field(field):
    if "AI/ML" in field or "Computer Science" in field or "Data Science" in field or "IT" in field:
        return [
            # Pune
            ("College of Engineering Pune (COEP)", "Pune", "Autonomous Tier-1 in Maharashtra. Best for competitive programming and research.", "https://www.coep.org.in"),
            ("Pune Institute of Computer Technology (PICT)", "Pune", "Near 100% CS/IT placement rate. Extremely rigorous academics.", "https://pict.edu"),
            ("Pimpri Chinchwad College of Engineering (PCCOE)", "Pune", "Top private institute with rapidly expanding AI/ML dedicated branches.", "http://www.pccoepune.com"),
            ("MIT World Peace University (MIT-WPU)", "Pune", "Premium infrastructure, specialized B.Tech in AI & Data Science.", "https://mitwpu.edu.in"),
            ("JSPM Rajarshi Shahu College of Engineering (RSCOE)", "Pune", "Excellent industry connections and robust placements in TCS/Infosys.", "https://jspmrscoe.edu.in"),
            ("JSPM University, Wagholi", "Pune", "New-age university campus in Wagholi with dedicated AI/ML, Cloud & Data Science tracks and industry-focused curriculum.", "https://www.jspmuniversity.ac.in"),
            ("Dr. D. Y. Patil Institute of Technology (DYP)", "Pune", "Massive campus, modern labs specifically built for ML frameworks.", "https://engg.dypvp.edu.in"),
            ("Symbiosis Institute of Technology (SIT)", "Pune", "Tier-1 private university with premium CS and AI infrastructure.", "https://www.sitpune.edu.in"),
            ("Vishwakarma Institute of Technology (VIT Pune)", "Pune", "Highly reputed autonomous engineering college with strong CS placements.", "https://www.vit.edu"),
            ("Indira College of Engineering & Management (ICEM)", "Pune", "Growing tech-focused engineering institute with industry collaborations.", "https://www.indiraicem.ac.in"),
            # Nashik
            ("K. K. Wagh Institute of Engineering", "Nashik", "Premier engineering college of Nashik with top-class CS/AI departments.", "https://engg.kkwagh.edu.in"),
            ("Sandip University", "Nashik", "New-age specialization tracks in Cloud, AI and Cybersecurity.", "https://www.sandipuniversity.edu.in"),
            # Mumbai
            ("IIT Bombay", "Mumbai", "India's #1 engineering institute. Best for CS, AI, and research.", "https://www.iitb.ac.in"),
            ("VJTI Mumbai", "Mumbai", "Top government engineering college with strong placements.", "https://vjti.ac.in"),
            ("SPIT Mumbai", "Mumbai", "Premier private CS college with excellent industry connections.", "https://www.spit.ac.in"),
            # Bengaluru
            ("IISc Bengaluru", "Bengaluru", "World-class research institute. Best for AI/ML research careers.", "https://www.iisc.ac.in"),
            ("RV College of Engineering", "Bengaluru", "Top private engineering college in Karnataka.", "https://www.rvce.edu.in"),
            ("PES University", "Bengaluru", "Strong CS and AI programs with excellent startup culture.", "https://pes.edu"),
            # Delhi/NCR
            ("IIT Delhi", "Delhi", "Top-tier IIT with world-class CS and AI departments.", "https://home.iitd.ac.in"),
            ("DTU (Delhi Technological University)", "Delhi", "One of the best government engineering colleges in North India.", "https://dtu.ac.in"),
            ("Netaji Subhas University of Technology (NSUT)", "Delhi", "Premier Delhi government college for CS and IT.", "https://www.nsut.ac.in"),
            # Hyderabad
            ("IIT Hyderabad", "Hyderabad", "Cutting-edge IIT with dedicated AI department.", "https://www.iith.ac.in"),
            ("CBIT Hyderabad", "Hyderabad", "Top private engineering college in Telangana.", "https://cbit.ac.in"),
            # Chennai
            ("IIT Madras", "Chennai", "Ranked #1 in India by NIRF. Best for CS, AI, Data Science.", "https://www.iitm.ac.in"),
            ("Anna University", "Chennai", "Premier state university with excellent engineering programs.", "https://www.annauniv.edu"),
            # Jaipur
            ("BITS Pilani", "Pilani/Jaipur", "Tier-1 private university with excellent CS and AI programs.", "https://www.bits-pilani.ac.in"),
            ("Manipal Institute of Technology", "Manipal", "Top private university with strong industry placements.", "https://manipal.edu"),
        ] + EXTENDED_CS_COLLEGES
    elif "Electronics" in field or "Mechanical" in field or "Civil" in field:
        return [
            ("College of Engineering Pune (COEP)", "Pune", "Gold-standard for mechanical and civil core fields in Maharashtra.", "https://www.coep.org.in"),
            ("MIT Academy of Engineering", "Alandi, Pune", "Strong focus on robotics and mechanical design.", "https://mitaoe.ac.in"),
            ("K. K. Wagh Institute of Engineering", "Nashik", "Outstanding placements in manufacturing hubs like Mahindra/Bosch.", "https://engg.kkwagh.edu.in"),
            ("IIT Bombay", "Mumbai", "World-class Mechanical and Civil Engineering programs.", "https://www.iitb.ac.in"),
            ("IIT Delhi", "Delhi", "Top-tier programs in Civil and Structural Engineering.", "https://home.iitd.ac.in"),
            ("NIT Trichy", "Trichy", "Premier NIT known for excellent core engineering placements.", "https://www.nitt.edu"),
            ("IIT Madras", "Chennai", "Outstanding Mechanical and Electrical Engineering research.", "https://www.iitm.ac.in"),
            ("PCCOE", "Pune", "Excellent industrial tie-ups with Tata Motors & Bajaj.", "http://www.pccoepune.com"),
        ] + EXTENDED_CORE_COLLEGES
    elif "BBA" in field:
        return [
            ("Symbiosis Centre for Management Studies (SCMS)", "Pune", "Tier-1 BBA institute in India. Exceptional placement record.", "https://www.scmspune.ac.in"),
            ("BMCC Pune", "Pune", "Historical prestige with an amazing alumni network.", "https://www.bmcc.ac.in"),
            ("MIT-WPU Faculty of Management", "Pune", "Corporate-driven BBA degrees with industry mentorship.", "https://mitwpu.edu.in"),
            ("Narsee Monjee College (NMIMS)", "Mumbai", "One of the best BBA programs in India.", "https://nmims.edu"),
            ("Christ University", "Bengaluru", "Highly reputed management programs in South India.", "https://christuniversity.in"),
            ("Delhi University (DU)", "Delhi", "SRCC and Hindu College are India's top commerce colleges.", "https://www.du.ac.in"),
            ("Sandip University", "Nashik", "Comprehensive management wing with practical learning.", "https://www.sandipuniversity.edu.in"),
        ] + EXTENDED_BBA_COLLEGES
    elif "Medicine" in field:
        return [
            ("Armed Forces Medical College (AFMC)", "Pune", "One of the best medical colleges in India. NEET top scorers only.", "https://afmc.nic.in"),
            ("BJ Government Medical College", "Pune", "Top government medical college with massive attached hospital.", "https://www.bjmcpune.org"),
            ("AIIMS New Delhi", "Delhi", "India's #1 medical institute. Extremely competitive NEET cutoff.", "https://www.aiims.edu"),
            ("AIIMS Nagpur", "Nagpur", "Premier AIIMS institute in central India.", "https://aiimsnagpur.edu.in"),
            ("Grant Medical College", "Mumbai", "One of the oldest and most reputed medical colleges in Maharashtra.", "https://www.gmcmumbai.org"),
            ("Kasturba Medical College", "Manipal", "Top private medical college in India.", "https://manipal.edu/kmc-manipal.html"),
            ("Dr. Vasantrao Pawar Medical College", "Nashik", "A leading medical institute in Nashik.", "https://drvasantraopawarmedicalcollege.com"),
            ("Christian Medical College (CMC)", "Vellore", "World-class medical education and research.", "https://www.cmch-vellore.edu"),
        ] + EXTENDED_MED_COLLEGES
    else:
        return [
            ("Fergusson College", "Pune", "Historic arts, science, and psychology powerhouse.", "https://www.fergusson.edu"),
            ("Savitribai Phule Pune University (SPPU)", "Pune", "Diverse offerings across all spectrums.", "http://www.unipune.ac.in"),
            ("Miranda House", "Delhi", "India's top women's college for arts and humanities.", "https://mirandahouse.ac.in"),
            ("Lady Shri Ram College (LSR)", "Delhi", "Premier arts and commerce college in DU.", "https://lsr.edu.in"),
            ("St. Xavier's College", "Mumbai", "Historic Jesuit college known for arts and social science.", "https://xaviers.edu"),
            ("Presidency College", "Kolkata", "Oldest and most prestigious liberal arts college in India.", "https://www.presiuniv.ac.in"),
            ("Christ University", "Bengaluru", "Outstanding arts, psychology, and journalism programs.", "https://christuniversity.in"),
            ("Sandip University", "Nashik", "Modern comprehensive university across all tracks.", "https://www.sandipuniversity.edu.in"),
        ] + EXTENDED_ARTS_COLLEGES

def get_four_year_roadmap(field):
    if "AI/ML" in field or "Computer Science" in field or "Data Science" in field or "IT" in field:
        return {
            "🟡 Year 1: Foundations & Fundamentals": {
                "summary": "Focus on building a rock-solid programming base. This is the year to master the 'logic' of coding before moving to complex frameworks.",
                "topics": [
                    "Step 1: Master C/C++ to understand memory management and logic.",
                    "Step 2: Learn Discrete Mathematics - essential for algorithm design.",
                    "Step 3: Introduction to Data Structures (Arrays, Stacks, Queues).",
                    "Step 4: Set up your GitHub profile and learn basic Git workflow.",
                    "Step 5: Start solving 2 easy problems daily on platforms like HackerRank."
                ],
                "resources": {
                    "GeeksForGeeks - C Programming": "https://www.geeksforgeeks.org/c-programming-language/",
                    "GitHub Guide": "https://guides.github.com/activities/hello-world/",
                    "HackerRank - Problem Solving": "https://www.hackerrank.com/domains/algorithms"
                }
            },
            "🟠 Year 2: Data Structures & Web Core": {
                "summary": "Mastering DSA is the single most important part of your degree. Parallelly, build your first full-stack application.",
                "topics": [
                    "Step 1: Deep dive into Linked Lists, Trees, and Graphs.",
                    "Step 2: Learn Object-Oriented Programming (OOP) via Java or Python.",
                    "Step 3: Database Year: Master SQL and understand how data is stored efficiently.",
                    "Step 4: Web Development: Build a personal portfolio using HTML, CSS, and JS.",
                    "Step 5: Begin solving LeetCode Easy-Medium problems (Aim for 100+)."
                ],
                "resources": {
                    "LeetCode": "https://leetcode.com/",
                    "SQL Tutorial": "https://www.w3schools.com/sql/",
                    "MDN Web Docs": "https://developer.mozilla.org/"
                }
            },
            "🔴 Year 3: AI Specialization & Internships": {
                "summary": "This is your professional entry year. You must specialize (AI/ML/Cloud) and secure an internship.",
                "topics": [
                    "Step 1: Machine Learning Core (Regression, Classification, Neural Networks).",
                    "Step 2: Learn Python libraries: NumPy, Pandas, Scikit-Learn.",
                    "Step 3: Industry Project: Build an AI-powered app (e.g., Sentiment Analyzer).",
                    "Step 4: Prepare for Aptitude tests and Technical Interview rounds.",
                    "Step 5: Apply for Summer Internships at startups or tech giants."
                ],
                "resources": {
                    "Kaggle ML Courses": "https://www.kaggle.com/learn",
                    "Fast.ai - Practical Deep Learning": "https://www.fast.ai/",
                    "Internshala": "https://internshala.com/"
                }
            },
            "🟢 Year 4: Deployment, Projects & Placement": {
                "summary": "Final stretch. Focus on system design, heavy projects, and cracking the top-tier campus placements.",
                "topics": [
                    "Step 1: Complete and deploy a Major Capstone Project on Cloud (AWS/GCP).",
                    "Step 2: Master System Design basics: Scalability, Load Balancers, Databases.",
                    "Step 3: Intensive Placement Prep: OS, Networking, and HR Round Prep.",
                    "Step 4: Crack your dream job offer through campus or off-campus drives.",
                    "Step 5: Build a professional LinkedIn presence and start networking."
                ],
                "resources": {
                    "InterviewBit": "https://www.interviewbit.com/",
                    "System Design Primer": "https://github.com/donnemartin/system-design-primer",
                    "LinkedIn Job Search": "https://www.linkedin.com/jobs/"
                }
            }
        }
    elif "Mechanical" in field or "Civil" in field or "Electronics" in field:
        return {
            "🟡 Year 1: Foundations": {
                "summary": "Understand engineering principles and build a strong academic base.",
                "topics": [
                    "Step 1: Master Engineering Graphics & AutoCAD basics.",
                    "Step 2: Learn Engineering Mechanics fundamentals.",
                    "Step 3: Basic C Programming for embedded systems.",
                    "Step 4: Mathematics (Calculus, Linear Algebra) for analysis.",
                    "Step 5: Hands-on Workshop Practice & Tooling."
                ],
                "resources": {
                    "GFG - C Programming": "https://www.geeksforgeeks.org/c-programming-language/",
                    "YouTube - AutoCAD Basics": "https://www.youtube.com/results?search_query=autocad+for+beginners",
                    "NPTEL - Engineering Mechanics": "https://nptel.ac.in"
                }
            },
            "🟠 Year 2: Core Fundamentals": {
                "summary": "Deep dive into core engineering subjects and software tools.",
                "topics": [
                    "Step 1: Study Thermodynamics, Fluid Mechanics & Circuit Theory.",
                    "Step 2: Master Core Software: SolidWorks or STAAD Pro.",
                    "Step 3: Understand advanced Material Science.",
                    "Step 4: Learn modern Manufacturing Processes.",
                    "Step 5: Start simple design projects on cloud repositories."
                ],
                "resources": {
                    "NPTEL Courses": "https://nptel.ac.in",
                    "YouTube - SolidWorks": "https://www.youtube.com/results?search_query=solidworks+tutorial",
                    "GFG - GATE Preparation": "https://www.geeksforgeeks.org/gate-cs-notes-gq/"
                }
            },
            "🔴 Year 3: Advanced Tools & Internship": {
                "summary": "Master simulation software and secure a core industrial internship.",
                "topics": [
                    "Step 1: Master Simulation tools: ANSYS / MATLAB / PLC Programming.",
                    "Step 2: Secure an Industrial Internship (Mahindra, Bosch, L&T).",
                    "Step 3: Execute complex Design Projects.",
                    "Step 4: Begin early GATE Preparation for higher studies.",
                    "Step 5: Build a professional profile for core sector networking."
                ],
                "resources": {
                    "NPTEL - MATLAB": "https://nptel.ac.in",
                    "Internshala": "https://internshala.com",
                    "Made Easy GATE": "https://www.madeeasy.in"
                }
            },
            "🟢 Year 4: Thesis & Placements": {
                "summary": "Complete a major project and sit for core engineering company drives.",
                "topics": [
                    "Step 1: Complete a Major Capstone Project / Thesis.",
                    "Step 2: participate in Baja SAE / Robocon competitions.",
                    "Step 3: Crack the GATE Exam or GRE for Masters.",
                    "Step 4: Sit for Core Company Drives (Tata, Bajaj, L&T, Siemens).",
                    "Step 5: Intensive Resume & Interview Prep for technical rounds."
                ],
                "resources": {
                    "GFG - GATE": "https://www.geeksforgeeks.org/gate-cs-notes-gq/",
                    "LinkedIn Jobs": "https://www.linkedin.com/jobs/",
                    "Naukri.com": "https://www.naukri.com"
                }
            }
        }
    elif "BBA" in field:
        return {
            "🟡 Year 1: Business Basics": {
                "summary": "Learn the fundamentals of economics, accounting, and communication.",
                "topics": [
                    "Step 1: Get comfortable with Micro & Macro Economics.",
                    "Step 2: Learn core Principles of Management.",
                    "Step 3: Business Communication & Presentation skills.",
                    "Step 4: Basics of Accounting & Bookkeeping.",
                    "Step 5: Master MS Excel & PowerPoint for corporate work."
                ],
                "resources": {
                    "YouTube - Economics": "https://www.youtube.com/results?search_query=economics+for+beginners",
                    "W3Schools - Excel": "https://www.w3schools.com/excel/",
                    "Coursera - Business Basics": "https://www.coursera.org/browse/business"
                }
            },
            "🟠 Year 2: Specialization": {
                "summary": "Explore core domains and learn analytical tools.",
                "topics": [
                    "Step 1: Master Marketing & Financial Management.",
                    "Step 2: Learn HR Management & Organizational Behavior.",
                    "Step 3: Introduction to PowerBI / Tableau Basics.",
                    "Step 4: Business Analytics with Excel and Python.",
                    "Step 5: Start participating in Case Study competitions."
                ],
                "resources": {
                    "GFG - Business Analytics": "https://www.geeksforgeeks.org/business-analytics/",
                    "YouTube - PowerBI": "https://www.youtube.com/results?search_query=power+bi+full+course",
                    "Coursera - Marketing": "https://www.coursera.org/browse/business/marketing"
                }
            },
            "🔴 Year 3: Internship & Capstone": {
                "summary": "Put theory into practice with a corporate internship.",
                "topics": [
                    "Step 1: Complete a 6-Month Corporate Internship.",
                    "Step 2: Dedicated MBA/CAT Preparation.",
                    "Step 3: Lead Leadership & Fest Management activities.",
                    "Step 4: Analyze real-world Business Case Studies.",
                    "Step 5: Apply for Pre-Placement Offers (PPO) seriously."
                ],
                "resources": {
                    "Internshala": "https://internshala.com",
                    "CAT Prep - IMS": "https://www.imsindia.com",
                    "LinkedIn Jobs": "https://www.linkedin.com/jobs/"
                }
            }
        }
    else:
        return {
            "🟡 Year 1: Academic Foundations": {
                "summary": "Build top grades and explore your area of interest.",
                "topics": [
                    "Step 1: Master core academic subjects for top grades.",
                    "Step 2: Join relevant college clubs & local communities.",
                    "Step 3: Attend seminars and tech workshops.",
                    "Step 4: Build strong relationships with mentors & professors.",
                    "Step 5: Start a blog or portfolio of your learnings."
                ],
                "resources": {"YouTube - Study Tips": "https://www.youtube.com/results?search_query=study+tips+university", "Coursera - Free Courses": "https://www.coursera.org"}
            },
            "🟠 Year 2: Exploration": {
                "summary": "Identify your specialization and get hands-on experience.",
                "topics": ["Explore sub-disciplines", "Attend industry events", "Start a small research project", "Build an online presence (LinkedIn)"],
                "resources": {"LinkedIn Learning": "https://www.linkedin.com/learning/", "Coursera": "https://www.coursera.org"}
            },
            "🔴 Year 3: Portfolio & Internship": {
                "summary": "Secure an internship and build your portfolio.",
                "topics": ["Internship applications", "Portfolio / thesis work", "Networking events", "Research publications"],
                "resources": {"Internshala": "https://internshala.com", "LinkedIn Jobs": "https://www.linkedin.com/jobs/"}
            },
            "🟢 Year 4: Career Launch": {
                "summary": "Complete research, polish your resume and begin career applications.",
                "topics": ["Final thesis / project", "Campus placement drives", "Off-campus applications", "Interview preparation"],
                "resources": {"Naukri.com": "https://www.naukri.com", "LinkedIn Jobs": "https://www.linkedin.com/jobs/"}
            }
        }
