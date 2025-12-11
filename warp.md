# Warp.md - TanaChat Import Testing Guidelines

## Purpose
This document provides comprehensive guidelines for safely testing data import processes in TanaChat without exposing sensitive data to GitHub.

## Quick Reference

### Testing Command Matrix
| Task | Command | Location | Notes |
|------|---------|----------|-------|
| Create test data | `cp templates/sample-import.json temp/` | Project root | Use templates, never real data |
| Test import | `./bin/tanachat-importjson temp/test-data.json` | Project root | Always use temp/ directory |
| Validate import | `./temp/test-import-script.py` | temp/ | Run validation script |
| Clean up | `rm temp/test-data.json` | temp/ | Remove after testing |

### Safety Checklist Before Import Testing
- [ ] Test data is in `temp/` directory
- [ ] Data contains sample/fake content only
- [ ] No real API keys or tokens in test files
- [ ] Environment variables set in `.env.local` only
- [ ] Run `gitleaks detect --no-git` to verify no secrets

## Import Testing Workflow

### Phase 1: Preparation
```bash
# 1. Navigate to temp directory
cd temp/

# 2. Create or copy test data template
cp ../templates/sample-import.json test-import-data.json

# 3. Edit test data (never use real user data)
# Edit the file to match your expected data structure
```

### Phase 2: Local Testing
```bash
# 1. Run validation script first
./test-import-script.py

# 2. Test with actual import command
../bin/tanachat-importjson test-import-data.json

# 3. Verify results
# Check your local database or storage to confirm import worked
```

### Phase 3: Real Data Testing (Optional)
```bash
# 1. Place real data in temp/ ONLY
cp /path/to/real-data.json temp/

# 2. Test import
../bin/tanachat-importjson temp/real-data.json

# 3. IMMEDIATELY remove real data
rm temp/real-data.json
```

### Phase 4: Cleanup
```bash
# 1. Remove test files
rm test-import-data.json

# 2. Verify no sensitive data left
gitleaks detect --no-git

# 3. Return to project root
cd ..
```

## Data Structure Templates

### Sample Import JSON Template
```json
{
  "conversations": [
    {
      "id": "test-conv-1",
      "title": "Sample Test Conversation",
      "created_at": "2024-01-15T10:00:00Z",
      "messages": [
        {
          "role": "user",
          "content": "This is a sample user message for testing",
          "timestamp": "2024-01-15T10:00:00Z"
        },
        {
          "role": "assistant",
          "content": "This is a sample assistant response for testing",
          "timestamp": "2024-01-15T10:00:30Z"
        }
      ],
      "tags": ["test", "sample", "testing"]
    }
  ],
  "metadata": {
    "total_conversations": 1,
    "import_date": "2024-12-10T10:37:00Z",
    "source": "test-data",
    "version": "1.0"
  }
}
```

## Security Rules

### RED FLAGS - Never Do These
- ❌ Commit real user data to git
- ❌ Store real data outside `temp/` directory
- ❌ Hardcode API keys in test files
- ❌ Use production credentials for testing
- ❌ Forget to run gitleaks before commits

### GREEN FLAGS - Always Do These
- ✅ Use `temp/` directory for all test data
- ✅ Create sample data that mimics real structure
- ✅ Use environment variables for credentials
- ✅ Run `gitleaks` before committing
- ✅ Clean up test files after validation

## Common Pitfalls and Solutions

### Pitfall 1: "I just need to test with real data quickly"
**Solution**: Create realistic sample data instead
```bash
# Instead of copying real data, create a sample version
cat > temp/realistic-test.json << 'EOF'
{
  "conversations": [
    {
      "id": "sample-conv-project-alpha",
      "title": "Project Alpha Planning Session",
      "messages": [
        {"role": "user", "content": "Let's plan the architecture for Project Alpha"},
        {"role": "assistant", "content": "I'll help you design a scalable architecture"}
      ]
    }
  ]
}
EOF
```

### Pitfall 2: "I'll just commit this temporarily and fix it later"
**Solution**: Use git worktrees or branches instead
```bash
# Create a temporary branch for testing
git checkout -b temp-import-testing
# Add your test files to temp/
# Test your import
# Discard the branch without merging
git checkout main
git branch -D temp-import-testing
```

### Pitfall 3: "My test data is safe, it's just sample content"
**Solution**: Run gitleaks anyway
```bash
# Even sample data can accidentally contain real patterns
gitleaks detect --no-git --no-banner
```

## Emergency Procedures

### If You Accidentally Commit Real Data
```bash
# 1. IMMEDIATE ACTION
git reset --hard HEAD~1

# 2. Check what was committed
git log --oneline -5

# 3. If already pushed, force push carefully
git push --force-with-lease origin main

# 4. Scan entire repository
gitleaks detect --no-banner

# 5. If data contained credentials, rotate them immediately
```

### If You're Unsure About Data Safety
```bash
# When in doubt, assume it's not safe
# 1. Move file to temp/ if not already there
mv suspect-file.json temp/

# 2. Create a safe sample version
# 3. Test with the sample version
# 4. Delete the original if not needed
```

## Integration with Development Tools

### VS Code Integration
Add this to your `.vscode/settings.json`:
```json
{
  "files.exclude": {
    "**/temp/*.json": true,
    "**/temp/*real*": true,
    "**/temp/*actual*": true
  },
  "search.exclude": {
    "**/temp/": true
  }
}
```

### Git Hooks (Optional)
Create `.git/hooks/pre-commit`:
```bash
#!/bin/sh
# Check for real data in temp/ directory
if find temp/ -name "*real*" -o -name "*actual*" 2>/dev/null | grep -q .; then
    echo "❌ Warning: Potential real data files detected in temp/"
    echo "Please remove or rename these files before committing"
    exit 1
fi

# Run gitleaks
gitleaks detect --no-git --no-banner
if [ $? -ne 0 ]; then
    echo "❌ Gitleaks detected potential secrets"
    exit 1
fi
```

## Testing Commands Reference

### Import Commands
```bash
# Test import with sample data
./bin/tanachat-importjson temp/test-import-data.json

# Test import with verbose output
./bin/tanachat-importjson temp/test-import-data.json --verbose

# Test import validation (dry run)
./bin/tanachat-importjson temp/test-import-data.json --dry-run
```

### Validation Commands
```bash
# Run the test validation script
./temp/test-import-script.py

# Check file structure
python3 -c "
import json
with open('temp/test-import-data.json') as f:
    data = json.load(f)
    print(f'Conversations: {len(data[\"conversations\"])}')
    print(f'Total messages: {sum(len(c[\"messages\"]) for c in data[\"conversations\"])}')
"

# Security scan
gitleaks detect --no-git --no-banner
```

## Support

If you encounter issues or have questions about import testing:
1. Check this document first
2. Review `CLAUDE.md` for general security rules
3. Create an issue using the `.claude/commands/issue.md` template
4. Ask in team channels, never share real data publicly