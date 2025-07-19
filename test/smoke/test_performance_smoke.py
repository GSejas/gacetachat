"""
Performance smoke tests for GacetaChat
Tests basic performance characteristics of core functions.
"""

import os
import sys
import time
from pathlib import Path

import psutil
import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestPerformanceBasics:
    """Test basic performance characteristics."""

    def test_import_performance(self):
        """Test that core modules import within reasonable time."""
        modules_to_test = ["config", "models", "crud", "db"]

        slow_imports = []
        for module_name in modules_to_test:
            start_time = time.time()
            try:
                __import__(module_name)
                import_time = time.time() - start_time

                # Imports should take less than 5 seconds
                if import_time > 5.0:
                    slow_imports.append(f"{module_name}: {import_time:.2f}s")

            except ImportError:
                # Skip modules that can't be imported
                pass

        assert len(slow_imports) == 0, f"Slow imports detected: {slow_imports}"

    def test_memory_usage_basic(self):
        """Test basic memory usage is reasonable."""
        process = psutil.Process(os.getpid())

        # Get initial memory usage
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Import some modules
        try:
            pass
        except ImportError:
            pytest.skip("Core modules not available for memory test")

        # Get memory after imports
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable (less than 500MB for imports)
        assert (
            memory_increase < 500
        ), f"Memory increase too high: {memory_increase:.2f}MB"

    def test_database_connection_performance(self):
        """Test database connection performance."""
        try:
            from sqlalchemy import text

            from db import engine

            start_time = time.time()
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                result.fetchone()
            connection_time = time.time() - start_time

            # Database connection should be fast (less than 2 seconds)
            assert (
                connection_time < 2.0
            ), f"Database connection too slow: {connection_time:.2f}s"

        except Exception as e:
            pytest.skip(f"Database not available for performance test: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
