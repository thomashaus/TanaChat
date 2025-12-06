# Contributing to TanaChat.ai

Thank you for your interest in contributing to TanaChat.ai! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- Docker (optional, for containerized development)

### Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/TanaChat.git
   cd TanaChat
   ```
3. Install dependencies:
   ```bash
   make setup
   ```
4. Copy environment configuration:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your settings
   ```
5. Start development:
   ```bash
   make dev
   ```

## 📋 Development Workflow

### Branch Organization

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Critical fixes for production

### Making Changes

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes with atomic, well-documented commits
3. Test your changes thoroughly
4. Ensure code formatting:
   ```bash
   make format
   make lint
   make test
   ```
5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Open a Pull Request

### Code Style

- **Python**: Follow PEP 8, use black for formatting
- **TypeScript/JavaScript**: Use ESLint and Prettier configurations
- **Commit messages**: Follow conventional commits format

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run API tests
cd api && uv run pytest

# Run frontend tests
cd app && npm test
```

### Test Coverage

Maintain test coverage above 80% for new code. Write tests for:
- New features
- Bug fixes
- Critical paths

## 📝 Documentation

- Update README.md for user-facing changes
- Add inline documentation for complex code
- Update API docs for endpoint changes
- Consider adding examples for new features

## 🐛 Bug Reports

When filing bug reports:
1. Use the provided bug report template
2. Include steps to reproduce
3. Provide environment details
4. Add relevant logs or screenshots

## 💡 Feature Requests

1. Check existing issues first
2. Use the feature request template
3. Describe the use case clearly
4. Consider implementation complexity

## 🔒 Security

If you discover a security vulnerability:
1. Don't open a public issue
2. Email security@tanachat.ai with details
3. We'll respond within 48 hours

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤝 Community

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)

## 🏆 Recognition

Contributors will be:
- Listed in our contributors section
- Mentioned in release notes for significant contributions
- Invited to our contributor Discord channel

Thank you for contributing to TanaChat.ai! 🙏