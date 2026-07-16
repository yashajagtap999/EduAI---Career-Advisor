# 🚀 EduAI: AI-Powered Career Advisor

## 📌 Project Overview
**EduAI** is a comprehensive, state-of-the-art SaaS platform designed to guide students and professionals through their career journeys. Leveraging Artificial Intelligence, it provides personalized mentorship, resume analysis, college recommendations, and data-driven career insights.

---

## ✨ Key Features

### 1. 🧠 AI Career Mentor
A 24/7 intelligent consultant that provides:
- Instant answers to career and interview questions.
- Personalized skill mapping based on your profile.
- Real-time interaction with a simulated typing effect for a premium feel.

### 2. 📄 Resume X-Ray (ATS Analysis)
A powerful tool to optimize your professional presence:
- **Deep Scan**: Extracts text and skills from PDF/DOCX resumes.
- **ATS Scoring**: Calculates a preparedness score based on industry standards.
- **Role Prediction**: Uses Machine Learning to predict the best-fit job role for your skill set.
- **Skill Gaps**: Identifies missing skills and provides structured learning roadmaps.

### 3. 🎓 Future-Builder: College Finder
Helps students transition from high school to higher education:
- **Institutional Search**: Find top-tier colleges based on specific fields of study.
- **Geographic Filtering**: Filter institutions by city/region.
- **4-Year Blueprint**: Generates a detailed academic roadmap for the chosen degree.

### 4. 📊 Career Analytics & Forecasting
Data-driven insights into the job market:
- **Demand Forecast**: Visualizes skill demand trends from 2026 to 2030 using interactive charts.
- **Global Benchmarks**: Compares your preparedness against global averages.

### 5. 🛡️ Secure Authentication
A robust user system for personalizing the experience:
- Secure Login and Sign-up functionality.
- Persistent storage of user progress and scan history.

---

## 🛠️ Technical Stack

| Category | Technology |
| :--- | :--- |
| **Frontend** | [Streamlit](https://streamlit.io/) |
| **Styling** | Vanilla CSS (Glassmorphism & Modern UI) |
| **Backend** | Python |
| **Database** | SQLite |
| **Machine Learning** | Scikit-learn (Job Role Prediction) |
| **NLP** | Regex-based Skill Extraction |
| **Visualization** | Plotly & Pandas |
| **File Processing** | PDF/DOCX Parsing |

---

## 📂 Project Structure

```text
AI Job Advisor/
├── app.py                # Main Streamlit application entry point
├── style.css             # Custom modern UI design system
├── eduai_users.db        # SQLite database for user data
├── hero.png              # Landing page visual asset
├── models/               # Machine Learning assets
│   ├── job_model.pkl     # Pre-trained classification model
│   ├── job_predictor.py  # Prediction logic
│   └── vectorizer.pkl    # Text vectorization model
├── utils/                # Modular logic components
│   ├── analyzer.py       # Resume scoring & gap analysis
│   ├── database.py       # DB operations (Auth, Logs)
│   ├── mentor_engine.py  # AI Mentor conversational logic
│   ├── student_advisor.py# College & Roadmap data
│   └── export.py         # PDF generation & export
└── train_model.ipynb     # Model training research
```

---

## 🚀 How It Works

1.  **Onboarding**: User creates an account or logs in via the Auth module.
2.  **Analysis**: The user uploads a resume. The system parses the text, extracts skills, and runs them through the ML model to predict a job role.
3.  **Gap Assessment**: The `analyzer` compares the profile with the predicted role, generates an ATS score, and suggests missing skills.
4.  **Guidance**: The `mentor_engine` provides a conversational interface for further questions, while the `recommender` provides learning resources for missing skills.
5.  **Planning**: For students, the `student_advisor` provides college lists and a year-by-year academic plan.

---

## 🎨 Design Philosophy
EduAI uses a **Premium SaaS Aesthetic**:
- **Gradient Typography**: Sleek, modern headers.
- **Glassmorphism**: Subtle backgrounds and translucent containers.
- **Micro-animations**: Interactive buttons and typing simulations.
- **Responsive Layout**: Designed to work across different screen sizes.

---
*© 2026 EduAI SaaS Platform. Built for the future of careers.*
