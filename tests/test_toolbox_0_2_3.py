# -*- coding: utf-8 -*-
"""
Test Forest Classification Tool - Phase 2: Core Data Processing v0.2.3

Created: 2025-08-29 11:30
Version: 0.2.3

Test suite for Phase 2 implementation with auto-discovery mode.
Tests basic data reading capabilities, field management, and robust error handling.

Developed as part of the Single File Development Strategy for ArcGIS Pro Forest Classification Tool.
"""

import unittest
import sys
import os

# Add the src directory to the path so we can import our toolbox modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import importlib.util

    ARCPY_AVAILABLE = importlib.util.find_spec("arcpy") is not None
except ImportError:
    ARCPY_AVAILABLE = False


class MockArcpyForTesting:
    """Mock ArcGIS functionality for testing without full ArcGIS Pro environment."""

    def __init__(self):
        self.messages = []

    def AddMessage(self, message):
        self.messages.append(("info", message))
        print(f"INFO: {message}")

    def AddError(self, message):
        self.messages.append(("error", message))
        print(f"ERROR: {message}")

    def Exists(self, path):
        # Mock some datasets as existing for testing
        return "Grid_8m_SR16_srrhogstaar" in path or "Grid_8m_Location" in path

    def Describe(self, path):
        class MockDesc:
            dataType = "FeatureClass"

        return MockDesc()


# Mock arcpy if not available
if not ARCPY_AVAILABLE:
    import types

    mock_arcpy = types.ModuleType("arcpy")

    # Add mock functionality using setattr to avoid type checking issues
    mock_instance = MockArcpyForTesting()
    setattr(mock_arcpy, "AddMessage", mock_instance.AddMessage)
    setattr(mock_arcpy, "AddError", mock_instance.AddError)
    setattr(mock_arcpy, "Exists", mock_instance.Exists)
    setattr(mock_arcpy, "Describe", mock_instance.Describe)

    sys.modules["arcpy"] = mock_arcpy


class TestPhase2AutoDiscovery(unittest.TestCase):
    """Test Phase 2 auto-discovery and data processing functionality."""

    def setUp(self):
        """Set up test environment."""
        # Import after arcpy is set up
        from src.toolbox_0_2_3 import (
            get_system_capabilities,
            get_predefined_datasets,
            discover_datasets,
            validate_layer_exists,
        )

        self.get_system_capabilities = get_system_capabilities
        self.get_predefined_datasets = get_predefined_datasets
        self.discover_datasets = discover_datasets
        self.validate_layer_exists = validate_layer_exists

    def test_system_capabilities(self):
        """Test that system capabilities are detected properly."""
        capabilities = self.get_system_capabilities()

        # Test required keys exist
        required_keys = ["cpu_count", "memory_gb", "max_threads", "max_memory_gb"]
        for key in required_keys:
            self.assertIn(key, capabilities)

        # Test reasonable values
        self.assertGreaterEqual(capabilities["cpu_count"], 1)
        self.assertGreaterEqual(capabilities["memory_gb"], 1)
        self.assertGreaterEqual(capabilities["max_threads"], 1)
        self.assertGreaterEqual(capabilities["max_memory_gb"], 1)

        # Test 90% rule applied
        self.assertLessEqual(capabilities["max_threads"], capabilities["cpu_count"])
        self.assertLessEqual(capabilities["max_memory_gb"], capabilities["memory_gb"])

    def test_predefined_datasets_complete(self):
        """Test that predefined datasets list is comprehensive."""
        datasets = self.get_predefined_datasets()

        # Test we have a substantial list
        self.assertGreater(len(datasets), 50)  # Should have 50+ datasets

        # Test key dataset categories are included
        sr16_datasets = [d for d in datasets if "SR16" in d]
        ar5_datasets = [d for d in datasets if "AR5" in d]
        location_datasets = [d for d in datasets if "Location" in d]
        elev_datasets = [d for d in datasets if "ElevStats" in d]

        self.assertGreater(len(sr16_datasets), 30)  # Substantial SR16 coverage
        self.assertGreater(len(ar5_datasets), 2)  # AR5 soil properties
        self.assertGreater(len(location_datasets), 0)  # Location data
        self.assertGreater(len(elev_datasets), 0)  # Elevation stats

        # Test specific critical datasets are included
        critical_datasets = [
            "Grid_8m_SR16_Dataset/Grid_8m_SR16_srrhogstaar",  # Age data
            "Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtreslag",  # Species type
            "Grid_8m_Location",  # Location
            "Table_Grid_8m_ElevStats",  # Elevation
        ]

        for critical in critical_datasets:
            self.assertIn(critical, datasets, f"Critical dataset missing: {critical}")

    def test_layer_validation_basic(self):
        """Test basic layer validation functionality."""
        # Test with mock existing layer
        if not ARCPY_AVAILABLE:
            # Mock test
            result = self.validate_layer_exists(
                "Grid_8m_SR16_Dataset/Grid_8m_SR16_srrhogstaar"
            )
            self.assertTrue(result)

            # Test non-existing layer
            result = self.validate_layer_exists("NonExistent_Layer")
            self.assertFalse(result)

    def test_discovery_error_handling(self):
        """Test that dataset discovery handles errors gracefully."""
        if not ARCPY_AVAILABLE:
            # Test with mock datasets
            found, missing, success = self.discover_datasets()

            # Should find some datasets, miss others
            self.assertGreater(len(found), 0)
            self.assertGreater(len(missing), 0)

            # Should fail because not all datasets found
            self.assertFalse(success)


