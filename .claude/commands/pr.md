---
name: pr
description: Create a pull request from reviewed changes
---

# Create Pull Request

Create a well-documented pull request for the current changes.

## Process

1. **Verify** review report exists and passes
2. **Collect** all commits since branch creation
3. **Generate** PR description
4. **Link** to spec and issues
5. **Create** PR

## Pre-PR Checklist

```bash
# Ensure on feature branch
git branch --show-current

# Ensure all changes committed
git status

# Ensure tests pass
make test

# Ensure lint passes
make lint

# Check review report exists
ls temp/reports/review-*.md
```

## PR Template

```markdown
## Summary

[2-3 sentence summary of changes]

## Related

- **Spec**: [SPEC-XXX](docs/specs/SPEC-XXX-name.md)
- **Issue**: Closes #XX

## Changes

### Added
- [New feature/file]

### Changed
- [Modified behavior]

### Fixed
- [Bug fix]

## Type of Change

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to change)
- [ ] 📚 Documentation update
- [ ] 🔧 Refactor (no functional changes)

## Testing

### Test Results
- API: X/Y passing
- WWW: X/Y passing
- MCP: X/Y passing

### Manual Testing
- [ ] Tested locally
- [ ] Tested MCP with inspector

## Checklist

- [ ] My code follows the project style guidelines
- [ ] I have performed a self-review
- [ ] I have added tests for my changes
- [ ] All tests pass locally
- [ ] I have updated documentation
- [ ] I have updated the spec status to "Implemented"
- [ ] I have verified no real user data is committed
- [ ] I have run gitleaks and confirmed no secrets
- [ ] Import-related changes use temp/ directory only

## Review Report

See: `temp/reports/review-TIMESTAMP.md`
```

## Create PR Commands

```bash
# Push branch
git push -u origin $(git branch --show-current)

# Create PR with GitHub CLI
gh pr create \
  --title "feat: [Title from spec]" \
  --body-file pr-description.md \
  --base main

# Or open in browser
gh pr create --web
```

## User Input
$ARGUMENTS
