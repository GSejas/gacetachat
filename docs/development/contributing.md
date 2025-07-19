# Contributing Guide

## Overview
Guidelines for contributing to the GacetaChat project.

## Status
⚠️ **Documentation in Progress**

This section is under development. Please check back later or contribute to its development.

## Quick Start for Contributors

### Setting Up Development Environment
```bash
# Clone the repository
git clone https://github.com/gacetachat/gacetachat.git
cd gacetachat

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
tox -e smoke-test
```

### Code Standards
- Follow PEP 8 style guidelines
- Use Tox for testing: `tox -e py`
- Format code with Black: `tox -e format`
- Run linting: `tox -e lint`

### Documentation Standards
- Use MkDocs for documentation
- Test documentation build: `tox -e docs`
- Follow the [ASCII Mockup Standards](../ui-ux/ascii-mockup-standards.md)

## Contributing
See the main [Development Guide](../development/guide.md) for detailed development setup and practices.