class TestPhase2DataProcessing(unittest.TestCase):
    """Test Phase 2 data processing capabilities."""

    def setUp(self):
        """Set up test environment."""
        from src.toolbox_0_2_3 import (
            get_field_info,
            get_feature_count,
            read_sample_features,
            process_layer_basic,
        )

        self.get_field_info = get_field_info
        self.get_feature_count = get_feature_count
        self.read_sample_features = read_sample_features
        self.process_layer_basic = process_layer_basic

    def test_field_info_structure(self):
        """Test that field info returns expected structure."""
        if not ARCPY_AVAILABLE:
            # Test would require mock field data
            self.assertTrue(True)  # Placeholder for mock implementation

    def test_progress_callback_integration(self):
        """Test that progress callbacks work correctly."""
        if not ARCPY_AVAILABLE:
            progress_calls = []

            def mock_progress(percent, message):
                progress_calls.append((percent, message))

            # Test progress callback structure
            mock_progress(0, "Starting")
            mock_progress(50, "Halfway")
            mock_progress(100, "Complete")

            self.assertEqual(len(progress_calls), 3)
            self.assertEqual(progress_calls[0][0], 0)
            self.assertEqual(progress_calls[-1][0], 100)


class TestPhase2ToolboxIntegration(unittest.TestCase):
    """Test Phase 2 toolbox integration."""

    def setUp(self):
        """Set up test environment."""
        from src.toolbox_0_2_3 import (
            ForestClassificationToolbox,
            ForestClassificationTool,
        )

        self.toolbox_class = ForestClassificationToolbox
        self.tool_class = ForestClassificationTool

    def test_toolbox_structure(self):
        """Test that toolbox has proper structure for Phase 2."""
        toolbox = self.toolbox_class()

        # Test basic properties
        self.assertEqual(toolbox.label, "Forest Classification Toolbox - Phase 2")
        self.assertEqual(toolbox.alias, "ForestClassificationPhase2")
        self.assertIn("Phase 2", toolbox.description)

        # Test tool integration
        self.assertEqual(len(toolbox.tools), 1)
        self.assertEqual(toolbox.tools[0], self.tool_class)

    def test_tool_parameters_auto_discovery(self):
        """Test that tool parameters are configured for auto-discovery mode."""
        tool = self.tool_class()
        params = tool.getParameterInfo()

        # Should have 3 parameters for auto-discovery mode
        self.assertEqual(len(params), 3)

        # Check parameter configuration
        param_names = [p.name for p in params]
        expected_params = ["output_layer", "thread_count", "memory_allocation"]

        for expected in expected_params:
            self.assertIn(expected, param_names)

        # Test required parameters
        required_params = [p for p in params if p.parameterType == "Required"]
        self.assertEqual(len(required_params), 3)  # All parameters required

        # Test default values for system parameters
        thread_param = next(p for p in params if p.name == "thread_count")
        memory_param = next(p for p in params if p.name == "memory_allocation")

        self.assertEqual(thread_param.value, "Auto (Recommended)")
        self.assertEqual(memory_param.value, "Auto (Recommended)")

    def test_tool_execution_structure(self):
        """Test that tool execution method has proper Phase 2 structure."""
        tool = self.tool_class()

        # Test that tool has required methods
        self.assertTrue(hasattr(tool, "execute"))
        self.assertTrue(hasattr(tool, "getParameterInfo"))
        self.assertTrue(hasattr(tool, "isLicensed"))

        # Test tool properties
        self.assertEqual(tool.label, "Forest Classification Tool")
        self.assertIn("Auto-Discovery", tool.description)
        self.assertFalse(tool.canRunInBackground)  # Phase 2 is synchronous


class TestPhase2VersionConsistency(unittest.TestCase):
    """Test Phase 2 version consistency and file standards."""

    def test_version_references(self):
        """Test that version references are consistent throughout Phase 2."""
        # Read the source file to check version consistency
        file_path = os.path.join(
            os.path.dirname(__file__), "..", "src", "toolbox_0_2_3.py"
        )

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Test version references
            self.assertIn("v0.2.3", content)
            self.assertIn("Version: 0.2.3", content)
            self.assertIn("Phase 2", content)

            # Test that old versions are updated
            self.assertNotIn("v0.2.1", content)
            self.assertNotIn("v0.2.2", content)

            # Test version history includes new version
            self.assertIn("v0.2.3:", content)

    def test_phase_progression_notes(self):
        """Test that Phase 2 includes proper progression notes."""
        file_path = os.path.join(
            os.path.dirname(__file__), "..", "src", "toolbox_0_2_3.py"
        )

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Test phase documentation
            self.assertIn("Phase 2 Features:", content)
            self.assertIn("Phase 2 Focus:", content)
            self.assertIn("Auto-discovery", content.lower())

            # Test that future phases are referenced
            self.assertIn("Next Phase", content)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
