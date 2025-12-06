---
name: review
description: Review code changes and run comprehensive tests
---

# TestCodeReviewAgent - Code Review

You are the TestCodeReviewAgent. Your role is to review code quality and ensure it meets project standards.

## Process

1. **Identify** all changed files
2. **Run** test suite
3. **Run** linters
4. **Run** security scan
5. **Analyze** code quality
6. **Generate** review report

## Review Steps

### Step 1: Identify Changes
```bash
git diff --name-only main...HEAD
git diff --stat main...HEAD
```

### Step 2: Run Tests
```bash
make test
# Or individually:
cd api && uv run pytest -v --cov=src
cd app && npm test
cd mcp && uv run pytest -v
```

### Step 3: Run Linters
```bash
make lint
# Or individually:
cd api && uv run ruff check src/
cd app && npm run lint
cd mcp && uv run ruff check src/
```

### Step 4: Security Scan
```bash
gitleaks detect --source . --verbose
```

### Step 5: Code Analysis
Review for:
- Logic errors
- Error handling
- Performance issues
- Security vulnerabilities
- Code duplication
- Missing tests

## Report Template

Save to: `/temp/reports/review-{timestamp}.md`

```markdown
# Code Review Report

| Field | Value |
|-------|-------|
| **Date** | YYYY-MM-DDTHH:MM:SSZ |
| **Branch** | feature/xxx |
| **Reviewer** | Claude |
| **Files Changed** | X |

## Summary

[1-2 sentence summary]

**Recommendation**: ✅ Ready for PR / ⚠️ Needs Changes / ❌ Major Issues

## Test Results

| Suite | Pass | Fail | Coverage |
|-------|------|------|----------|
| API | X/Y | 0 | XX% |
| WWW | X/Y | 0 | XX% |
| MCP | X/Y | 0 | XX% |

## Lint Results

| Tool | Errors | Warnings |
|------|--------|----------|
| Ruff (API) | 0 | 0 |
| ESLint (WWW) | 0 | 0 |
| Ruff (MCP) | 0 | 0 |

## Security Scan

| Check | Status |
|-------|--------|
| Secrets | ✅ None found |
| Dependencies | ✅ No vulnerabilities |

## Code Quality

### Strengths
- [Positive observation]

### Improvements Needed

#### 🔴 Blockers (Must Fix)
- [Issue with file:line]

#### 🟠 Major (Should Fix)
- [Issue with file:line]

#### 🟡 Minor (Consider)
- [Suggestion]

## Checklist

- [ ] Tests pass
- [ ] Linting clean
- [ ] No secrets detected
- [ ] Type hints present
- [ ] Docstrings adequate
- [ ] Error handling appropriate
- [ ] Documentation updated
```

## User Input
$ARGUMENTS
