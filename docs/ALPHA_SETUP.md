# GacetaChat Alpha - Setup Guide

## Overview

This guide will help you set up the **serverless alpha** version of GacetaChat that:
- Scrapes La Gaceta daily using GitHub Actions (free)
- Summarizes with GPT-4o (costs ~$2-5/day)
- Stores summaries in Git (no database needed)
- Updates Streamlit demo with real data automatically

**Total cost**: $60-150/month
**Setup time**: 30 minutes

---

## Prerequisites

1. GitHub repository (you already have this)
2. OpenAI API key ([get one here](https://platform.openai.com/api-keys))
3. Streamlit Cloud account ([free tier](https://streamlit.io/cloud))
4. Google Form for NGO signups ([create one](https://forms.google.com))

---

## Step 1: Set up OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy the key (starts with `sk-proj-...`)
4. Add $10-20 credit to your account

**Monthly cost estimate**: $60-150 (30 days × $2-5/day)

---

## Step 2: Add GitHub Secret

1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `OPENAI_API_KEY`
4. Value: Paste your OpenAI key
5. Click "Add secret"

---

## Step 3: Enable GitHub Actions

1. Go to Actions tab in your repo
2. Click "I understand my workflows, go ahead and enable them"
3. The daily scraper will run automatically at 6 AM Costa Rica time
4. You can also run it manually: Actions → Daily La Gaceta Scraper → Run workflow

---

## Step 4: Create Google Form for NGO Signups

### Form Title
"GacetaChat Alpha - Registro de Organizaciones"

### Questions

**1. Nombre de la Organización** (Short answer, required)
- Ej: FECON, Costa Rica Limpia, etc.

**2. Tipo de Organización** (Multiple choice, required)
- ONG Ambiental
- ONG Transparencia/Anti-corrupción
- ONG Derechos Laborales
- Organización de Justicia Social
- Medio de Comunicación
- Bufete Legal
- Academia/Universidad
- Otro (especificar)

**3. Persona de Contacto** (Short answer, required)

**4. Email de Contacto** (Short answer, required)

**5. ¿Con qué frecuencia consultan La Gaceta actualmente?** (Multiple choice)
- Diariamente
- Semanalmente
- Mensualmente
- Ocasionalmente
- Nunca

**6. ¿Qué información de La Gaceta les interesa más?** (Checkboxes, multiple)
- Cambios ambientales y regulaciones ecológicas
- Contratos y licitaciones gubernamentales
- Nombramientos y decisiones políticas
- Cambios en leyes laborales y seguridad social
- Regulaciones de salud pública
- Cambios fiscales e impuestos
- Avisos legales y notificaciones
- Otro (especificar)

**7. ¿Estarían dispuestos a pagar $50/mes por alertas personalizadas?** (Multiple choice)
- Sí, definitivamente
- Probablemente sí
- Tal vez
- Probablemente no
- No

**8. ¿Qué funcionalidad sería más valiosa para su organización?** (Checkboxes)
- Alertas por email cuando aparecen palabras clave específicas
- Alertas por WhatsApp
- Integración con Google Sheets
- API para su propio sistema
- Análisis de tendencias históricas
- Exportación de datos
- Otro (especificar)

**9. Comentarios adicionales** (Paragraph, optional)

### After Creating Form

1. Click "Send" → Copy link
2. Replace `YOUR_GOOGLE_FORM_ID` in `demo_simple.py` line 211 with your form link
3. Set form to collect email addresses
4. Enable response notifications

---

## Step 5: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Repository: `GSejas/gacetachat` (your repo)
5. Branch: `master`
6. Main file path: `demo_simple.py`
7. Click "Deploy"

**Note**: Streamlit Cloud will auto-redeploy when you push updates to GitHub.

---

## Step 6: Test the Scraper

### Manual Test Run

1. Go to Actions → Daily La Gaceta Scraper
2. Click "Run workflow" → Run workflow
3. Wait 2-5 minutes
4. Check if `data/summaries.json` was created
5. Check if commit was pushed: "🤖 Daily summary: YYYY-MM-DD"

### Verify Summary Quality

1. Open `data/summaries.json`
2. Check that summary makes sense
3. Verify 5 bullets are present
4. Confirm topics are relevant
5. Check PDF URL is correct

---

## Step 7: Update README

Add alpha status to README:

```markdown
## Status: Alpha - Live Data

🟢 **Alpha is LIVE!** GacetaChat now scrapes La Gaceta daily and generates real AI summaries.

- **Demo**: https://gacetachat.streamlit.app/
- **Cost**: ~$60-150/month
- **Updates**: Daily at 6 AM Costa Rica time

**Alpha testers wanted**: If your organization monitors La Gaceta, we want your feedback!
[Register here](https://forms.gle/YOUR_FORM_ID)
```

---

## Monitoring & Maintenance

### Daily Checks (First Week)

- [ ] Did GitHub Action run successfully?
- [ ] Was summary generated and committed?
- [ ] Is Streamlit app showing new data?
- [ ] Are summaries accurate and useful?

### Weekly Checks

- [ ] OpenAI API costs (should be $10-35/week)
- [ ] GitHub Actions minutes (should be <100 min/week)
- [ ] Form submissions from NGOs
- [ ] Any errors in GitHub Actions logs

### Monthly Tasks

- [ ] Review OpenAI billing
- [ ] Analyze which dates got most views
- [ ] Reach out to form respondents
- [ ] Adjust scraper if needed

---

## Troubleshooting

### Scraper Fails

**Symptom**: GitHub Action fails, no new summary

**Possible causes**:
1. La Gaceta didn't publish that day (happens on holidays)
2. PDF URL changed format
3. OpenAI API quota exceeded
4. PDF extraction failed

**Solution**:
- Check GitHub Actions logs for error message
- Try running manually for previous day
- Verify OpenAI API has credits

### Summary Quality Issues

**Symptom**: Summary doesn't make sense or misses important info

**Fixes**:
1. Increase `max_pages` in `scrape_and_summarize.py` (line 32)
2. Adjust GPT-4 prompt for better instructions
3. Lower `temperature` for more conservative summaries

### High Costs

**Symptom**: OpenAI bill higher than expected

**Solutions**:
- Reduce `max_pages` from 50 to 30
- Use `gpt-4o-mini` instead of `gpt-4o` (50% cheaper)
- Only run on weekdays (Mon-Fri)

---

## Next Steps After Alpha

Once you have 5-10 NGO testers using it:

1. **Collect feedback**: What features do they actually use?
2. **Validate willingness to pay**: Would they pay $50/month?
3. **Measure impact**: Are they using it daily? Weekly?
4. **Document case studies**: How are they using GacetaChat?
5. **Apply for grants**: Use alpha data to show traction

Then decide:
- Option A: Keep it simple, just improve the alpha
- Option B: Build full MVP with Next.js + FastAPI
- Option C: Pursue government partnership

---

## Cost Breakdown

### Confirmed Costs
- **OpenAI API**: $60-150/month (actual usage)
- **GitHub Actions**: $0 (within free tier)
- **Streamlit Cloud**: $0 (free tier)
- **Google Forms**: $0

### Total: $60-150/month

**Compare to full MVP**: $30k development + $1,560/year operations

**Alpha advantage**: Validate demand for <$200/month before committing $30k+

---

## Success Metrics

### Week 1
- [ ] Scraper runs successfully daily
- [ ] At least 1 NGO signs up via form
- [ ] No critical errors

### Month 1
- [ ] 5+ NGO signups
- [ ] 2+ NGOs using it weekly
- [ ] 1+ NGO willing to pay for premium

### Month 3
- [ ] 10+ active organizational users
- [ ] Clear feedback on must-have features
- [ ] Evidence of democratic impact (e.g., media citations)
- [ ] Decision: continue alpha or build full MVP

---

## Contact for Help

- **GitHub Issues**: https://github.com/GSejas/gacetachat/issues
- **Email**: [your email]
- **Discussions**: Use GitHub Discussions for questions

---

**Good luck with the alpha! 🚀**

*Remember: The goal is to validate demand cheaply, not build the perfect product.*
