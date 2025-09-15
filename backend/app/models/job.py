from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    requirements = Column(JSON)  # Structured requirements from LLM
    questionnaire = Column(JSON)  # Auto-generated questionnaire
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(String, default="active")  # active, paused, closed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    creator = relationship("User", backref="jobs")
    candidates = relationship("Candidate", back_populates="job")