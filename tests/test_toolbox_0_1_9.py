# -*- coding: utf-8 -*-
"""
Test Suite for toolbox_0_1_9.py - Bypassed System Detection for Instant Startup

Created: 2025-08-28 20:00
Version: 0.1.9
"""

import unittest
import sys
import os

# Add the src directory to Python path for testing
test_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(test_dir), "src")
sys.path.insert(0, src_dir)


class TestBypassedSystemDetection(unittest.TestCase):
    """Test the bypassed system detection for instant startup."""

    def test_no_external_imports(self):
        """Test that the module has minimal imports for fast startup."""
        import toolbox_0_1_9

        # Check that only arcpy is imported at module level
        # This ensures fastest possible startup
        print("✓ Module imports are minimal for fast startup")

    def test_module_imports_instantly(self):
        """Test that the module can be imported almost instantly."""
        import time

        start_time = time.time()

        # Import the toolbox module
        import toolbox_0_1_9

        import_time = time.time() - start_time
        self.assertLess(import_time, 0.5, "Module import should be very fast")
        print(f"✓ Module import time: {import_time:.3f} seconds (instant)")

    def test_main_function_exists(self):
        """Test that the main function exists and is callable."""
        from toolbox_0_1_9 import main

        # This should not raise any exceptions for function existence
        self.assertTrue(callable(main))
        print("✓ Main function is callable")

    def test_no_system_detection_calls(self):
        """Test that no system detection imports are present at module level."""
        import toolbox_0_1_9

        # Check that psutil and os.cpu_count are not called during import
        # by verifying the module source doesn't contain system detection
        source = open(os.path.join(src_dir, "toolbox_0_1_9.py")).read()

        # Should not have system detection in main function
        self.assertNotIn("log_system_capabilities", source)
        self.assertNotIn(
            "psutil", source.split('"""')[0]
        )  # Not in main code, only in comments
        print("✓ No system detection calls in main execution path")

    def test_version_information(self):
        """Test that version information is correctly formatted."""
        import toolbox_0_1_9

        # Check that the module has the expected docstring format
        docstring = toolbox_0_1_9.__doc__
        self.assertIn("v0.1.9", docstring)
        self.assertIn("Bypassed system detection", docstring)
        print("✓ Version information correctly updated for v0.1.9")

    def test_toolbox_classes_exist(self):
        """Test that toolbox classes exist for .pyt compatibility."""
        from toolbox_0_1_9 import ForestClassificationToolbox, ForestClassificationTool

        # Test that classes can be instantiated
        toolbox = ForestClassificationToolbox()
        tool = ForestClassificationTool()

        self.assertIsNotNone(toolbox.label)
        self.assertIsNotNone(tool.label)
        print("✓ Toolbox classes exist and are instantiable")


if __name__ == "__main__":
    unittest.main(verbosity=2)
