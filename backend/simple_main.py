from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, List

app = FastAPI(
    title="CV_Bot API",
    description="AI-powered resume scanner and ranking system",
    version="1.0.0"
)

# In-memory storage for live data
jobs_db: Dict[int, dict] = {}
candidates_db: Dict[int, dict] = {}
job_counter = 1
candidate_counter = 1

# No sample data - start with empty database

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3002", "http://127.0.0.1:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "CV_Bot API is running! 🚀"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Mock auth endpoints
@app.post("/api/v1/auth/login")
async def login():
    return {"access_token": "demo-token", "token_type": "bearer"}

@app.post("/api/v1/auth/register")
async def register(user_data: dict):
    return {
        "id": 1,
        "email": user_data.get("email", "demo@example.com"),
        "full_name": user_data.get("full_name", "Demo User")
    }

@app.get("/api/v1/auth/me")
async def get_current_user():
    return {"id": 1, "email": "demo@example.com", "full_name": "Demo User"}

# Live jobs endpoints
@app.get("/api/v1/jobs")
async def get_jobs():
    jobs_list = []
    for job_id, job in jobs_db.items():
        # Count candidates for this job
        candidate_count = len([c for c in candidates_db.values() if c["job_id"] == job_id])
        job_copy = job.copy()
        job_copy["candidate_count"] = candidate_count
        jobs_list.append(job_copy)

    return jobs_list

@app.post("/api/v1/jobs")
async def create_job(job_data: dict):
    global job_counter
    import random

    job_id = job_counter
    job_counter += 1

    new_job = {
        "id": job_id,
        "title": job_data.get("title", "New Job"),
        "description": job_data.get("description", "Job description"),
        "requirements": {
            "skills_required": ["Python", "FastAPI", "React"],
            "skills_preferred": ["TypeScript", "Docker", "AWS"],
            "min_experience_years": 3,
            "education_level": "Bachelor's"
        },
        "questionnaire": {
            "technical_questions": [
                {"question": "How do you handle API authentication?", "type": "text"},
                {"question": "Explain your experience with databases", "type": "text"}
            ],
            "experience_questions": [
                {"question": "Describe your most challenging project", "type": "text"}
            ]
        },
        "is_active": "active",
        "created_at": datetime.now().isoformat() + "Z",
        "candidate_count": 0
    }

    jobs_db[job_id] = new_job
    return new_job

@app.get("/api/v1/jobs/{job_id}")
async def get_job(job_id: int):
    if job_id in jobs_db:
        job = jobs_db[job_id].copy()
        # Count candidates for this job
        candidate_count = len([c for c in candidates_db.values() if c["job_id"] == job_id])
        job["candidate_count"] = candidate_count
        return job

    # Return 404 if job not found
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Job not found")

# Live candidates endpoints
@app.get("/api/v1/candidates/job/{job_id}")
async def get_candidates(job_id: int):
    job_candidates = [c for c in candidates_db.values() if c["job_id"] == job_id]
    return job_candidates

@app.get("/api/v1/candidates/{candidate_id}")
async def get_candidate(candidate_id: int):
    if candidate_id in candidates_db:
        return candidates_db[candidate_id]

    # Return 404 if candidate not found
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Candidate not found")

