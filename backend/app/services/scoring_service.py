import httpx
import numpy as np
from typing import Dict, Any, List
import json

from app.core.config import settings
from app.models.candidate import Candidate, CandidateChunk
from app.models.job import Job


class ScoringService:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.base_url = settings.DEEPSEEK_BASE_URL

        # Scoring weights
        self.weights = {
            "semantic_similarity": 0.45,
            "keyword_overlap": 0.30,
            "experience_match": 0.15,
            "education_match": 0.10
        }

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text using DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": settings.EMBEDDING_MODEL,
            "input": text
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/embeddings",
                    json=payload,
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                return result["data"][0]["embedding"]

        except Exception as e:
            print(f"Embedding generation failed: {e}")
            # Return a random embedding as fallback
            return np.random.normal(0, 0.1, 1536).tolist()

    async def calculate_candidate_score(
        self,
        candidate: Candidate,
        job: Job,
        chunks: List[CandidateChunk]
    ) -> Dict[str, float]:
        """Calculate comprehensive candidate score"""

        # Generate job description embedding
        job_embedding = await self.generate_embedding(job.description)

        # Calculate semantic similarity
        semantic_score = await self._calculate_semantic_similarity(chunks, job_embedding)

        # Calculate keyword overlap
        keyword_score = await self._calculate_keyword_overlap(candidate, job)

        # Calculate experience match
        experience_score = await self._calculate_experience_match(candidate, job)

        # Calculate education match
        education_score = await self._calculate_education_match(candidate, job)

        # Calculate weighted total
        total_score = (
            semantic_score * self.weights["semantic_similarity"] +
            keyword_score * self.weights["keyword_overlap"] +
            experience_score * self.weights["experience_match"] +
            education_score * self.weights["education_match"]
        )

        return {
            "semantic_similarity": round(semantic_score, 3),
            "keyword_overlap": round(keyword_score, 3),
            "experience_match": round(experience_score, 3),
            "education_match": round(education_score, 3),
            "total_weighted_score": round(total_score, 3)
        }

    async def _calculate_semantic_similarity(
        self,
        chunks: List[CandidateChunk],
        job_embedding: List[float]
    ) -> float:
        """Calculate semantic similarity between resume chunks and job description"""

        if not chunks:
            return 0.0

        similarities = []
        job_vector = np.array(job_embedding)

        for chunk in chunks:
            try:
                chunk_vector = np.array(chunk.embedding_vector)
                # Calculate cosine similarity
                similarity = np.dot(chunk_vector, job_vector) / (
                    np.linalg.norm(chunk_vector) * np.linalg.norm(job_vector)
                )
                similarities.append(similarity)
                # Store similarity in chunk for later use
                chunk.similarity_score = float(similarity)

            except Exception as e:
                print(f"Similarity calculation failed for chunk {chunk.id}: {e}")
                similarities.append(0.0)

        # Return average of top 3 similarities
        top_similarities = sorted(similarities, reverse=True)[:3]
        return sum(top_similarities) / len(top_similarities) if top_similarities else 0.0

    async def _calculate_keyword_overlap(self, candidate: Candidate, job: Job) -> float:
        """Calculate keyword overlap score"""
        try:
            job_requirements = job.requirements or {}
            candidate_data = candidate.structured_data or {}

            required_skills = set(skill.lower() for skill in job_requirements.get("skills_required", []))
            preferred_skills = set(skill.lower() for skill in job_requirements.get("skills_preferred", []))
            candidate_skills = set(skill.lower() for skill in candidate_data.get("skills", []))

            if not (required_skills or preferred_skills):
                return 0.5  # Neutral score if no specific skills required

            # Calculate overlap scores
            required_overlap = len(candidate_skills.intersection(required_skills))
            preferred_overlap = len(candidate_skills.intersection(preferred_skills))

            # Weight required skills more heavily
            total_required = len(required_skills)
            total_preferred = len(preferred_skills)

            required_score = required_overlap / total_required if total_required > 0 else 1.0
            preferred_score = preferred_overlap / total_preferred if total_preferred > 0 else 1.0

            # Combined score (70% required, 30% preferred)
            return (required_score * 0.7) + (preferred_score * 0.3)

        except Exception as e:
            print(f"Keyword overlap calculation failed: {e}")
            return 0.0

    async def _calculate_experience_match(self, candidate: Candidate, job: Job) -> float:
        """Calculate experience match score"""
        try:
            job_requirements = job.requirements or {}
            candidate_data = candidate.structured_data or {}

            required_years = job_requirements.get("min_experience_years", 0)
            candidate_years = candidate_data.get("experience_years", 0)

            if required_years == 0:
                return 1.0  # Perfect score if no specific experience required

            # Calculate score based on experience ratio
            if candidate_years >= required_years:
                # Bonus for having more experience, but diminishing returns
                excess_years = candidate_years - required_years
                bonus = min(excess_years * 0.1, 0.3)  # Max 30% bonus
                return min(1.0 + bonus, 1.0)
            else:
                # Penalty for having less experience
                return candidate_years / required_years

        except Exception as e:
            print(f"Experience match calculation failed: {e}")
            return 0.0

    async def _calculate_education_match(self, candidate: Candidate, job: Job) -> float:
        """Calculate education match score"""
        try:
            job_requirements = job.requirements or {}
            candidate_data = candidate.structured_data or {}

            required_education = job_requirements.get("education_level", "").lower()
            candidate_education = candidate_data.get("education", [])

            if not required_education or required_education == "any":
                return 1.0  # Perfect score if no specific education required

            # Education hierarchy
            education_levels = {
                "high school": 1,
                "associate": 2,
                "bachelor": 3,
                "master": 4,
                "phd": 5,
                "doctorate": 5
            }

            required_level = education_levels.get(required_education, 0)

            # Check candidate's highest education level
            candidate_level = 0
            for edu in candidate_education:
                edu_lower = edu.lower()
                for level_name, level_value in education_levels.items():
                    if level_name in edu_lower:
                        candidate_level = max(candidate_level, level_value)

            if candidate_level >= required_level:
                return 1.0
            elif candidate_level > 0:
                return candidate_level / required_level
            else:
                return 0.3  # Some credit for not specifying education

        except Exception as e:
            print(f"Education match calculation failed: {e}")
            return 0.0

    async def calculate_similarity_matrix(self, candidates: List[Candidate], job: Job) -> Dict[str, Any]:
        """Calculate similarity matrix for ranking candidates"""
        try:
            scores = []
            for candidate in candidates:
                score_data = {
                    "candidate_id": candidate.id,
                    "name": candidate.name,
                    "total_score": candidate.total_score,
                    "breakdown": candidate.score_breakdown
                }
                scores.append(score_data)

            # Sort by total score
            scores.sort(key=lambda x: x["total_score"], reverse=True)

            return {
                "job_id": job.id,
                "candidate_scores": scores,
                "total_candidates": len(candidates),
                "average_score": sum(s["total_score"] for s in scores) / len(scores) if scores else 0
            }

        except Exception as e:
            print(f"Similarity matrix calculation failed: {e}")
            return {"error": str(e)}