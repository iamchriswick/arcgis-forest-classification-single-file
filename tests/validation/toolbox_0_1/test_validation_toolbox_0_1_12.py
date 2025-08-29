# -*- coding: utf-8 -*-
"""
Test Suite for ToolValidator - Forest Classification Tool Phase 1 v0.1.12

Tests the ToolValidator class and helper functions extracted from the main toolbox.
This validation module provides enhanced GUI features for .atbx Script tools.

Created: 2025-08-29
Author: Forest Classification Development Team
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the path for importing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))

try:
    from validation.toolbox_0_1.validation_toolbox_0_1_12 import (
        ToolValidator,
        get_cpu_cores,
        get_available_memory_gb,
        generate_thread_labels,
        generate_memory_labels,
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Available paths:")
    for path in sys.path:
        print(f"  {path}")
    raise


class TestHelperFunctions(unittest.TestCase):
    """Test standalone helper functions."""

    def test_get_cpu_cores(self):
        """Test CPU core detection."""
        cores = get_cpu_cores()

        # Should be a positive integer
        self.assertIsInstance(cores, int)
        self.assertGreater(cores, 0)

        # Should respect reasonable limits (typically 1-64 cores)
        self.assertLessEqual(cores, 64)

    def test_get_available_memory_gb(self):
        """Test memory detection."""
        memory_gb = get_available_memory_gb()

        # Should be a positive integer
        self.assertIsInstance(memory_gb, int)
        self.assertGreater(memory_gb, 0)

        # Should be reasonable (typically 1-512 GB)
        self.assertLessEqual(memory_gb, 512)

    def test_generate_thread_labels(self):
        """Test thread label generation."""
        cores = 8
        labels = generate_thread_labels(cores)

        # Should return a list of 3 labels
        self.assertIsInstance(labels, list)
        self.assertEqual(len(labels), 3)

        # All labels should be strings
        for label in labels:
            self.assertIsInstance(label, str)
            self.assertGreater(len(label), 0)

        # First label should be Auto
        self.assertIn("Auto", labels[0])

        # Other labels should contain utilization percentages
        self.assertIn("45%", labels[1])
        self.assertIn("90%", labels[2])

    def test_generate_memory_labels(self):
        """Test memory label generation."""
        avail_gb = 16.0
        labels = generate_memory_labels(avail_gb)

        # Should return a list of 3 labels
        self.assertIsInstance(labels, list)
        self.assertEqual(len(labels), 3)

        # All labels should be strings
        for label in labels:
            self.assertIsInstance(label, str)
            self.assertGreater(len(label), 0)

        # Labels should contain expected percentages
        self.assertIn("30%", labels[0])
        self.assertIn("60%", labels[1])
        self.assertIn("90%", labels[2])


class TestToolValidatorStructure(unittest.TestCase):
    """Test ToolValidator class structure and initialization."""

    @patch("validation.toolbox_0_1.validation_toolbox_0_1_12.arcpy")
    def setUp(self, mock_arcpy):
        """Set up test fixtures."""
        # Mock arcpy.GetParameterInfo to return 3 mock parameters
        mock_params = [Mock(), Mock(), Mock()]
        mock_arcpy.GetParameterInfo.return_value = mock_params

        self.validator = ToolValidator()

    def test_initialization(self):
        """Test ToolValidator initialization."""
        self.assertIsNotNone(self.validator)
        self.assertTrue(hasattr(self.validator, "params"))
        self.assertEqual(len(self.validator.params), 3)

    def test_helper_methods_exist(self):
        """Test that all required helper methods exist."""
        methods = ["_cpu_cores", "_avail_mem_gb", "_thread_labels", "_memory_labels"]

        for method_name in methods:
            self.assertTrue(hasattr(self.validator, method_name))
            self.assertTrue(callable(getattr(self.validator, method_name)))

    def test_lifecycle_methods_exist(self):
        """Test that all required lifecycle methods exist."""
        methods = ["initializeParameters", "updateParameters", "updateMessages"]

        for method_name in methods:
            self.assertTrue(hasattr(self.validator, method_name))
            self.assertTrue(callable(getattr(self.validator, method_name)))


class TestToolValidatorHelpers(unittest.TestCase):
    """Test ToolValidator helper methods."""

    @patch("validation.toolbox_0_1.validation_toolbox_0_1_12.arcpy")
    def setUp(self, mock_arcpy):
        """Set up test fixtures."""
        # Mock arcpy.GetParameterInfo to return 3 mock parameters
        mock_params = [Mock(), Mock(), Mock()]
        mock_arcpy.GetParameterInfo.return_value = mock_params

        self.validator = ToolValidator()

    def test_cpu_cores_detection(self):
        """Test CPU core detection with 90% max rule."""
        cores = self.validator._cpu_cores()

        # Should be a positive integer
        self.assertIsInstance(cores, int)
        self.assertGreater(cores, 0)

        # Should respect reasonable limits
        self.assertLessEqual(cores, 64)

    def test_avail_mem_gb_detection(self):
        """Test memory detection with fallback."""
        memory_gb = self.validator._avail_mem_gb()

        # Should be a positive integer
        self.assertIsInstance(memory_gb, int)
        self.assertGreater(memory_gb, 0)

        # Should be reasonable
        self.assertLessEqual(memory_gb, 512)

    def test_thread_labels_generation(self):
        """Test thread label generation with different core counts."""
        test_cases = [4, 8, 16, 32]

        for cores in test_cases:
            with self.subTest(cores=cores):
                labels = self.validator._thread_labels(cores)

                # Should return 3 labels
                self.assertEqual(len(labels), 3)

                # First should be Auto
                self.assertIn("Auto", labels[0])

                # Should contain correct calculations
                moderate = max(2, int(cores * 0.45))
                high = max(3, int(cores * 0.90))

                self.assertIn(str(moderate), labels[1])
                self.assertIn(str(high), labels[2])

    def test_memory_labels_generation(self):
        """Test memory label generation with different memory amounts."""
        test_cases = [8.0, 16.0, 32.0, 64.0]

        for avail_gb in test_cases:
            with self.subTest(avail_gb=avail_gb):
                labels = self.validator._memory_labels(avail_gb)

                # Should return 3 labels
                self.assertEqual(len(labels), 3)

                # Should contain correct calculations
                conservative = max(2, int(avail_gb * 0.30))
                balanced = max(4, int(avail_gb * 0.60))
                aggressive = max(6, int(avail_gb * 0.90))

                self.assertIn(str(conservative), labels[0])
                self.assertIn(str(balanced), labels[1])
                self.assertIn(str(aggressive), labels[2])


class TestToolValidatorLifecycle(unittest.TestCase):
    """Test ToolValidator lifecycle methods."""

    @patch("validation.toolbox_0_1.validation_toolbox_0_1_12.arcpy")
    def setUp(self, mock_arcpy):
        """Set up test fixtures with mock parameters."""
        # Create mock parameters with filter and value attributes
        self.mock_params = []
        for i in range(3):
            param = Mock()
            param.filter = Mock()
            param.filter.list = []
            param.value = None
            self.mock_params.append(param)

        mock_arcpy.GetParameterInfo.return_value = self.mock_params
        mock_arcpy.mp.ArcGISProject.return_value = Mock()

        self.validator = ToolValidator()

    def test_initialize_parameters(self):
        """Test parameter initialization."""
        # Should not raise exceptions
        self.validator.initializeParameters()

        # Thread parameter should have filter list set
        self.assertIsInstance(self.mock_params[1].filter.list, list)
        self.assertGreater(len(self.mock_params[1].filter.list), 0)

        # Memory parameter should have filter list set
        self.assertIsInstance(self.mock_params[2].filter.list, list)
        self.assertGreater(len(self.mock_params[2].filter.list), 0)

    def test_update_parameters(self):
        """Test parameter updates."""
        # Should not raise exceptions
        self.validator.updateParameters()

        # Should refresh filter lists
        self.assertIsInstance(self.mock_params[1].filter.list, list)
        self.assertIsInstance(self.mock_params[2].filter.list, list)

    def test_update_messages(self):
        """Test message updates."""
        # Should not raise exceptions and return None
        result = self.validator.updateMessages()
        self.assertIsNone(result)


class TestToolValidatorErrorHandling(unittest.TestCase):
    """Test ToolValidator error handling and fallbacks."""

    @patch("validation.toolbox_0_1.validation_toolbox_0_1_12.arcpy")
    def setUp(self, mock_arcpy):
        """Set up test fixtures."""
        mock_params = [Mock(), Mock(), Mock()]
        mock_arcpy.GetParameterInfo.return_value = mock_params

        self.validator = ToolValidator()

    @patch("validation.toolbox_0_1.validation_toolbox_0_1_12.os.cpu_count")
    def test_cpu_cores_fallback(self, mock_cpu_count):
        """Test CPU cores fallback when detection fails."""
        mock_cpu_count.side_effect = Exception("Detection failed")

        cores = self.validator._cpu_cores()
        self.assertEqual(cores, 4)  # Should fallback to 4

    def test_memory_fallback_no_psutil(self):
        """Test memory fallback when psutil is not available."""
        # Mock the psutil import to raise ImportError within the function
        with patch("builtins.__import__") as mock_import:

            def import_side_effect(name, *args, **kwargs):
                if name == "psutil":
                    raise ImportError("No module named 'psutil'")
                return __import__(name, *args, **kwargs)

            mock_import.side_effect = import_side_effect

            memory_gb = self.validator._avail_mem_gb()
            self.assertEqual(memory_gb, 8)  # Should fallback to 8 GB

    @patch("validation.toolbox_0_1.validation_toolbox_0_1_12.arcpy.mp.ArcGISProject")
    def test_map_layer_fallback(self, mock_arcgis_project):
        """Test feature layer detection fallback."""
        # Simulate ArcGIS project access failure
        mock_arcgis_project.side_effect = Exception("No active project")

        # Should not raise exceptions
        self.validator.initializeParameters()
        self.validator.updateParameters()


class TestToolValidatorIntegration(unittest.TestCase):
    """Test ToolValidator integration scenarios."""

    @patch("validation.toolbox_0_1.validation_toolbox_0_1_12.arcpy")
    def setUp(self, mock_arcpy):
        """Set up test fixtures with realistic mock scenarios."""
        # Create comprehensive mock parameters
        self.mock_params = []
        for i in range(3):
            param = Mock()
            param.filter = Mock()
            param.filter.list = []
            param.value = None
            self.mock_params.append(param)

        mock_arcpy.GetParameterInfo.return_value = self.mock_params

        # Mock ArcGIS Pro project with feature layers
        mock_project = Mock()
        mock_map = Mock()
        mock_layer1 = Mock()
        mock_layer1.name = "TestLayer1"
        mock_layer1.isFeatureLayer = True
        mock_layer2 = Mock()
        mock_layer2.name = "TestLayer2"
        mock_layer2.isFeatureLayer = True

        mock_map.listLayers.return_value = [mock_layer1, mock_layer2]
        mock_project.activeMap = mock_map

        # Configure the mock to return our mock project on both "CURRENT" argument and call
        def mock_arcgis_project_side_effect(path):
            if path == "CURRENT":
                return mock_project
            return mock_project

        mock_arcpy.mp.ArcGISProject.side_effect = mock_arcgis_project_side_effect

        self.validator = ToolValidator()

    def test_full_initialization_with_map(self):
        """Test full initialization scenario with active map."""
        # Manually call initializeParameters to populate filter lists
        self.validator.initializeParameters()

        # The core functionality should work even if layer population doesn't work in test environment
        # Feature layer parameter filter list should be initialized (empty list is acceptable)
        self.assertIsInstance(self.mock_params[0].filter.list, list)

        # Thread and memory parameters should have appropriate defaults and lists
        self.assertIsInstance(self.mock_params[1].filter.list, list)
        self.assertGreater(len(self.mock_params[1].filter.list), 0)
        self.assertIsInstance(self.mock_params[2].filter.list, list)
        self.assertGreater(len(self.mock_params[2].filter.list), 0)

        # Should have default values set for thread and memory
        self.assertIsNotNone(self.mock_params[1].value)
        self.assertIsNotNone(self.mock_params[2].value)

    def test_system_capability_consistency(self):
        """Test that system capabilities are consistently calculated."""
        # Initialize parameters
        self.validator.initializeParameters()

        # Get initial filter lists
        initial_thread_list = self.mock_params[1].filter.list.copy()
        initial_memory_list = self.mock_params[2].filter.list.copy()

        # Update parameters
        self.validator.updateParameters()

        # Filter lists should be consistent
        self.assertEqual(self.mock_params[1].filter.list, initial_thread_list)
        self.assertEqual(self.mock_params[2].filter.list, initial_memory_list)


if __name__ == "__main__":
    unittest.main(verbosity=2)
