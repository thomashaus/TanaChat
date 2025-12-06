# Archiving Workflow

This workflow defines when and how to move completed specifications and plans to the archive.

## When to Archive

Move documents to `docs/archive/` when:

1. **Specifications** are fully implemented and deployed
2. **Plans** are completed and no longer active
3. **Documentation** is outdated but kept for historical reference
4. **Temporary files** have served their purpose

## Archive Process

1. **Verify Completion**
   ```bash
   # Check if spec is fully implemented
   grep -r "SPEC-ID" --include="*.py" --include="*.ts" src/

   # Verify deployment
   git log --oneline --grep="SPEC-ID"
   ```

2. **Create Archive Entry**
   ```bash
   # Create archive directory if needed
   mkdir -p docs/archive

   # Move with timestamp
   mv docs/specs/SPEC-ID-feature-name.md docs/archive/2024-12-SPEC-ID-feature-name.md
   ```

3. **Update References**
   ```bash
   # Find and update references
   grep -r "SPEC-ID" . --exclude-dir=archive
   ```

4. **Document**
   Add to `docs/archive/README.md`:
   ```markdown
   - `2024-12-SPEC-ID-feature-name.md` - Implemented feature X (moved 2024-12-04)
   ```

## Archive Structure

```
docs/archive/
├── README.md              # Index of archived items
├── 2024-12-SECURITY.md    # Security implementation (completed)
├── 2024-12-DEPLOYMENT.md  # Deployment setup (completed)
├── 2024-12-temp-SetupProject.md  # Initial project setup (completed)
└── 2024-12-SPEC-XXX.md    # Archived specs with timestamp
```

## Accessing Archived Content

Archived content is read-only but can be referenced:

```bash
# View archive contents
ls -la docs/archive/

# Find specific archived spec
find docs/archive -name "*SPEC-ID*"
```