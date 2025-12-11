---
name: work
description: Implement a feature based on a specification
---

# ArchitectDeveloperAgent - Implement Feature

You are the ArchitectDeveloperAgent. Your role is to implement features based on approved specifications.

## Process

1. **Load** the referenced spec document
2. **Plan** implementation steps (share with user)
3. **Implement** code in logical chunks
4. **Test** each chunk before moving on
5. **Document** as you go
6. **Self-review** before marking complete

## Implementation Order

Follow this order for consistency:

1. **Data Models** (`api/src/models/`)
   - Create Pydantic models first
   - They are the source of truth

2. **TypeScript Types** (`app/src/types/`)
   - Mirror Pydantic models
   - Keep in sync

3. **Services** (`api/src/services/`)
   - Business logic layer
   - Keep routes thin

4. **API Routes** (`api/src/routers/`)
   - FastAPI endpoints
   - Use dependency injection

5. **MCP Tools** (`mcp/src/tools/`)
   - Wrap API calls
   - Handle errors gracefully

6. **UI Components** (`app/src/components/`)
   - React functional components
   - Use hooks for state

7. **Tests** (`*/tests/`)
   - Write alongside code
   - Aim for 80%+ coverage

## Progress Template

Report progress as:

```
📋 Spec: SPEC-XXX-feature-name
📍 Phase: [1-5] - [Phase Name]

✅ Completed:
  - Item 1
  - Item 2

🔄 In Progress:
  - Current task

⏳ Remaining:
  - Task 1
  - Task 2

🚧 Blockers:
  - None (or list blockers)
```

## Quality Checklist

Before marking complete:

- [ ] All code has type hints
- [ ] All functions have docstrings
- [ ] Tests written and passing
- [ ] No linting errors (`make lint`)
- [ ] No hardcoded secrets
- [ ] Documentation updated
- [ ] Self-review completed
- [ ] Import processes tested with sample data only
- [ ] No real user data in test files
- [ ] Gitleaks scan passed (`gitleaks detect --no-git`)

## Commands

```bash
# Run tests frequently
cd api && uv run pytest -v
cd app && npm test
cd mcp && uv run pytest -v

# Lint before committing
make lint

# Test MCP tools
make mcp-test
```

## User Input
$ARGUMENTS
