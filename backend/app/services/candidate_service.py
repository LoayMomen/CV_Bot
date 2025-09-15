from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
import os
import json

from app.models.candidate import Candidate, CandidateChunk
from app.models.job import Job
from app.schemas.candidate import CandidateUpdate
from app.services.resume_parser_service import ResumeParserService
from app.services.scoring_service import ScoringService
from app.services.llm_service import LLMService
from app.core.config import settings


class CandidateService:
    def __init__(self):
        self.resume_parser = ResumeParserService()
        self.scoring_service = ScoringService()
        self.llm_service = LLMService()

    async def upload_resume(
        self,
        db: Session,
        job_id: int,
        file: UploadFile,
        name: str,
        email: str,
        phone: Optional[str],
        user_id: int
    ) -> Candidate:
        # Verify job exists and belongs to user
        job = db.query(Job).filter(Job.id == job_id, Job.created_by == user_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        # Check file type
        if not any(file.filename.lower().endswith(ext) for ext in settings.ALLOWED_EXTENSIONS):
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Save uploaded file
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(settings.UPLOAD_DIR, f"{job_id}_{name}_{file.filename}")

        with open(file_path, "wb") as buffer:
            content = await file.read()
            if len(content) > settings.MAX_FILE_SIZE:
                raise HTTPException(status_code=400, detail="File too large")
            buffer.write(content)

        try:
            # Parse resume
            resume_text, structured_data = await self.resume_parser.parse_resume(file_path)

            # Create candidate record
            candidate = Candidate(
                job_id=job_id,
                name=name,
                email=email,
                phone=phone,
                resume_filename=file.filename,
                resume_text=resume_text,
                structured_data=structured_data
            )
            db.add(candidate)
            db.commit()
            db.refresh(candidate)

            # Process resume chunks and calculate scores
            await self._process_candidate_chunks(db, candidate, job)

            return candidate

        except Exception as e:
            # Clean up file if processing fails
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Resume processing failed: {str(e)}")

    async def _process_candidate_chunks(self, db: Session, candidate: Candidate, job: Job):
        """Process resume into chunks and calculate scores"""
        # Create text chunks
        chunks = await self.resume_parser.create_chunks(candidate.resume_text)

        chunk_records = []
        for chunk_data in chunks:
            # Generate embeddings for each chunk
            embedding = await self.scoring_service.generate_embedding(chunk_data["text"])

            chunk_record = CandidateChunk(
                candidate_id=candidate.id,
                chunk_text=chunk_data["text"],
                chunk_type=chunk_data["type"],
                embedding_vector=embedding.tolist() if hasattr(embedding, 'tolist') else embedding
            )
            chunk_records.append(chunk_record)

        db.add_all(chunk_records)

        # Calculate overall score
        score_breakdown = await self.scoring_service.calculate_candidate_score(
            candidate, job, chunk_records
        )

        # Generate explanation
        explanation = await self.llm_service.explain_candidate_match(
            job.description, candidate.resume_text, score_breakdown
        )

        # Update candidate with scores
        candidate.score_breakdown = score_breakdown
        candidate.total_score = score_breakdown.get("total_weighted_score", 0.0)
        candidate.match_explanation = explanation

        db.commit()

    async def get_job_candidates(
        self,
        db: Session,
        job_id: int,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        min_score: float = 0.0
    ) -> List[Candidate]:
        # Verify job ownership
        job = db.query(Job).filter(Job.id == job_id, Job.created_by == user_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        return (
            db.query(Candidate)
            .filter(
                Candidate.job_id == job_id,
                Candidate.total_score >= min_score
            )
            .order_by(Candidate.total_score.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def get_candidate_details(self, db: Session, candidate_id: int, user_id: int) -> Candidate:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        # Verify job ownership
        job = db.query(Job).filter(Job.id == candidate.job_id, Job.created_by == user_id).first()
        if not job:
            raise HTTPException(status_code=403, detail="Access denied")

        return candidate

    async def update_candidate_status(
        self,
        db: Session,
        candidate_id: int,
        candidate_data: CandidateUpdate,
        user_id: int
    ) -> Candidate:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        # Verify job ownership
        job = db.query(Job).filter(Job.id == candidate.job_id, Job.created_by == user_id).first()
        if not job:
            raise HTTPException(status_code=403, detail="Access denied")

        # Update status
        if candidate_data.status:
            candidate.status = candidate_data.status

        db.commit()
        db.refresh(candidate)
        return candidate