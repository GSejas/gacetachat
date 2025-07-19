"""
Smoke tests for GacetaChat - Basic functionality verification
These tests verify that the core system components can start and respond.
"""

import importlib
import os
import sys
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestBasicImports:
    """Test that all core modules can be imported without errors."""

    def test_import_core_modules(self):
        """Test importing main application modules."""
        modules_to_test = [
            "config",
            "models",
            "crud",
            "db",
            "qa",
            "pdf_processor",
            "faiss_helper",
        ]

        failed_imports = []
        for module_name in modules_to_test:
            try:
                importlib.import_module(module_name)
            except ImportError as e:
                failed_imports.append(f"{module_name}: {str(e)}")

        assert len(failed_imports) == 0, f"Failed to import modules: {failed_imports}"

    def test_import_streamlit_app(self):
        """Test that Streamlit app can be imported."""
        try:
            import streamlit_app

            assert hasattr(streamlit_app, "main") or callable(streamlit_app)
        except ImportError as e:
            pytest.fail(f"Could not import streamlit_app: {e}")

    def test_import_fastapi_app(self):
        """Test that FastAPI app can be imported."""
        try:
            import fastapp

            assert hasattr(fastapp, "app")
        except ImportError as e:
            pytest.fail(f"Could not import fastapp: {e}")


class TestConfiguration:
    """Test configuration and environment setup."""

    def test_config_module_loads(self):
        """Test that config module loads and has required attributes."""
        try:
            import config

            # Check for required configuration attributes
            required_attrs = ["OPENAI_API_KEY", "DATABASE_URL"]
            missing_attrs = [
                attr for attr in required_attrs if not hasattr(config, attr)
            ]

            # In test environment, some configs might be None - that's ok
            assert (
                len(missing_attrs) == 0
            ), f"Missing config attributes: {missing_attrs}"

        except ImportError as e:
            pytest.fail(f"Could not load config module: {e}")

    def test_database_connection(self):
        """Test basic database connection."""
        try:
            from sqlalchemy import text

            from db import engine

            # Test basic connection
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                assert result.fetchone()[0] == 1

        except Exception as e:
            pytest.fail(f"Database connection failed: {e}")


class TestFileStructure:
    """Test that required files and directories exist."""

    def test_required_files_exist(self):
        """Test that core application files exist."""
        required_files = [
            "streamlit_app.py",
            "fastapp.py",
            "config.py",
            "models.py",
            "crud.py",
            "db.py",
            "requirements.txt",
        ]

        missing_files = []
        for file_name in required_files:
            file_path = project_root / file_name
            if not file_path.exists():
                missing_files.append(file_name)

        assert len(missing_files) == 0, f"Missing required files: {missing_files}"

    def test_required_directories_exist(self):
        """Test that required directories exist."""
        required_dirs = ["test", "docs", "mpages", "services"]

        missing_dirs = []
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)

        assert len(missing_dirs) == 0, f"Missing required directories: {missing_dirs}"


class TestBasicFunctionality:
    """Test basic application functionality."""

    def test_pdf_processor_basics(self):
        """Test PDF processor can be initialized."""
        try:
            from pdf_processor import PDFProcessor

            processor = PDFProcessor()
            assert processor is not None
        except Exception as e:
            pytest.fail(f"PDF processor initialization failed: {e}")

    def test_qa_module_basics(self):
        """Test QA module basic functionality."""
        try:
            import qa

            # Test that basic functions exist
            assert hasattr(qa, "get_llm") or hasattr(qa, "query_folder")
        except Exception as e:
            pytest.fail(f"QA module test failed: {e}")

    def test_crud_operations_basic(self):
        """Test basic CRUD operations."""
        try:
            from crud import PromptExecutionEngine

            # Test that we can create the engine
            engine = PromptExecutionEngine()
            assert engine is not None

        except Exception as e:
            pytest.fail(f"CRUD operations test failed: {e}")


class TestApplicationStartup:
    """Test that applications can start (without full execution)."""

    @pytest.mark.skipif(os.getenv("SKIP_SERVER_TESTS"), reason="Server tests skipped")
    def test_fastapi_app_creation(self):
        """Test FastAPI app can be created."""
        try:
            import fastapp

            app = fastapp.app
            assert app is not None
            assert hasattr(app, "openapi")  # Basic FastAPI method
        except Exception as e:
            pytest.fail(f"FastAPI app creation failed: {e}")

    def test_streamlit_app_syntax(self):
        """Test Streamlit app has valid Python syntax."""
        streamlit_app_path = project_root / "streamlit_app.py"

        try:
            with open(streamlit_app_path, "r", encoding="utf-8") as f:
                app_code = f.read()

            # Compile to check syntax
            compile(app_code, str(streamlit_app_path), "exec")

        except SyntaxError as e:
            pytest.fail(f"Streamlit app has syntax errors: {e}")
        except FileNotFoundError:
            pytest.fail("streamlit_app.py not found")


class TestDependencies:
    """Test that critical dependencies are available."""

    def test_critical_packages_importable(self):
        """Test that critical packages can be imported."""
        critical_packages = [
            "streamlit",
            "fastapi",
            "sqlalchemy",
            "openai",
            "langchain",
            "faiss",
            "requests",
            "pandas",
            "numpy",
        ]

        failed_imports = []
        for package in critical_packages:
            try:
                if package == "faiss":
                    # FAISS might be installed as faiss-cpu
                    try:
                        pass
                    except ImportError:
                        pass
                else:
                    importlib.import_module(package)
            except ImportError as e:
                failed_imports.append(f"{package}: {str(e)}")

        assert len(failed_imports) == 0, f"Failed to import packages: {failed_imports}"


if __name__ == "__main__":
    # Run smoke tests
    pytest.main([__file__, "-v", "--tb=short"])
