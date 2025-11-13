#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "streamlit>=1.28.2",
# ]
# ///
"""
GacetaChat - Simple Demo
========================

Minimal demo showing what the final product will look like.
This is just a static mockup - the real version will use the backend.

Run with uv: uv run demo_simple.py
Or: streamlit run demo_simple.py
"""

import streamlit as st
from datetime import datetime, timedelta
import json
from pathlib import Path

# Load demo data
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_demo_data():
    """Load summaries from JSON file (live data or fallback to demo)"""
    # Try live data first
    live_file = Path(__file__).parent / "data" / "summaries.json"
    if live_file.exists():
        with open(live_file, 'r', encoding='utf-8') as f:
            return json.load(f), True  # True = live data

    # Fallback to demo data
    demo_file = Path(__file__).parent / "demo_data.json"
    if demo_file.exists():
        with open(demo_file, 'r', encoding='utf-8') as f:
            return json.load(f), False  # False = demo data

    return {}, False

# Page config
st.set_page_config(
    page_title="GacetaChat - Demo",
    page_icon="📰",
    layout="centered"
)

# Load data
demo_data, is_live = load_demo_data()
available_dates = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in demo_data.keys()], reverse=True)

# Title
st.title("🇨🇷 GacetaChat")
if is_live:
    st.caption("🟢 Resúmenes diarios de La Gaceta Oficial - Generados con IA")
else:
    st.caption("🟡 Demo con datos de ejemplo - Versión Alpha próximamente")

# What is La Gaceta? - Prominent onboarding (NGO-focused)
with st.expander("📖 ¿Qué es GacetaChat?", expanded=True):
    st.markdown("""
    **GacetaChat es infraestructura democrática para organizaciones de la sociedad civil.**

    **La Gaceta Oficial** publica 50-200 páginas diarias de leyes, decretos, y regulaciones.
    Esta información es crítica para el trabajo de defensoría, pero nadie tiene tiempo de leerla.

    **Nuestra solución:** Inteligencia artificial lee La Gaceta cada día y crea resúmenes
    accionables en 30 segundos. No es una app - es infraestructura pública para la democracia.

    **¿Para quién es esto?**
    - 🌱 **ONGs Ambientales** - Monitorea cambios en políticas de SINAC, MINAE, regulaciones de bosques
    - ⚖️ **ONGs de Transparencia** - Rastrea contratos gubernamentales, nombramientos, avisos inusuales
    - 👷 **ONGs de Derechos Laborales** - Sigue cambios en leyes laborales, CCSS, salarios mínimos
    - 📰 **Periodistas** - Detecta historias antes que nadie
    - 🇨🇷 **Ciudadanía** - Entiende qué hace el gobierno (beneficiarios secundarios)

    **Teoría de Cambio:** ONGs → Medios/Defensoría → Ciudadanía → Democracia más fuerte
    """)

st.divider()

# Date selector with navigation
if available_dates:
    # available_dates is sorted newest first (reverse=True)
    default_date = available_dates[0]  # Newest date
    max_date = available_dates[0]      # Newest date
    min_date = available_dates[-1]     # Oldest date
else:
    default_date = datetime.now().date()
    max_date = datetime.now().date()
    min_date = datetime.now().date() - timedelta(days=90)

# Initialize session state for selected date
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = default_date

# Date navigation with large centered display
nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])

# Get current date index
current_idx = available_dates.index(st.session_state.selected_date) if st.session_state.selected_date in available_dates else 0
has_prev = current_idx < len(available_dates) - 1
has_next = current_idx > 0

with nav_col1:
    if st.button("← Anterior", use_container_width=True, type="secondary", disabled=not has_prev):
        if has_prev:
            st.session_state.selected_date = available_dates[current_idx + 1]
            st.rerun()

with nav_col2:
    # Large centered date display
    st.markdown(
        f"<h2 style='text-align: center; color: #1E40AF; margin: 0;'>"
        f"📅 {st.session_state.selected_date.strftime('%d de %B, %Y')}"
        f"</h2>",
        unsafe_allow_html=True
    )

with nav_col3:
    if st.button("Siguiente →", use_container_width=True, type="secondary", disabled=not has_next):
        if has_next:
            st.session_state.selected_date = available_dates[current_idx - 1]
            st.rerun()

