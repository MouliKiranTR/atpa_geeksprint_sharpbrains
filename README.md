# Onboarding Agent API

A powerful middleware API for onboarding agents that reads data from various sources, feeds it to Large Language Models (LLM), and provides intelligent, summarized answers based on user queries.

## Features

- 🤖 **AI-Powered Q&A**: Ask questions and get intelligent answers based on your documents
- 📄 **Multi-Format Support**: Process PDF, DOCX, TXT, XLSX, and CSV files
- 🔍 **Smart Search**: Find relevant information across all uploaded documents
- 📊 **Document Summarization**: Generate concise summaries with different styles
- 🔌 **RESTful API**: Easy integration with frontend applications
- 🚀 **FastAPI Framework**: High-performance, auto-documented API
- 💾 **Multiple Data Sources**: Support for file uploads, future integration with Confluence, SharePoint, Slack

## Architecture

```
Frontend Application
        ↓
Onboarding Agent API (This Project)
        ↓
├── File Processing Service
├── LLM Service (OpenAI)
├── Data Source Service
└── Document Search & Indexing
```

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API Key
- PostgreSQL (optional, uses SQLite by default)
- Redis (optional, for caching)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd onboarding-agent-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp env.example .env
```

5. **Configure Python environment** (prevents __pycache__ creation)
```bash
# Run the setup script
./setup_env.sh

# Or manually set the environment variable
export PYTHONDONTWRITEBYTECODE=1
```

Edit `.env` file with your configuration:
```env
# Required
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///./onboarding_agent.db

# Optional
API_HOST=localhost
API_PORT=8000
DEBUG=True
```

5. **Run the application**
```bash
python -m uvicorn app.main:app --reload --host localhost --port 8000
```

The API will be available at:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Core Endpoints

#### Query & Answer
- `POST /api/v1/query/ask` - Ask questions and get AI-powered answers
- `POST /api/v1/query/summarize` - Summarize content using AI
- `GET /api/v1/query/documents` - Get all available documents
- `GET /api/v1/query/documents/{id}` - Get specific document
- `DELETE /api/v1/query/documents/{id}` - Delete document

#### File Upload
- `POST /api/v1/upload/file` - Upload file (base64 encoded)
- `POST /api/v1/upload/multipart-file` - Upload file (multipart form)
- `GET /api/v1/upload/status/{file_id}` - Get upload status

#### Health & Monitoring
- `GET /api/v1/health/` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health with dependencies
- `GET /api/v1/health/ready` - Readiness check
- `GET /api/v1/health/live` - Liveness check

## Usage Examples

### 1. Upload a Document

```bash
curl -X POST "http://localhost:8000/api/v1/upload/file" \
     -H "Content-Type: application/json" \
     -d '{
       "file_name": "company_handbook.pdf",
       "file_type": "pdf",
       "content": "base64_encoded_content_here",
       "description": "Company employee handbook"
     }'
```

### 2. Ask a Question

```bash
curl -X POST "http://localhost:8000/api/v1/query/ask" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What is the company vacation policy?",
       "include_sources": true,
       "context_limit": 5000
     }'
```

### 3. Summarize Content

```bash
curl -X POST "http://localhost:8000/api/v1/query/summarize" \
     -H "Content-Type: application/json" \
     -d '{
       "content": "Long text content to summarize...",
       "max_length": 200,
       "style": "professional"
     }'
```

## Response Examples

### Query Response
```json
{
  "answer": "According to the company handbook, employees are entitled to 20 days of paid vacation per year...",
  "confidence": 0.85,
  "sources": [
    {
      "document_id": "doc_123",
      "document_name": "company_handbook.pdf",
      "source_type": "file_upload",
      "relevance_score": 5
    }
  ],
  "processing_time": 2.3,
  "timestamp": "2024-01-20T10:30:00Z"
}
```

### Upload Response
```json
{
  "file_id": "abc-123-def",
  "status": "success",
  "message": "File company_handbook.pdf processed successfully",
  "processed": true
}
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for LLM services | Yes | - |
| `SECRET_KEY` | Secret key for authentication | Yes | - |
| `DATABASE_URL` | Database connection URL | No | SQLite |
| `API_HOST` | API host address | No | localhost |
| `API_PORT` | API port number | No | 8000 |
| `DEBUG` | Enable debug mode | No | True |
| `MAX_FILE_SIZE` | Maximum file size in bytes | No | 10MB |
| `ALLOWED_FILE_TYPES` | Comma-separated file extensions | No | pdf,docx,txt,xlsx,csv |

### Supported File Types

- **PDF** (.pdf) - Portable Document Format
- **Word** (.docx) - Microsoft Word documents
- **Text** (.txt) - Plain text files
- **Excel** (.xlsx) - Microsoft Excel spreadsheets
- **CSV** (.csv) - Comma-separated values

## Development

### Project Structure

```
onboarding-agent-api/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   ├── query.py      # Q&A endpoints
│   │   │   ├── upload.py     # File upload endpoints
│   │   │   └── health.py     # Health check endpoints
│   │   └── api.py           # API router
│   ├── core/
│   │   ├── config.py        # Configuration settings
│   │   └── database.py      # Database setup
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── services/
│   │   ├── llm_service.py   # LLM integration
│   │   └── data_source_service.py # Data processing
│   └── main.py             # FastAPI application
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
├── env.example            # Environment template
└── README.md              # This file
```

### Running Tests

```bash
pytest tests/ -v
```

### Code Style

The project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting

```bash
# Format code
black app/
isort app/

# Check linting
flake8 app/
```

## Deployment

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

1. **Database**: Use PostgreSQL for production
2. **Caching**: Implement Redis for better performance
3. **Security**: Configure proper CORS and authentication
4. **Monitoring**: Set up logging and health monitoring
5. **Scaling**: Use multiple workers for high load

## Future Enhancements

- 🔌 **External Integrations**: Confluence, SharePoint, Slack APIs
- 🔍 **Advanced Search**: Vector embeddings and semantic search
- 🔒 **Authentication**: User management and access control
- 📊 **Analytics**: Usage tracking and performance metrics
- 🌐 **Multi-language**: Support for multiple languages
- 📱 **Real-time**: WebSocket support for live interactions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For questions and support:
- Check the API documentation at `/docs`
- Review the health endpoints for system status
- Check logs for debugging information

---

**Happy Onboarding! 🚀** 