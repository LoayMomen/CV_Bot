from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.job import Job
from app.models.candidate import Candidate
from app.schemas.job import JobCreate, JobUpdate
from app.services.llm_service import LLMService


class JobService:
    def __init__(self):
        self.llm_service = LLMService()

    async def create_job(self, db: Session, job_data: JobCreate, user_id: int) -> Job:
        # Generate requirements and questionnaire using LLM
        requirements = await self.llm_service.extract_requirements(job_data.description)
        questionnaire = await self.llm_service.generate_questionnaire(job_data.description, requirements)

        db_job = Job(
            title=job_data.title,
            description=job_data.description,
            requirements=requirements,
            questionnaire=questionnaire,
            created_by=user_id
        )
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job

    async def get_job(self, db: Session, job_id: int) -> Optional[Job]:
        return db.query(Job).filter(Job.id == job_id).first()

    async def get_user_jobs(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Job]:
        jobs = db.query(Job).filter(Job.created_by == user_id).offset(skip).limit(limit).all()

        # Add candidate count for each job
        for job in jobs:
            job.candidate_count = db.query(Candidate).filter(Candidate.job_id == job.id).count()

        return jobs

    async def update_job(self, db: Session, job_id: int, job_data: JobUpdate, user_id: int) -> Job:
        job = db.query(Job).filter(Job.id == job_id, Job.created_by == user_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        update_data = job_data.dict(exclude_unset=True)

        # If description is updated, regenerate requirements and questionnaire
        if "description" in update_data:
            requirements = await self.llm_service.extract_requirements(update_data["description"])
            questionnaire = await self.llm_service.generate_questionnaire(update_data["description"], requirements)
            update_data["requirements"] = requirements
            update_data["questionnaire"] = questionnaire

        for field, value in update_data.items():
            setattr(job, field, value)

        db.commit()
        db.refresh(job)
        return job

    async def delete_job(self, db: Session, job_id: int, user_id: int) -> bool:
        job = db.query(Job).filter(Job.id == job_id, Job.created_by == user_id).first()
        if not job:
            return False

        # Check if job has candidates
        candidate_count = db.query(Candidate).filter(Candidate.job_id == job_id).count()
        if candidate_count > 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete job with existing candidates. Archive it instead."
            )

        db.delete(job)
        db.commit()
        return True