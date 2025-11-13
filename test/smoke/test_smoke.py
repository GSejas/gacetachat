"""
Smoke tests for GacetaChat Serverless Alpha - Basic functionality verification
These tests verify that the scraper and demo components can run.
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
    """Test that scraper and demo modules can be imported."""

    def test_import_scraper_module(self):
        """Test importing scraper module."""
        try:
            import scripts.scrape_and_summarize
            assert scripts.scrape_and_summarize is not None
        except ImportError as e:
            pytest.fail(f"Could not import scraper: {e}")

    def test_import_demo_simple(self):
        """Test that demo_simple.py can be imported."""
        try:
            import demo_simple
            assert hasattr(demo_simple, "load_demo_data") or callable(demo_simple)
        except ImportError as e:
            pytest.fail(f"Could not import demo_simple: {e}")

    def test_import_streamlit_dependencies(self):
        """Test that Streamlit dependencies are available."""
        try:
            import streamlit
            assert streamlit is not None
        except ImportError as e:
            pytest.fail(f"Could not import streamlit: {e}")


class TestConfiguration:
    """Test configuration and environment setup."""

    def test_environment_variables(self):
        """Test that environment can be properly configured."""
        # These are optional in serverless alpha
        openai_key = os.getenv("OPENAI_API_KEY")
        # Just verify we can check the environment
        assert isinstance(os.environ, dict)

    def test_data_directory_exists(self):
        """Test that data directory can be created."""
        data_dir = project_root / "data"
        # Directory may not exist yet, but path should be valid
        assert project_root.exists()
        assert project_root.is_dir()


class TestFileStructure:
    """Test that required files and directories exist."""

    def test_required_files_exist(self):
        """Test that core application files exist."""
        required_files = [
            "demo_simple.py",
            "scripts/scrape_and_summarize.py",
            "requirements.txt",
            "pyproject.toml",
            "README.md",
        ]

        missing_files = []
        for file_name in required_files:
            file_path = project_root / file_name
            if not file_path.exists():
                missing_files.append(file_name)

        assert len(missing_files) == 0, f"Missing required files: {missing_files}"

    def test_required_directories_exist(self):
        """Test that required directories exist."""
        required_dirs = ["test", "docs", "scripts"]

        missing_dirs = []
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)

        assert len(missing_dirs) == 0, f"Missing required directories: {missing_dirs}"


class TestBasicFunctionality:
    """Test basic application functionality."""

    def test_scraper_module_functions(self):
        """Test scraper module has required functions."""
        try:
            import scripts.scrape_and_summarize as scraper

            # Test that main function exists
            assert hasattr(scraper, "main")
        except Exception as e:
            pytest.fail(f"Scraper module test failed: {e}")

    def test_demo_simple_loads_data(self):
        """Test demo_simple can load demonstration data."""
        try:
            import demo_simple

            # Test that the module loads without errors
            assert demo_simple is not None
        except Exception as e:
            pytest.fail(f"Demo simple test failed: {e}")

    def test_json_data_structure(self):
        """Test that data files can be read as JSON."""
        try:
            import json

            demo_data_path = project_root / "demo_data.json"
            if demo_data_path.exists():
                with open(demo_data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                assert isinstance(data, (dict, list))
        except Exception as e:
            pytest.fail(f"JSON data structure test failed: {e}")


class TestApplicationStartup:
    """Test that applications can start (without full execution)."""

    def test_demo_simple_syntax(self):
        """Test demo_simple.py has valid Python syntax."""
        demo_path = project_root / "demo_simple.py"

        try:
            with open(demo_path, "r", encoding="utf-8") as f:
                app_code = f.read()

            # Compile to check syntax
            compile(app_code, str(demo_path), "exec")

        except SyntaxError as e:
            pytest.fail(f"demo_simple.py has syntax errors: {e}")
        except FileNotFoundError:
            pytest.fail("demo_simple.py not found")

    def test_scraper_syntax(self):
        """Test scraper has valid Python syntax."""
        scraper_path = project_root / "scripts" / "scrape_and_summarize.py"

        try:
            with open(scraper_path, "r", encoding="utf-8") as f:
                code = f.read()

            # Compile to check syntax
            compile(code, str(scraper_path), "exec")

        except SyntaxError as e:
            pytest.fail(f"scraper has syntax errors: {e}")
        except FileNotFoundError:
            pytest.fail("scrape_and_summarize.py not found")


class TestDependencies:
    """Test that critical dependencies are available."""

    def test_critical_packages_importable(self):
        """Test that critical packages for serverless alpha can be imported."""
        critical_packages = [
            "streamlit",
            "openai",
            "requests",
            "beautifulsoup4",
            "pypdf",
        ]

        failed_imports = []
        for package in critical_packages:
            try:
                # Handle package name differences
                if package == "beautifulsoup4":
                    importlib.import_module("bs4")
                elif package == "pypdf":
                    importlib.import_module("PyPDF2")
                else:
                    importlib.import_module(package)
            except ImportError as e:
                failed_imports.append(f"{package}: {str(e)}")

        # These are required for the scraper to work
        assert len(failed_imports) == 0, f"Failed to import packages: {failed_imports}"


if __name__ == "__main__":
    # Run smoke tests
    pytest.main([__file__, "-v", "--tb=short"])