# Date picker for manual selection (smaller, below the main display)
with st.expander("🗓️ Seleccionar otra fecha"):
    selected_date = st.date_input(
        "Elegir fecha específica",
        value=st.session_state.selected_date,
        max_value=max_date,
        min_value=min_date,
        help="Fechas con datos disponibles: 15-24 julio 2024",
        label_visibility="collapsed"
    )

    # Update session state if date picker changes
    if selected_date != st.session_state.selected_date:
        st.session_state.selected_date = selected_date
        st.rerun()

# Use the session state date for content display
selected_date = st.session_state.selected_date

st.divider()

# Get data for selected date
date_key = selected_date.strftime("%Y-%m-%d")
day_data = demo_data.get(date_key)

if day_data:
    # Display header image if available (darkened first page of PDF)
    if "header_image" in day_data:
        header_path = Path(__file__).parent / "data" / day_data["header_image"]
        if header_path.exists():
            st.image(str(header_path), use_container_width=True, caption="La Gaceta Oficial")

    # Real data from demo_data.json
    st.subheader(f"📋 Resumen - {selected_date.strftime('%d de %B, %Y')}")
    st.write(day_data["summary"])

    st.markdown("### 📌 Puntos Clave:")
    for bullet in day_data["bullets"]:
        # Include page references if available (for transparency)
        if "pages" in bullet and bullet["pages"]:
            pages_str = ", ".join([f"p.{p}" for p in bullet["pages"]])
            st.markdown(f"**{bullet['icon']}** {bullet['text']} *({pages_str})*")
        else:
            st.markdown(f"**{bullet['icon']}** {bullet['text']}")

    st.divider()

    # Topics
    st.markdown("### 🏷️ Temas:")
    st.markdown(" • ".join([f"**{t}**" for t in day_data["topics"]]))

    # Metadata (for transparency and reproducibility)
    if "prompt_version" in day_data or "model" in day_data or "generated_at" in day_data:
        with st.expander("🔍 Metadata del Resumen"):
            col_meta1, col_meta2, col_meta3 = st.columns(3)
            with col_meta1:
                if "model" in day_data:
                    st.caption(f"**Modelo**: {day_data['model']}")
            with col_meta2:
                if "prompt_version" in day_data:
                    st.caption(f"**Prompt**: v{day_data['prompt_version']}")
            with col_meta3:
                if "generated_at" in day_data:
                    from datetime import datetime
                    gen_time = datetime.fromisoformat(day_data['generated_at'])
                    st.caption(f"**Generado**: {gen_time.strftime('%H:%M UTC')}")

    # Store PDF URL for later use
    pdf_url = day_data.get("pdf_url", "https://www.imprentanacional.go.cr/gaceta/")
else:
    # Fallback for dates without data
    st.subheader(f"📋 Resumen - {selected_date.strftime('%d de %B, %Y')}")
    st.info("⏳ No hay datos disponibles para esta fecha en el demo. Selecciona una fecha de julio 2024.")
    pdf_url = "https://www.imprentanacional.go.cr/gaceta/"

st.divider()

# Action buttons
col1, col2, col3 = st.columns(3)

with col1:
    # Use actual PDF URL if available, otherwise fallback to homepage
    if day_data and "pdf_url" in day_data:
        pdf_link = day_data["pdf_url"]
        button_text = "📄 Abrir PDF Original"
    else:
        pdf_link = "https://www.imprentanacional.go.cr/gaceta/"
        button_text = "📄 Ir a La Gaceta"

    st.link_button(
        button_text,
        pdf_link,
        use_container_width=True,
        type="primary"
    )

with col2:
    if st.button("🔗 Compartir", use_container_width=True):
        st.info("Funcionalidad de compartir estará disponible en v2.0")

with col3:
    if st.button("🔍 Buscar", use_container_width=True):
        st.info("Búsqueda estará disponible en v2.0")

st.divider()

# NGO/Organization Signup Form
st.markdown("### 🤝 ¿Tu organización monitorea La Gaceta?")
st.markdown("""
**Estamos buscando ONGs y organizaciones de la sociedad civil para probar la versión Alpha.**

Si tu organización necesita monitorear La Gaceta regularmente, únete al programa Alpha:
""")

