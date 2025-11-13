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

# What is La Gaceta? - Prominent onboarding
with st.expander("📖 ¿Qué es La Gaceta Oficial?", expanded=True):
    st.markdown("""
    **La Gaceta** es el diario oficial de Costa Rica donde se publican todas las leyes,
    decretos, reglamentos y avisos del gobierno.

    **El problema:** Cada día se publican 50-200 páginas de texto legal denso.
    Nadie tiene tiempo de leerlo, pero contiene información importante para ciudadanos y empresas.

    **Nuestra solución:** GacetaChat usa inteligencia artificial para leer La Gaceta
    cada día y crear un resumen de 5 puntos que puedes leer en 30 segundos.

    **¿Para quién es esto?**
    - 👨‍💼 Empresarios que necesitan estar al día con regulaciones
    - 📰 Periodistas buscando noticias de gobierno
    - ⚖️ Abogados monitoreando cambios legales
    - 🇨🇷 Cualquier ciudadano que quiera entender qué hace su gobierno
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
    # Real data from demo_data.json
    st.subheader(f"📋 Resumen - {selected_date.strftime('%d de %B, %Y')}")
    st.write(day_data["summary"])

    st.markdown("### 📌 Puntos Clave:")
    for bullet in day_data["bullets"]:
        st.markdown(f"**{bullet['icon']}** {bullet['text']}")

    st.divider()

    # Topics
    st.markdown("### 🏷️ Temas:")
    st.markdown(" • ".join([f"**{t}**" for t in day_data["topics"]]))

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
    if st.button("📄 PDF Original", use_container_width=True):
        # Check if we have a local PDF
        if day_data and "pdf_url" in day_data and Path(day_data["pdf_url"]).exists():
            st.success(f"✅ PDF local disponible: `{day_data['pdf_url']}`")
        st.link_button(
            "Abrir en sitio oficial",
            "https://www.imprentanacional.go.cr/gaceta/",
            use_container_width=True
        )

with col2:
    if st.button("🔗 Compartir", use_container_width=True):
        st.info("Funcionalidad de compartir estará disponible en v2.0")

with col3:
    if st.button("🔍 Buscar", use_container_width=True):
        st.info("Búsqueda estará disponible en v2.0")

st.divider()

# NGO/Organization Feedback Section
if is_live:
    st.markdown("### 🤝 ¿Eres parte de una ONG u organización?")
    st.markdown("""
    **Estamos buscando organizaciones para probar la versión Alpha** con resúmenes reales diarios.

    Si tu organización monitorea La Gaceta regularmente, queremos tu feedback:
    """)

    col_a, col_b = st.columns(2)
    with col_a:
        st.link_button(
            "📝 Registra tu Organización",
            "https://forms.gle/YOUR_GOOGLE_FORM_ID",  # Replace with actual form
            use_container_width=True,
            type="primary"
        )
    with col_b:
        st.link_button(
            "📧 Contacto Directo",
            "mailto:contact@gacetachat.cr",
            use_container_width=True
        )

    st.info("💡 **Beneficios del Alpha**: Acceso anticipado, influencia en el desarrollo, soporte directo")

st.divider()

# Info box
with st.expander("ℹ️ Acerca de GacetaChat"):
    st.markdown("""
    **GacetaChat** es una herramienta de código abierto que utiliza inteligencia artificial
    para resumir La Gaceta Oficial de Costa Rica.

    **Características:**
    - 🤖 Resúmenes generados con GPT-4
    - 📅 Archivo de 90 días disponible
    - 🔍 Búsqueda por palabras clave
    - 🆓 Gratis y de código abierto

    **Estado actual:** Demo simplificado

    **Próxima versión (v2.0):**
    - API pública y gratuita
    - Interfaz moderna con Next.js
    - Backend escalable con FastAPI
    - Lanzamiento en 4 semanas
    """)

# Footer
st.divider()
st.caption("🚧 **Demo simplificado** - Este es un prototipo para demostración del concepto")
st.caption("💡 La versión 2.0 será construida con Next.js + FastAPI + PostgreSQL")
st.caption("📖 Código abierto | 🇨🇷 Hecho en Costa Rica | ❤️ Para la democracia")