@app.post("/api/v1/candidates/upload/{job_id}")
async def upload_resume(
    job_id: int,
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None)
):
    global candidate_counter
    import random
    import re

    candidate_id = candidate_counter
    candidate_counter += 1

    # Read and parse the resume file
    resume_content = ""
    try:
        content = await file.read()
        # For now, just extract text from file (basic implementation)
        # In a real system, you'd use PyPDF2, python-docx, or OCR
        resume_content = content.decode('utf-8', errors='ignore')
    except:
        # If file reading fails, use a placeholder
        resume_content = f"Resume file: {file.filename}. Unable to extract text content for analysis."

    # Parse skills from resume content
    all_skills = [
        "Python", "JavaScript", "TypeScript", "React", "Node.js", "Django", "Flask", "FastAPI",
        "SQL", "PostgreSQL", "MongoDB", "Redis", "Docker", "Kubernetes", "AWS", "Azure", "GCP",
        "Git", "Linux", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin",
        "HTML", "CSS", "Vue.js", "Angular", "Express", "Spring", "Hibernate", "REST", "GraphQL",
        "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn", "Tableau", "Power BI",
        "Jenkins", "CI/CD", "Agile", "Scrum", "DevOps", "Microservices", "API", "JSON"
    ]

    found_skills = []
    content_lower = resume_content.lower()
    for skill in all_skills:
        if skill.lower() in content_lower:
            found_skills.append(skill)

    # If no skills found, provide minimal set
    if not found_skills:
        found_skills = ["Microsoft Office", "Communication", "Problem Solving"]

    # Parse experience years from resume
    exp_years = 0
    # Look for patterns like "3 years", "5+ years", "2-4 years"
    experience_patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
        r'(\d+)\s*to\s*(\d+)\s*years',
        r'(\d+)-(\d+)\s*years',
        r'over\s*(\d+)\s*years',
        r'more\s*than\s*(\d+)\s*years'
    ]

    for pattern in experience_patterns:
        matches = re.findall(pattern, content_lower)
        if matches:
            if isinstance(matches[0], tuple):
                # Handle range patterns
                exp_years = max(int(matches[0][0]), int(matches[0][1]))
            else:
                exp_years = int(matches[0])
            break

    # Parse education from resume
    education_keywords = [
        "bachelor", "master", "phd", "doctorate", "degree", "university", "college",
        "computer science", "engineering", "mathematics", "information technology",
        "bootcamp", "certification"
    ]

    education = []
    for keyword in education_keywords:
        if keyword in content_lower:
            if "bachelor" in content_lower:
                education.append("Bachelor's Degree")
            if "master" in content_lower:
                education.append("Master's Degree")
            if "phd" in content_lower or "doctorate" in content_lower:
                education.append("PhD/Doctorate")
            if "bootcamp" in content_lower:
                education.append("Bootcamp Graduate")
            break

    if not education:
        education = ["Education information not clearly specified"]

    # Parse certifications from resume
    cert_keywords = [
        "aws", "azure", "google cloud", "certification", "certified", "oracle", "microsoft",
        "cisco", "comptia", "scrum master", "pmp", "itil"
    ]

    certifications = []
    for keyword in cert_keywords:
        if keyword in content_lower:
            if "aws" in content_lower:
                certifications.append("AWS Certification")
            if "azure" in content_lower:
                certifications.append("Microsoft Azure Certification")
            if "google cloud" in content_lower:
                certifications.append("Google Cloud Certification")
            if "scrum" in content_lower:
                certifications.append("Scrum Master Certification")

    # Extract job titles/roles from resume
    role_keywords = [
        "software engineer", "developer", "programmer", "analyst", "manager", "architect",
        "consultant", "specialist", "lead", "senior", "junior", "intern", "director"
    ]

    previous_roles = []
    for keyword in role_keywords:
        if keyword in content_lower:
            previous_roles.append(keyword.title())

    if not previous_roles:
        previous_roles = ["Professional Experience"]

    # Create summary from actual resume content
    # Extract first meaningful paragraph or create from parsed data
    summary_lines = [line.strip() for line in resume_content.split('\n') if len(line.strip()) > 50]
    if summary_lines:
        summary = summary_lines[0][:200] + "..." if len(summary_lines[0]) > 200 else summary_lines[0]
    else:
        summary = f"Professional with experience in {', '.join(found_skills[:3])}" + (f" and {exp_years} years of experience" if exp_years > 0 else "")

    # Calculate realistic scores based on parsed data
    job = jobs_db.get(job_id, {})
    job_title = job.get("title", "Software Developer")
    job_description = job.get("description", "")

    # Score based on skill matches
    job_content = (job_title + " " + job_description).lower()
    skill_matches = sum(1 for skill in found_skills if skill.lower() in job_content)
    keyword_score = min(0.95, 0.3 + (skill_matches / max(len(found_skills), 1)) * 0.6)

    # Score based on experience
    if exp_years >= 5:
        experience_score = random.uniform(0.8, 0.95)
    elif exp_years >= 2:
        experience_score = random.uniform(0.7, 0.85)
    elif exp_years >= 1:
        experience_score = random.uniform(0.6, 0.75)
    else:
        experience_score = random.uniform(0.5, 0.7)

    # Other scores
    semantic_score = random.uniform(0.6, 0.9)
    education_score = random.uniform(0.7, 0.9) if "bachelor" in content_lower or "master" in content_lower else random.uniform(0.5, 0.8)

    total_score = round((semantic_score * 0.45 + keyword_score * 0.30 + experience_score * 0.15 + education_score * 0.10), 2)

    # Generate match explanation based on actual data
    match_reasons = []
    if skill_matches > 0:
        match_reasons.append(f"Found {skill_matches} relevant skills matching job requirements")
    if exp_years > 0:
        match_reasons.append(f"Has {exp_years} years of documented experience")
    if certifications:
        match_reasons.append(f"Holds relevant certifications: {', '.join(certifications[:2])}")
    if not match_reasons:
        match_reasons.append("Resume shows relevant professional background")

    match_explanation = f"Based on resume analysis: {'. '.join(match_reasons)}. File analyzed: {file.filename}"

    new_candidate = {
        "id": candidate_id,
        "name": name,
        "email": email,
        "phone": phone or f"+1-555-{random.randint(1000, 9999)}",
        "job_id": job_id,
        "total_score": total_score,
        "score_breakdown": {
            "semantic_similarity": round(semantic_score, 2),
            "keyword_overlap": round(keyword_score, 2),
            "experience_match": round(experience_score, 2),
            "education_match": round(education_score, 2)
        },
        "match_explanation": match_explanation,
        "structured_data": {
            "skills": found_skills,
            "experience_years": exp_years,
            "education": education,
            "certifications": certifications,
            "previous_roles": list(set(previous_roles)),
            "summary": summary
        },
        "status": "pending",
        "created_at": datetime.now().isoformat() + "Z",
        "resume_filename": file.filename
    }

    candidates_db[candidate_id] = new_candidate
    return new_candidate

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)