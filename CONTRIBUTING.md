# Contributing Guide

Thank you for considering contributing to the Blog Platform API!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `pytest`
6. Commit changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker (optional)

### Local Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment:
```bash
cp .env.example .env
# Edit .env with your local configuration
```

4. Run migrations:
```bash
alembic upgrade head
```

5. Start development server:
```bash
uvicorn app.main:app --reload
```

## Code Standards

### Style Guide

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for functions and classes

### Naming Conventions

- Variables and functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

### Example Code

```python
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user_by_email(
    db: AsyncSession,
    email: str
) -> Optional[User]:
    """Get user by email address.
    
    Args:
        db: Database session
        email: User email address
        
    Returns:
        User if found, None otherwise
    """
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()
```

## Testing

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_auth.py

# With coverage
pytest --cov=app

# Verbose
pytest -v
```

### Writing Tests

- Test file names: `test_*.py`
- Test function names: `test_*`
- Use fixtures for common setup
- Test both success and failure cases

Example:
```python
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Test user creation."""
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "Password123!"
    }
    
    response = await client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
```

## Database Migrations

### Creating Migrations

1. Make changes to models in `app/db/models/`
2. Generate migration:
```bash
alembic revision --autogenerate -m "Description"
```
3. Review generated migration in `alembic/versions/`
4. Apply migration:
```bash
alembic upgrade head
```

### Migration Best Practices

- Review auto-generated migrations
- Test migrations on development database
- Never modify existing migrations
- Include both upgrade and downgrade
- Use descriptive migration messages

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commit messages are clear

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Tests pass
- [ ] Code follows style guide
- [ ] Documentation updated
```

### Review Process

1. Automated tests must pass
2. Code review by maintainers
3. Address feedback
4. Approval and merge

## Commit Messages

### Format

```
type(scope): Brief description

Longer description if needed

Fixes #123
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### Examples

```
feat(articles): Add article publishing feature

Implement article publishing workflow with status changes
and publication date tracking

Fixes #42
```

## Code Review Guidelines

### For Authors

- Keep PRs focused and small
- Write clear descriptions
- Respond to feedback promptly
- Update based on suggestions

### For Reviewers

- Be constructive and respectful
- Focus on code quality
- Suggest improvements
- Approve when satisfied

## Documentation

### API Documentation

- Document all endpoints
- Include request/response examples
- Describe all parameters
- List possible error codes

### Code Documentation

```python
def create_article(
    article_data: ArticleCreate,
    author_id: str
) -> Article:
    """Create a new article.
    
    Args:
        article_data: Article creation data
        author_id: ID of the article author
        
    Returns:
        Created article instance
        
    Raises:
        HTTPException: If validation fails
    """
```

## Getting Help

- Check existing issues
- Review documentation
- Ask in discussions
- Contact maintainers

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Maintain professional conduct

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
