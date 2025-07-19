# Tox Migration and Usage Guide for GacetaChat

## Overview

This guide will help you migrate to using Tox for automated testing, linting, documentation building, and quality assurance in the GacetaChat project.

## What is Tox?

Tox is a generic virtual environment management and test command line tool that allows you to:
- Test your package against multiple Python versions
- Run linting and code quality checks
- Build documentation
- Automate development workflows
- Ensure consistent environments across different systems

## Installation

### 1. Install Tox

```bash
# Install tox globally
pip install tox

# Or install with development dependencies
pip install -r requirements-dev.txt
```

### 2. Verify Installation

```bash
tox --version
```

## Configuration Files

The following files have been created for Tox configuration:

### `tox.ini` - Main configuration file
- Defines test environments (Python versions, dependencies)
- Configures linting, formatting, documentation building
- Sets up smoke tests and performance tests

### `requirements-dev.txt` - Development dependencies
- All tools needed for development and testing
- Used by Tox environments

## Available Tox Environments

### Core Testing Environments

#### `tox -e py` - Run tests with default Python version
```bash
tox -e py
```
- Runs all tests in the `test/` directory
- Includes coverage reporting
- Generates HTML coverage report

#### `tox -e py39,py310,py311` - Test multiple Python versions
```bash
tox -e py39,py310,py311
```
- Tests compatibility across Python versions
- Requires multiple Python versions installed

### Code Quality Environments

#### `tox -e lint` - Run linting checks
```bash
tox -e lint
```
- Flake8 for style checking
- MyPy for type checking
- Bandit for security analysis

#### `tox -e format` - Auto-format code
```bash
tox -e format
```
- Removes unused imports with autoflake
- Sorts imports with isort
- Formats code with black

#### `tox -e format-check` - Check formatting without changes
```bash
tox -e format-check
```
- Checks if code is properly formatted
- Exits with error if formatting needed

### Documentation Environments

#### `tox -e docs` - Build and serve documentation
```bash
tox -e docs
```
- Builds MkDocs documentation
- Serves on localhost:8001
- Watches for changes in development

#### `tox -e docs-deploy` - Deploy documentation
```bash
tox -e docs-deploy latest
```
- Deploys documentation with versioning
- Uses Mike for version management

### Specialized Testing Environments

#### `tox -e smoke-test` - Run smoke tests
```bash
tox -e smoke-test
```
- Quick verification that basic functionality works
- Tests imports, configuration, basic operations
- Fast execution for CI/CD pipelines

#### `tox -e integration` - Run integration tests
```bash
tox -e integration
```
- Tests interaction between components
- May use Docker containers for external services

#### `tox -e performance` - Run performance tests
```bash
tox -e performance
```
- Benchmarks critical functions
- Memory usage analysis
- Performance regression detection

#### `tox -e security` - Run security checks
```bash
tox -e security
```
- Bandit security analysis
- Safety dependency vulnerability check
- Pip-audit for known vulnerabilities

### Utility Environments

#### `tox -e clean` - Clean build artifacts
```bash
tox -e clean
```
- Removes cache directories
- Cleans build artifacts
- Resets environment

## Migration Steps

### Step 1: Backup Current Setup
```bash
# Create backup of current dependencies
cp requirements.txt requirements-backup.txt
```

### Step 2: Install Development Dependencies
```bash
pip install -r requirements-dev.txt
```

### Step 3: Run Initial Tests
```bash
# Run smoke tests to verify basic functionality
tox -e smoke-test

# Run full test suite
tox -e py
```

### Step 4: Set Up Pre-commit Hooks (Optional)
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: local
    hooks:
      - id: tox-lint
        name: tox lint
        entry: tox -e lint
        language: system
        pass_filenames: false
      - id: tox-format-check
        name: tox format check
        entry: tox -e format-check
        language: system
        pass_filenames: false
EOF

# Install hooks
pre-commit install
```

### Step 5: Update CI/CD Pipeline
```yaml
# Example GitHub Actions workflow
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install tox
    
    - name: Run tests
      run: tox -e py
    
    - name: Run linting
      run: tox -e lint
    
    - name: Run smoke tests
      run: tox -e smoke-test
```

## Common Commands

### Daily Development Workflow
```bash
# Format code before committing
tox -e format

# Run tests and linting
tox -e py,lint

# Build documentation
tox -e docs
```

### Pre-commit Workflow
```bash
# Check formatting
tox -e format-check

# Run smoke tests (quick verification)
tox -e smoke-test

# Run security checks
tox -e security
```

### Release Workflow
```bash
# Run all tests
tox

# Run performance tests
tox -e performance

# Build and deploy docs
tox -e docs-deploy
```

## Troubleshooting

### Common Issues

#### 1. Python Version Not Found
```bash
# Install required Python versions
pyenv install 3.9.16
pyenv install 3.10.11
pyenv install 3.11.4

# Or skip missing interpreters
tox --skip-missing-interpreters
```

#### 2. Dependency Conflicts
```bash
# Recreate environments
tox -r

# Clean and recreate
tox -e clean
tox -r
```

#### 3. Test Failures
```bash
# Run specific test
tox -e py -- test/specific_test.py::test_function

# Verbose output
tox -e py -- -v

# Stop on first failure
tox -e py -- -x
```

#### 4. Import Errors in Tests
```bash
# Check PYTHONPATH
tox -e py -- --pdb

# Debug environment
tox -e py --recreate
```

### Environment Variables

Set these in your development environment:

```bash
# For testing
export TESTING=true
export OPENAI_API_KEY=test-api-key
export DATABASE_URL=sqlite:///test.db

# For CI/CD
export SKIP_SERVER_TESTS=true  # Skip server startup tests in CI
export SMOKE_TEST=true         # Enable smoke test mode
```

## Best Practices

### 1. Test Organization
- Use smoke tests for quick verification
- Use integration tests for component interaction
- Use performance tests for benchmarking

### 2. Environment Management
- Use `tox -r` to recreate environments when dependencies change
- Use `tox -e clean` to clean up artifacts
- Keep environments isolated

### 3. CI/CD Integration
- Run smoke tests first (fast feedback)
- Run full test suite on multiple Python versions
- Use caching to speed up CI runs

### 4. Documentation
- Build docs locally before committing
- Use versioned documentation deployment
- Keep documentation dependencies separate

## Monitoring and Maintenance

### Regular Tasks
```bash
# Weekly: Update dependencies and run full test suite
tox -r
pip-audit --format=json --output=security-report.json

# Monthly: Review test coverage
tox -e py -- --cov-report=html
open htmlcov/index.html

# Before releases: Run all checks
tox -e clean
tox
tox -e security
tox -e performance
```

### Performance Monitoring
```bash
# Track test performance
tox -e performance -- --benchmark-json=results.json

# Monitor memory usage
tox -e py -- --memprof
```

This setup provides a robust foundation for development workflow automation, ensuring code quality, proper testing, and consistent environments across the GacetaChat project.
