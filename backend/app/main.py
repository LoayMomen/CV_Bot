from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.api.api_v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up CV_Bot API...")
    yield
    # Shutdown
    print("Shutting down CV_Bot API...")


app = FastAPI(
    title="CV_Bot API",
    description="AI-powered resume scanner and ranking system",
    version="1.0.0",
    lifespan=lifespan
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "CV_Bot API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )