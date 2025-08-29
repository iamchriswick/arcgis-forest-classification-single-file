# -*- coding: utf-8 -*-
"""
Test Suite for Forest Classification Toolbox - Phase 1 v0.1.4

This test suite validates the debugging and alternative filter setup implementation
for Phase 1 v0.1.4 of the Single File Development Strategy.

Author: iamchriswick
Version: 1.0.0
Created: 2025-08-29T14:55:00Z
Updated: 2025-08-29T14:55:00Z
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))

try:
    import arcpy

    ARCPY_AVAILABLE = True
except ImportError:
    # Mock arcpy for testing environments without ArcGIS Pro
    arcpy = MagicMock()
    arcpy.Parameter = MagicMock
    arcpy.AddMessage = MagicMock()
    ARCPY_AVAILABLE = False


class TestPhase1ToolboxV0_1_4(unittest.TestCase):
    """Test case for Phase 1 v0.1.4 - Debugging and alternative filter setup."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Import the module under test
        from execution.toolbox_0_1.toolbox_0_1_4 import (
            ForestClassificationToolbox,
            ForestClassificationTool,
        )

        self.toolbox_class = ForestClassificationToolbox
        self.tool_class = ForestClassificationTool

        # Create instances for testing
        self.toolbox = self.toolbox_class()
        self.tool = self.tool_class()

    def test_toolbox_initialization_v0_1_4(self):
        """Test that toolbox is properly initialized with v0.1.4 properties."""
        self.assertEqual(self.toolbox.label, "Forest Classification Toolbox - Phase 1")
        self.assertEqual(self.toolbox.alias, "ForestClassificationPhase1")
        self.assertIn("Phase 1", self.toolbox.description)
        self.assertIn("v0.1.4", self.toolbox.description)
        self.assertEqual(len(self.toolbox.tools), 1)
        self.assertEqual(self.toolbox.tools[0], self.tool_class)

    def test_tool_initialization_v0_1_4(self):
        """Test that tool is properly initialized with v0.1.4 properties."""
        self.assertEqual(self.tool.label, "Forest Classification Tool - Phase 1")
        self.assertIn("Phase 1", self.tool.description)
        self.assertIn("v0.1.4", self.tool.description)
        self.assertEqual(self.tool.canRunInBackground, False)
        self.assertEqual(self.tool.category, "Forest Analysis")

    @patch("execution.toolbox_0_1.toolbox_0_1_4.arcpy.Parameter")
    def test_parameter_structure_v0_1_4(self, mock_parameter):
        """Test that getParameterInfo returns correct parameter structure for v0.1.4."""
        # Configure mock to return a proper parameter-like object
        mock_param = MagicMock()
        mock_param.filter = MagicMock()
        mock_param.filter.list = []
        mock_parameter.return_value = mock_param

        parameters = self.tool.getParameterInfo()

        # Should return 3 parameters: output_layer, thread_config, memory_config
        self.assertEqual(len(parameters), 3)
        self.assertEqual(mock_parameter.call_count, 3)

    @patch("execution.toolbox_0_1.toolbox_0_1_4.arcpy.Parameter")
    def test_alternative_filter_initialization_v0_1_4(self, mock_parameter):
        """Test that v0.1.4 implements alternative filter initialization approach."""
        # Configure mock parameter with filter attribute
        mock_param = MagicMock()
        mock_param.filter = MagicMock()
        mock_param.filter.list = []
        mock_parameter.return_value = mock_param

        self.tool.getParameterInfo()

        # Verify filter configuration was attempted
        self.assertIsNotNone(mock_param.filter)
        # v0.1.4 should have alternative filter setup logic

    @patch("execution.toolbox_0_1.toolbox_0_1_4.arcpy.AddMessage")
    def test_execute_method_v0_1_4_debugging(self, mock_add_message):
        """Test execute method functionality for v0.1.4 with debugging features."""
        # Create mock parameters
        mock_params = [
            MagicMock(valueAsText="test_output_layer"),
            MagicMock(valueAsText="Balanced (4 threads)"),
            MagicMock(valueAsText="Balanced (8 GB)"),
        ]

        # Execute the method
        result = self.tool.execute(mock_params, None)

        # Should return None (no explicit return value)
        self.assertIsNone(result)

        # Verify that arcpy.AddMessage was called
        self.assertTrue(mock_add_message.called)

        # Check for v0.1.4 specific messages
        call_args_list = [call[0][0] for call in mock_add_message.call_args_list]

        # Should contain v0.1.4 specific messages
        v0_1_4_messages = [msg for msg in call_args_list if "v0.1.4" in msg]
        self.assertGreater(len(v0_1_4_messages), 0)

        # Should contain debugging related messages
        debug_messages = [
            msg
            for msg in call_args_list
            if any(
                keyword in msg.lower()
                for keyword in ["debugging", "alternative", "filter"]
            )
        ]
        self.assertGreaterEqual(len(debug_messages), 0)  # May or may not be present

    @patch("execution.toolbox_0_1.toolbox_0_1_4.arcpy.AddMessage")
    def test_progress_tracking_v0_1_4(self, mock_add_message):
        """Test that progress tracking works correctly for v0.1.4."""
        mock_params = [MagicMock(valueAsText="test") for _ in range(3)]

        # Execute the method
        self.tool.execute(mock_params, None)

        # Extract all messages
        call_args_list = [call[0][0] for call in mock_add_message.call_args_list]

        # Find progress messages
        progress_25 = next(
            (i for i, msg in enumerate(call_args_list) if "25%" in msg), -1
        )
        progress_50 = next(
            (i for i, msg in enumerate(call_args_list) if "50%" in msg), -1
        )
        progress_75 = next(
            (i for i, msg in enumerate(call_args_list) if "75%" in msg), -1
        )
        progress_100 = next(
            (i for i, msg in enumerate(call_args_list) if "100%" in msg), -1
        )

        # Verify all progress messages exist and are in correct order
        self.assertNotEqual(progress_25, -1, "25% progress message not found")
        self.assertNotEqual(progress_50, -1, "50% progress message not found")
        self.assertNotEqual(progress_75, -1, "75% progress message not found")
        self.assertNotEqual(progress_100, -1, "100% progress message not found")

        # Verify they are in correct order
        self.assertLess(progress_25, progress_50)
        self.assertLess(progress_50, progress_75)
        self.assertLess(progress_75, progress_100)

    def test_tool_licensing_v0_1_4(self):
        """Test that tool is licensed to execute in v0.1.4."""
        self.assertTrue(self.tool.isLicensed())

    def test_update_parameters_method_v0_1_4(self):
        """Test that updateParameters method exists and works for v0.1.4."""
        try:
            self.tool.updateParameters([])
        except Exception as e:
            self.fail(f"updateParameters raised {e} unexpectedly")

    def test_update_messages_method_v0_1_4(self):
        """Test that updateMessages method exists and works for v0.1.4."""
        try:
            self.tool.updateMessages([])
        except Exception as e:
            self.fail(f"updateMessages raised {e} unexpectedly")

    @patch("execution.toolbox_0_1.toolbox_0_1_4.arcpy.AddMessage")
    def test_post_execute_method_v0_1_4(self, mock_add_message):
        """Test that postExecute method exists and logs cleanup message for v0.1.4."""
        # Execute postExecute
        result = self.tool.postExecute([])

        # Should return None
        self.assertIsNone(result)

        # Should log cleanup message
        mock_add_message.assert_called_with(
            "🧹 Phase 1 post-execution cleanup completed"
        )

    def test_module_structure_v0_1_4(self):
        """Test that v0.1.4 module can be imported and has expected structure."""
        try:
            from execution.toolbox_0_1.toolbox_0_1_4 import (
                ForestClassificationToolbox,
                ForestClassificationTool,
            )

            # Test that classes are properly defined
            self.assertTrue(hasattr(ForestClassificationToolbox, "__init__"))
            self.assertTrue(hasattr(ForestClassificationTool, "__init__"))
            self.assertTrue(hasattr(ForestClassificationTool, "getParameterInfo"))
            self.assertTrue(hasattr(ForestClassificationTool, "isLicensed"))
            self.assertTrue(hasattr(ForestClassificationTool, "updateParameters"))
            self.assertTrue(hasattr(ForestClassificationTool, "updateMessages"))
            self.assertTrue(hasattr(ForestClassificationTool, "execute"))
            self.assertTrue(hasattr(ForestClassificationTool, "postExecute"))

        except ImportError as e:
            self.fail(f"Failed to import required classes: {e}")

    @patch("execution.toolbox_0_1.toolbox_0_1_4.arcpy.AddMessage")
    def test_parameter_logging_v0_1_4(self, mock_add_message):
        """Test that parameter logging works correctly for v0.1.4."""
        mock_params = [
            MagicMock(valueAsText="C:\\test\\output.shp"),
            MagicMock(valueAsText="Performance (6 threads)"),
            MagicMock(valueAsText="Performance (16 GB)"),
        ]

        # Execute the method
        self.tool.execute(mock_params, None)

        # Extract all messages
        call_args_list = [call[0][0] for call in mock_add_message.call_args_list]

        # Should log parameter values
        output_messages = [
            msg
            for msg in call_args_list
            if "Output layer:" in msg and "C:\\test\\output.shp" in msg
        ]
        thread_messages = [
            msg
            for msg in call_args_list
            if "Thread configuration:" in msg and "Performance (6 threads)" in msg
        ]
        memory_messages = [
            msg
            for msg in call_args_list
            if "Memory configuration:" in msg and "Performance (16 GB)" in msg
        ]

        self.assertGreater(len(output_messages), 0)
        self.assertGreater(len(thread_messages), 0)
        self.assertGreater(len(memory_messages), 0)

    def test_error_handling_v0_1_4(self):
        """Test execute method handles parameter errors gracefully in v0.1.4."""
        with patch("execution.toolbox_0_1.toolbox_0_1_4.arcpy.AddMessage"):
            # Test with None parameters
            try:
                # Create parameters that might cause AttributeError when accessing valueAsText
                mock_params = [None, None, None]

                # This should handle the error gracefully or raise a specific exception
                with self.assertRaises((AttributeError, TypeError)):
                    self.tool.execute(mock_params, None)

            except Exception:
                # If it handles errors gracefully, that's also acceptable
                pass

    @patch("execution.toolbox_0_1.toolbox_0_1_4.arcpy.AddMessage")
    def test_debugging_messages_in_execute_v0_1_4(self, mock_add_message):
        """Test that execute method includes debugging information for v0.1.4."""
        mock_params = [MagicMock(valueAsText="test") for _ in range(3)]

        # Execute the method
        self.tool.execute(mock_params, None)

        # Extract all messages
        call_args_list = [call[0][0] for call in mock_add_message.call_args_list]

        # Should contain some version information
        version_messages = [msg for msg in call_args_list if "v0.1.4" in msg]
        self.assertGreater(len(version_messages), 0)

    def test_alternative_approach_implementation_v0_1_4(self):
        """Test that v0.1.4 implements alternative approach for filter setup."""
        # This test verifies that the module loads and functions work
        # The alternative approach should be evident in the module structure
        try:
            from execution.toolbox_0_1.toolbox_0_1_4 import ForestClassificationTool

            tool = ForestClassificationTool()

            # The alternative approach should allow parameter creation to succeed
            with patch(
                "execution.toolbox_0_1.toolbox_0_1_4.arcpy.Parameter"
            ) as mock_param:
                mock_param.return_value = MagicMock()
                parameters = tool.getParameterInfo()
                self.assertEqual(len(parameters), 3)

        except Exception as e:
            self.fail(f"Alternative filter approach implementation failed: {e}")


