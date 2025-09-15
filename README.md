# CV_Bot - AI-Powered Resume Scanner

An intelligent resume screening and ranking system that helps HR professionals efficiently evaluate candidates using AI-powered matching and semantic analysis.

## 🚀 Quick Start

Get started in 5 minutes! See [QUICKSTART.md](./QUICKSTART.md) for detailed setup instructions.

```bash
git clone https://github.com/LoayMomen/CV_Bot.git
cd CV_Bot
cp .env.example .env
# Add your DeepSeek API key to .env
python scripts/setup.py
```

Then visit http://localhost:3000 to start using CV_Bot!

## ✨ Features

### 🤖 AI-Powered Analysis
- **Smart Job Creation**: AI extracts requirements and generates interview questions
- **Resume Parsing**: Extract structured data from PDF/DOCX with OCR fallback
- **Semantic Matching**: Vector embeddings for intelligent candidate matching
- **Explainable Rankings**: Clear AI explanations for candidate scores

### 📊 Intelligent Scoring
- **Multi-Factor Analysis**: Skills, experience, education, and semantic similarity
- **Weighted Scoring**: Customizable scoring weights (45% semantic, 30% skills, 15% experience, 10% education)
- **Detailed Breakdowns**: Per-category scores with visual indicators
- **Match Explanations**: LLM-generated reasoning for each candidate

### 🎯 Complete Workflow
- **Job Management**: Create, edit, and track job postings
- **Resume Upload**: Drag-and-drop interface with real-time processing
- **Candidate Dashboard**: Ranked list with filtering and sorting
- **Status Tracking**: Mark candidates as reviewed, shortlisted, or rejected

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js       │    │   FastAPI       │    │   PostgreSQL    │
│   Frontend      │◄──►│   Backend       │◄──►│   Database      │
│   (TypeScript)  │    │   (Python)      │    │   + Redis       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                         ┌─────────────────┐
                         │   DeepSeek API  │
                         │   (LLM + Embed) │
                         └─────────────────┘
```

### Tech Stack
- **Frontend**: Next.js 15, React, TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI, SQLAlchemy, Alembic, Pydantic
- **Database**: PostgreSQL, Redis
- **AI/ML**: DeepSeek API for embeddings and LLM
- **Vector Store**: FAISS (easily upgradeable to Milvus/Weaviate)
- **File Processing**: PyPDF2, python-docx, Tesseract OCR

## 📱 Demo Screenshots

### Dashboard
![Dashboard](docs/images/dashboard.png)

### Job Creation with AI
![Job Creation](docs/images/job-creation.png)

### Candidate Ranking
![Candidate Ranking](docs/images/candidate-ranking.png)

### AI Score Breakdown
![Score Breakdown](docs/images/score-breakdown.png)

## 🛠️ Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional, for databases)

### Quick Setup
```bash
# Automated setup
python scripts/setup.py

# Manual setup
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

### Running the Application
```bash
# Backend
cd backend && python run.py

# Frontend
cd frontend && npm run dev

# Access at http://localhost:3000
```

See [DEVELOPMENT.md](./DEVELOPMENT.md) for detailed development instructions.

## 📚 Documentation

- **[Quick Start](./QUICKSTART.md)** - Get running in 5 minutes
- **[Development Guide](./DEVELOPMENT.md)** - Detailed setup and development
- **[MVP Specification](./mvp.md)** - Complete project architecture and features
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when running)

## 🧪 Testing

```bash
# Test API endpoints
python scripts/test.py

# Frontend tests
cd frontend && npm run test

# Backend tests
cd backend && pytest
```

## 🚀 Deployment

The application is containerized and ready for deployment:

```bash
# Build and run with Docker
docker-compose -f docker-compose.prod.yml up -d

# Or deploy to your preferred platform
# (Vercel, Railway, DigitalOcean, AWS, etc.)
```

## 🔧 Configuration

Key environment variables:

```bash
# Required
DEEPSEEK_API_KEY=your-api-key

# Optional (defaults provided)
DATABASE_URL=postgresql://user:pass@localhost/cv_bot
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-jwt-secret
```

## 📊 Features Comparison

| Feature | CV_Bot | Traditional ATS | Manual Review |
|---------|--------|-----------------|---------------|
| AI Job Analysis | ✅ | ❌ | ❌ |
| Semantic Matching | ✅ | ❌ | ❌ |
| Auto Questionnaires | ✅ | ❌ | ❌ |
| Explainable AI | ✅ | ❌ | ❌ |
| Resume Parsing | ✅ | ✅ | ❌ |
| Candidate Ranking | ✅ | ✅ | ❌ |
| Setup Time | 5 minutes | Days/Weeks | N/A |
| Cost | Free/Low | High | Time-intensive |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 🙋‍♂️ Support

- **Issues**: [GitHub Issues](https://github.com/LoayMomen/CV_Bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/LoayMomen/CV_Bot/discussions)
- **Email**: support@cvbot.ai

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=LoayMomen/CV_Bot&type=Date)](https://star-history.com/#LoayMomen/CV_Bot&Date)

---

**Made with ❤️ for HR professionals worldwide**