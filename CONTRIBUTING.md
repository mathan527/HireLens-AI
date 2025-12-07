# Contributing to HireLens AI

Thank you for your interest in contributing to HireLens AI! 🎉

## 🤝 How to Contribute

### Reporting Bugs
- Use the GitHub Issues tab
- Include detailed steps to reproduce
- Provide system information (OS, Python version, etc.)
- Include error messages and logs

### Suggesting Features
- Open a GitHub Issue with the "enhancement" label
- Describe the feature and its benefits
- Include mockups or examples if applicable

### Pull Requests
1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Write/update tests if applicable
5. Update documentation
6. Commit with clear messages: `git commit -m "Add feature: description"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## 📋 Code Standards

### Python Backend
- Follow PEP 8 style guide
- Use type hints for all functions
- Add docstrings to public functions
- Write unit tests for new features
- Ensure all tests pass before submitting

### JavaScript Frontend
- Use ES6+ syntax
- Follow consistent naming conventions
- Add comments for complex logic
- Ensure responsive design

### Commit Messages
- Use present tense: "Add feature" not "Added feature"
- Be descriptive but concise
- Reference issues: "Fix #123: Bug description"

## 🧪 Testing

Run tests before submitting:
```bash
# Backend tests (when available)
pytest tests/ -v

# Linting
flake8 backend/
black backend/ --check
```

## 📖 Documentation

- Update README.md if adding features
- Add API documentation for new endpoints
- Include code examples where helpful

## 🔒 Security

- Never commit API keys or secrets
- Report security vulnerabilities privately to [security@hirelens.ai]
- Use `.env` for sensitive configuration

## ❓ Questions?

- Open a GitHub Discussion
- Check existing issues and documentation
- Reach out to maintainers

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making HireLens AI better! 🚀**
