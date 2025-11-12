"""
pytest configuration and fixtures for GacetaChat tests
"""
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_openai_response():
    """Mock GPT-4o response to avoid API costs in tests"""
    return {
        "summary": "Resumen de prueba de La Gaceta del día",
        "bullets": [
            {"icon": "⚖️", "text": "Nuevo decreto modifica regulaciones ambientales para proyectos de infraestructura"},
            {"icon": "💰", "text": "Ministerio de Hacienda anuncia cambios en tasas de impuestos para PYMEs"},
            {"icon": "🏥", "text": "CCSS amplía cobertura de medicamentos para enfermedades crónicas"},
            {"icon": "📚", "text": "MEP implementa nuevo programa de becas para estudiantes de bajos recursos"},
            {"icon": "🌱", "text": "MINAE establece nuevas áreas de protección en la Zona Norte"}
        ],
        "topics": ["Legal", "Fiscal", "Salud", "Educación", "Ambiente"]
    }

@pytest.fixture
def mock_gpt4_call(monkeypatch, mock_openai_response):
    """Replace OpenAI API calls with mock response to save costs"""
    def mock_summarize(*args, **kwargs):
        return mock_openai_response

    monkeypatch.setattr(
        'scripts.scrape_and_summarize.summarize_with_gpt4',
        mock_summarize
    )
    return mock_openai_response

@pytest.fixture
def sample_pdf_url():
    """Sample La Gaceta PDF URL for testing"""
    return "https://www.imprentanacional.go.cr/gaceta/2024/07/15/gaceta_20240715.pdf"

@pytest.fixture
def sample_gaceta_text():
    """Sample extracted text from La Gaceta PDF"""
    return """
    LA GACETA - DIARIO OFICIAL
    Número 135 - 15 de julio de 2024

    PODER EJECUTIVO
    DECRETOS

    N° 12345-MINAE
    EL PRESIDENTE DE LA REPÚBLICA Y EL MINISTRO DE AMBIENTE Y ENERGÍA

    Considerando:
    1. Que es necesario proteger los recursos naturales...
    2. Que la Constitución Política establece...

    Por tanto,
    DECRETAN:

    Artículo 1°—Objeto. El presente decreto tiene por objeto...
    Artículo 2°—Ámbito de aplicación...
    """

@pytest.fixture(autouse=True)
def clear_streamlit_cache():
    """Clear Streamlit cache between tests to avoid interference"""
    try:
        import streamlit as st
        st.cache_data.clear()
    except:
        pass  # Streamlit not imported in non-Streamlit tests
