# Architecture Documentation

## Overview

This document describes the architecture and design patterns used in the Blog Platform API.

## Architecture Layers

### 1. API Layer (`app/api/`)

The API layer handles HTTP requests and responses. It's organized into versioned routes for better API evolution.

**Components:**
- `routes/v1/`: Version 1 API endpoints
- `deps.py`: Shared dependencies (authentication, authorization)

**Responsibilities:**
- Request validation
- Response formatting
- Route definition
- Authentication/authorization enforcement

### 2. Service Layer (`app/services/`)

The service layer contains business logic and orchestrates data operations.

**Components:**
- `user_service.py`: User management logic
- `article_service.py`: Article operations
- `comment_service.py`: Comment management

**Responsibilities:**
- Business rule enforcement
- Data validation
- Transaction management
- Cross-entity operations

### 3. Data Layer (`app/db/`)

The data layer manages database models and connections.

**Components:**
- `models/`: SQLAlchemy ORM models
- `base.py`: Base model with common fields
- `session.py`: Database session management

**Responsibilities:**
- Database schema definition
- Relationship management
- Query execution
- Connection pooling

### 4. Schema Layer (`app/schemas/`)

Pydantic schemas for request/response validation.

**Components:**
- Request models (Create, Update)
- Response models
- Common schemas (pagination, errors)

**Responsibilities:**
- Input validation
- Output serialization
- Type checking
- Documentation generation

### 5. Core Layer (`app/core/`)

Core application configuration and utilities.

**Components:**
- `config.py`: Application settings
- `security.py`: Authentication utilities

**Responsibilities:**
- Configuration management
- Security functions
- Shared utilities

## Design Patterns

### Dependency Injection

FastAPI's dependency injection system is used throughout:

```python
async def get_article(
    article_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Function implementation
```

### Repository Pattern

Services act as repositories, abstracting data access:

```python
class ArticleService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, article_id: str) -> Optional[Article]:
        # Data access logic
```

### Async/Await Pattern

All I/O operations use async/await for non-blocking execution:

```python
async def create_article(article_data: ArticleCreate):
    article = Article(**article_data.dict())
    self.db.add(article)
    await self.db.flush()
    return article
```

## Security Architecture

### Authentication Flow

1. User registers/logs in
2. Server generates JWT token
3. Client includes token in Authorization header
4. Server validates token on each request
5. User information extracted from token

### Authorization

Role-based access control (RBAC):
- User: Can manage own content
- Moderator: Can moderate comments
- Admin: Full system access

### Password Security

- Passwords hashed with bcrypt
- Salt automatically generated
- Never stored in plain text
- Password strength validation

## Database Architecture

### Entity Relationships

```
User (1) ──< (N) Article
User (1) ──< (N) Comment
Article (1) ──< (N) Comment
```

### Key Features

- UUID primary keys for security
- Soft deletes (is_active flag)
- Created/updated timestamps
- Foreign key constraints
- Cascading deletes

## API Design

### RESTful Principles

- Resource-based URLs
- HTTP methods for operations
- Proper status codes
- Consistent response format

### Versioning

API versioned via URL path (`/api/v1/`)

### Pagination

List endpoints support pagination:
- `page`: Page number (default: 1)
- `size`: Items per page (default: 10, max: 100)

### Error Handling

Consistent error responses:
```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Performance Considerations

### Database Optimization

- Connection pooling (10 connections, 20 overflow)
- Async queries for non-blocking I/O
- Eager loading of relationships
- Proper indexing on frequently queried fields

### Caching Strategy

Redis used for:
- Session management
- Rate limiting
- Frequently accessed data

### Query Optimization

- Use `selectinload` for relationships
- Pagination to limit result sets
- Indexes on foreign keys and search fields

## Testing Strategy

### Test Pyramid

1. **Unit Tests**: Service and utility functions
2. **Integration Tests**: API endpoints with database
3. **E2E Tests**: Complete user workflows

### Test Database

- SQLite in-memory for tests
- Isolated test sessions
- Fixtures for common data

## Deployment Architecture

### Docker Containers

- `api`: FastAPI application
- `db`: PostgreSQL database
- `redis`: Redis cache

### Environment Configuration

- Environment variables for secrets
- Different configs for dev/staging/prod
- Volume mounts for persistence

## Monitoring and Logging

### Health Checks

- Database connectivity
- Redis connectivity
- Application status

### Logging

- Structured logging
- Different levels (DEBUG, INFO, WARNING, ERROR)
- Security event logging

## Future Enhancements

Potential improvements:
- GraphQL API
- WebSocket support for real-time comments
- Full-text search with Elasticsearch
- Image upload and CDN integration
- Email notifications
- Social authentication (OAuth)
- Rate limiting per user
- API analytics
