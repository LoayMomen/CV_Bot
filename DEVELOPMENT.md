# CV_Bot Development Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Environment Setup

1. **Clone and setup environment**:
```bash
git clone https://github.com/LoayMomen/CV_Bot.git
cd CV_Bot
cp .env.example .env
```

2. **Configure environment variables** in `.env`:
```bash
# Database
DATABASE_URL=postgresql://cv_bot_user:cv_bot_password@localhost:5432/cv_bot

# DeepSeek API
DEEPSEEK_API_KEY=your-deepseek-api-key

# Other settings (see .env.example for full list)
```

### Backend Setup

1. **Create virtual environment**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Start services with Docker**:
```bash
docker-compose up -d postgres redis
```

4. **Run database migrations**:
```bash
alembic upgrade head
```

5. **Start FastAPI server**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Start development server**:
```bash
npm run dev
```

## 📁 Project Structure

```
CV_Bot/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── requirements.txt    # Python dependencies
│   └── docker-compose.yml  # Local services
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   └── lib/           # Utilities & API
│   └── package.json       # Node dependencies
├── services/              # Microservices
│   ├── resume_parser/     # Resume parsing service
│   ├── embeddings/        # Vector embeddings
│   └── scoring/           # Candidate scoring
├── database/              # Database files
│   ├── migrations/        # Alembic migrations
│   └── seeds/             # Seed data
└── docs/                  # Documentation
```

## 🔧 Development Workflow

### 1. Week 1: Backend Foundation
- [x] Project structure and FastAPI setup
- [x] Database models and migrations
- [x] Authentication system
- [x] Job creation API with LLM integration
- [ ] Basic testing setup

### 2. Week 2: Resume Processing
- [x] Resume parsing service (PDF/DOCX)
- [x] Text chunking and embeddings
- [x] Scoring algorithm implementation
- [ ] OCR integration for scanned documents
- [ ] Error handling and validation

### 3. Week 3: Frontend UI
- [x] Next.js setup and basic components
- [ ] Authentication pages (login/register)
- [ ] Job creation interface
- [ ] Resume upload functionality
- [ ] Candidate ranking dashboard

### 4. Week 4: Integration & Polish
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Error handling improvements
- [ ] Documentation completion
- [ ] Deployment preparation

## 🛠️ Available Scripts

### Backend
```bash
# Start development server
uvicorn app.main:app --reload

# Run tests
pytest

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Start with Docker
docker-compose up
```

### Frontend
```bash
# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Lint code
npm run lint
```

## 📋 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user

### Jobs
- `GET /api/v1/jobs` - List user's jobs
- `POST /api/v1/jobs` - Create new job
- `GET /api/v1/jobs/{id}` - Get job details
- `PUT /api/v1/jobs/{id}` - Update job
- `DELETE /api/v1/jobs/{id}` - Delete job

### Candidates
- `POST /api/v1/candidates/upload/{job_id}` - Upload resume
- `GET /api/v1/candidates/job/{job_id}` - Get job candidates
- `GET /api/v1/candidates/{id}` - Get candidate details
- `PUT /api/v1/candidates/{id}/status` - Update candidate status

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/ -v
```

### Frontend Testing
```bash
cd frontend
npm run test
```

## 🔍 Debugging

### Backend Debugging
- API docs available at: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Database admin: Use pgAdmin or similar tool

### Frontend Debugging
- Dev server: http://localhost:3000
- React DevTools browser extension recommended

## 🚀 Deployment

### Production Environment Variables
```bash
# Security
SECRET_KEY=your-production-secret-key

# Database
DATABASE_URL=postgresql://user:pass@prod-db:5432/cv_bot

# API Keys
DEEPSEEK_API_KEY=your-production-api-key

# CORS
ALLOWED_HOSTS=["https://your-domain.com"]
```

### Docker Deployment
```bash
# Build and run entire stack
docker-compose -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

1. Create feature branch from `main`
2. Make changes following code style
3. Write/update tests
4. Submit pull request

### Code Style
- Backend: Black formatter, isort, flake8
- Frontend: ESLint, Prettier
- Commit messages: Conventional commits format

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [DeepSeek API Docs](https://api.deepseek.com/docs)
- [PostgreSQL Guide](https://www.postgresql.org/docs/)

## 🐛 Troubleshooting

### Common Issues

1. **Database connection failed**
   - Check PostgreSQL is running
   - Verify DATABASE_URL in .env

2. **DeepSeek API errors**
   - Verify API key is valid
   - Check rate limits

3. **Frontend build errors**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility

4. **Resume parsing fails**
   - Ensure Tesseract is installed for OCR
   - Check file permissions in uploads directory