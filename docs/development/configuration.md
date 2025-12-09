# Configuration & Environment Variables

TanaChat uses environment variables for configuration. Do not hardcode secrets.

## Common Variables

| Variable | Description | Required | Source |
|----------|-------------|----------|--------|
| `TANA_API_KEY` | Key for Tana API | Yes | Tana Settings |
| `API_SECRET_KEY` | JWT signing secret | Yes | Generated |
| `DATABASE_URL` | Postgres/SQLite URI | Yes | DB Provider |

## Storage (S3 Compatible)

TanaChat supports any S3-compatible storage provider (AWS S3, MinIO, Cloudflare R2, etc.).

| Variable | Description | Default |
|----------|-------------|---------|
| `S3_BUCKET` | Bucket Name | `tanachat` |
| `S3_REGION` | Region | `us-east-1` |
| `S3_ENDPOINT` | Endpoint URL | - |
| `S3_ACCESS_KEY` | Access Key ID | - |
| `S3_SECRET_KEY` | Secret Access Key | - |

## Frontend

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | URL of Backend API |

## Local Development
Copy `.env.example` to `.env.local` and set your keys.

```bash
cp .env.example .env.local
```
