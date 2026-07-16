# Course recommendations (you can expand later)
COURSES = {
    "python": "https://www.youtube.com/watch?v=rfscVS0vtbw",
    "machine learning": "https://www.youtube.com/watch?v=Gv9_4yMHFhI",
    "deep learning": "https://www.youtube.com/watch?v=aircAruvnKk",
    "sql": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
    "html": "https://www.youtube.com/watch?v=qz0aGYrrlhU",
    "css": "https://www.youtube.com/watch?v=1Rs2ND1ryYc",
    "javascript": "https://www.youtube.com/watch?v=PkZNo7MFNFg",
    "power bi": "https://www.youtube.com/watch?v=AGrl-H87pRU",
    "data analysis": "https://www.youtube.com/watch?v=r-uOLxNrNk8"
}


# Recommend courses based on missing skills dynamically
def recommend_courses(missing_skills):
    recommendations = {}

    for skill in missing_skills:
        if skill in COURSES:
            recommendations[skill] = COURSES[skill]
        else:
            # Dynamically generate search link if not in hardcoded dict
            search_query = skill.replace(" ", "+")
            recommendations[skill] = f"https://www.youtube.com/results?search_query={search_query}+course"

    return recommendations

#  Generate deep study month-wise roadmap
def generate_roadmap(job_role):
    
    def get_link(topic):
        # Create a dynamic search query link pointing to YouTube
        query = topic.replace(" ", "+")
        return (
            f"<br><a href='https://www.youtube.com/results?search_query={query}+tutorial+course' "
            f"target='_blank' style='display: inline-flex; align-items: center; gap: 6px; "
            f"background: linear-gradient(135deg, var(--primary-blue), var(--accent-purple)); color: #ffffff; "
            f"text-decoration: none; padding: 6px 14px; border-radius: 50px; "
            f"font-size: 12px; font-weight: bold; margin-top: 8px; margin-bottom: 4px; "
            f"box-shadow: 0 4px 12px rgba(139, 92, 246, 0.15); transition: all 0.2s ease-in-out;'>"
            f"🎥 Study Guide & Video Courses</a>"
        )

    roadmap = {
        "Data Scientist": {
            "Month 1: Native Python & Mathematics": f"Master native Python structures and deeply understand Linear Algebra and Statistics.{get_link('python statistics data science')}",
            "Month 2: Data Handling & Visualization": f"Learn Pandas, NumPy, Matplotlib and Seaborn for massive data wrangling.{get_link('pandas numpy data analysis')}",
            "Month 3: Core ML Algorithms": f"Study Scikit-Learn: Regression, Decision Trees, and Random Forests.{get_link('scikit learn random forest')}",
            "Month 4: Deep Learning Foundations": f"Dive into Neural Networks using TensorFlow or PyTorch.{get_link('tensorflow neural networks')}",
            "Month 5: NLP & Computer Vision": f"Analyze text using NLP techniques and explore computer vision frameworks.{get_link('natural language processing')}",
            "Month 6: Cloud Deployment & ML Ops": f"Deploy models effectively utilizing Docker and AWS/GCP.{get_link('mlops model deployment')}"
        },
        "Java Developer": {
            "Month 1: Core Java Programming": f"Deep dive into OOP concepts, multithreading, and standard libraries.{get_link('core java programming')}",
            "Month 2: Data Structures & Algorithms": f"Master Collections framework and algorithmic problem solving.{get_link('java data structures')}",
            "Month 3: Advanced Frameworks": f"Learn Spring Boot and Hibernate natively.{get_link('spring boot hibernate')}",
            "Month 4: Relational Databases": f"Implement JDBC and optimize complex SQL queries.{get_link('java database connectivity')}",
            "Month 5: Web Services": f"Build enterprise-scale RESTful APIs and microservices.{get_link('java rest api microservices')}",
            "Month 6: DevOps Integration": f"Learn Jenkins, Docker, and deployment strategies.{get_link('java ci cd docker')}"
        },
        "Web Developer": {
            "Month 1: Frontend Holy Trinity": f"Master HTML5, CSS3, and JavaScript ES6+.{get_link('html css javascript ES6')}",
            "Month 2: Modern Frontend Frameworks": f"Deep study into React or Vue, including state management.{get_link('react js frontend')}",
            "Month 3: UI/UX & Responsive Design": f"Learn TailwindCSS, Bootstrap, and mobile-first principles.{get_link('tailwind responsive design')}",
            "Month 4: Backend Integration": f"Understand APIs, Node.js basics, and asynchronous JavaScript.{get_link('javascript fetch api node')}",
            "Month 5: Database Basics": f"Learn MongoDB or Firebase for rapid data storage.{get_link('mongodb web dev')}",
            "Month 6: Hosting & Version Control": f"Deploy to Vercel/Netlify and master advanced Git commands.{get_link('git github deployment')}"
        }
    }
    
    # Generic, intelligent fallback for newly added non-tech or diverse Kaggle roles
    default_roadmap = {
        "Month 1: Core Fundamentals": f"Master the absolute core competencies required for the {job_role} industry.{get_link(job_role + ' core fundamentals')}",
        "Month 2: Essential Tooling": f"Adopt the most dominant software frameworks currently used by {job_role} professionals.{get_link(job_role + ' tools software')}",
        "Month 3: Advanced Concepts": f"Dive into rigorous, complex topics unique to {job_role} specialization.{get_link(job_role + ' advanced concepts')}",
        "Month 4: Portfolio Building": f"Start compiling a publicly available, high-quality portfolio of industry case studies.{get_link(job_role + ' portfolio projects')}",
        "Month 5: Certification & Compliance": f"Secure vital certifications and licenses to validate your expertise.{get_link(job_role + ' certifications')}",
        "Month 6: Interview Preparation": f"Rigorous refinement of behavioral and technical interviews.{get_link(job_role + ' interview preparation')}"
    }

    return roadmap.get(job_role, default_roadmap)


