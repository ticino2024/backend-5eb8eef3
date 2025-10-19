# Blog Platform API

A comprehensive FastAPI backend application for a blog platform with user authentication, article management with markdown support, and a commenting system.

## Features

- 🔐 **User Authentication**: JWT-based authentication with secure password hashing
- 📝 **Article Management**: Create, read, update, and delete articles with markdown support
- 💬 **Comment System**: Users can comment on published articles
- 🔒 **Role-Based Access Control**: Admin, moderator, and user roles
- 🗄️ **PostgreSQL Database**: Production-ready database with SQLAlchemy ORM
- 🚀 **Redis Caching**: Fast caching layer for improved performance
- 📊 **Database Migrations**: Alembic for seamless schema updates
- 🐳 **Docker Support**: Complete containerization with Docker Compose
- ✅ **Comprehensive Testing**: Full test suite with pytest
- 📚 **API Documentation**: Interactive Swagger/OpenAPI documentation

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL 15 with asyncpg
- **ORM**: SQLAlchemy 2.0 (async)
- **Caching**: Redis 7
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic 2.0
- **Migrations**: Alembic
- **Testing**: pytest with async support
- **Containerization**: Docker & Docker Compose

## Project Structure

```
.
├── app/
│   ├── api/
│   │   ├── deps.py              # Shared dependencies
│   │   └── routes/
│   │       └── v1/
│   │           ├── auth.py      # Authentication endpoints
│   │           ├── users.py     # User management
│   │           ├── articles.py  # Article CRUD
│   │           ├── comments.py  # Comment system
│   │           └── health.py    # Health checks
│   ├── core/
│   │   ├── config.py            # Application configuration
│   │   └── security.py          # Security utilities
│   ├── db/
│   │   ├── base.py              # Database base
│   │   ├── session.py           # Database session
│   │   └── models/              # SQLAlchemy models
│   ├── schemas/                 # Pydantic schemas
│   ├── services/                # Business logic
│   ├── utils/                   # Utility functions
│   └── main.py                  # Application entry point
├── alembic/                     # Database migrations
├── tests/                       # Test suite
├── docker-compose.yml           # Docker orchestration
├── Dockerfile                   # Container image
└── requirements.txt             # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Installation

#### Option 1: Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd blog-platform-api
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start services with Docker Compose:
```bash
docker-compose up -d
```

4. The API will be available at `http://localhost:8000`

#### Option 2: Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd blog-platform-api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the application:
```bash
uvicorn app.main:app --reload
```

### Environment Variables

Key environment variables (see `.env.example` for complete list):

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/blog_db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

#### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/{user_id}` - Get user by ID

#### Articles
- `POST /api/v1/articles/` - Create article
- `GET /api/v1/articles/` - List articles
- `GET /api/v1/articles/{article_id}` - Get article
- `PUT /api/v1/articles/{article_id}` - Update article
- `DELETE /api/v1/articles/{article_id}` - Delete article
- `POST /api/v1/articles/{article_id}/publish` - Publish article

#### Comments
- `POST /api/v1/articles/{article_id}/comments` - Create comment
- `GET /api/v1/articles/{article_id}/comments` - List comments
- `PUT /api/v1/comments/{comment_id}` - Update comment
- `DELETE /api/v1/comments/{comment_id}` - Delete comment

#### Health
- `GET /api/v1/health` - Health check

## Database Migrations

### Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations:
```bash
alembic upgrade head
```

### Rollback migration:
```bash
alembic downgrade -1
```

## Testing

Run the complete test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## Development

### Code Quality

The project follows industry best practices:
- Type hints throughout the codebase
- Comprehensive input validation with Pydantic
- Async/await for I/O operations
- Proper error handling and logging
- Security best practices (password hashing, JWT, input sanitization)

### Project Guidelines

- Follow PEP 8 style guide
- Use type hints for all functions
- Write comprehensive docstrings
- Add tests for new features
- Keep functions small and focused
- Use meaningful variable names

## Security Features

- **Password Hashing**: bcrypt with salt
- **JWT Authentication**: Secure token-based auth
- **Input Validation**: Pydantic models validate all inputs
- **SQL Injection Protection**: Parameterized queries via SQLAlchemy
- **XSS Protection**: Markdown content sanitization
- **CORS Configuration**: Configurable allowed origins
- **Security Headers**: X-Content-Type-Options, X-Frame-Options, etc.
- **Role-Based Access Control**: Fine-grained permissions

## Performance Considerations

- Async/await for non-blocking I/O
- Database connection pooling
- Redis caching layer
- Efficient database queries with proper indexing
- Pagination for list endpoints

## Production Deployment

### Docker Deployment

1. Build production image:
```bash
docker build -t blog-api:latest .
```

2. Deploy with Docker Compose:
```bash
docker-compose -f docker-compose.yml up -d
```

### Environment Configuration

Ensure the following in production:
- Use strong `SECRET_KEY`
- Set `DEBUG=False`
- Configure proper `ALLOWED_ORIGINS`
- Use production-grade PostgreSQL
- Set up proper logging
- Configure HTTPS/TLS
- Implement rate limiting
- Set up monitoring and alerting

## API Usage Examples

### Register a new user
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "SecurePass123!"
  }'
```

### Create an article
```bash
curl -X POST "http://localhost:8000/api/v1/articles/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Article",
    "content": "# Hello World\n\nThis is my **first** article!",
    "summary": "An introduction article",
    "status": "published"
  }'
```

### Add a comment
```bash
curl -X POST "http://localhost:8000/api/v1/articles/ARTICLE_ID/comments" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Great article!"
  }'
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review the test suite for usage examples

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
