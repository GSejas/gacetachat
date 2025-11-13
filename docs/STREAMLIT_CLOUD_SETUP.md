# Streamlit Cloud Setup Guide

## Overview
This guide shows how to configure GacetaChat's demo on Streamlit Cloud to capture NGO signups using GitHub Issues API.

---

## Step 1: Create GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Name it: `GacetaChat Streamlit Form`
4. Set expiration: **No expiration** (or 1 year)
5. Select scopes:
   - ✅ **`public_repo`** (to create issues on public repos)
6. Click **"Generate token"**
7. **IMPORTANT:** Copy the token immediately (you won't see it again)
   - Example: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## Step 2: Add Token to Streamlit Cloud Secrets

1. Go to your Streamlit Cloud dashboard: https://share.streamlit.io/
2. Find your GacetaChat app
3. Click the **⚙️ Settings** button
4. Go to **"Secrets"** tab
5. Add this TOML configuration:

```toml
# .streamlit/secrets.toml (Streamlit Cloud)
GITHUB_TOKEN = "ghp_your_token_here"
```

6. Click **"Save"**
7. App will automatically reboot with the new secret

---

## Step 3: Test the Form

1. Visit your Streamlit app: https://gacetachat.streamlit.app/
2. Go to the **"Para Organizaciones"** tab
3. Fill out the form with test data
4. Click **"Registrar Organización"**
5. You should see: ✅ Success message
6. Check GitHub: https://github.com/GSejas/gacetachat/issues
7. You should see a new issue titled: **"NGO Signup: [Organization Name]"**

---

## How It Works

### Production (Streamlit Cloud with token)
```
User fills form → Streamlit calls GitHub API → Creates issue → You get email notification
```

### Local Development (without token)
```
User fills form → Streamlit saves to data/ngo_signups.json → Manual review
```

### Fallback (API failure)
```
GitHub API fails → Streamlit saves locally → Shows warning to user
```

---

## Benefits of GitHub Issues Approach

✅ **Email notifications** - Automatic when someone signs up
✅ **No database needed** - GitHub handles storage
✅ **Free forever** - No API costs
✅ **Searchable** - Use GitHub's issue search
✅ **Collaborative** - Team can comment/assign
✅ **Trackable** - Close issues when contacted
✅ **Works in Streamlit Cloud** - No filesystem access needed

---

## Viewing Signups

### On GitHub
- **All signups:** https://github.com/GSejas/gacetachat/issues?q=is%3Aissue+label%3Ango-signup
- **Open (not contacted yet):** https://github.com/GSejas/gacetachat/issues?q=is%3Aopen+label%3Ango-signup
- **Closed (contacted):** https://github.com/GSejas/gacetachat/issues?q=is%3Aclosed+label%3Ango-signup

### Email Notifications
- You'll receive an email for each new issue created
- Configure at: https://github.com/settings/notifications

---

## Labels

The form automatically adds these labels to issues:
- `ngo-signup` - Identifies all form submissions
- `alpha-program` - Marks for Alpha pilot program

You can add more labels manually:
- `tier-1-environmental` - High-priority environmental NGO
- `tier-2-transparency` - Transparency/anti-corruption NGO
- `contacted` - Follow-up email sent
- `scheduled-call` - Demo call scheduled
- `alpha-active` - Currently in Alpha pilot

---

## Workflow After Signup

1. **New issue created** → You receive GitHub email notification
2. **Review details** → Check org type, topics, premium interest
3. **Send follow-up email** → Use contact email from issue
4. **Schedule call** → Add `scheduled-call` label
5. **Start Alpha** → Add `alpha-active` label
6. **Close issue** → Mark as completed when onboarded

---

## Security Considerations

✅ **Token permissions:** Only `public_repo` (minimal access)
✅ **Token storage:** Encrypted in Streamlit Cloud secrets
✅ **Rate limiting:** GitHub allows 5,000 API calls/hour
✅ **Spam protection:** Streamlit form validation
✅ **Email privacy:** Only visible to repo collaborators

---

## Troubleshooting

### "No se pudo conectar con el servidor"
- **Cause:** GitHub token not configured or invalid
- **Fix:** Check Streamlit Cloud secrets, regenerate token if needed

### No email notifications
- **Cause:** GitHub notifications disabled
- **Fix:** https://github.com/settings/notifications → Enable "Issues"

### Issues not created
- **Cause:** Token expired or insufficient permissions
- **Fix:** Generate new token with `public_repo` scope

### Form shows "modo desarrollo local"
- **Cause:** Running locally without token (expected behavior)
- **Fix:** Normal - data saved to `data/ngo_signups.json` for local testing

---

## Alternative: Make Repo Private

If you want private issues (not publicly visible):

1. Make gacetachat repo private
2. Update token scope to `repo` (full access)
3. Issues will only be visible to collaborators

**Trade-off:** Private repos have limits on Streamlit Cloud free tier.

---

**Last Updated:** 2025-11-12
**Version:** 1.0
**Status:** Production-ready
