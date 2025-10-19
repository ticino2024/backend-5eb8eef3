# Available Commands Reference

Quick reference for all available commands and scripts.

## 🚀 Getting Started

### Using Docker (Recommended)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up -d --build

# View running containers
docker-compose ps
```

### Local Development
```bash
# Run setup script
./scripts/setup_dev.sh

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🏃 Running the Application

### Development Server
```bash
# With auto-reload
uvicorn app.main:app --reload

# Specify host and port
uvicorn app.main:app --host 0.0.0.0 --port 8000

# With Python
python -m app.main
```

### Docker
```bash
# Start with docker-compose
docker-compose up

# Run in background
docker-compose up -d

# Follow logs
docker-compose logs -f api
```

## 🗄️ Database Commands

### Migrations with Alembic
```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current migration
alembic current

# Show migration history
alembic history

# Rollback to base (WARNING: drops all tables)
alembic downgrade base

# Show SQL for migration (without applying)
alembic upgrade head --sql
```

### Using Scripts
```bash
# Create initial migration
./scripts/create_initial_migration.sh
```

### Docker Database Access
```bash
# Access PostgreSQL CLI
docker-compose exec db psql -U postgres -d blog_db

# Backup database
docker-compose exec db pg_dump -U postgres blog_db > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres blog_db < backup.sql

# Check database status
docker-compose exec db pg_isready
```

## 🧪 Testing Commands

### Run Tests
```bash
# All tests
pytest

# With verbose output
pytest -v

# Specific test file
pytest tests/test_auth.py

# Specific test function
pytest tests/test_auth.py::TestAuth::test_register_user

# With coverage report
pytest --cov=app

# Coverage with HTML report
pytest --cov=app --cov-report=html

# Stop on first failure
pytest -x

# Show print statements
pytest -s

# Run in parallel
pytest -n auto
```

### Using Test Script
```bash
# Run test script
./RUN_TESTS.sh
```

### Docker Tests
```bash
# Run tests in container
docker-compose exec api pytest

# With coverage
docker-compose exec api pytest --cov=app
```

## 📝 Code Quality

### Linting
```bash
# Format with black (if installed)
black app/ tests/

# Check with flake8 (if installed)
flake8 app/ tests/

# Type checking with mypy (if installed)
mypy app/
```

## 🔍 API Interaction

### Health Check
```bash
# Check API health
curl http://localhost:8000/api/v1/health

# Using httpie (if installed)
http GET localhost:8000/api/v1/health
```

### Authentication
```bash
# Register user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "Test User",
    "password": "Password123!"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Password123!"
  }'

# Save token
export TOKEN="your-token-here"
```

### Articles
```bash
# Create article
curl -X POST "http://localhost:8000/api/v1/articles/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Article",
    "content": "# Content here",
    "summary": "Summary",
    "status": "published"
  }'

# List articles
curl "http://localhost:8000/api/v1/articles/"

# Get article
curl "http://localhost:8000/api/v1/articles/{article_id}"
```

### Comments
```bash
# Create comment
curl -X POST "http://localhost:8000/api/v1/articles/{article_id}/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Great article!"}'

# List comments
curl "http://localhost:8000/api/v1/articles/{article_id}/comments"
```

## 🐳 Docker Commands

### Container Management
```bash
# View logs
docker-compose logs api      # API logs
docker-compose logs db       # Database logs
docker-compose logs redis    # Redis logs
docker-compose logs -f       # Follow all logs

# Execute commands in container
docker-compose exec api bash
docker-compose exec db psql -U postgres
docker-compose exec redis redis-cli

# Restart services
docker-compose restart api
docker-compose restart db

# Stop and remove containers
docker-compose down

# Remove with volumes (WARNING: deletes data)
docker-compose down -v

# View resource usage
docker-compose stats
```

### Image Management
```bash
# Build images
docker-compose build

# Build without cache
docker-compose build --no-cache

# Pull latest images
docker-compose pull

# Remove unused images
docker image prune

# Remove all unused Docker resources
docker system prune
```

## 🔧 Development Commands

### Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit environment file
nano .env
# or
vim .env
```

### Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate.bat     # Windows CMD
venv\Scripts\Activate.ps1     # Windows PowerShell

# Deactivate
deactivate

# Install requirements
pip install -r requirements.txt

# Freeze current packages
pip freeze > requirements.txt

# Update pip
pip install --upgrade pip
```

### Python Interactive Shell
```bash
# Start Python shell with app context
python

# In shell:
from app.main import app
from app.db.models import User, Article, Comment
```

## 📊 Monitoring

### View Logs
```bash
# API logs
docker-compose logs -f api

# Database logs
docker-compose logs -f db

# Last 100 lines
docker-compose logs --tail=100 api

# Since specific time
docker-compose logs --since 2024-01-01T00:00:00 api
```

### Resource Monitoring
```bash
# Container stats
docker-compose stats

# Disk usage
docker system df

# Network inspection
docker network ls
docker network inspect blog_network
```

## 🛠️ Maintenance

### Database Maintenance
```bash
# Backup
docker-compose exec db pg_dump -U postgres blog_db > backup_$(date +%Y%m%d).sql

# Clean old migrations (development only)
alembic downgrade base
rm alembic/versions/*.py

# Recreate database (development only)
docker-compose down -v
docker-compose up -d
```

### Cache Management
```bash
# Clear Redis cache
docker-compose exec redis redis-cli FLUSHALL

# View Redis keys
docker-compose exec redis redis-cli KEYS '*'

# Monitor Redis
docker-compose exec redis redis-cli MONITOR
```

## 📚 Documentation

### View Documentation
```bash
# Start server and visit:
# http://localhost:8000/docs        (Swagger UI)
# http://localhost:8000/redoc       (ReDoc)
# http://localhost:8000/openapi.json (OpenAPI spec)
```

### Generate Documentation
```bash
# Export OpenAPI spec
curl http://localhost:8000/openapi.json > openapi.json
```

## 🔍 Debugging

### Python Debugging
```bash
# Run with debugger
python -m pdb app/main.py

# With ipdb (if installed)
pip install ipdb
# Add breakpoint in code: import ipdb; ipdb.set_trace()
```

### View Container Logs
```bash
# All containers
docker-compose logs

# Specific container with tail
docker-compose logs --tail=50 api

# Follow logs
docker-compose logs -f
```

### Inspect Container
```bash
# Shell into API container
docker-compose exec api bash

# Check running processes
docker-compose exec api ps aux

# Check environment variables
docker-compose exec api env
```

## 🎯 Quick Commands Summary

### Most Used Commands
```bash
# Start development
docker-compose up -d && docker-compose logs -f api

# Run tests
pytest -v

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# View API docs
open http://localhost:8000/docs

# Check health
curl http://localhost:8000/api/v1/health

# Stop everything
docker-compose down
```

### One-Line Setup
```bash
# Complete setup in one command
cp .env.example .env && docker-compose up -d && sleep 5 && curl http://localhost:8000/api/v1/health
```

## 📖 Help Commands

```bash
# FastAPI help
uvicorn --help

# Alembic help
alembic --help
alembic upgrade --help

# Pytest help
pytest --help

# Docker Compose help
docker-compose --help
docker-compose up --help

# Python help
python --help
```

---

**Tip**: Add commonly used commands as shell aliases in your `~/.bashrc` or `~/.zshrc`:

```bash
alias blog-start="docker-compose up -d"
alias blog-stop="docker-compose down"
alias blog-logs="docker-compose logs -f api"
alias blog-test="pytest -v"
alias blog-shell="docker-compose exec api bash"
```
