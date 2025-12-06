# Testing Documentation

## Testing Strategy

### Overview

The TanaChat.ai project employs a comprehensive testing strategy covering unit tests, integration tests, end-to-end tests, and performance testing. The testing pyramid emphasizes fast unit tests at the base with fewer, slower integration and E2E tests at the top.

```
Testing Pyramid
    ┌─────────────────┐
    │   E2E Tests     │  ← Full user workflows
    │   (5%)          │
    ├─────────────────┤
    │ Integration     │  ← Service integration
    │ Tests (25%)     │
    ├─────────────────┤
    │ Unit Tests      │  → Fast, isolated tests
    │ (70%)          │
    └─────────────────┘
```

## Test Structure

### Directory Organization

```
testing/
├── unit/                    # Unit tests
│   ├── lib/                # Library tests
│   ├── api/                # API unit tests
│   └── cli/                # CLI tool tests
├── integration/            # Integration tests
│   ├── api/                # API integration tests
│   ├── storage/            # Storage integration tests
│   └── external/           # External API tests
├── e2e/                    # End-to-end tests
│   ├── workflows/          # User workflow tests
│   └── api/                # API E2E tests
├── performance/            # Performance tests
│   ├── load/               # Load testing
│   └── stress/             # Stress testing
├── fixtures/               # Test data
│   ├── tana_exports/       # Sample Tana exports
│   └── mock_responses/     # Mock API responses
└── utils/                  # Testing utilities
    ├── helpers.py          # Test helpers
    ├── factories.py        # Test data factories
    └── fixtures.py         # Fixture management
```

## Unit Testing

### CLI Tools Testing

#### Test Framework: pytest

```python
# tests/unit/cli/test_tana_importjson.py
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from bin.tana_importjson import TanaImporter


class TestTanaImporter:
    def setup_method(self):
        """Setup for each test method"""
        self.importer = TanaImporter()
        self.sample_tana_data = {
            "version": "TanaIntermediateFile V0.1",
            "nodes": [
                {
                    "uid": "node_1",
                    "name": "Test Node",
                    "children": []
                }
            ]
        }

    @pytest.fixture
    def mock_file_system(self):
        """Mock file system operations"""
        with patch("pathlib.Path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data='{"test": "data"}')):
            yield

    def test_validate_valid_tana_file(self, mock_file_system):
        """Test validation of valid Tana file"""
        result = self.importer.validate_tana_file(self.sample_tana_data)

        assert result.valid is True
        assert result.node_count == 1
        assert result.error is None

    def test_validate_invalid_tana_file(self):
        """Test validation of invalid Tana file"""
        invalid_data = {"invalid": "structure"}
        result = self.importer.validate_tana_file(invalid_data)

        assert result.valid is False
        assert result.error is not None
        assert "Invalid Tana file version" in result.error

    def test_extract_supertags(self):
        """Test supertag extraction"""
        data_with_supertags = {
            "nodes": [
                {
                    "uid": "node_1",
                    "name": "Project Task",
                    "supertags": [{"uid": "st_1", "name": "Project"}]
                }
            ]
        }
        supertags = self.importer.extract_supertags(data_with_supertags)

        assert len(supertags) == 1
        assert supertags[0].name == "Project"

    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_export_to_markdown(self, mock_file, mock_mkdir):
        """Test markdown export functionality"""
        self.importer.export_to_markdown(self.sample_tana_data, "/tmp/export")

        mock_mkdir.assert_called_with(parents=True, exist_ok=True)
        mock_file.assert_called_once()

    def test_progress_callback(self):
        """Test progress reporting"""
        progress_calls = []

        def progress_callback(current, total, message):
            progress_calls.append((current, total, message))

        self.importer.import_with_progress(
            self.sample_tana_data,
            "/tmp/export",
            progress_callback
        )

        assert len(progress_calls) > 0
        assert progress_calls[0] == (0, 1, "Starting import...")
        assert progress_calls[-1] == (1, 1, "Import complete")
```

#### API Service Testing

