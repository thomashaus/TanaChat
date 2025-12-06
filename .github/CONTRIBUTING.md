# Contributing to TanaChat

Thank you for your interest in contributing to TanaChat! This document provides guidelines and information for contributors.

## 🎯 How to Contribute

### Reporting Issues

- **Bug Reports**: Use the [🐛 Bug Report](https://github.com/thomashaus/TanaChat/issues/new?assignees=&labels=bug&template=bug_report.md) template
- **Feature Requests**: Use the [🚀 Feature Request](https://github.com/thomashaus/TanaChat/issues/new?assignees=&labels=enhancement&template=feature_request.md) template
- **Tana Integration Issues**: Use the [🌴 Tana Integration](https://github.com/thomashaus/TanaChat/issues/new?assignees=&labels=tana-integration&template=tana_integration.md) template
- **Documentation Issues**: Use the [📚 Documentation](https://github.com/thomashaus/TanaChat/issues/new?assignees=&labels=documentation&template=documentation.md) template

### Submitting Changes

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes following our guidelines
4. **Test** your changes thoroughly
5. **Commit** your changes with clear messages
6. **Push** to your fork: `git push origin feature/amazing-feature`
7. **Create** a Pull Request using our template

## 🏗 Development Setup

### Prerequisites

- **Python 3.10+** for backend and CLI tools
- **Node.js 18+** for frontend
- **Docker** for containerized development
- **Tana API key** for Tana integration features

### Quick Start

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/TanaChat.git
cd TanaChat

# Install dependencies and setup environment
make setup

# Start development services
make dev

# Run tests
make test
```

### Project Structure

```
TanaChat/
├── api/              # FastAPI backend
├── app/              # React frontend
├── mcp/              # MCP server for Claude Desktop
├── bin/              # CLI tools
├── lib/              # Shared Python libraries
├── tests/            # Test suite
├── docs/             # Documentation
├── scripts/          # Utility scripts
└── .github/          # GitHub configuration
```

## 📝 Coding Standards

### Python

- **Style**: Follow PEP 8 and use Black for formatting
- **Type Hints**: Use type hints for all public functions
- **Docstrings**: Use Google-style docstrings
- **Testing**: Write tests for all new functionality

```bash
# Format code
make format

# Lint code
make lint

# Run type checking
mypy src/
```

### TypeScript/JavaScript

- **Style**: Use ESLint and Prettier
- **Type Safety**: Use TypeScript features
- **Components**: Follow React best practices
- **Testing**: Write tests for new components

```bash
# From app/ directory
npm run lint
npm run format
npm test
```

### Git Commits

Use conventional commit messages:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

Examples:
```
feat(api): add user authentication endpoints
fix(cli): resolve tana-importjson memory leak
docs(readme): update installation instructions
```

## 🧪 Testing

### Running Tests

```bash
# All tests
make test

# Python tests only
pytest tests/

# Frontend tests only
cd app && npm test

# Integration tests
pytest tests/test_integration.py

# Performance tests
pytest tests/test_performance.py
```

### Writing Tests

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test service interactions
- **Performance Tests**: Ensure acceptable performance
- **Security Tests**: Verify security measures work

### Test Coverage

- Maintain at least 80% test coverage
- Add tests for all new features
- Ensure critical paths are well-tested

## 🔍 Code Review Process

### Before Submitting

1. **Self-review**: Review your own changes
2. **Test thoroughly**: Ensure all tests pass
3. **Documentation**: Update relevant documentation
4. **Style checks**: Ensure code follows project style

### Review Guidelines

Reviewers should check:
- **Correctness**: Does the code work as intended?
- **Performance**: Is the code efficient?
- **Security**: Are there any security implications?
- **Documentation**: Is the code well-documented?
- **Testing**: Are there adequate tests?

### Approval Requirements

- **At least one** approval from a maintainer
- **All automated checks** must pass
- **Security reviews** for sensitive changes
- **Breaking changes** require additional review

## 🌴 Tana Integration Guidelines

### API Usage

- **Rate Limiting**: Respect Tana API rate limits
- **Error Handling**: Handle API errors gracefully
- **Authentication**: Secure API key management
- **Data Validation**: Validate Tana data before processing

### Workspace Processing

- **Performance**: Handle large workspaces efficiently
- **Memory**: Optimize memory usage for large exports
- **Validation**: Validate Tana JSON format
- **Supertags**: Handle supertag metadata correctly

### Testing Tana Features

- **Mock API**: Use mock responses for unit tests
- **Test Data**: Use sanitized test workspaces
- **Integration**: Test with real Tana workspaces when possible

## 📚 Documentation

### Types of Documentation

- **API Documentation**: OpenAPI specifications
- **User Guides**: How-to guides and tutorials
- **Developer Docs**: Architecture and development guides
- **CLI Reference**: Command-line tool documentation

### Writing Documentation

- **Clear Language**: Use simple, clear language
- **Examples**: Provide code examples
- **Screenshots**: Include relevant screenshots
- **Up-to-date**: Keep documentation current

## 🚀 Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. **Tests**: All tests pass
2. **Documentation**: Updated and accurate
3. **Changelog**: Comprehensive changelog
4. **Security**: No known security issues
5. **Performance**: Acceptable performance

## 🏷️ Labels and Issues

### Issue Labels

- `bug`: Bug reports
- `enhancement`: Feature requests
- `documentation`: Documentation issues
- `tana-integration`: Tana-specific issues
- `security`: Security-related issues
- `performance`: Performance issues
- `dependencies`: Dependency updates

### Priority Levels

- `high`: Urgent issues, release blockers
- `medium`: Important issues, next release
- `low`: Nice to have, future consideration

## 💬 Communication

### Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and ideas
- **Discord**: Community discussions (link in README)

### Community Guidelines

- **Respect**: Be respectful and inclusive
- **Constructive**: Provide constructive feedback
- **Helpful**: Help others when possible
- **Patient**: Be patient with newcomers

## 🔒 Security

### Reporting Security Issues

- **Private**: Report security issues privately
- **Email**: security@tanachat.ai
- **Responsible**: Follow responsible disclosure

### Security Best Practices

- **No secrets**: Never commit secrets or keys
- **Validation**: Validate all inputs
- **Dependencies**: Keep dependencies updated
- **Review**: Review code for security issues

## 🎉 Recognition

### Contributors

We recognize and appreciate all contributions:
- **Contributors list**: Maintained in README
- **Release notes**: Mention significant contributors
- **Community**: Highlight helpful community members

### Ways to Contribute

- **Code**: Bug fixes, features, improvements
- **Documentation**: Guides, tutorials, examples
- **Testing**: Bug reports, test cases
- **Community**: Help others, share feedback
- **Design**: UI/UX improvements, graphics

## 📄 License

By contributing to TanaChat, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## 🤝 Thank You

Thank you for contributing to TanaChat! Your contributions help make Tana workspace management better for everyone.

If you have any questions about contributing, feel free to:
- Open an issue with the "question" label
- Start a discussion in GitHub Discussions
- Contact us at [community@tanachat.ai](mailto:community@tanachat.ai)

Happy coding! 🚀