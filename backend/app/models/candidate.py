from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    resume_filename = Column(String, nullable=False)
    resume_text = Column(Text, nullable=False)
    structured_data = Column(JSON)  # Parsed skills, experience, education
    total_score = Column(Float, default=0.0)
    score_breakdown = Column(JSON)  # Detailed scoring by category
    match_explanation = Column(Text)  # LLM-generated explanation
    status = Column(String, default="pending")  # pending, reviewed, shortlisted, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    job = relationship("Job", back_populates="candidates")
    chunks = relationship("CandidateChunk", back_populates="candidate")


class CandidateChunk(Base):
    __tablename__ = "candidate_chunks"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_type = Column(String)  # skills, experience, education, summary
    embedding_vector = Column(JSON)  # Store as JSON array for FAISS
    similarity_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    candidate = relationship("Candidate", back_populates="chunks")