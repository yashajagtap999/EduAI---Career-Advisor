import random
import os
import google.generativeai as genai
from backend.api.recommender import generate_roadmap
from dotenv import load_dotenv

# Load environment variables from absolute path
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(base_dir, ".env")
load_dotenv(env_path)

def _get_fallback_response(user_input, user_role, user_skills):
    input_lower = user_input.lower()
    
    # ── 1. PLATFORM FEATURES & ABOUT EDUAI ──
    if any(k in input_lower for k in ["features", "website", "what is eduai", "platform", "how to use", "what can you do"]):
        return (
            "Welcome to **EduAI**! We are an all-in-one AI career guide designed to help students and graduates step into their dream roles. Our core features include:\n\n"
            "1. **📄 AI Resume X-Ray**: Upload your CV to check your ATS compatibility score, find skill gaps, and download a customized ATS-optimized resume.\n"
            "2. **🎓 College Finder & Blueprints**: Search top universities by study field and city, and download structured 4-year degree roadmaps.\n"
            "3. **📊 Application Analytics**: View real-world job demand forecasts (2026-2030) and global career readiness stats.\n"
            "4. **🧠 AI Career Mentor**: 24/7 personalized coaching for interview preparation, skill development, and roadmaps.\n\n"
            "Which of these features would you like to explore first?"
        )

    # 📄 Resume X-Ray / ATS Specifics
    if any(k in input_lower for k in ["resume xray", "ats", "resume help", "cv", "score", "scan"]):
        return (
            "Our **📄 AI Resume X-Ray** feature uses a multi-dimensional ATS scoring system. It evaluates your resume on four key parameters:\n\n"
            "1. **Skill Match (60%)**: Relevancy of keywords to the target role.\n"
            "2. **Section Completeness (20%)**: Verifying headers like Education, Experience, and Skills.\n"
            "3. **Contact Details & Links (10%)**: Checking for Email, Phone, and professional profiles (GitHub/LinkedIn).\n"
            "4. **Writing Quality (10%)**: Reviewing word count and use of active verbs.\n\n"
            "To use it, select **Resume X-Ray** in the sidebar, upload your PDF, and get your instant score + gap analysis!"
        )

    # 🎓 College Finder Feature
    if any(k in input_lower for k in ["college finder", "find colleges", "university", "12th"]):
        return (
            "The **🎓 College Finder** is built to help school-leavers and college students choose the best pathway. "
            "You can select your field of study (e.g. Data Science, Web Design) and city to discover top institutes. "
            "Additionally, you can view and export a **4-Year Academic Blueprint** that outlines exactly what subjects, tools, and milestones you need to master each semester to be industry-ready. "
            "Give it a try in the sidebar!"
        )

    # 📊 Analytics Feature
    if any(k in input_lower for k in ["analytics", "demand", "market trends", "forecast", "jobs"]):
        return (
            "Our **📊 Application Analytics** page provides deep insights into the global tech and business markets. "
            "It includes a **Future Skills Demand Forecast (2026-2030)** detailing emerging fields like AI/ML, Cloud Computing, Cybersecurity, and Data Engineering. "
            "It also showcases global metrics like the total scans performed and the average career preparedness score. "
            "Check it out via the **Analytics** link in the sidebar to align your learning with market demands."
        )

    # ── 2. GRADUATE & STUDENT CAREER FAQs ──
    
    # Internships & Placements
    if any(k in input_lower for k in ["internship", "placement", "campus placement", "off campus", "get a job"]):
        return (
            "Landing an internship or preparing for placements is the top goal for college students! Here is the action plan:\n\n"
            "1. **Start Early**: Apply for internships 3-6 months before the season starts. Keep tracking dates.\n"
            "2. **Tailor Your Resume**: A generic resume gets filtered. Use our **Resume X-Ray** to customize your resume for the target job role.\n"
            "3. **Build Core Projects**: Showcase 2-3 high-quality GitHub projects where you solved a real problem, rather than copying standard tutorials.\n"
            "4. **Practice Coding & Theory**: Focus on Data Structures (DSA) and fundamental computer science concepts (DBMS, OS).\n"
            "5. **LinkedIn Networking**: Connect with alumni at your target companies and ask for advice or referral opportunities.\n\n"
            "Would you like me to generate a 6-month roadmap for your specific career role?"
        )

    # Interview Prep & DSA
    if any(k in input_lower for k in ["interview", "dsa", "coding practice", "leetcode", "crack"]):
        return (
            "Technical interviews usually focus on problem-solving. Here is how to prepare:\n\n"
            "- **Data Structures & Algorithms (DSA)**: Focus on Arrays, HashMaps, Two Pointers, Trees, Graphs, and Dynamic Programming. Use platforms like LeetCode or GeeksforGeeks to practice.\n"
            "- **System Design**: For software engineering roles, understand core concepts like APIs, databases (SQL vs NoSQL), scaling, and caching.\n"
            "- **Behavioral Round**: Prepare stories using the **STAR Method** (Situation, Task, Action, Result) to talk about teamwork, challenges, and leader skills.\n\n"
            "Let me know if you want to practice mock interview questions for your role!"
        )

    # Resume Projects
    if any(k in input_lower for k in ["project", "portfolio", "build", "github project"]):
        return (
            "To stand out to recruiters, skip basic tutorial copies (like simple calculators) and build:\n\n"
            "1. **Real-world Solutions**: Solve a real problem (e.g. an automated expense parser, a local pet shelter dashboard).\n"
            "2. **Production-grade Apps**: Deploy your app online (using Vercel, Netlify, or Render), use databases (PostgreSQL, MongoDB), and add authentication.\n"
            "3. **Open Source Contributions**: Contributed to a public repository on GitHub? Mention it! It proves you know how to read and write team-based code.\n\n"
            "Make sure to describe your projects on your resume with action verbs and quantifiable results (e.g. *Built full-stack React portal that reduced data entry time by 30%*)."
        )

    # CGPA vs Skills
    if any(k in input_lower for k in ["cgpa", "gpa", "low grades", "marks", "grades"]):
        return (
            "It's a common worry among graduates. Here is the reality:\n\n"
            "- **In-Campus Placements**: Some large companies set a strict CGPA cutoff (usually 7.0 or 7.5 out of 10) to filter candidates quickly. If you are participating in campus placements, try to stay above this limit.\n"
            "- **Off-Campus Placements**: Skills, personal projects, open-source work, and referrals matter **much** more than CGPA. Most startups and modern tech firms don't even ask for your college GPA.\n\n"
            "**Action Plan if your CGPA is low**:\n"
            "1. Build a stellar portfolio of unique, hosted projects.\n"
            "2. Get active in developer communities and contribute to open source.\n"
            "3. Connect with engineers on LinkedIn and ask for referrals. A strong referral bypasses the CGPA filter 99% of the time!"
        )

    # Career Transition (Non-CS to CS)
    if any(k in input_lower for k in ["switch", "transition", "non-cs", "non tech", "another field"]):
        return (
            "Transitioning into tech from a different background is highly achievable if you focus on your portfolio:\n\n"
            "1. **Pick a Clear Goal**: Don't try to learn everything. Start with Frontend Web Development (React/Tailwind) or Data Analytics (Python/SQL).\n"
            "2. **Build Unique Projects**: Since you don't have a CS degree, your projects *are* your credential. Ensure they are fully functional, hosted, and well-documented.\n"
            "3. **Leverage Transferable Skills**: Highlight past skills like project management, analytical thinking, or domain knowledge (e.g., finance background is highly valued in FinTech).\n\n"
            "Would you like me to generate a learning path to guide your transition?"
        )

    # ── 3. STANDARD ROADMAPS & SKILLS ──
    if any(k in input_lower for k in ["roadmap", "6-month", "plan", "strategy", "path"]):
        if not user_role or user_role == "General / Entry-Level":
            return (
                "To give you a precise roadmap, I'd suggest scanning your resume first in **Resume X-Ray**! "
                "But generally, a solid 6-month career readiness plan involves: \n\n"
                "1. **Month 1-2**: Master core technical skills and theoretical fundamentals.\n"
                "2. **Month 3-4**: Build 2 robust, unique portfolio projects and publish them on GitHub.\n"
                "3. **Month 5-6**: Optimize your LinkedIn/Resume, practice coding questions, and start networking for referrals."
            )
        
        roadmap = generate_roadmap(user_role)
        roadmap_str = f"Here is your customized 6-month roadmap for **{user_role}**:\n\n"
        for month, content in roadmap.items():
            roadmap_str += f"### {month}\n{content}\n\n"
        return roadmap_str

    if any(k in input_lower for k in ["skill", "learn", "improve", "better"]):
        if user_skills:
            return f"You already have a solid foundation in **{', '.join(user_skills[:3])}**. To reach the next level, I'd suggest mastering related advanced frameworks or tools used in the industry. For a custom gap analysis, click **Resume X-Ray** in the sidebar!"
        return "I recommend uploading your resume in **Resume X-Ray** so I can see your current skill set and suggest exactly what's missing for your target role."

    if input_lower in ["yes", "yeah", "sure", "absolutely", "okay"]:
        if user_role:
            return _get_fallback_response("roadmap", user_role, user_skills)
        return "I'd love to! Please tell me your target job role or upload your resume so I can personalize it for you."

    # Default Responses
    defaults = [
        "I'm here to help you navigate your career journey. Do you have questions about resume building, interview prep, finding the right college, or platform features like Resume X-Ray?",
        "That's an interesting perspective. Could you tell me more about your specific career goals?",
        f"Based on your profile as a **{user_role or 'student'}**, focusing on building a strong network on LinkedIn can be as important as learning new skills. Have you optimized your profile yet?",
        "I'm analyzing current market trends... it looks like there's a high demand for specialized skills right now. What's the one skill you're most excited to learn next?"
    ]
    return random.choice(defaults)


