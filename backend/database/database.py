import sqlite3
import hashlib
import os
import json
import contextlib

DB_PATH = "eduai_users.db"

@contextlib.contextmanager
def db_session():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with db_session() as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                job_role TEXT NOT NULL,
                month_key TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                UNIQUE(username, job_role, month_key)
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                ats_score INTEGER NOT NULL,
                predicted_role TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        try:
            c.execute("ALTER TABLE scans ADD COLUMN skills TEXT")
        except sqlite3.OperationalError:
            pass
        try:
            c.execute("ALTER TABLE scans ADD COLUMN suggestions TEXT")
        except sqlite3.OperationalError:
            pass
        try:
            c.execute("ALTER TABLE users ADD COLUMN theme TEXT DEFAULT 'Dark'")
        except sqlite3.OperationalError:
            pass
        conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, full_name):
    try:
        with db_session() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
                      (username.lower().strip(), hash_password(password), full_name))
            conn.commit()
            return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists. Please choose a different one."

def login_user(username, password):
    with db_session() as conn:
        c = conn.cursor()
        c.execute("SELECT full_name FROM users WHERE username=? AND password=?",
                  (username.lower().strip(), hash_password(password)))
        row = c.fetchone()
        if row:
            return True, row[0]
        return False, None

def user_exists(username):
    with db_session() as conn:
        c = conn.cursor()
        c.execute("SELECT 1 FROM users WHERE username=?", (username.lower().strip(),))
        row = c.fetchone()
        return row is not None

def save_progress(username, job_role, month_key, completed):
    with db_session() as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO progress (username, job_role, month_key, completed) VALUES (?, ?, ?, ?)
            ON CONFLICT(username, job_role, month_key) DO UPDATE SET completed=excluded.completed
        """, (username, job_role, month_key, 1 if completed else 0))
        conn.commit()

def get_progress(username, job_role):
    with db_session() as conn:
        c = conn.cursor()
        c.execute("SELECT month_key, completed FROM progress WHERE username=? AND job_role=?",
                  (username, job_role))
        rows = c.fetchall()
        return {row[0]: bool(row[1]) for row in rows}

def log_scan(username, score, role, skills=None, suggestions=None):
    with db_session() as conn:
        c = conn.cursor()
        skills_json = json.dumps(skills) if skills else "[]"
        suggestions_json = json.dumps(suggestions) if suggestions else "[]"
        try:
            c.execute("INSERT INTO scans (username, ats_score, predicted_role, skills, suggestions) VALUES (?, ?, ?, ?, ?)",
                      (username.lower().strip(), score, role, skills_json, suggestions_json))
        except sqlite3.OperationalError:
            c.execute("INSERT INTO scans (username, ats_score, predicted_role) VALUES (?, ?, ?)",
                      (username.lower().strip(), score, role))
        conn.commit()

def get_dashboard_data():
    with db_session() as conn:
        c = conn.cursor()
        c.execute("SELECT predicted_role, COUNT(*) FROM scans GROUP BY predicted_role ORDER BY COUNT(*) DESC")
        career_stats = c.fetchall()
        
        c.execute("SELECT ats_score FROM scans")
        scores = [row[0] for row in c.fetchall()]
        
        c.execute("SELECT DATE(timestamp), COUNT(*) FROM scans GROUP BY DATE(timestamp) ORDER BY DATE(timestamp)")
        engagement_stats = c.fetchall()
        
        c.execute("SELECT COUNT(*), AVG(ats_score) FROM scans")
        kpi_row = c.fetchone()
        total_scans = kpi_row[0] if kpi_row[0] else 0
        avg_score = round(kpi_row[1], 1) if kpi_row[1] else 0
        
        return {
            "career_paths": career_stats,
            "scores": scores,
            "engagement": engagement_stats,
            "total_scans": total_scans,
            "avg_score": avg_score
        }

def get_user_scans(username):
    with db_session() as conn:
        c = conn.cursor()
        c.execute("SELECT id, ats_score, predicted_role, timestamp FROM scans WHERE username=? ORDER BY timestamp ASC", (username.lower().strip(),))
        return c.fetchall()

def get_latest_scan(username):
    with db_session() as conn:
        c = conn.cursor()
        c.execute("SELECT ats_score, predicted_role FROM scans WHERE username=? ORDER BY timestamp DESC LIMIT 1", (username.lower().strip(),))
        return c.fetchone()

def get_latest_scan_full(username):
    with db_session() as conn:
        c = conn.cursor()
        try:
            c.execute("SELECT ats_score, predicted_role, skills, suggestions FROM scans WHERE username=? ORDER BY timestamp DESC LIMIT 1", (username.lower().strip(),))
            row = c.fetchone()
            if row:
                skills = json.loads(row[2]) if row[2] else []
                suggestions = json.loads(row[3]) if row[3] else []
                return {
                    "ats_score": row[0],
                    "predicted_role": row[1],
                    "skills": skills,
                    "suggestions": suggestions
                }
        except sqlite3.OperationalError:
            return None
        return None