```python
# tests/unit/api/services/test_tana_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from api.services.tana_service import TanaFileService
from api.models.metadata import TanaImportMetadata


class TestTanaFileService:
    @pytest.fixture
    def mock_spaces_client(self):
        """Mock DigitalOcean Spaces client"""
        client = AsyncMock()
        client.upload_file.return_value = {
            "success": True,
            "key": "tana/testuser/file_123.json",
            "url": "https://spaces.TanaChat.ai/file.json"
        }
        return client

    @pytest.fixture
    def tana_service(self, mock_spaces_client):
        """Create TanaFileService with mocked dependencies"""
        return TanaFileService(mock_spaces_client)

    @pytest.mark.asyncio
    async def test_upload_file_success(self, tana_service, mock_spaces_client):
        """Test successful file upload"""
        file_content = b'{"version": "TanaIntermediateFile V0.1", "nodes": []}'
        username = "testuser"
        filename = "test.json"

        result = await tana_service.upload_file(
            filename, username, file_content
        )

        assert isinstance(result, TanaImportMetadata)
        assert result.original_filename == filename
        assert result.username == username
        assert result.total_nodes == 0

        mock_spaces_client.upload_file.assert_called()
        assert mock_spaces_client.upload_file.call_count == 2  # file + metadata

    @pytest.mark.asyncio
    async def test_upload_file_validation_error(self, tana_service):
        """Test upload with invalid file"""
        invalid_content = b'{"invalid": "structure"}'

        with pytest.raises(ValueError, match="Invalid Tana file"):
            await tana_service.upload_file(
                "invalid.json", "testuser", invalid_content
            )

    @pytest.mark.asyncio
    async def test_list_files(self, tana_service, mock_spaces_client):
        """Test file listing"""
        mock_spaces_client.list_files.return_value = [
            {
                "key": "tana/testuser/file_1.json",
                "size": 1024,
                "last_modified": "2025-12-04T22:50:00Z",
                "url": "https://spaces.TanaChat.ai/file_1.json"
            }
        ]

        files = await tana_service.list_files("testuser")

        assert len(files) == 1
        assert files[0]["key"] == "tana/testuser/file_1.json"

    def test_extract_supertags_from_nodes(self, tana_service):
        """Test supertag extraction from node structure"""
        nodes = [
            {
                "uid": "node_1",
                "name": "Task 1",
                "supertags": [
                    {"uid": "st_1", "name": "Project"},
                    {"uid": "st_2", "name": "Task"}
                ]
            },
            {
                "uid": "node_2",
                "name": "Meeting",
                "supertags": [{"uid": "st_1", "name": "Project"}]
            }
        ]

        supertags = tana_service.extract_supertags_from_nodes(nodes)

        assert len(supertags) == 2
        project_tag = next(st for st in supertags if st.name == "Project")
        assert project_tag.count == 2

        task_tag = next(st for st in supertags if st.name == "Task")
        assert task_tag.count == 1
```

## Integration Testing

### API Integration Tests

