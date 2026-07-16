import os
import requests
from dotenv import load_dotenv

# Get workspace absolute path to .env dynamically relative to file location
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=dotenv_path)

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

def search_adzuna_internships(skills: list, cgpa: float, location: str, branch: str):
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        return {"error": "Adzuna API credentials not configured in .env"}

    # Define country code based on location preference keywords
    country_code = "in"
    loc_lower = location.lower() if location else ""
    if any(k in loc_lower for k in ["us", "usa", "york", "california", "london", "uk", "gb", "england"]):
        country_code = "us" if "us" in loc_lower or "york" in loc_lower or "california" in loc_lower else "gb"

    # Build progressive query attempts to prevent search term overloading
    query_attempts = []
    
    # Attempt 1: Top skill
    if skills:
        query_attempts.append(f"internship {skills[0]}")
        if len(skills) > 1:
            query_attempts.append(f"internship {skills[0]} {skills[1]}")
            
    # Attempt 2: Branch
    if branch:
        # Simplify branch names for better search matching (e.g. "Computer Science / CSE" -> "Computer Science")
        clean_branch = branch.split("/")[0].split("&")[0].strip()
        query_attempts.append(f"internship {clean_branch}")
        
    # Attempt 3: General fallbacks
    query_attempts.append("internship engineering")
    query_attempts.append("internship")

    url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"
    results = []
    
    # Try query attempts progressively until we find results
    for q in query_attempts:
        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "results_per_page": 15,
            "what": q,
            "content-type": "application/json"
        }
        
        if location and location.lower() != "remote":
            params["where"] = location
        elif location and location.lower() == "remote":
            params["what"] = f"{q} remote"
            
        try:
            response = requests.get(url, params=params, timeout=8)
            
            # Fallback to US if India search fails due to region restrictions or rate limit codes
            if response.status_code != 200 and country_code == "in":
                fallback_url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
                response = requests.get(fallback_url, params=params, timeout=8)
                
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if results:
                    break
        except Exception as e:
            print(f"Error querying Adzuna with '{q}': {e}")
            continue

    # Format the results
    formatted_results = []
    for job in results:
        # Compute mock CGPA requirements and rating
        if cgpa >= 8.5:
            eligibility = "Highly Recommended ⭐⭐⭐⭐⭐"
            match_class = "badge-green"
        elif cgpa >= 7.0:
            eligibility = "Eligible ⭐⭐⭐⭐"
            match_class = "badge-green"
        else:
            eligibility = "Meets Minimum Criteria ⭐⭐⭐"
            match_class = "badge-orange"
            
        formatted_results.append({
            "id": job.get("id"),
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name", "N/A"),
            "location": job.get("location", {}).get("display_name", "N/A"),
            "description": job.get("description", ""),
            "url": job.get("redirect_url"),
            "eligibility": eligibility,
            "match_class": match_class,
            "salary": job.get("salary_min", "Competitive")
        })
        
    return {"results": formatted_results}
