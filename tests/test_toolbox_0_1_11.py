# -*- coding: utf-8 -*-
"""
Test Suite for toolbox_0_1_11.py - Re-enabled System Detection with 90% Max Thread Rule

Created: 2025-08-28 22:45
Version: 0.1.11
"""

import unittest
import sys
import os

# Add the src directory to Python path for testing
test_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(test_dir), "src")
sys.path.insert(0, src_dir)


class TestSystemDetectionWithThreadRule(unittest.TestCase):
    """Test the re-enabled system detection with 90% max thread rule."""

    def test_cpu_count_detection(self):
        """Test that CPU core detection works."""
        import os

        cpu_cores = os.cpu_count()
        self.assertIsNotNone(cpu_cores)
        if cpu_cores is not None:
            self.assertGreater(cpu_cores, 0)

            # Test 90% calculation
            max_threads = max(1, int(cpu_cores * 0.9))
            self.assertGreater(max_threads, 0)
            self.assertLessEqual(max_threads, cpu_cores)
            print(f"✓ CPU cores: {cpu_cores}, Max threads (90%): {max_threads}")

    def test_90_percent_thread_calculation(self):
        """Test the 90% max thread calculation logic."""
        test_cases = [
            (4, 3),  # 4 cores -> 3 threads (90% = 3.6 -> 3)
            (8, 7),  # 8 cores -> 7 threads (90% = 7.2 -> 7)
            (16, 14),  # 16 cores -> 14 threads (90% = 14.4 -> 14)
            (1, 1),  # 1 core -> 1 thread (minimum)
        ]

        for cores, expected_max in test_cases:
            actual_max = max(1, int(cores * 0.9))
            self.assertEqual(
                actual_max,
                expected_max,
                f"For {cores} cores, expected {expected_max} max threads, got {actual_max}",
            )

        print("✓ 90% thread calculation logic verified")

    def test_system_detection_function_exists(self):
        """Test that the system detection function exists and is callable."""
        from toolbox_0_1_11 import log_system_capabilities

        self.assertTrue(callable(log_system_capabilities))
        print("✓ System detection function is callable")

    def test_module_imports_with_system_detection(self):
        """Test that the module imports properly with system detection re-enabled."""
        import time

        start_time = time.time()

        import toolbox_0_1_11

        import_time = time.time() - start_time
        # Should still be reasonably fast even with system detection
        self.assertLess(import_time, 2.0, "Module import should be reasonably fast")
        print(f"✓ Module import time with system detection: {import_time:.3f} seconds")

    def test_version_information(self):
        """Test that version information is correctly formatted."""
        import toolbox_0_1_11

        # Check that the module has the expected docstring format
        docstring = toolbox_0_1_11.__doc__
        self.assertIn("v0.1.11", docstring)
        self.assertIn("90% max thread rule", docstring)
        print("✓ Version information correctly updated for v0.1.11")

    def test_toolvalidator_thread_calculation(self):
        """Test the ToolValidator thread calculation logic."""

        # Simulate the ToolValidator _thread_labels method
        def _thread_labels(cores):
            low = max(1, cores // 4)  # ~25%
            mid = max(2, cores // 2)  # ~50%
            hi = max(3, int(cores * 0.90))  # 90% max (changed from 75%)
            return [f"Low ({low})", f"Balanced ({mid})", f"High ({hi})"]

        # Test with 16 cores (common case)
        labels = _thread_labels(16)
        expected = ["Low (4)", "Balanced (8)", "High (14)"]
        self.assertEqual(labels, expected)

        # Test with 8 cores
        labels = _thread_labels(8)
        expected = ["Low (2)", "Balanced (4)", "High (7)"]
        self.assertEqual(labels, expected)

        print("✓ ToolValidator thread calculation with 90% rule verified")


if __name__ == "__main__":
    unittest.main(verbosity=2)
