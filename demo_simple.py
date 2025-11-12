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

# Page config
st.set_page_config(
    page_title="GacetaChat - Demo",
    page_icon="📰",
    layout="centered"
)

# Title
st.title("🇨🇷 GacetaChat")
st.caption("Resúmenes diarios de La Gaceta Oficial - Generados con IA")

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

# Date selector
selected_date = st.date_input(
    "Seleccionar fecha",
    value=datetime.now().date(),
    max_value=datetime.now().date(),
    min_value=datetime.now().date() - timedelta(days=90)
)

st.divider()

# Hardcoded demo summary
st.subheader(f"📋 Resumen - {selected_date.strftime('%d de %B, %Y')}")

demo_summary = """
Resumen general de las publicaciones más importantes del día en La Gaceta Oficial de Costa Rica.
"""

st.write(demo_summary)

st.markdown("### 📌 Puntos Clave:")

# Bullet points with emojis
bullets = [
    ("⚖️", "Nueva regulación sobre permisos sanitarios para establecimientos comerciales. Empresas deben renovar antes del 31 de marzo."),
    ("💰", "Modificación en tasas de impuestos municipales para el período 2025. Aumento del 3.5% en promedio."),
    ("🏥", "Actualización de protocolos de salud pública post-pandemia. Incluye nuevas directrices para hospitales."),
    ("🎓", "Cambios en el calendario escolar para instituciones públicas. Año lectivo inicia el 10 de febrero."),
    ("🌳", "Nuevas disposiciones para protección de áreas forestales. Prohibiciones adicionales en zonas protegidas.")
]

for icon, text in bullets:
    st.markdown(f"**{icon}** {text}")

st.divider()

# Topics
st.markdown("### 🏷️ Temas:")
topics = ["Legal", "Fiscal", "Salud", "Educación", "Ambiente"]
st.markdown(" • ".join([f"**{t}**" for t in topics]))

st.divider()

# Action buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 PDF Original", use_container_width=True):
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