with st.form("ngo_signup_form"):
    st.markdown("#### 📋 Registro para Organizaciones")

    # Organization details
    col1, col2 = st.columns(2)
    with col1:
        org_name = st.text_input("Nombre de la Organización *", placeholder="Ej: FECON, Costa Rica Limpia")
        org_type = st.selectbox(
            "Tipo de Organización *",
            ["Seleccionar...", "ONG Ambiental", "ONG de Transparencia/Anti-corrupción",
             "ONG de Derechos Laborales", "Medio de Comunicación", "Firma Legal",
             "Institución Académica", "Empresa", "Otro"]
        )

    with col2:
        contact_name = st.text_input("Nombre de Contacto *", placeholder="Tu nombre")
        contact_email = st.text_input("Email de Contacto *", placeholder="email@organizacion.org")

    # Usage details
    monitoring_frequency = st.select_slider(
        "¿Con qué frecuencia monitorean La Gaceta actualmente?",
        options=["Nunca", "Mensual", "Semanal", "Diario", "Múltiples veces al día"]
    )

    # Interests
    st.markdown("**¿Qué temas monitorean?** (selecciona todos los relevantes)")
    col_int1, col_int2, col_int3 = st.columns(3)
    with col_int1:
        topic_env = st.checkbox("🌱 Ambiente")
        topic_legal = st.checkbox("⚖️ Legal/Justicia")
        topic_health = st.checkbox("🏥 Salud")
    with col_int2:
        topic_labor = st.checkbox("👷 Laboral")
        topic_education = st.checkbox("📚 Educación")
        topic_economy = st.checkbox("💰 Economía/Fiscal")
    with col_int3:
        topic_govt = st.checkbox("🏛️ Contratos/Nombramientos")
        topic_other = st.checkbox("📌 Otro")

    # Premium interest
    premium_interest = st.radio(
        "¿Estaría tu organización dispuesta a pagar por funciones premium? (alertas personalizadas, API, análisis histórico)",
        ["No estoy seguro/a", "Sí, si el valor es claro ($50-200/mes)", "No, solo usaríamos la versión gratuita"]
    )

    # Additional comments
    comments = st.text_area(
        "Comentarios adicionales o necesidades específicas",
        placeholder="Ej: Necesitamos alertas de WhatsApp cuando aparezca 'SINAC' o 'contaminación'"
    )

    # Submit button
    submitted = st.form_submit_button("🚀 Registrar Organización", use_container_width=True, type="primary")

    if submitted:
        if not org_name or not contact_email or org_type == "Seleccionar...":
            st.error("⚠️ Por favor completa los campos marcados con * (Nombre de organización, tipo, y email)")
        else:
            # Save to JSON file (in production, send to Google Sheets or database)
            import json
            from pathlib import Path
            from datetime import datetime

            signup_data = {
                "timestamp": datetime.now().isoformat(),
                "org_name": org_name,
                "org_type": org_type,
                "contact_name": contact_name,
                "contact_email": contact_email,
                "monitoring_frequency": monitoring_frequency,
                "topics": {
                    "ambiente": topic_env,
                    "legal": topic_legal,
                    "salud": topic_health,
                    "laboral": topic_labor,
                    "educacion": topic_education,
                    "economia": topic_economy,
                    "gobierno": topic_govt,
                    "otro": topic_other
                },
                "premium_interest": premium_interest,
                "comments": comments
            }

            # Save to GitHub Issues (works in Streamlit Cloud)
            try:
                import requests

                # Format topics for readability
                selected_topics = [k.title() for k, v in signup_data["topics"].items() if v]
                topics_str = ", ".join(selected_topics) if selected_topics else "Ninguno"

                # Create GitHub issue body
                issue_body = f"""## 📋 Nueva Organización Registrada

**Organización:** {org_name}
**Tipo:** {org_type}
**Contacto:** {contact_name}
**Email:** {contact_email}

### Detalles de Uso
- **Frecuencia de monitoreo actual:** {monitoring_frequency}
- **Temas de interés:** {topics_str}
- **Interés en premium:** {premium_interest}

### Comentarios Adicionales
{comments if comments else "*Sin comentarios*"}

---

**Timestamp:** {signup_data['timestamp']}
**Fuente:** Formulario web en demo GacetaChat
"""

                # Get GitHub token from Streamlit secrets (or environment)
                github_token = st.secrets.get("GITHUB_TOKEN", os.environ.get("GITHUB_TOKEN"))

                if github_token:
                    # Create GitHub issue
                    response = requests.post(
                        "https://api.github.com/repos/GSejas/gacetachat/issues",
                        headers={
                            "Authorization": f"token {github_token}",
                            "Accept": "application/vnd.github.v3+json"
                        },
                        json={
                            "title": f"NGO Signup: {org_name}",
                            "body": issue_body,
                            "labels": ["ngo-signup", "alpha-program"]
                        },
                        timeout=10
                    )

                    if response.status_code == 201:
                        st.success(f"""
✅ **¡Gracias, {org_name}!**

Tu organización ha sido registrada para el programa Alpha de GacetaChat.

**Próximos pasos:**
1. Recibirás un email en {contact_email} en las próximas 48 horas
2. Te daremos acceso anticipado a funciones premium (gratis durante Alpha)
3. Agendaremos una llamada de 30 minutos para co-diseñar las funciones que tu organización necesita

**Beneficios del Alpha:**
- Acceso anticipado (6 meses antes del lanzamiento público)
- Funciones premium gratis durante el piloto
- Influencia directa en el desarrollo del producto
- Soporte directo del equipo técnico
- Reconocimiento como organización fundadora
                        """)
                    else:
                        # Fallback: Save locally (for local development)
                        st.warning("⚠️ No se pudo conectar con el servidor. Tu registro ha sido guardado localmente.")
                        signups_file = Path(__file__).parent / "data" / "ngo_signups.json"
                        signups_file.parent.mkdir(exist_ok=True)

                        if signups_file.exists():
                            with open(signups_file, 'r', encoding='utf-8') as f:
                                signups = json.load(f)
                        else:
                            signups = []

                        signups.append(signup_data)

                        with open(signups_file, 'w', encoding='utf-8') as f:
                            json.dump(signups, f, indent=2, ensure_ascii=False)
                else:
                    # Fallback for local development without token
                    signups_file = Path(__file__).parent / "data" / "ngo_signups.json"
                    signups_file.parent.mkdir(exist_ok=True)

                    if signups_file.exists():
                        with open(signups_file, 'r', encoding='utf-8') as f:
                            signups = json.load(f)
                    else:
                        signups = []

                    signups.append(signup_data)

                    with open(signups_file, 'w', encoding='utf-8') as f:
                        json.dump(signups, f, indent=2, ensure_ascii=False)

                    st.success(f"✅ ¡Gracias, {org_name}! Tu registro ha sido guardado (modo desarrollo local).")

                # Show mailto link
                st.markdown(f"📧 **Contacto directo:** [contact@gacetachat.cr](mailto:contact@gacetachat.cr?subject=Alpha%20-%20{org_name})")

            except Exception as e:
                st.error(f"⚠️ Error al guardar: {e}. Por favor contáctanos directamente a contact@gacetachat.cr")

