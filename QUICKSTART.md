# Quick Start Guide

Get the Blog Platform API up and running in minutes!

## 🚀 Quick Start with Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed

### Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd blog-platform-api
```

2. **Set up environment**
```bash
cp .env.example .env
# The default values work out of the box for Docker
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Verify services are running**
```bash
docker-compose ps
```

5. **Access the API**
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/api/v1/health

### Test the API

```bash
# Register a user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "password": "Password123!"
  }'
```

## 🛠️ Local Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Steps

1. **Clone and navigate**
```bash
git clone <repository-url>
cd blog-platform-api
```

2. **Run setup script**
```bash
chmod +x scripts/setup_dev.sh
./scripts/setup_dev.sh
```

3. **Configure environment**
```bash
# Edit .env with your database and Redis URLs
nano .env
```

4. **Start services**
```bash
# Start PostgreSQL and Redis (if not running)
# Then start the API
uvicorn app.main:app --reload
```

5. **Access the API**
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs

## 📝 First API Calls

### 1. Register a User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "author@example.com",
    "name": "John Doe",
    "password": "SecurePass123!"
  }'
```

Save the `access_token` from the response.

### 2. Create an Article
```bash
curl -X POST "http://localhost:8000/api/v1/articles/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Article",
    "content": "# Hello World\n\nThis is my **first** article!",
    "summary": "My first blog post",
    "status": "published"
  }'
```

### 3. List Articles
```bash
curl "http://localhost:8000/api/v1/articles/?status=published"
```

### 4. Add a Comment
```bash
curl -X POST "http://localhost:8000/api/v1/articles/ARTICLE_ID/comments" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Great article!"
  }'
```

## 🧪 Running Tests

```bash
# Install test dependencies (included in requirements.txt)
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py -v
```

## 📚 Next Steps

1. **Explore the API**
   - Visit http://localhost:8000/docs for interactive documentation
   - Try different endpoints and parameters

2. **Read the Documentation**
   - [API Guide](API_GUIDE.md) - Detailed endpoint documentation
   - [Architecture](ARCHITECTURE.md) - System architecture and design
   - [Contributing](CONTRIBUTING.md) - Contribution guidelines

3. **Customize the Application**
   - Modify models in `app/db/models/`
   - Add new endpoints in `app/api/routes/`
   - Extend business logic in `app/services/`

## 🐛 Troubleshooting

### Docker Issues

**Problem:** Containers won't start
```bash
# Check logs
docker-compose logs

# Rebuild images
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Problem:** Database connection fails
```bash
# Check if database is ready
docker-compose exec db pg_isready

# Restart database
docker-compose restart db
```

### Local Development Issues

**Problem:** Import errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem:** Database migration fails
```bash
# Check database connection
psql $DATABASE_URL

# Reset migrations (development only!)
alembic downgrade base
alembic upgrade head
```

**Problem:** Port already in use
```bash
# Change port in .env
PORT=8001

# Or kill process on port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows
```

## 🔧 Configuration

### Environment Variables

Key variables in `.env`:

```env
# Required
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
SECRET_KEY=your-secret-key-here

# Optional
DEBUG=False
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000
```

### Docker Configuration

Modify `docker-compose.yml` to:
- Change database credentials
- Adjust port mappings
- Add volume mounts
- Configure environment variables

## 📖 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **GitHub Repository**: <repository-url>
- **Issue Tracker**: <repository-url>/issues

## 🤝 Getting Help

- Check [API_GUIDE.md](API_GUIDE.md) for endpoint details
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Open an issue for bugs or questions
- Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## ✅ Success Indicators

You know everything is working when:
- ✅ Health check returns `{"status": "healthy"}`
- ✅ You can register and login
- ✅ You can create and publish articles
- ✅ You can add comments to articles
- ✅ All tests pass with `pytest`

Happy coding! 🎉
