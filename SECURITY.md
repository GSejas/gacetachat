# Security Policy

## Supported Versions

GacetaChat is currently in Alpha development. Security updates will be applied to:

| Version | Supported          |
| ------- | ------------------ |
| 2.x     | ✅ Active development |
| 1.x     | ❌ Archived (no longer maintained) |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

### How to Report

Email security concerns to: **security@gacetachat.cr**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if applicable)

### What to Expect

- **Acknowledgment:** Within 48 hours
- **Assessment:** Within 7 days
- **Fix timeline:** Depends on severity
  - Critical: 24-48 hours
  - High: 7 days
  - Medium: 30 days
  - Low: Next release cycle

### Disclosure Policy

We follow responsible disclosure:
1. Report received and acknowledged
2. Vulnerability confirmed and assessed
3. Fix developed and tested
4. Security advisory published
5. CVE assigned (if applicable)

## Security Best Practices

### For Users

- Keep dependencies updated
- Don't share API keys or tokens
- Use environment variables for secrets
- Enable 2FA on your GitHub account

### For Contributors

- Never commit secrets (`.env` files, API keys, passwords)
- Use `.gitignore` to exclude sensitive files
- Sanitize user inputs
- Follow OWASP guidelines for web security
- Run security checks: `pip-audit`, `bandit`

### For Self-Hosters

- Use HTTPS in production
- Set strong passwords
- Keep Python and dependencies updated
- Monitor access logs
- Use secrets management (e.g., GitHub Secrets, HashiCorp Vault)

## Known Security Considerations

### Current Implementation

✅ **Secure:**
- API keys stored in environment variables
- GitHub token with minimal permissions (`public_repo`)
- No user authentication (no passwords to leak)
- Open source (community auditable)
- Daily scraper runs in isolated GitHub Actions

⚠️ **Limitations (Alpha):**
- No rate limiting on NGO signup form (TODO for production)
- Streamlit demo has no auth (public access by design)
- PDF scraping could be abused (TODO: implement scraping limits)

### Production Roadmap (v2.0)

- [ ] Rate limiting on API endpoints
- [ ] CAPTCHA on forms
- [ ] Input sanitization and validation
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS protection (CSP headers)
- [ ] CSRF tokens for forms
- [ ] Dependency vulnerability scanning in CI/CD
- [ ] Security headers (HSTS, X-Frame-Options, etc.)

## Security Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Python Security Best Practices: https://python.readthedocs.io/en/stable/library/security_warnings.html
- Streamlit Security: https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso

## Third-Party Dependencies

We monitor security advisories for:
- Python packages: `pip-audit`, Dependabot
- GitHub Actions: Dependabot
- Docker images: Trivy (planned)

## Bug Bounty

**We currently do not have a bug bounty program.** However, we deeply appreciate responsible disclosure and will publicly acknowledge security researchers who help us improve GacetaChat.

---

**Contact:** security@gacetachat.cr
**PGP Key:** (Coming soon)