def get_mentor_response(user_input, user_role, user_skills, resume_text=None, chat_history=None):
    """
    Sophisticated career mentor engine responding to platform features and student/graduate FAQs.
    Yields chunks of text for real-time streaming using Gemini API.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Yield the fallback response if API key is not present
        yield _get_fallback_response(user_input, user_role, user_skills)
        return

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # 1. Gemini-based Intent Classification
        classification_prompt = f"""
Analyze the user's career mentor query and classify it into one of these 5 intents:
1. "career_guidance" (asking for career advice, roles, choices, options)
2. "resume_review" (asking to review resume, ATS score, resume check, resume advice)
3. "skill_gap" (asking what to learn next, missing skills, how to become a certain role)
4. "roadmap" (asking for roadmaps, learning path, plan for a role)
5. "projects" (asking for project recommendations, portfolio projects)

Query: "{user_input}"

Return ONLY the intent string: "career_guidance", "resume_review", "skill_gap", "roadmap", or "projects". No other text.
"""
        try:
            intent_res = model.generate_content(classification_prompt)
            intent = intent_res.text.strip().lower()
        except Exception:
            intent = "career_guidance" # Default fallback intent classification

        # Map to valid intent strings
        valid_intents = ["career_guidance", "resume_review", "skill_gap", "roadmap", "projects"]
        matched_intent = "career_guidance"
        for v in valid_intents:
            if v in intent:
                matched_intent = v
                break

        # 2. Build Chat History Context
        history_context = ""
        if chat_history:
            history_context = "\nRecent Conversation History:\n"
            for role, msg in chat_history[-6:]: # Include last 6 messages for context
                speaker = "User" if role == "user" else "EduAI Mentor"
                history_context += f"{speaker}: {msg}\n"

        # 3. Handle intents & response requirements
        system_prompt = "You are EduAI, an expert AI Career Mentor.\n\n"
        
        system_prompt += """Your task is to provide personalized, highly actionable career advice.
