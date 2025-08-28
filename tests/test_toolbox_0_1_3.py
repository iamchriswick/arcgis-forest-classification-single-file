"""
Test module for Phase 1 Forest Classification Tool v0.1.3

Tests the corrected ArcGIS Pro data types and dropdown filter functionality.
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Mock arcpy BEFORE any imports that might use it
mock_arcpy = MagicMock()
sys.modules["arcpy"] = mock_arcpy

# Add the src directory to the path for imports
script_dir = Path(__file__).parent.parent
src_dir = script_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    from toolbox_0_1_3 import ForestClassificationToolbox, ForestClassificationTool
    from toolbox_0_1_3 import (
        get_system_capabilities,
        create_dynamic_thread_options,
        create_dynamic_memory_options,
    )
except ImportError:
    # If we can't import, we'll handle it in tests
    ForestClassificationToolbox = None


class TestForestClassificationToolboxV0_1_3(unittest.TestCase):
    """Test suite for the ForestClassificationToolbox class v0.1.3."""

    def setUp(self):
        """Set up test fixtures."""
        if ForestClassificationToolbox is None:
            self.skipTest("Could not import ForestClassificationToolbox")
        self.toolbox = ForestClassificationToolbox()

    def test_toolbox_initialization(self):
        """Test toolbox is properly initialized with v0.1.3 properties."""
        self.assertEqual(
            self.toolbox.label, "Forest Classification Toolbox - Phase 1 v0.1.3"
        )
        self.assertEqual(self.toolbox.alias, "ForestClassificationPhase1v0_1_3")
        self.assertIn("Forest species classification tool", self.toolbox.description)
        self.assertEqual(len(self.toolbox.tools), 1)
        self.assertEqual(self.toolbox.tools[0], ForestClassificationTool)

    def test_toolbox_description_content(self):
        """Test toolbox description contains key information."""
        description = self.toolbox.description
        self.assertIn("dynamic system detection", description)
        self.assertIn("CPU cores", description)
        self.assertIn("memory allocation", description)


class TestForestClassificationToolV0_1_3(unittest.TestCase):
    """Test suite for the ForestClassificationTool class v0.1.3."""

    def setUp(self):
        """Set up test fixtures."""
        if ForestClassificationTool is None:
            self.skipTest("Could not import ForestClassificationTool")
        self.tool = ForestClassificationTool()

    def test_tool_initialization(self):
        """Test tool is properly initialized with v0.1.3 properties."""
        self.assertEqual(self.tool.label, "Forest Classification Tool - Phase 1 v0.1.3")
        self.assertIn("Classifies forest features", self.tool.description)
        self.assertFalse(self.tool.canRunInBackground)
        self.assertEqual(self.tool.category, "Forest Analysis")

    def test_is_licensed(self):
        """Test tool licensing."""
        self.assertTrue(self.tool.isLicensed())

    @patch("toolbox_0_1_3.get_system_capabilities")
    def test_get_parameter_info_structure(self, mock_capabilities):
        """Test parameter info returns correct structure with v0.1.3 data types."""
        # Mock system capabilities
        mock_capabilities.return_value = (8, 32.0, 16.0)

        # Mock Parameter class
        mock_param = Mock()
        mock_param.filter = Mock()
        mock_arcpy.Parameter.return_value = mock_param

        parameters = self.tool.getParameterInfo()

        # Should return 3 parameters
        self.assertEqual(len(parameters), 3)

        # Verify Parameter constructor calls with correct data types
        expected_calls = [
            # Output layer parameter
            {
                "displayName": "Output Feature Layer",
                "name": "output_layer",
                "datatype": "GPFeatureLayer",  # v0.1.3 correction
                "parameterType": "Required",
                "direction": "Input",
            },
            # Thread config parameter
            {
                "displayName": "Thread Count",
                "name": "thread_config",
                "datatype": "GPString",  # v0.1.3 correction
                "parameterType": "Required",
                "direction": "Input",
            },
            # Memory config parameter
            {
                "displayName": "Memory Allocation",
                "name": "memory_config",
                "datatype": "GPString",  # v0.1.3 correction
                "parameterType": "Required",
                "direction": "Input",
            },
        ]

        # Verify each parameter was created with correct data types
        self.assertEqual(mock_arcpy.Parameter.call_count, 3)
        for i, expected_call in enumerate(expected_calls):
            actual_call = mock_arcpy.Parameter.call_args_list[i]
            for key, expected_value in expected_call.items():
                self.assertEqual(actual_call.kwargs[key], expected_value)

    @patch("toolbox_0_1_3.get_system_capabilities")
    def test_parameter_categories(self, mock_capabilities):
        """Test parameters have correct categories."""
        mock_capabilities.return_value = (8, 32.0, 16.0)

        mock_param = Mock()
        mock_param.filter = Mock()
        mock_arcpy.Parameter.return_value = mock_param

        parameters = self.tool.getParameterInfo()

        # Check that categories were set
        self.assertEqual(
            mock_param.category, "Performance Settings"
        )  # Last parameter set

    def test_update_parameters(self):
        """Test updateParameters method."""
        result = self.tool.updateParameters([])
        self.assertIsNone(result)

    def test_update_messages(self):
        """Test updateMessages method."""
        result = self.tool.updateMessages([])
        self.assertIsNone(result)

    def test_execute_basic_functionality(self):
        """Test execute method basic functionality."""
        # Mock parameters
        mock_params = [Mock(), Mock(), Mock()]
        mock_params[0].valueAsText = "test_layer"
        mock_params[1].valueAsText = "Balanced (4 threads)"
        mock_params[2].valueAsText = "Balanced (8 GB)"

        # Test execute doesn't raise exceptions
        with patch(
            "toolbox_0_1_3.get_system_capabilities", return_value=(8, 32.0, 16.0)
        ):
            result = self.tool.execute(mock_params, [])
            self.assertIsNone(result)

        # Verify AddMessage was called for v0.1.3
        self.assertTrue(mock_arcpy.AddMessage.called)

        # Check that v0.1.3 specific messages were logged
        messages = [call.args[0] for call in mock_arcpy.AddMessage.call_args_list]
        v0_1_3_messages = [msg for msg in messages if "v0.1.3" in msg]
        self.assertGreater(
            len(v0_1_3_messages), 0, "Should contain v0.1.3 specific messages"
        )

    def test_post_execute(self):
        """Test postExecute method."""
        result = self.tool.postExecute([])
        self.assertIsNone(result)

        # Verify cleanup message was logged
        self.assertTrue(mock_arcpy.AddMessage.called)


class TestSystemCapabilityFunctionsV0_1_3(unittest.TestCase):
    """Test suite for system capability detection functions v0.1.3."""

    @patch("os.cpu_count")
    @patch("psutil.virtual_memory")
    def test_get_system_capabilities_success(self, mock_memory, mock_cpu):
        """Test successful system capability detection."""
        # Mock successful detection
        mock_cpu.return_value = 8
        mock_memory_info = Mock()
        mock_memory_info.total = 32 * 1024**3  # 32 GB
        mock_memory_info.available = 16 * 1024**3  # 16 GB
        mock_memory.return_value = mock_memory_info

        cpu_cores, total_memory_gb, available_memory_gb = get_system_capabilities()

        self.assertEqual(cpu_cores, 8)
        self.assertAlmostEqual(total_memory_gb, 32.0, places=1)
        self.assertAlmostEqual(available_memory_gb, 16.0, places=1)

    @patch("os.cpu_count")
    @patch("psutil.virtual_memory")
    def test_get_system_capabilities_fallback(self, mock_memory, mock_cpu):
        """Test fallback values when detection fails."""
        # Mock detection failure
        mock_cpu.side_effect = Exception("Detection failed")
        mock_memory.side_effect = Exception("Detection failed")

        cpu_cores, total_memory_gb, available_memory_gb = get_system_capabilities()

        # Should return fallback values
        self.assertEqual(cpu_cores, 4)
        self.assertEqual(total_memory_gb, 16.0)
        self.assertEqual(available_memory_gb, 8.0)

    def test_create_dynamic_thread_options(self):
        """Test dynamic thread option creation."""
        # Test with 8 cores
        options = create_dynamic_thread_options(8)

        self.assertEqual(len(options), 3)
        self.assertEqual(options[0], "Conservative (2 threads)")  # 25% of 8 = 2
        self.assertEqual(options[1], "Balanced (4 threads)")  # 50% of 8 = 4
        self.assertEqual(options[2], "Performance (6 threads)")  # 75% of 8 = 6

    def test_create_dynamic_thread_options_minimum_values(self):
        """Test dynamic thread options respect minimum values."""
        # Test with 2 cores (should enforce minimums)
        options = create_dynamic_thread_options(2)

        self.assertEqual(len(options), 3)
        self.assertEqual(options[0], "Conservative (1 threads)")  # minimum 1
        self.assertEqual(options[1], "Balanced (2 threads)")  # minimum 2
        self.assertEqual(options[2], "Performance (3 threads)")  # minimum 3

    def test_create_dynamic_memory_options(self):
        """Test dynamic memory option creation."""
        # Test with 32 GB available
        options = create_dynamic_memory_options(32.0)

        self.assertEqual(len(options), 3)
        self.assertEqual(options[0], "Conservative (8 GB)")  # 25% of 32 = 8
        self.assertEqual(options[1], "Balanced (16 GB)")  # 50% of 32 = 16
        self.assertEqual(options[2], "Performance (24 GB)")  # 75% of 32 = 24

    def test_create_dynamic_memory_options_minimum_values(self):
        """Test dynamic memory options respect minimum values."""
        # Test with 4 GB available (should enforce minimums)
        options = create_dynamic_memory_options(4.0)

        self.assertEqual(len(options), 3)
        self.assertEqual(options[0], "Conservative (2 GB)")  # minimum 2
        self.assertEqual(options[1], "Balanced (4 GB)")  # minimum 4
        self.assertEqual(options[2], "Performance (6 GB)")  # minimum 6


if __name__ == "__main__":
    unittest.main()
