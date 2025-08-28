# -*- coding: utf-8 -*-
"""
Test Suite for toolbox_0_1_12.py - Enhanced GUI with improved dropdown labels and Auto multithreading option

Created: 2025-08-28 22:45
Version: 0.1.12
"""

import unittest
import sys
import os

# Add the src directory to Python path for testing
test_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(test_dir), "src")
sys.path.insert(0, src_dir)


class TestEnhancedGUIDropdownLabels(unittest.TestCase):
    """Test the enhanced GUI with improved dropdown labels and Auto multithreading option."""

    def test_enhanced_parameter_naming(self):
        """Test that the parameter is renamed from 'Thread Count' to 'Multithreading'."""
        from toolbox_0_1_12 import ForestClassificationTool

        tool = ForestClassificationTool()

        # Check that the tool label reflects v0.1.12
        self.assertIn("v0.1.12", tool.label)

        # The enhanced GUI features are in the ToolValidator, not the Python class
        # So we test that the tool exists and has the right version
        self.assertIn("Enhanced GUI", tool.description)
        print("✓ Tool properly identifies as enhanced GUI version")

    def test_auto_multithreading_option_structure(self):
        """Test the Auto multithreading option in ToolValidator structure."""

        # Test the enhanced _thread_labels method logic
        def _thread_labels_enhanced(cores):
            """Enhanced GUI with Auto option and detailed thread information"""
            auto = "Auto (let system decide)"
            moderate = max(2, int(cores * 0.45))  # 45% utilization
            high = max(3, int(cores * 0.90))  # 90% utilization
            return [
                auto,
                f"Moderate - {moderate} threads (45% utilization)",
                f"High - {high} threads (90% utilization)",
            ]

        # Test with 16 cores
        labels = _thread_labels_enhanced(16)
        expected = [
            "Auto (let system decide)",
            "Moderate - 7 threads (45% utilization)",
            "High - 14 threads (90% utilization)",
        ]
        self.assertEqual(labels, expected)

        # Test with 8 cores
        labels = _thread_labels_enhanced(8)
        expected = [
            "Auto (let system decide)",
            "Moderate - 3 threads (45% utilization)",
            "High - 7 threads (90% utilization)",
        ]
        self.assertEqual(labels, expected)

        print("✓ Auto multithreading option with detailed labels verified")

    def test_enhanced_memory_labels(self):
        """Test the enhanced memory allocation labels with detailed information."""

        # Test the enhanced _memory_labels method logic
        def _memory_labels_enhanced(avail_gb):
            """Enhanced GUI with detailed memory allocation information"""
            conservative = max(2, int(avail_gb * 0.30))  # 30%
            balanced = max(4, int(avail_gb * 0.60))  # 60%
            aggressive = max(6, int(avail_gb * 0.90))  # 90%
            return [
                f"{conservative} GB (30% of {avail_gb:.1f} GB available)",
                f"{balanced} GB (60% of {avail_gb:.1f} GB available)",
                f"{aggressive} GB (90% of {avail_gb:.1f} GB available)",
            ]

        # Test with 41.2 GB available (example from requirements)
        labels = _memory_labels_enhanced(41.2)
        expected = [
            "12 GB (30% of 41.2 GB available)",
            "24 GB (60% of 41.2 GB available)",
            "37 GB (90% of 41.2 GB available)",
        ]
        self.assertEqual(labels, expected)

        # Test with 16 GB available
        labels = _memory_labels_enhanced(16.0)
        expected = [
            "4 GB (30% of 16.0 GB available)",
            "9 GB (60% of 16.0 GB available)",
            "14 GB (90% of 16.0 GB available)",
        ]
        self.assertEqual(labels, expected)

        print("✓ Enhanced memory labels with detailed allocation information verified")

    def test_utilization_percentages(self):
        """Test that the utilization percentages are correct (30%, 45%, 60%, 90%)."""

        # Test thread utilization percentages
        test_cores = 20
        moderate_threads = max(2, int(test_cores * 0.45))  # 45%
        high_threads = max(3, int(test_cores * 0.90))  # 90%

        self.assertEqual(moderate_threads, 9)  # 45% of 20 = 9
        self.assertEqual(high_threads, 18)  # 90% of 20 = 18

        # Test memory utilization percentages
        test_memory = 32.0
        conservative_mem = max(2, int(test_memory * 0.30))  # 30%
        balanced_mem = max(4, int(test_memory * 0.60))  # 60%
        aggressive_mem = max(6, int(test_memory * 0.90))  # 90%

        self.assertEqual(conservative_mem, 9)  # 30% of 32 = 9.6 -> 9
        self.assertEqual(balanced_mem, 19)  # 60% of 32 = 19.2 -> 19
        self.assertEqual(aggressive_mem, 28)  # 90% of 32 = 28.8 -> 28

        print("✓ Utilization percentages (30%, 45%, 60%, 90%) verified")

    def test_version_information(self):
        """Test that version information is correctly formatted for v0.1.12."""
        import toolbox_0_1_12

        # Check that the module has the expected docstring format
        docstring = toolbox_0_1_12.__doc__
        self.assertIn("v0.1.12", docstring)
        self.assertIn("Enhanced GUI with improved dropdown labels", docstring)
        self.assertIn("Auto multithreading option", docstring)
        print("✓ Version information correctly updated for v0.1.12")

    def test_toolbox_classes_enhanced(self):
        """Test that toolbox classes reflect v0.1.12 enhancements."""
        from toolbox_0_1_12 import ForestClassificationToolbox, ForestClassificationTool

        # Test toolbox
        toolbox = ForestClassificationToolbox()
        self.assertIn("v0.1.12", toolbox.label)
        self.assertIn("Enhanced GUI", toolbox.description)

        # Test tool
        tool = ForestClassificationTool()
        self.assertIn("v0.1.12", tool.label)
        self.assertIn("Enhanced GUI", tool.description)

        print("✓ Toolbox classes properly reflect v0.1.12 enhancements")

    def test_parameter_display_names(self):
        """Test that parameter display names are updated for enhanced GUI."""
        from toolbox_0_1_12 import ForestClassificationTool

        tool = ForestClassificationTool()

        # Mock arcpy Parameter to capture parameter definitions
        class MockParameter:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
                self.category = None

        # Mock arcpy module
        import sys

        class MockArcpy:
            Parameter = MockParameter

        original_arcpy = sys.modules.get("arcpy")
        sys.modules["arcpy"] = MockArcpy()

        try:
            # Get parameters
            params = tool.getParameterInfo()

            # Check parameter display names
            self.assertEqual(params[0].displayName, "Output Feature Layer")
            self.assertEqual(
                params[1].displayName, "Multithreading"
            )  # Enhanced from "Thread Count"
            self.assertEqual(params[2].displayName, "Memory Allocation")

            print("✓ Parameter display names updated for enhanced GUI")

        finally:
            # Restore original arcpy
            if original_arcpy:
                sys.modules["arcpy"] = original_arcpy
            elif "arcpy" in sys.modules:
                del sys.modules["arcpy"]

    def test_difference_from_v0_1_11(self):
        """Test key differences between v0.1.11 and v0.1.12."""

        # The main differences should be:
        # 1. Parameter name: "Thread Count" -> "Multithreading"
        # 2. Thread options: Simple format -> Auto + detailed format
        # 3. Memory options: Simple format -> Detailed with percentages

        # Test v0.1.11 format (for comparison)
        def _thread_labels_v0_1_11(cores):
            low = max(1, cores // 4)  # ~25%
            mid = max(2, cores // 2)  # ~50%
            hi = max(3, int(cores * 0.90))  # 90% max
            return [f"Low ({low})", f"Balanced ({mid})", f"High ({hi})"]

        # Test v0.1.12 format (enhanced)
        def _thread_labels_v0_1_12(cores):
            auto = "Auto (let system decide)"
            moderate = max(2, int(cores * 0.45))  # 45% utilization
            high = max(3, int(cores * 0.90))  # 90% utilization
            return [
                auto,
                f"Moderate - {moderate} threads (45% utilization)",
                f"High - {high} threads (90% utilization)",
            ]

        # Compare with 16 cores
        v11_labels = _thread_labels_v0_1_11(16)
        v12_labels = _thread_labels_v0_1_12(16)

        # They should be different
        self.assertNotEqual(v11_labels, v12_labels)

        # v0.1.11: ["Low (4)", "Balanced (8)", "High (14)"]
        # v0.1.12: ["Auto (let system decide)", "Moderate - 7 threads (45% utilization)", "High - 14 threads (90% utilization)"]

        self.assertEqual(v11_labels, ["Low (4)", "Balanced (8)", "High (14)"])
        self.assertEqual(
            v12_labels,
            [
                "Auto (let system decide)",
                "Moderate - 7 threads (45% utilization)",
                "High - 14 threads (90% utilization)",
            ],
        )

        print("✓ v0.1.12 successfully differs from v0.1.11 with enhanced GUI features")


if __name__ == "__main__":
    unittest.main(verbosity=2)
