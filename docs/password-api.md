# Password Management API

This document describes the password management endpoints available in the TanaChat API.

## Base URL
- **Production**: https://mcp.tanachat.ai
- **Local Development**: http://localhost:8000

## Authentication
All password management endpoints require user authentication or admin credentials.

## Endpoints

### 1. Change Password
Change a user's password by providing their current password.

**Endpoint**: `POST /api/auth/change-password`

**Request Body**:
```json
{
  "username": "string",
  "current_password": "string",
  "new_password": "string"
}
```

**Response**:
```json
{
  "message": "Password changed successfully",
  "username": "testuser",
  "updated_at": "2025-12-08T11:30:00.000Z"
}
```

**Error Responses**:
- `400`: New password must be at least 8 characters long
- `401`: Invalid current password
- `404`: User not found
- `500`: Server error

**Example**:
```bash
curl -X POST https://mcp.tanachat.ai/api/auth/change-password \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "current_password": "oldpassword123",
    "new_password": "newpassword123"
  }'
```

### 2. Reset Password
Reset a user's password (admin function or password recovery).

**Endpoint**: `POST /api/auth/reset-password`

**Request Body**:
```json
{
  "username": "string",
  "new_password": "string",
  "admin_key": "string (optional)"
}
```

**Response**:
```json
{
  "message": "Password reset successfully",
  "username": "testuser",
  "reset_at": "2025-12-08T11:30:00.000Z",
  "note": "User will need to login with new password"
}
```

**Error Responses**:
- `400`: New password must be at least 8 characters long
- `403`: Invalid admin key
- `404`: User not found
- `500`: Server error

**Example**:
```bash
curl -X POST https://mcp.tanachat.ai/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "new_password": "temp123456",
    "admin_key": "your-admin-key"
  }'
```

### 3. Set Password
Directly set a user's password (admin function).

**Endpoint**: `POST /api/auth/set-password`

**Request Body**:
```json
{
  "username": "string",
  "new_password": "string",
  "admin_key": "string (optional)"
}
```

**Response**:
```json
{
  "message": "Password set successfully",
  "username": "testuser",
  "set_at": "2025-12-08T11:30:00.000Z",
  "note": "User can now login with new password"
}
```

**Error Responses**:
- `400`: Password must be at least 8 characters long
- `403`: Invalid admin key
- `404`: User not found
- `500`: Server error

**Example**:
```bash
curl -X POST https://mcp.tanachat.ai/api/auth/set-password \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "new_password": "securepassword123",
    "admin_key": "your-admin-key"
  }'
```

## Password Requirements

- **Minimum Length**: 8 characters
- **Storage**: SHA-256 hashing
- **Security**: Passwords are hashed and salted

## Security Considerations

1. **HTTPS Only**: Always use HTTPS in production
2. **Admin Key**: Optional admin key provides additional security
3. **Rate Limiting**: Consider implementing rate limiting for password changes
4. **Audit Trail**: All password changes are logged with timestamps
5. **Session Management**: Consider invalidating existing sessions after password changes

## Testing

Use the provided test script to verify endpoints:

```bash
python test_password_api.py
```

## Integration with Frontend

For frontend integration, ensure proper error handling and user feedback:

```javascript
// Example frontend password change
async function changePassword(oldPassword, newPassword) {
  try {
    const response = await fetch('/api/auth/change-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: 'current_user',
        current_password: oldPassword,
        new_password: newPassword,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Password changed:', data.message);
    } else {
      const error = await response.json();
      console.error('Error:', error.detail);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}
```

## Error Handling

All endpoints return standard HTTP status codes and JSON error messages:

```json
{
  "detail": "Error description"
}
```

Common error scenarios:
- Invalid credentials
- Password too short
- User not found
- Server errors