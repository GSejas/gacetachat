# Contributing to GacetaChat

Thank you for considering contributing to GacetaChat! This project is public democratic infrastructure for Costa Rica, and we welcome contributions that help strengthen transparency and civic participation.

## Current Status

**We're in the planning/funding phase.** The V1 prototype has been archived, and we're preparing for a complete rewrite (see [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)).

## How to Contribute

### 🎯 High-Priority Contributions

1. **Grant Writing** - Help apply for funding ($30k target)
2. **NGO Partnerships** - Connect us with Costa Rican environmental/transparency NGOs
3. **Design Feedback** - Review UI mockups and suggest improvements
4. **Documentation** - Improve setup guides, translate docs

### 🔧 Code Contributions (After Funding)

Once we secure funding and begin the 4-week development sprint, we'll need:
- React/Next.js developers (frontend)
- Python/FastAPI developers (backend)
- DevOps help (deployment, CI/CD)

**For now:** Please don't submit PRs for new features. Focus on documentation and planning.

## Contribution Guidelines

### Reporting Issues

- **Bugs:** Open an issue with steps to reproduce
- **Feature requests:** Explain the use case and why it's important for NGOs/citizens
- **Questions:** Check existing issues first, then open a new one

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests: `pytest -v`
5. Commit with clear messages (see below)
6. Push and open a PR

### Commit Message Format

```
<type>: <subject>

<body>

🤖 Generated with Claude Code (if applicable)

Co-Authored-By: Your Name <your@email.com>
```

**Types:** feat, fix, docs, test, refactor, chore

**Examples:**
```
feat: Add WhatsApp notification support for NGOs

Implements Twilio integration for sending daily summaries
via WhatsApp. Includes rate limiting and opt-in/opt-out.

🤖 Generated with Claude Code

Co-Authored-By: María González <maria@example.com>
```

### Code Style

- **Python:** Follow PEP 8, use `black` for formatting
- **JavaScript/TypeScript:** Follow Airbnb style guide, use Prettier
- **Commits:** Use conventional commits format
- **Tests:** Write tests for new features

### Testing

```bash
# Install dependencies
uv pip install pytest pytest-mock pytest-cov

# Run all tests
pytest -v

# Run specific test file
pytest tests/test_scraper_unit.py -v

# Check coverage
pytest --cov=scripts --cov-report=term-missing
```

## Development Setup

### Local Development

```bash
# Clone the repository
git clone https://github.com/GSejas/gacetachat.git
cd gacetachat

# Install dependencies
uv pip install -r requirements.txt

# Run demo locally
uv run demo_simple.py
```

### Environment Variables

Create `.env` file (see `.env.example`):
```
OPENAI_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here  # For NGO signup form
```

## Project Structure

```
gacetachat/
├── demo_simple.py           # Streamlit demo (current)
├── scripts/                 # Daily scraper scripts
├── tests/                   # Test suite
├── docs/                    # Documentation
├── data/                    # Summaries and data files
└── archive/v1/             # Old prototype (archived)
```

## Community

- **Issues:** https://github.com/GSejas/gacetachat/issues
- **Discussions:** Use GitHub Discussions for questions
- **Email:** contact@gacetachat.cr

## License

By contributing, you agree that your contributions will be licensed under the MIT License (see [LICENSE](LICENSE)).

## Recognition

Contributors will be recognized in:
- README.md contributors section (coming soon)
- Release notes
- Project documentation

## Questions?

Open an issue with the `question` label, or email contact@gacetachat.cr.

---

**Thank you for helping build public democratic infrastructure for Costa Rica!** 🇨🇷