```python
# tests/integration/api/test_file_upload_flow.py
import pytest
import json
from httpx import AsyncClient

from api.main import app


class TestFileUploadIntegration:
    @pytest.mark.asyncio
    async def test_complete_upload_flow(self):
        """Test complete file upload and retrieval flow"""
        # Sample Tana file content
        tana_content = {
            "version": "TanaIntermediateFile V0.1",
            "nodes": [
                {
                    "uid": "node_1",
                    "name": "Test Project",
                    "supertags": [{"uid": "st_1", "name": "Project"}],
                    "children": [
                        {
                            "uid": "node_2",
                            "name": "Task 1",
                            "supertags": [{"uid": "st_2", "name": "Task"}]
                        }
                    ]
                }
            ]
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Step 1: Login and get token
            login_response = await client.post("/api/auth/login", json={
                "username": "testuser",
                "password": "testpass"
            })
            assert login_response.status_code == 200
            token = login_response.json()["access_token"]
            auth_headers = {"Authorization": f"Bearer {token}"}

            # Step 2: Upload file
            upload_response = await client.post(
                "/api/tana/upload",
                files={"file": ("test.json", json.dumps(tana_content), "application/json")},
                headers=auth_headers
            )
            assert upload_response.status_code == 200
            upload_result = upload_response.json()
            file_id = upload_result["file_id"]

            # Step 3: List files and verify upload
            list_response = await client.get(
                "/api/tana/files",
                headers=auth_headers
            )
            assert list_response.status_code == 200
            files = list_response.json()["files"]
            assert len(files) >= 1
            uploaded_file = next(f for f in files if f["file_id"] == file_id)
            assert uploaded_file["original_filename"] == "test.json"

            # Step 4: Get file metadata
            metadata_response = await client.get(
                f"/api/tana/files/{file_id}/meta",
                headers=auth_headers
            )
            assert metadata_response.status_code == 200
            metadata = metadata_response.json()
            assert metadata["total_nodes"] == 2
            assert len(metadata["supertags"]) == 2

            # Step 5: Download original file
            download_response = await client.get(
                f"/api/tana/files/{file_id}",
                headers=auth_headers
            )
            assert download_response.status_code == 200
            downloaded_content = download_response.json()
            assert downloaded_content["version"] == "TanaIntermediateFile V0.1"

            # Step 6: Clean up - delete file
            delete_response = await client.delete(
                f"/api/tana/files/{file_id}",
                headers=auth_headers
            )
            assert delete_response.status_code == 200

            # Step 7: Verify deletion
            list_response_after_delete = await client.get(
                "/api/tana/files",
                headers=auth_headers
            )
            files_after_delete = list_response_after_delete.json()["files"]
            deleted_file = next((f for f in files_after_delete if f["file_id"] == file_id), None)
            assert deleted_file is None

    @pytest.mark.asyncio
    async def test_spaces_connectivity(self):
        """Test DigitalOcean Spaces connectivity"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Login first
            login_response = await client.post("/api/auth/login", json={
                "username": "testuser",
                "password": "testpass"
            })
            token = login_response.json()["access_token"]
            auth_headers = {"Authorization": f"Bearer {token}"}

            # Check Spaces status
            spaces_response = await client.get(
                "/api/spaces/status",
                headers=auth_headers
            )
            assert spaces_response.status_code == 200
            status = spaces_response.json()
            assert "connected" in status
            assert "bucket" in status

            # List user files in Spaces
            list_response = await client.get(
                "/api/spaces/list",
                headers=auth_headers
            )
            assert list_response.status_code == 200
            list_result = list_response.json()
            assert "files" in list_result
            assert "user_prefix" in list_result
```

### External API Integration Tests

```python
# tests/integration/external/test_tana_api.py
import pytest
from unittest.mock import patch, AsyncMock

from lib.tana_poster import TanaPoster


class TestTanaAPIIntegration:
    @pytest.mark.asyncio
    @pytest.mark.integration  # Mark as integration test
    async def test_real_tana_api_connection(self):
        """Test real connection to Tana API (requires API key)"""
        # This test should only run with valid API key
        api_key = pytest.config.getini("tana_api_key")
        if not api_key:
            pytest.skip("Tana API key not configured")

        poster = TanaPoster(api_key)

        # Create a test node
        result = await poster.create_node(
            content="Test node from integration tests",
            supertags=["Test"],
            node_name="INBOX"
        )

        assert "node_id" in result
        assert result["success"] is True

        # Clean up - delete the test node
        await poster.delete_node(result["node_id"])

    @pytest.mark.asyncio
    async def test_tana_api_error_handling(self):
        """Test error handling for Tana API failures"""
        poster = TanaPoster("invalid_api_key")

        with pytest.raises(TanaAPIError) as exc_info:
            await poster.create_node("Test content")

        assert "401" in str(exc_info.value) or "Unauthorized" in str(exc_info.value)
```

## End-to-End Testing

### CLI Workflow Testing

