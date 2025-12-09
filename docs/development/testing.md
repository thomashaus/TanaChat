# Testing Strategy

TanaChat uses a pyramid testing strategy comprising Unit, Integration, and End-to-End (E2E) tests.

## Test Commands

| Scope | Command | Description |
|-------|---------|-------------|
| **All** | `make test` | Run all test suites |
| **Unit** | `make test-unit` | Fast, isolated tests |
| **Integration** | `make test-integration` | Service interaction tests |
| **API** | `pytest tests/unit/api` | Backend specific tests |
| **MCP** | `pytest tests/unit/mcp` | MCP specific tests |

## Structure

```
tests/
├── unit/           # Logic tests (No DB/Network)
├── integration/    # Component interaction (S3, API calls)
├── e2e/            # Full workflows
└── fixtures/       # Mock data
```

## Writing Tests

### Unit Tests
Use `pytest` fixtures to mock dependencies.

```python
def test_validation():
    importer = TanaImporter()
    result = importer.validate(valid_data)
    assert result.is_valid
```

### Integration Tests
Use `pytest-asyncio` for async API tests.

```python
@pytest.mark.asyncio
async def test_upload_flow():
    async with AsyncClient(app=app) as client:
        response = await client.post("/upload", files=...)
        assert response.status_code == 200
```
