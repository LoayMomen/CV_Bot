from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class JobBase(BaseModel):
    title: str
    description: str


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[Dict[str, Any]] = None
    questionnaire: Optional[Dict[str, Any]] = None
    is_active: Optional[str] = None


class JobResponse(JobBase):
    id: int
    requirements: Optional[Dict[str, Any]] = None
    questionnaire: Optional[Dict[str, Any]] = None
    created_by: int
    is_active: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Additional computed fields
    candidate_count: Optional[int] = 0

    class Config:
        from_attributes = True


class QuestionnaireQuestion(BaseModel):
    question: str
    type: str  # "text", "number", "boolean", "select"
    options: Optional[List[str]] = None
    required: bool = True


class JobRequirements(BaseModel):
    skills_required: List[str]
    skills_preferred: List[str]
    min_experience_years: int
    education_level: str
    certifications: List[str]
    location: Optional[str] = None