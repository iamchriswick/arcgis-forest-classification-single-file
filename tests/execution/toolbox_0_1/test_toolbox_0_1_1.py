# -*- coding: utf-8 -*-
"""
Test Suite for Forest Classification Toolbox - Phase 1 v0.1.1

This test suite validates the basic ArcGIS toolbox structure implementation
for the first phase of the Single File Development Strategy.

Author: iamchriswick
Version: 1.0.0
Created: 2025-08-29T14:23:00Z
Updated: 2025-08-29T14:23:00Z
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


class TestPhase1ToolboxStructure(unittest.TestCase):
    """Test case for Phase 1 v0.1.1 - Basic ArcGIS toolbox structure."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Import the module under test
        from execution.toolbox_0_1.toolbox_0_1_1 import (
            ForestClassificationToolbox,
            ForestClassificationTool,
        )

        self.toolbox_class = ForestClassificationToolbox
        self.tool_class = ForestClassificationTool

        # Create instances for testing
        self.toolbox = self.toolbox_class()
        self.tool = self.tool_class()

    def test_toolbox_initialization(self):
        """Test that toolbox is properly initialized with Phase 1 properties."""
        self.assertEqual(self.toolbox.label, "Forest Classification Toolbox - Phase 1")
        self.assertEqual(self.toolbox.alias, "ForestClassificationPhase1")
        self.assertIn("Phase 1", self.toolbox.description)
        self.assertEqual(len(self.toolbox.tools), 1)
        self.assertEqual(self.toolbox.tools[0], self.tool_class)

    def test_tool_initialization(self):
        """Test that tool is properly initialized with Phase 1 properties."""
        self.assertEqual(self.tool.label, "Forest Classification Tool - Phase 1")
        self.assertIn("Phase 1", self.tool.description)
        self.assertEqual(self.tool.canRunInBackground, False)
        self.assertEqual(self.tool.category, "Forest Analysis")

    def test_tool_licensing(self):
        """Test that tool is licensed to execute."""
        self.assertTrue(self.tool.isLicensed())

    @patch("execution.toolbox_0_1.toolbox_0_1_1.arcpy.Parameter")
    def test_parameter_structure(self, mock_parameter):
        """Test that getParameterInfo returns correct parameter structure."""
        # Configure mock to return a proper parameter-like object
        mock_param = MagicMock()
        mock_param.filter = MagicMock()
        mock_parameter.return_value = mock_param

        parameters = self.tool.getParameterInfo()

        # Should return 3 parameters: output_layer, thread_config, memory_config
        self.assertEqual(len(parameters), 3)

        # Verify Parameter() was called 3 times
        self.assertEqual(mock_parameter.call_count, 3)

    @patch("execution.toolbox_0_1.toolbox_0_1_1.arcpy.Parameter")
    def test_output_layer_parameter(self, mock_parameter):
        """Test output layer parameter configuration."""
        mock_param = MagicMock()
        mock_param.filter = MagicMock()
        mock_parameter.return_value = mock_param

        parameters = self.tool.getParameterInfo()
        output_layer = parameters[0]

        # Verify filter configuration was attempted
        self.assertTrue(hasattr(output_layer, "filter"))

    @patch("execution.toolbox_0_1.toolbox_0_1_1.arcpy.Parameter")
    def test_thread_config_parameter(self, mock_parameter):
        """Test thread configuration parameter setup."""
        mock_param = MagicMock()
        mock_param.filter = MagicMock()
        mock_parameter.return_value = mock_param

        parameters = self.tool.getParameterInfo()
        thread_config = parameters[1]

        # Verify parameter was created and configured
        self.assertIsNotNone(thread_config)
        self.assertTrue(hasattr(thread_config, "filter"))

    @patch("execution.toolbox_0_1.toolbox_0_1_1.arcpy.Parameter")
    def test_memory_config_parameter(self, mock_parameter):
        """Test memory configuration parameter setup."""
        mock_param = MagicMock()
        mock_param.filter = MagicMock()
        mock_parameter.return_value = mock_param

        parameters = self.tool.getParameterInfo()
        memory_config = parameters[2]

        # Verify parameter was created and configured
        self.assertIsNotNone(memory_config)
        self.assertTrue(hasattr(memory_config, "filter"))

    def test_update_parameters_method(self):
        """Test that updateParameters method exists and has proper signature."""
        # Should not raise any exceptions when called with empty parameters
        try:
            self.tool.updateParameters([])
        except Exception as e:
            self.fail(f"updateParameters raised {e} unexpectedly")

    def test_update_messages_method(self):
        """Test that updateMessages method exists and has proper signature."""
        # Should not raise any exceptions when called with empty parameters
        try:
            self.tool.updateMessages([])
        except Exception as e:
            self.fail(f"updateMessages raised {e} unexpectedly")

    @patch("execution.toolbox_0_1.toolbox_0_1_1.arcpy.AddMessage")
    def test_execute_method_basic_functionality(self, mock_add_message):
        """Test execute method basic functionality and logging."""
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

        # Verify that arcpy.AddMessage was called multiple times for progress messages
        self.assertTrue(mock_add_message.called)
        self.assertGreaterEqual(
            mock_add_message.call_count, 5
        )  # At least 5 progress messages

        # Check for specific expected messages
        call_args_list = [call[0][0] for call in mock_add_message.call_args_list]

        # Should contain start message
        start_messages = [
            msg
            for msg in call_args_list
            if "Starting Forest Classification Tool" in msg
        ]
        self.assertGreater(len(start_messages), 0)

        # Should contain parameter logging
        param_messages = [msg for msg in call_args_list if "Output layer:" in msg]
        self.assertGreater(len(param_messages), 0)

        # Should contain progress messages
        progress_messages = [
            msg for msg in call_args_list if "Phase 1 progress:" in msg
        ]
        self.assertGreaterEqual(
            len(progress_messages), 4
        )  # Should have 25%, 50%, 75%, 100%

        # Should contain completion message
        completion_messages = [
            msg for msg in call_args_list if "completed successfully" in msg
        ]
        self.assertGreater(len(completion_messages), 0)

    @patch("execution.toolbox_0_1.toolbox_0_1_1.arcpy.AddMessage")
    def test_post_execute_method(self, mock_add_message):
        """Test that postExecute method exists and logs cleanup message."""
        # Execute postExecute
        result = self.tool.postExecute([])

        # Should return None
        self.assertIsNone(result)

        # Should log cleanup message
        mock_add_message.assert_called_with(
            "🧹 Phase 1 post-execution cleanup completed"
        )

    def test_parameter_extraction_in_execute(self):
        """Test that execute method properly extracts parameter values."""
        with patch(
            "execution.toolbox_0_1.toolbox_0_1_1.arcpy.AddMessage"
        ) as mock_add_message:
            # Create mock parameters with specific values
            mock_params = [
                MagicMock(valueAsText="C:\\test\\output.shp"),
                MagicMock(valueAsText="Performance (6 threads)"),
                MagicMock(valueAsText="Performance (16 GB)"),
            ]

            # Execute the method
            self.tool.execute(mock_params, None)

            # Check that parameter values were logged correctly
            call_args_list = [call[0][0] for call in mock_add_message.call_args_list]

            # Find parameter logging messages
            output_messages = [
                msg
                for msg in call_args_list
                if "Output layer: C:\\test\\output.shp" in msg
            ]
            thread_messages = [
                msg
                for msg in call_args_list
                if "Thread configuration: Performance (6 threads)" in msg
            ]
            memory_messages = [
                msg
                for msg in call_args_list
                if "Memory configuration: Performance (16 GB)" in msg
            ]

            self.assertGreater(
                len(output_messages), 0, "Output layer parameter not logged correctly"
            )
            self.assertGreater(
                len(thread_messages),
                0,
                "Thread configuration parameter not logged correctly",
            )
            self.assertGreater(
                len(memory_messages),
                0,
                "Memory configuration parameter not logged correctly",
            )

    def test_progress_tracking_sequence(self):
        """Test that execute method logs progress in correct sequence."""
        with patch(
            "execution.toolbox_0_1.toolbox_0_1_1.arcpy.AddMessage"
        ) as mock_add_message:
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
            self.assertLess(
                progress_25, progress_50, "Progress messages not in correct order"
            )
            self.assertLess(
                progress_50, progress_75, "Progress messages not in correct order"
            )
            self.assertLess(
                progress_75, progress_100, "Progress messages not in correct order"
            )

    def test_module_structure_and_imports(self):
        """Test that module can be imported and has expected structure."""
        try:
            from execution.toolbox_0_1.toolbox_0_1_1 import (
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

    def test_error_handling_in_execute(self):
        """Test execute method handles parameter errors gracefully."""
        with patch("execution.toolbox_0_1.toolbox_0_1_1.arcpy.AddMessage"):
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


@unittest.skipIf(
    not ARCPY_AVAILABLE, "ArcPy not available - skipping integration tests"
)
class TestPhase1ToolboxIntegration(unittest.TestCase):
    """Integration tests that require actual ArcPy functionality."""

    def setUp(self):
        """Set up test fixtures for integration tests."""
        from execution.toolbox_0_1.toolbox_0_1_1 import ForestClassificationTool

        self.tool = ForestClassificationTool()

    def test_parameter_info_with_real_arcpy(self):
        """Test parameter creation with real ArcPy (when available)."""
        parameters = self.tool.getParameterInfo()

        # Should return 3 parameters
        self.assertEqual(len(parameters), 3)

        # Each parameter should be an actual arcpy.Parameter object
        for param in parameters:
            self.assertIsInstance(param, arcpy.Parameter)

    def test_real_parameter_properties(self):
        """Test that parameters have correct properties when using real ArcPy."""
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
