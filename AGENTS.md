# AGENTS.md - Coding Guidelines for Agentic Agents

ShieldPrompt is a FastAPI-based API for detecting prompt injection attacks in AI systems. Python 3.12, async SQLAlchemy, Pydantic, pytest.

## Commands

### Running the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations
```bash
alembic upgrade head
alembic revision --autogenerate -m "description"
```

### Testing
```bash
pytest                         # Run all tests
pytest tests/test_chat.py      # Run single file
pytest tests/test_chat.py::test_analyze_returns_success -v  # Single test
pytest -v                      # Verbose
pytest --cov=app --cov-report=term-missing  # Coverage
```

### Linting
```bash
ruff check .
ruff format .
mypy app/
```

## Code Style

### Imports
- Use absolute imports: `from app.services.detector_service import DetectorService`
- Order: stdlib, third-party, local app
- Avoid wildcard imports

```python
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.schemas import PromptLogRead
```

### Formatting
- Max line length: 100 characters
- 4 spaces for indentation
- Trailing commas in multi-line structures

### Types
- Use type hints for all parameters/returns
- `Optional[X]` for compatibility (not `X | None`)
- Concrete types: `list`, `dict` (not `List`, `Dict`)

```python
async def get_history(
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
) -> List[PromptLogRead]:
```

### Naming
- **Classes**: PascalCase (`DetectorService`, `UserRepository`)
- **Functions/variables**: snake_case (`analyze_and_log`)
- **Constants**: UPPER_SNAKE_CASE (`DATABASE_URL`)
- **Files**: snake_case (`detector_service.py`)

### Error Handling
- Use `HTTPException` with appropriate status codes
- Catch specific exceptions, not bare `except`
- Log errors with context

```python
try:
    violation = await self.ai_service.check_rules_compliance(user_text, rules_list)
except Exception as e:
    logging.error(f"Error in compliance check: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal server error")
```

### Async/Await
- Always use `await` for async operations
- Use `AsyncSession` for database operations
- Mock async functions in tests with `AsyncMock`

```python
async def chat(request: TextPrompt, db: AsyncSession = Depends(get_db)):
    detector = DetectorService(db)
    result = await detector.analyze_and_log(...)
    return result
```

### Pydantic Models
- Use `BaseModel` for request/response schemas
- Use `from_attributes = True` for ORM compatibility

```python
class PromptLogRead(BaseModel):
    id: int
    timestamp: datetime
    prompt: str
    
    class Config:
        from_attributes = True
```

### SQLAlchemy Models
- Use declarative style with `Mapped` and `mapped_column`

```python
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
```

### FastAPI Routes
- Use `APIRouter` for grouping endpoints
- Define tags for documentation
- Use dependency injection for DB sessions and auth
- Return proper status codes (200 for GET/POST, 201 for creation)

```python
router = APIRouter(tags=["Chat"])

@router.post("/analyze", status_code=200)
async def analyze(request: TextPrompt, db: AsyncSession = Depends(get_db)):
    ...
```

### Testing
- Use pytest with pytest-asyncio
- Use `@pytest.mark.anyio` decorator for async tests
- Mock external dependencies with `mocker.patch` or `AsyncMock`
- Use fixtures from conftest.py

```python
@pytest.mark.anyio
async def test_analyze_returns_success(async_client: AsyncClient, mocker):
    mock_analyze = mocker.patch(
        "app.services.detector_service.DetectorService.analyze_and_log",
        new_callable=AsyncMock,
    )
    response = await async_client.post("/api/v1/chat/analyze", json=payload)
    assert response.status_code == 200
```

### Security
- Never expose secrets in logs or responses
- Use environment variables for sensitive config
- Validate all user inputs with Pydantic schemas
- Use proper authentication/authorization checks

## Project Structure
```
app/
├── api/
│   ├── deps.py          # Dependency injection (auth, db)
│   └── routes/          # API endpoints
│       ├── auth.py
│       ├── chat.py
│       └── rules.py
├── core/
│   ├── config.py        # Settings
│   └── database.py      # DB session management
├── models/              # SQLAlchemy models
├── repositories/        # Data access layer
├── schemas/             # Pydantic schemas
└── services/            # Business logic
tests/
├── conftest.py          # Test fixtures
└── test_*.py            # Test files
```

## Patterns
- Repository pattern for database access
- Service layer for business logic
- Dependency injection for testability
- Environment-based configuration via `.env`