You MUST use this EXACT structure for every response, using the provided emojis:

🎯 Current Situation
[1-2 brief sentences summarizing where the user is at]

💼 Recommended Roles
[Bullet points of 1-3 best matching roles]

📚 Skills To Learn
[Bullet points of top 2-3 most critical skills missing or needing improvement]

🚀 Action Plan
[Numbered list of 3 direct, immediate actions to take]

👉 Next Step
[A single specific question asking what they want to do next]

"""

        # Append overall constraints & rules
        system_prompt += """
General Rules:
- Keep answers practical, personalized and highly actionable.
- MAXIMUM RESPONSE LENGTH: 250 words. Be extremely concise. Do NOT write long paragraphs.
- DO NOT use markdown headers (###), just the emojis as shown above.
- Never say: 'Resume not provided' or similar unless the user explicitly requested resume review or ATS analysis.

Student Profile Context:
- Target Role: {user_role}
- Extracted/Detected Skills: {', '.join(user_skills) if user_skills else 'None detected yet'}
- Resume Text: {resume_text if resume_text else 'Not provided'}
"""

        # Formulate full prompt
        prompt = f"""{system_prompt}
{history_context}
User Query: {user_input}

Please generate the structured response now. Ensure the output is concise, structured under the requested sections, and matches the target style (300-400 words).
"""

        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
        return
    except Exception as e:
        print(f"Gemini API Error: {e}")
        yield _get_fallback_response(user_input, user_role, user_skills)

