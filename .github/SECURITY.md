# Security Policy

## 🛡️ Security

At TanaChat, we take security seriously. This document outlines our security policy and procedures.

## 📋 Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.1.x   | :white_check_mark: |

## 🔍 Reporting a Vulnerability

If you discover a security vulnerability in TanaChat, please report it to us privately before disclosing it publicly.

### How to Report

**Email**: security@tanachat.ai

Please include as much information as possible:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any screenshots or logs

### Response Time

We aim to respond to security reports within **48 hours** and provide a fix within **7 days** for critical vulnerabilities.

### What to Expect

1. **Acknowledgment**: We'll confirm receipt of your report within 48 hours
2. **Assessment**: We'll investigate and validate the vulnerability
3. **Resolution**: We'll develop and test a fix
4. **Disclosure**: We'll coordinate public disclosure with you

## 🔒 Security Features

### Authentication & Authorization
- JWT-based authentication
- User-scoped data isolation
- Secure password handling
- API key management for Tana integration

### Data Protection
- Encrypted data transmission (HTTPS)
- Secure file storage with DigitalOcean Spaces
- Input validation and sanitization
- SQL injection prevention

### Infrastructure Security
- Regular security scans with Gitleaks
- Dependency vulnerability monitoring
- Docker container security
- Environment variable protection

## 🚨 Security Best Practices

### For Users

1. **API Keys**: Never share your Tana API key
2. **Authentication**: Use strong passwords and enable 2FA when available
3. **Network**: Use TanaChat over secure networks only
4. **Updates**: Keep your TanaChat installation updated

### For Developers

1. **Environment Variables**: Never commit sensitive data
2. **Dependencies**: Regularly update dependencies
3. **Code Review**: All code changes require review
4. **Testing**: Include security tests in your workflow

## 🔧 Security Headers

TanaChat implements the following security headers:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

## 📊 Security Monitoring

We monitor for:
- Authentication failures
- Unusual API usage patterns
- Suspicious file access
- Security vulnerability disclosures

## 🤝 Responsible Disclosure Program

We believe in responsible disclosure and will work with researchers to ensure security issues are addressed appropriately.

### Guidelines

- Don't exploit vulnerabilities beyond what's necessary for demonstration
- Provide sufficient detail for us to reproduce the issue
- Allow us reasonable time to respond before public disclosure
- Follow any additional requests we may make regarding the vulnerability

### Recognition

We appreciate security research and will acknowledge researchers who responsibly disclose vulnerabilities (with their permission).

## 📞 Contact

For security-related questions:
- **Security Issues**: security@tanachat.ai
- **General Security Questions**: security@tanachat.ai

For non-security issues, please use our [GitHub Issues](https://github.com/thomashaus/TanaChat/issues).

---

## 🔄 Security Updates

Stay informed about security updates by:
- Watching our [GitHub repository](https://github.com/thomashaus/TanaChat)
- Subscribing to our security advisory notifications
- Following our security blog for announcements

Thank you for helping keep TanaChat secure! 🙏