from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.job import JobCreate, JobResponse, JobUpdate
from app.services.job_service import JobService
from app.services.auth_service import AuthService

router = APIRouter()
job_service = JobService()
auth_service = AuthService()


@router.post("/", response_model=JobResponse)
async def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """Create a new job with auto-generated questionnaire"""
    return await job_service.create_job(db, job_data, current_user.id)


@router.get("/", response_model=List[JobResponse])
async def get_jobs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """Get all jobs for the current user"""
    return await job_service.get_user_jobs(db, current_user.id, skip, limit)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """Get a specific job"""
    job = await job_service.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check ownership
    if job.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return job


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """Update a job"""
    return await job_service.update_job(db, job_id, job_data, current_user.id)


@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """Delete a job"""
    success = await job_service.delete_job(db, job_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}