#  Generate step-by-step roadmap for a specific missing skill
def generate_skill_roadmap(skill):
    skill_lower = skill.lower()
    
    # Dynamic search links
    yt_link = f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+full+course"
    gfg_link = f"https://www.google.com/search?q={skill.replace(' ', '+')}+geeksforgeeks+tutorial"
    official_link = f"https://www.google.com/search?q={skill.replace(' ', '+')}+official+documentation"

    # Specific roadmaps for common skills
    skill_plans = {
        "python": [
            "Step 1: Install Python and VS Code. Run your first 'Hello World'.",
            "Step 2: Master Basic Syntax: Variables, Loops, and Functions.",
            "Step 3: Learn Core Data Structures: Lists, Dictionaries, Sets.",
            "Step 4: Explore OOP: Classes, Objects, and Inheritance.",
            "Step 5: Build a simple project: Calculator or Scraping tool."
        ],
        "machine learning": [
            "Step 1: Master Mathematics: Linear Algebra, Calculus, and Statistics.",
            "Step 2: Learn Data handling with Pandas and NumPy.",
            "Step 3: Study Supervised Learning: Regression & Classification.",
            "Step 4: Understand Unsupervised Learning: Clustering & PCA.",
            "Step 5: Practice projects on real datasets from Kaggle."
        ],
        "sql": [
            "Step 1: Set up MySQL or PostgreSQL environment.",
            "Step 2: Learn Basic Queries: SELECT, WHERE, ORDER BY.",
            "Step 3: Master Joins: INNER, LEFT, RIGHT, FULL OUTER.",
            "Step 4: Understand Aggregations: GROUP BY, HAVING, COUNT.",
            "Step 5: Dive into Subqueries and Window Functions."
        ],
        "react": [
            "Step 1: Brush up on Modern JavaScript (ES6+ features).",
            "Step 2: Understand JSX, Components, and Props.",
            "Step 3: Master State Management with useState and useEffect.",
            "Step 4: Learn React Router for multi-page navigation.",
            "Step 5: Build a Todo App or a Weather Dashboard."
        ]
    }

    # Default plan if skill not in dict
    default_plan = [
        f"Step 1: Explore the fundamentals of {skill} through introductory tutorials.",
        f"Step 2: Set up a local development environment specifically for {skill}.",
        f"Step 3: Build 3 minor projects to apply theoretical knowledge.",
        f"Step 4: Study advanced optimization and best practices for {skill}.",
        f"Step 5: Showcase your work on GitHub to validate your expertise."
    ]

    plan = skill_plans.get(skill_lower, default_plan)
    
    return {
        "plan": plan,
        "links": {
            "🎥 YouTube Course": yt_link,
            "📚 GFG Tutorial": gfg_link,
            "🌐 Official Docs": official_link
        }
    }