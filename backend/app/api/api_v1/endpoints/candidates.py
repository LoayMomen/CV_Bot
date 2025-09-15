from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.candidate import CandidateResponse, CandidateUpdate
from app.services.candidate_service import CandidateService
from app.services.auth_service import AuthService

router = APIRouter()
candidate_service = CandidateService()
auth_service = AuthService()


@router.post("/upload/{job_id}", response_model=CandidateResponse)
async def upload_resume(
    job_id: int,
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """Upload and process a resume for a specific job"""
    return await candidate_service.upload_resume(
        db, job_id, file, name, email, phone, current_user.id
    )


@router.get("/job/{job_id}", response_model=List[CandidateResponse])
async def get_candidates_for_job(
    job_id: int,
    skip: int = 0,
    limit: int = 100,
    min_score: float = 0.0,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """Get all candidates for a specific job, ranked by score"""
    return await candidate_service.get_job_candidates(
        db, job_id, current_user.id, skip, limit, min_score
    )


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """Get a specific candidate with detailed scoring"""
    return await candidate_service.get_candidate_details(
        db, candidate_id, current_user.id
    )


@router.put("/{candidate_id}/status", response_model=CandidateResponse)
async def update_candidate_status(
    candidate_id: int,
    candidate_data: CandidateUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """Update candidate status (reviewed, shortlisted, rejected)"""
    return await candidate_service.update_candidate_status(
        db, candidate_id, candidate_data, current_user.id
    )