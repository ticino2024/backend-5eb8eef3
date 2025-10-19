# API Usage Guide

Complete guide for using the Blog Platform API.

## Authentication

### Register a New User

**Endpoint:** `POST /api/v1/auth/register`

**Request:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "SecurePass123!"
}
```

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  }
}
```

### Login

**Endpoint:** `POST /api/v1/auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  }
}
```

## Using Authentication

Include the access token in the Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## User Management

### Get Current User Profile

**Endpoint:** `GET /api/v1/users/me`

**Headers:** Authorization required

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

### Update Current User Profile

**Endpoint:** `PUT /api/v1/users/me`

**Headers:** Authorization required

**Request:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "email": "jane@example.com",
  "name": "Jane Doe",
  "role": "user",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

### Get User by ID

**Endpoint:** `GET /api/v1/users/{user_id}`

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

## Article Management

### Create an Article

**Endpoint:** `POST /api/v1/articles/`

**Headers:** Authorization required

**Request:**
```json
{
  "title": "My First Article",
  "content": "# Introduction\n\nThis is my **first** article with *markdown* support.\n\n## Features\n- Item 1\n- Item 2",
  "summary": "An introduction to the platform",
  "status": "draft"
}
```

**Status Options:**
- `draft`: Not published
- `published`: Publicly visible
- `archived`: Hidden but not deleted

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "title": "My First Article",
  "slug": "my-first-article-abc12345",
  "content": "# Introduction\n\nThis is my **first** article...",
  "summary": "An introduction to the platform",
  "status": "draft",
  "author_id": "author-uuid",
  "author": {
    "id": "author-uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  },
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

### List Articles

**Endpoint:** `GET /api/v1/articles/`

**Query Parameters:**
- `page`: Page number (default: 1)
- `size`: Items per page (default: 10, max: 100)
- `status`: Filter by status (draft, published, archived)
- `author_id`: Filter by author

**Example:** `GET /api/v1/articles/?page=1&size=20&status=published`

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "uuid-string",
      "title": "Article Title",
      "slug": "article-title-abc12345",
      "summary": "Article summary",
      "status": "published",
      "author_id": "author-uuid",
      "author": {
        "id": "author-uuid",
        "email": "user@example.com",
        "name": "John Doe",
        "role": "user",
        "is_active": true,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": null
      },
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": null
    }
  ],
  "total": 100,
  "page": 1,
  "size": 20,
  "pages": 5
}
```

### Get Article by ID

**Endpoint:** `GET /api/v1/articles/{article_id}`

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "title": "Article Title",
  "slug": "article-title-abc12345",
  "content": "Full article content...",
  "summary": "Article summary",
  "status": "published",
  "author_id": "author-uuid",
  "author": { /* author details */ },
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

### Get Article by Slug

**Endpoint:** `GET /api/v1/articles/slug/{slug}`

**Response (200 OK):** Same as Get Article by ID

### Update Article

**Endpoint:** `PUT /api/v1/articles/{article_id}`

**Headers:** Authorization required (author or admin)

**Request:**
```json
{
  "title": "Updated Title",
  "content": "Updated content",
  "status": "published"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "title": "Updated Title",
  "slug": "updated-title-xyz67890",
  "content": "Updated content",
  "summary": "Article summary",
  "status": "published",
  "author_id": "author-uuid",
  "author": { /* author details */ },
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

### Publish Article

**Endpoint:** `POST /api/v1/articles/{article_id}/publish`

**Headers:** Authorization required (author only)

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "title": "Article Title",
  "status": "published",
  /* ... other fields ... */
}
```

### Delete Article

**Endpoint:** `DELETE /api/v1/articles/{article_id}`

**Headers:** Authorization required (author or admin)

**Response (204 No Content)**

## Comment System

### Create Comment

**Endpoint:** `POST /api/v1/articles/{article_id}/comments`

**Headers:** Authorization required

**Request:**
```json
{
  "content": "Great article! Thanks for sharing."
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "content": "Great article! Thanks for sharing.",
  "article_id": "article-uuid",
  "author_id": "author-uuid",
  "author": {
    "id": "author-uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  },
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

### List Comments

**Endpoint:** `GET /api/v1/articles/{article_id}/comments`

**Query Parameters:**
- `page`: Page number (default: 1)
- `size`: Items per page (default: 10, max: 100)

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "uuid-string",
      "content": "Great article!",
      "article_id": "article-uuid",
      "author_id": "author-uuid",
      "author": { /* author details */ },
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": null
    }
  ],
  "total": 50,
  "page": 1,
  "size": 10,
  "pages": 5
}
```

### Get Comment by ID

**Endpoint:** `GET /api/v1/comments/{comment_id}`

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "content": "Great article!",
  "article_id": "article-uuid",
  "author_id": "author-uuid",
  "author": { /* author details */ },
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

### Update Comment

**Endpoint:** `PUT /api/v1/comments/{comment_id}`

**Headers:** Authorization required (author or admin)

**Request:**
```json
{
  "content": "Updated comment content"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "content": "Updated comment content",
  "article_id": "article-uuid",
  "author_id": "author-uuid",
  "author": { /* author details */ },
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

### Delete Comment

**Endpoint:** `DELETE /api/v1/comments/{comment_id}`

**Headers:** Authorization required (author or admin)

**Response (204 No Content)**

## Health Check

**Endpoint:** `GET /api/v1/health`

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0",
  "database": "healthy"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 409 Conflict
```json
{
  "detail": "User with this email already exists"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "Password must contain at least one uppercase letter",
      "type": "value_error"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

Rate limits (if enabled):
- Authentication endpoints: 5 requests per 5 minutes per IP
- Other endpoints: Configurable per deployment

## Pagination

All list endpoints support pagination:
- Default page size: 10
- Maximum page size: 100
- Use `page` and `size` query parameters

Example:
```
GET /api/v1/articles/?page=2&size=20
```

## Complete Example Workflow

### 1. Register and Login
```bash
# Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "author@example.com",
    "name": "Article Author",
    "password": "SecurePass123!"
  }'

# Save the token from response
TOKEN="your-token-here"
```

### 2. Create an Article
```bash
curl -X POST "http://localhost:8000/api/v1/articles/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting Started with FastAPI",
    "content": "# Introduction\n\nFastAPI is amazing...",
    "summary": "A beginner guide to FastAPI",
    "status": "draft"
  }'

# Save the article_id from response
ARTICLE_ID="article-uuid-here"
```

### 3. Publish the Article
```bash
curl -X POST "http://localhost:8000/api/v1/articles/$ARTICLE_ID/publish" \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Add a Comment
```bash
curl -X POST "http://localhost:8000/api/v1/articles/$ARTICLE_ID/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Great article!"
  }'
```

### 5. List Published Articles
```bash
curl "http://localhost:8000/api/v1/articles/?status=published&page=1&size=10"
```
