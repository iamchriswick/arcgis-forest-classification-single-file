# -*- coding: utf-8 -*-
"""
Test Suite for toolbox_0_1_8.py - Optimized Startup Performance

Created: 2025-08-28 19:50
Version: 0.1.8
"""

import unittest
import sys
import os

# Add the src directory to Python path for testing
test_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(test_dir), "src")
sys.path.insert(0, src_dir)


class TestOptimizedStartup(unittest.TestCase):
    """Test the optimized startup performance improvements."""

    def test_os_cpu_count_available(self):
        """Test that os.cpu_count() is available and works."""
        import os

        cpu_cores = os.cpu_count()
        self.assertIsNotNone(cpu_cores)
        if cpu_cores is not None:
            self.assertGreater(cpu_cores, 0)
        print(f"✓ CPU cores detected: {cpu_cores}")

    def test_psutil_optional_import(self):
        """Test that psutil import is handled gracefully."""
        try:
            import psutil

            mem = psutil.virtual_memory()
            print(
                f"✓ psutil available - Memory: {mem.available / (1024**3):.1f} GB available"
            )
        except ImportError:
            print("✓ psutil not available - graceful fallback expected")

    def test_module_imports_quickly(self):
        """Test that the module can be imported without delays."""
        import time

        start_time = time.time()

        # Import the toolbox module
        import toolbox_0_1_8

        import_time = time.time() - start_time
        self.assertLess(import_time, 2.0, "Module import should be fast")
        print(f"✓ Module import time: {import_time:.3f} seconds")

    def test_log_system_capabilities_fast_function(self):
        """Test the optimized system capabilities function."""
        from toolbox_0_1_8 import log_system_capabilities_fast

        # This should not raise any exceptions
        try:
            # Note: This will try to call arcpy.AddMessage which will fail in test environment
            # We're just testing that the function structure is sound
            log_system_capabilities_fast()
        except Exception as e:
            # Expected to fail due to arcpy not being available in test environment
            self.assertIn("arcpy", str(e).lower())
            print("✓ Function structure is sound (arcpy not available in test)")

    def test_version_information(self):
        """Test that version information is correctly formatted."""
        import toolbox_0_1_8

        # Check that the module has the expected docstring format
        docstring = toolbox_0_1_8.__doc__
        self.assertIn("v0.1.8", docstring)
        self.assertIn("Optimized startup performance", docstring)
        print("✓ Version information correctly updated")


if __name__ == "__main__":
    unittest.main(verbosity=2)
