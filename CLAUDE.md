# TanaChat Project Rules

## General Rules
- enforce and never bypass gitleaks
- 1 is done and verify it
- when waiting for a deployment always show the commit number
- it is not fixed until it is deployed and tested and real data is seen

## Directory Structure Rules

### `.do/` Directory - DigitalOcean Deployment
- **PURPOSE**: DigitalOcean-specific deployment configurations and scripts
- **STATUS**: Excluded from git via `.gitignore`
- **CONTAINS**: Sensitive deployment materials, API tokens, registry credentials
- **USAGE**: Always play DigitalOcean deployment operations in this directory
- **NEVER COMMIT**: Contains secrets and sensitive information

**Typical contents:**
- `appspec.yaml` - DigitalOcean App Platform deployment spec
- `docr-secret.json` - Container Registry credentials (sensitive!)
- `env.local` - Local environment variables with real tokens (sensitive!)
- `env.example` - Environment template (safe to commit)
- `deploy.sh` - Deployment automation scripts
- `build-images.sh` - Docker build & push scripts
- `status.sh` - Deployment monitoring scripts

### `temp/` Directory - Temporary Scripts
- **PURPOSE**: Temporary scripts, experiments, and one-off operations
- **STATUS**: Excluded from git via `.gitignore` (with .gitkeep to track directory)
- **CONTAINS**: Temporary code, experimental scripts, utility scripts
- **USAGE**: Always place temporary scripts in this directory
- **CLEANUP**: Remove scripts when no longer needed

### `db/` Directory - Database Files
- **PURPOSE**: Local database files, SQLite databases, and test data
- **STATUS**: Can be gitignored for local development
- **CONTAINS**: Database files, test imports, local data storage

### Project Root
- **Main documentation**: `README.md` should be comprehensive for new developers
- **Core code**: All permanent project code lives in respective directories
- **Configuration**: `.env.example` for templates, `.env.local` for real values
- **Cleanliness**: No temporary files or credentials in committed code

## Data Import and Testing Rules

### Import Testing Workflow
1. **ALWAYS** test import processes in the `temp/` directory first
2. **NEVER** commit real user data or credentials
3. **USE** sample/test data that mimics real data structure
4. **VERIFY** with gitleaks before any commits
5. **CLEANUP** test files after validation

### Safe Import Testing Process
```bash
# 1. Create test data in temp/ (gitignored)
cd temp/
# Create test-import-data.json with sample structure

# 2. Test import locally
./test-import-script.py
./bin/tanachat-importjson temp/test-import-data.json

# 3. Validate results
# Check that import worked correctly

# 4. Clean up (optional)
rm temp/test-import-data.json
```

### Real Data Testing
- Place real data files in `temp/` directory only
- Use environment variables for credentials
- Remove real data files after testing
- Never commit real data, even temporarily

## Security Rules - CRITICAL

### NEVER COMMIT These Items:
1. **Real API keys** (DigitalOcean, AWS, Tana, etc.)
2. **Secret tokens** or authentication credentials
3. **`docr-secret.json`** - Contains registry credentials
4. **`env.local`** - Contains real environment variables
5. **Files with real credentials** in any format
6. **Real user data** or import files with actual content

### ALWAYS Use Templates:
1. **`env.example`** for environment variable templates
2. **Placeholder values** like `YOUR_API_KEY_HERE`
3. **Example tokens** clearly marked as examples
4. **Environment variables** instead of hardcoded credentials
5. **Sample data** that mimics structure but contains fake content

### Git Security Practices:
1. **Run `gitleaks`** before committing to check for secrets
2. **Review git diff** carefully for any credentials
3. **Use `.gitignore`** properly to exclude sensitive files
4. **Never commit** files with real secrets, even if they're later deleted

## Development Workflow

### For DigitalOcean Deployments:
```bash
cd .do/
./build-images.sh     # Build and push to registry
./deploy.sh production  # Deploy to production
./status.sh          # Monitor deployment
```

### For Import Testing:
```bash
cd temp/
# Create test data files
# Run import tests
# Validate results
# Clean up when done
```

### For Regular Development:
```bash
make setup    # Initial setup
make dev      # Development server
make test     # Run tests
make build    # Build for production
```

## Code Quality Rules

### Before Committing:
1. **Run `gitleaks`** to ensure no secrets are committed
2. **Run `make lint`** for code quality
3. **Run `make test`** to ensure tests pass
4. **Review changes** for any accidental credentials
5. **Check for real data** in temp/ directory

### File Organization:
- **Permanent code** → Proper project directories
- **Deployment configs** → `.do/` directory
- **Temporary scripts** → `temp/` directory
- **Database files** → `db/` directory
- **No credentials** → Only in `.do/env.local`
- **No real data** → Only sample data in committed files

## Emergency Procedures

### If Real Credentials Are Committed:
1. **IMMEDIATE ACTION**: Remove credentials from files
2. **ROTATE KEYS**: Invalidate all exposed API keys/tokens
3. **GIT HISTORY**: Consider rewriting git history to remove commits with secrets
4. **SCAN REPO**: Run `gitleaks` to verify all secrets are removed
5. **UPDATE .gitignore**: Ensure sensitive files are properly excluded

### If Real Data Is Committed:
1. **IMMEDIATE ACTION**: Remove data from files
2. **GIT HISTORY**: Rewrite history to remove commits with real data
3. **SCAN REPO**: Review for any other data exposures
4. **ROTATE TOKENS**: If data contained tokens or credentials
5. **UPDATE WORKFLOW**: Review and fix import testing procedures

### Security Commands:
```bash
# Scan for secrets
gitleaks detect --no-banner

# Check current files only
gitleaks detect --no-git --no-banner

# Check git history (includes deleted files)
gitleaks detect --no-banner
```

## Examples of GOOD vs BAD

### GOOD - Template Environment:
```bash
# .env.example (safe to commit)
TANA_API_KEY=your_tana_api_key_here
DO_TOKEN=your_digitalocean_api_token_here
```

### BAD - Real Credentials:
```bash
# NEVER COMMIT THIS
TANA_API_KEY=real_tana_key_abc123
DO_TOKEN=dop_v1_real_do_token_xyz789
```

### GOOD - Sample Test Data:
```json
{
  "conversations": [
    {
      "id": "test-conv-1",
      "title": "Sample Conversation",
      "messages": [
        {"role": "user", "content": "Sample user message"},
        {"role": "assistant", "content": "Sample assistant response"}
      ]
    }
  ]
}
```

### BAD - Real User Data:
```json
{
  "conversations": [
    {
      "id": "real-conv-abc123",
      "title": "Actual User Conversation",
      "messages": [
        {"role": "user", "content": "Real user's private message"},
        {"role": "assistant", "content": "Real assistant response"}
      ]
    }
  ]
}
```