---
name: 🌴 Tana Integration Issue
about: Report issues related to Tana API, workspace parsing, or data synchronization
title: '[TANA] '
labels: ['tana-integration', 'needs-triage']
assignees: []

---

## <4 Tana Integration Type
- [ ] **API Integration**: Issues with Tana API calls
- [ ] **Import/Export**: Problems with Tana JSON processing
- [ ] **Workspace Parsing**: Issues interpreting Tana workspace structure
- [ ] **Supertag Handling**: Problems with supertag metadata or keytags
- [ ] ** MCP Server**: Issues with Claude Desktop integration
- [ ] **Synchronization**: Data sync problems between systems

## =� Issue Description
Clear description of the Tana-related issue.

## = Reproduction Steps
Steps to reproduce the Tana integration issue:

1. Export from Tana: [Describe the export process]
2. Process with TanaChat: [Which tool/command was used]
3. Observe issue: [What went wrong]

### Tana Export Details
- **Export Format**: [Tana Intermediate Format / JSON]
- **Export Size**: [Number of nodes, file size]
- **Workspace Structure**: [Brief description of workspace complexity]
- **Supertags Used**: [List relevant supertags]

## =' TanaChat Configuration
- **Command Used**: [e.g. `./bin/tana-importjson`, MCP tool]
- **Options/Parameters**: [List all options used]
- **Environment**: [Docker, local dev, production]

## L Actual Behavior
What happened instead of the expected behavior?

### Error Messages
```
Paste any error messages here
```

### Log Output
```bash
# Include relevant TanaChat logs
```

##  Expected Behavior
What should have happened?

## <4 Tana Workspace Context
If applicable, provide sanitized examples of:

### Node Structure
```json
{
  "type": "node",
  "name": "Example Node",
  "supertags": ["#project"],
  "children": [...]
}
```

### Supertag Definitions
```
#project
    field:: Status
    field:: Due Date
    field:: Assignee
```

## = Troubleshooting Steps Taken
What have you already tried to resolve this?

## =� Additional Files
- [ ] Tana export file (sanitized)
- [ ] TanaChat output files
- [ ] Screenshots of error
- [ ] Configuration files

## = Related Issues
- Related issue #1
- Similar issue #2

## =� Additional Context
Any other context about the Tana integration issue.