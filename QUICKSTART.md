# CV_Bot Quick Start Guide

Get CV_Bot running in 5 minutes!

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional, for easy database setup)

## Quick Setup

### 1. Clone and Configure

```bash
git clone https://github.com/LoayMomen/CV_Bot.git
cd CV_Bot
cp .env.example .env
```

Edit `.env` and add your DeepSeek API key:
```bash
DEEPSEEK_API_KEY=your-api-key-here
```

### 2. Automated Setup (Recommended)

```bash
python scripts/setup.py
```

This will:
- Install all dependencies
- Start database services
- Configure the environment

### 3. Manual Setup (Alternative)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
docker-compose up -d  # Start PostgreSQL and Redis
python run.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### 4. Test the Installation

```bash
python scripts/test.py
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Quick Demo

1. **Register**: Go to http://localhost:3000/register
2. **Create Job**: Click "Create Job" and paste a job description
3. **Upload Resume**: Upload a PDF/DOCX resume for the job
4. **View Results**: See AI-powered candidate ranking and scoring

## Key Features

### 🤖 AI-Powered Analysis
- Automatic job requirements extraction
- Smart questionnaire generation
- Semantic candidate matching

### 📊 Intelligent Scoring
- Vector embeddings for resume analysis
- Weighted scoring algorithm
- Detailed match explanations

### 🎯 Complete Workflow
- Job creation and management
- Resume upload and parsing
- Candidate ranking dashboard
- Status tracking and notes

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Jobs
- `GET /api/v1/jobs` - List jobs
- `POST /api/v1/jobs` - Create job (with AI analysis)
- `GET /api/v1/jobs/{id}` - Get job details

### Candidates
- `POST /api/v1/candidates/upload/{job_id}` - Upload resume
- `GET /api/v1/candidates/job/{job_id}` - Get ranked candidates
- `GET /api/v1/candidates/{id}` - Get candidate details

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js       │    │   FastAPI       │    │   PostgreSQL    │
│   Frontend      │◄──►│   Backend       │◄──►│   Database      │
│   (Port 3000)   │    │   (Port 8000)   │    │   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                         ┌─────────────────┐
                         │   DeepSeek API  │
                         │   (Embeddings)  │
                         └─────────────────┘
```

## Troubleshooting

### Backend Issues
```bash
# Check if backend is running
curl http://localhost:8000/health

# View backend logs
cd backend && python run.py

# Reset database
docker-compose down -v && docker-compose up -d
```

### Frontend Issues
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Check for build errors
npm run build
```

### Database Issues
```bash
# Restart database services
cd backend
docker-compose restart

# Check database connection
docker-compose logs postgres
```

## Environment Variables

Required variables in `.env`:

```bash
# DeepSeek API
DEEPSEEK_API_KEY=your-api-key

# Database (default values work with Docker)
DATABASE_URL=postgresql://cv_bot_user:cv_bot_password@localhost:5432/cv_bot

# Redis
REDIS_URL=redis://localhost:6379

# JWT Secret (change in production)
SECRET_KEY=your-secret-key
```

## Next Steps

1. **Add More Jobs**: Create different job types to test AI analysis
2. **Upload Various Resumes**: Test with different formats and styles
3. **Explore Scoring**: Review AI explanations and score breakdowns
4. **Customize Weights**: Modify scoring weights in `backend/app/services/scoring_service.py`
5. **Deploy**: Follow deployment guide for production setup

## Support

- **Documentation**: See `DEVELOPMENT.md` for detailed docs
- **Issues**: Report bugs on GitHub
- **API Reference**: Visit http://localhost:8000/docs

Happy recruiting with AI! 🚀