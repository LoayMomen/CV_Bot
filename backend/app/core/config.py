from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Database
    DATABASE_URL: str = "postgresql://username:password@localhost/cv_bot"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # DeepSeek API
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"

    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".doc"]

    # Embeddings
    EMBEDDING_MODEL: str = "deepseek-embedding"
    CHUNK_SIZE: int = 400
    CHUNK_OVERLAP: int = 50

    # Vector Store
    FAISS_INDEX_PATH: str = "vector_store/faiss_index"

    class Config:
        env_file = ".env"


settings = Settings()