```python
# tests/e2e/workflows/test_complete_cli_workflow.py
import pytest
import subprocess
import tempfile
import json
from pathlib import Path


class TestCLIWorkflow:
    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def sample_tana_export(self, temp_workspace):
        """Create sample Tana export file"""
        tana_data = {
            "version": "TanaIntermediateFile V0.1",
            "summary": {
                "totalNodes": 3,
                "topLevelNodes": 1
            },
            "nodes": [
                {
                    "uid": "node_1",
                    "name": "My Project",
                    "supertags": [{"uid": "st_project", "name": "Project"}],
                    "children": [
                        {
                            "uid": "node_2",
                            "name": "Task 1",
                            "supertags": [{"uid": "st_task", "name": "Task"}]
                        },
                        {
                            "uid": "node_3",
                            "name": "Meeting Notes",
                            "supertags": [{"uid": "st_meeting", "name": "Meeting"}]
                        }
                    ]
                }
            ]
        }

        export_file = temp_workspace / "workspace.json"
        export_file.write_text(json.dumps(tana_data, indent=2))
        return export_file

    def test_complete_import_workflow(self, sample_tana_export, temp_workspace):
        """Test complete CLI import workflow"""
        import_dir = temp_workspace / "import"
        export_dir = temp_workspace / "export"
        import_dir.mkdir()
        export_dir.mkdir()

        # Step 1: Copy file to import directory
        import_file = import_dir / "workspace.json"
        import_file.write_text(sample_tana_export.read_text())

        # Step 2: Run import tool
        result = subprocess.run(
            ["./bin/tana-importjson"],
            cwd=str(temp_workspace),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "Import complete" in result.stdout

        # Step 3: Verify export directory structure
        assert (export_dir / "Projects" / "My-Project.md").exists()
        assert (export_dir / "Tasks" / "Task-1.md").exists()
        assert (export_dir / "Context" / "Meeting-Notes.md").exists()

        # Step 4: Run keytags extraction
        keytags_result = subprocess.run(
            ["./bin/tana-keytags", "add", "--from-export"],
            cwd=str(temp_workspace),
            capture_output=True,
            text=True
        )

        assert keytags_result.returncode == 0

        # Step 5: Verify keytags file created
        keytags_file = temp_workspace / "keytags.json"
        assert keytags_file.exists()

        keytags_data = json.loads(keytags_file.read_text())
        assert "supertags" in keytags_data
        assert "Project" in keytags_data["supertags"]
        assert "Task" in keytags_data["supertags"]
        assert "Meeting" in keytags_data["supertags"]

        # Step 6: Test search functionality
        search_result = subprocess.run(
            ["./bin/tana-find", "--project"],
            cwd=str(temp_workspace),
            capture_output=True,
            text=True
        )

        assert search_result.returncode == 0
        assert "My-Project.md" in search_result.stdout

    def test_error_recovery_workflow(self, temp_workspace):
        """Test error handling and recovery in CLI workflow"""
        # Test with invalid JSON file
        invalid_file = temp_workspace / "invalid.json"
        invalid_file.write_text("{ invalid json content")

        result = subprocess.run(
            ["./bin/tana-importjson"],
            cwd=str(temp_workspace),
            capture_output=True,
            text=True
        )

        assert result.returncode != 0
        assert "error" in result.stderr.lower()

        # Test recovery with valid file
        valid_data = {
            "version": "TanaIntermediateFile V0.1",
            "nodes": [{"uid": "node_1", "name": "Test"}]
        }
        valid_file = temp_workspace / "valid.json"
        valid_file.write_text(json.dumps(valid_data))

        result = subprocess.run(
            ["./bin/tana-importjson"],
            cwd=str(temp_workspace),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
```

## Performance Testing

### Load Testing

```python
# tests/performance/load/test_api_load.py
import pytest
import asyncio
import time
from httpx import AsyncClient
from concurrent.futures import ThreadPoolExecutor


class TestAPILoad:
    """API load testing with concurrent requests"""

    @pytest.mark.asyncio
    @pytest.mark.performance
    async def test_concurrent_file_uploads(self):
        """Test concurrent file upload performance"""
        concurrent_users = 10
        files_per_user = 5

        async def upload_file(user_id: int, file_index: int):
            """Upload a single file"""
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Login
                login_response = await client.post("/api/auth/login", json={
                    "username": f"user{user_id}",
                    "password": "testpass"
                })
                token = login_response.json()["access_token"]
                headers = {"Authorization": f"Bearer {token}"}

                # Upload file
                start_time = time.time()
                response = await client.post(
                    "/api/tana/upload",
                    files={
                        "file": (
                            f"test_{file_index}.json",
                            b'{"version": "TanaIntermediateFile V0.1", "nodes": []}',
                            "application/json"
                        )
                    },
                    headers=headers
                )
                upload_time = time.time() - start_time

                return {
                    "status_code": response.status_code,
                    "upload_time": upload_time,
                    "user_id": user_id,
                    "file_index": file_index
                }

        # Run concurrent uploads
        start_time = time.time()
        tasks = []
        for user in range(concurrent_users):
            for file_idx in range(files_per_user):
                task = asyncio.create_task(upload_file(user, file_idx))
                tasks.append(task)

        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time

        # Analyze results
        successful_uploads = [r for r in results if r["status_code"] == 200]

        assert len(successful_uploads) == concurrent_users * files_per_user

        # Performance assertions
        avg_upload_time = sum(r["upload_time"] for r in successful_uploads) / len(successful_uploads)
        assert avg_upload_time < 2.0  # Average upload should be under 2 seconds
        assert total_time < 30.0  # Total test should complete within 30 seconds

        # Calculate throughput
        total_uploads = len(successful_uploads)
        throughput = total_uploads / total_time
        print(f"Upload throughput: {throughput:.2f} uploads/second")

    @pytest.mark.asyncio
    @pytest.mark.performance
    async def test_file_search_performance(self):
        """Test search performance with large datasets"""
        # This would require setting up a large test dataset
        pass
```

