from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime


class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class CandidateCreate(CandidateBase):
    job_id: int
    resume_filename: str
    resume_text: str


class CandidateUpdate(BaseModel):
    status: Optional[str] = None  # pending, reviewed, shortlisted, rejected


class CandidateResponse(CandidateBase):
    id: int
    job_id: int
    resume_filename: str
    structured_data: Optional[Dict[str, Any]] = None
    total_score: float
    score_breakdown: Optional[Dict[str, Any]] = None
    match_explanation: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CandidateChunkResponse(BaseModel):
    id: int
    chunk_text: str
    chunk_type: Optional[str] = None
    similarity_score: float

    class Config:
        from_attributes = True


class CandidateDetailResponse(CandidateResponse):
    chunks: List[CandidateChunkResponse] = []


class ScoreBreakdown(BaseModel):
    semantic_similarity: float
    keyword_overlap: float
    experience_match: float
    education_match: float
    total_weighted_score: float


class StructuredResumeData(BaseModel):
    skills: List[str]
    experience_years: int
    education: List[str]
    certifications: List[str]
    previous_roles: List[str]
    summary: Optional[str] = None