from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, jobs, candidates

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(candidates.router, prefix="/candidates", tags=["candidates"])