## Test Configuration

### pytest.ini

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=api
    --cov=lib
    --cov=bin
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-fail-under=80

markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    performance: Performance tests
    slow: Slow running tests

# Custom configuration
tana_api_key =

[coverage:run]
omit =
    */tests/*
    */venv/*
    */.venv/*
    setup.py

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

### Test Data Management

```python
# tests/utils/fixtures.py
import json
from pathlib import Path
from typing import Dict, Any


class TestFixtures:
    """Manages test data fixtures"""

    def __init__(self, fixtures_dir: Path = Path("tests/fixtures")):
        self.fixtures_dir = fixtures_dir

    def get_tana_export(self, name: str) -> Dict[str, Any]:
        """Load Tana export fixture"""
        fixture_path = self.fixtures_dir / "tana_exports" / f"{name}.json"
        with open(fixture_path) as f:
            return json.load(f)

    def get_mock_api_response(self, name: str) -> Dict[str, Any]:
        """Load mock API response fixture"""
        fixture_path = self.fixtures_dir / "mock_responses" / f"{name}.json"
        with open(fixture_path) as f:
            return json.load(f)


# Test data factories
def create_sample_tana_file(node_count: int = 5) -> Dict[str, Any]:
    """Create sample Tana file for testing"""
    import random

    nodes = []
    for i in range(node_count):
        node = {
            "uid": f"node_{i}",
            "name": f"Node {i}",
            "supertags": [
                {"uid": f"st_{i}", "name": random.choice(["Project", "Task", "Meeting"])}
            ]
        }
        if i > 0:
            node["children"] = []
        nodes.append(node)

    return {
        "version": "TanaIntermediateFile V0.1",
        "nodes": nodes
    }


def create_test_user(username: str = "testuser") -> Dict[str, Any]:
    """Create test user data"""
    return {
        "id": "user_123",
        "username": username,
        "email": f"{username}@example.com",
        "created_at": "2025-12-04T22:50:00Z",
        "preferences": {}
    }
```

## Continuous Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12]

    services:
      # Add any required services like databases

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install uv
      uses: astral-sh/setup-uv@v3

    - name: Install dependencies
      run: |
        cd api && uv sync --dev

    - name: Run unit tests
      run: |
        cd api && uv run pytest tests/unit -v

    - name: Run integration tests
      run: |
        cd api && uv run pytest tests/integration -v
      env:
        TANA_API_KEY: ${{ secrets.TANA_API_KEY }}
        DO_SPACES_KEY: ${{ secrets.DO_SPACES_KEY }}
        DO_SPACES_SECRET: ${{ secrets.DO_SPACES_SECRET }}

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./api/htmlcov/index.html
```

## Running Tests

### Command Line Usage

```bash
# Run all tests
make test

# Run specific test categories
pytest tests/unit
pytest tests/integration
pytest tests/e2e

# Run with coverage
pytest --cov=api --cov=lib --cov-report=html

# Run performance tests
pytest -m performance

# Run specific test file
pytest tests/unit/api/test_tana_service.py -v

# Run with specific markers
pytest -m "not slow"  # Skip slow tests
pytest -m "unit and not integration"  # Only unit tests
```

This comprehensive testing documentation ensures the TanaChat.ai project maintains high code quality and reliability through systematic testing across all levels of the application stack.