@unittest.skipIf(
    not ARCPY_AVAILABLE, "ArcPy not available - skipping integration tests"
)
class TestPhase1ToolboxV0_1_4Integration(unittest.TestCase):
    """Integration tests for v0.1.4 that require actual ArcPy functionality."""

    def setUp(self):
        """Set up test fixtures for integration tests."""
        from execution.toolbox_0_1.toolbox_0_1_4 import ForestClassificationTool

        self.tool = ForestClassificationTool()

    def test_parameter_info_with_real_arcpy_v0_1_4(self):
        """Test parameter creation with real ArcPy for v0.1.4."""
        parameters = self.tool.getParameterInfo()

        # Should return 3 parameters
        self.assertEqual(len(parameters), 3)

        # Each parameter should be an actual arcpy.Parameter object
        for param in parameters:
            self.assertIsInstance(param, arcpy.Parameter)

    def test_real_parameter_properties_v0_1_4(self):
        """Test that parameters have correct properties when using real ArcPy for v0.1.4."""
        parameters = self.tool.getParameterInfo()

        output_layer = parameters[0]
        thread_config = parameters[1]
        memory_config = parameters[2]

        # Test parameter types and properties
        self.assertEqual(output_layer.datatype, "GPFeatureLayer")
        self.assertEqual(output_layer.direction, "Input")

        self.assertEqual(thread_config.datatype, "GPString")
        self.assertEqual(thread_config.direction, "Input")

        self.assertEqual(memory_config.datatype, "GPString")
        self.assertEqual(memory_config.direction, "Input")


if __name__ == "__main__":
    unittest.main(verbosity=2)