st.info("💡 **¿Por qué enfocarnos en ONGs?** Las organizaciones de la sociedad civil son la infraestructura de la democracia. Si empoderamos a las ONGs, ellas amplifican el impacto a toda la ciudadanía.")

st.divider()

# Info box
with st.expander("ℹ️ Acerca de GacetaChat"):
    st.markdown("""
    **GacetaChat es infraestructura democrática pública**, no una startup.

    **Enfoque estratégico:**
    - 🎯 **ONGs primero**: Diseñado para organizaciones de la sociedad civil
    - 🔄 **Teoría de cambio**: ONGs → Medios/Defensoría → Ciudadanía → Democracia
    - 🌱 **Modelo freemium**: Gratis para ciudadanos, accesible para ONGs ($50-200/mes)
    - 💰 **Sostenibilidad**: Contratos institucionales + suscripciones + donaciones filantrópicas

    **Características actuales:**
    - 🤖 Resúmenes generados con GPT-4o (probados para precisión >95%)
    - 📅 Archivo de 90 días disponible
    - 🆓 Código abierto (MIT License)
    - 🚀 Replicable para otros países con sistemas de gaceta oficial

    **Estado actual:** Demo simplificado + Scraper automático diario

    **Próxima versión (v2.0 MVP) - 4 semanas desde financiamiento:**
    - API pública RESTful
    - Alertas por WhatsApp/Telegram (crítico para Costa Rica)
    - Búsqueda por palabras clave
    - Interfaz moderna (Next.js + FastAPI)
    - Funciones premium para ONGs (análisis histórico, alertas personalizadas)

    **Aplicando para financiamiento:**
    - Open Society Foundations, Omidyar Network, National Endowment for Democracy
    - Meta: $30k-50k para desarrollo MVP
    - Timeline: 4 semanas con desarrollo acelerado por IA (Claude Code Plus)

    **¿Quieres replicar esto en tu país?** Toda la arquitectura es código abierto.
    """)

# Footer
st.divider()
st.caption("🏛️ **Infraestructura democrática pública** - No es una app, es un bien común digital")
st.caption("🎯 **Diseñado para ONGs** - Empoderando a la sociedad civil para fortalecer la democracia")
st.caption("📖 Código abierto (MIT) | 🇨🇷 Hecho en Costa Rica | ❤️ Para la democracia costarricense")
