# TanaChat.ai Shared Library

This directory contains shared business logic and utilities used across the TanaChat.ai project.

## Structure

```
lib/
├── __init__.py          # Main library exports
├── colors.py            # Terminal color utilities
├── tana_io.py           # Tana file I/O operations
└── user_manager.py      # User management system
```

## Components

### Colors

Terminal color output utilities with consistent formatting.

```python
from lib import Colors

Colors.success("Operation completed")
Colors.error("Something went wrong")
Colors.info("Information message")
Colors.warning("Warning message")
```

### TanaIO

Handle Tana file input/output operations with sensible defaults.

```python
from lib import TanaIO

# Initialize with default ./files directory
tana = TanaIO()

# Load latest export
export_path = tana.find_latest_export()
data = tana.load_tana_file(export_path)

# Save file
tana.save_tana_file(data, Path("output.json"))

# List files
files = tana.list_files()
```

### UserManager

Manage users for tanachat with JWT authentication.

```python
from lib import UserManager

# Initialize user manager
users = UserManager()

# Create user
result = users.create_user(
    name="John Doe",
    username="jdoe",
    email="john@example.com",
    tana_api_key="abc123",
    password="securepassword"
)

# Authenticate
user_info = users.authenticate_user("jdoe", "password")

# Validate token
user = users.validate_token("jwt-token-here")
```

## Default Paths

The shared library uses these default paths:

- **Files Directory**: `./files`
- **Exports**: `./files/exports`
- **Imports**: `./files/imports`
- **Tana Data**: `./files/tana`
- **User Metadata**: `./files/metadata`
- **Users Database**: `./files/metadata/users.json`

These can be customized by passing a custom `files_dir` path when initializing:

```python
# Custom directory
tana = TanaIO(Path("/custom/path/files"))
users = UserManager(Path("/custom/path/files"))
```

## Usage in Scripts

All bin scripts should use the shared library:

```python
#!/usr/bin/env python3

import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from lib import TanaIO, Colors, UserManager

# Your script logic here
```

## Usage in API

The API services import from the shared library:

```python
import sys
from pathlib import Path

# Add parent directory to import from lib
parent_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(parent_dir / "lib"))

from user_manager import UserManager

user_manager = UserManager()
```

## Environment Variables

- `TANACHAT_FILES_DIR`: Override default files directory
- `TANACHAT_DEBUG`: Enable debug logging

## Testing

The shared library includes testable components with clear separation of concerns:

- **TanaIO**: File operations only
- **UserManager**: User data management only
- **Colors**: Display formatting only

## Security Notes

- Passwords are hashed using SHA-256 (replace with bcrypt in production)
- JWT tokens are simple HMAC-based (use proper JWT library in production)
- User data is stored in JSON files (consider database for production)
