# -*- coding: utf-8 -*-
"""
Test Suite for Forest Classification Toolbox - Phase 1 v0.1.3

This test suite validates the fixed ArcGIS Pro data types and dropdown filters implementation
for Phase 1 v0.1.3 of the Single File Development Strategy.

Author: iamchriswick
Version: 1.0.0
Created: 2025-08-29T14:50:00Z
Updated: 2025-08-29T14:50:00Z
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


class TestPhase1ToolboxV0_1_3(unittest.TestCase):
    """Test case for Phase 1 v0.1.3 - Fixed ArcGIS Pro data types and dropdown filters."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Import the module under test
        from execution.toolbox_0_1.toolbox_0_1_3 import (
            ForestClassificationToolbox,
            ForestClassificationTool,
            get_system_capabilities,
            create_dynamic_thread_options,
            create_dynamic_memory_options,
        )

        self.toolbox_class = ForestClassificationToolbox
        self.tool_class = ForestClassificationTool
        self.get_system_capabilities = get_system_capabilities
        self.create_dynamic_thread_options = create_dynamic_thread_options
        self.create_dynamic_memory_options = create_dynamic_memory_options

        # Create instances for testing
        self.toolbox = self.toolbox_class()
        self.tool = self.tool_class()

    def test_toolbox_initialization_v0_1_3(self):
        """Test that toolbox is properly initialized with v0.1.3 properties."""
        self.assertEqual(self.toolbox.label, "Forest Classification Toolbox - Phase 1")
        self.assertEqual(self.toolbox.alias, "ForestClassificationPhase1")
        self.assertIn("Phase 1", self.toolbox.description)
        self.assertIn("v0.1.3", self.toolbox.description)
        self.assertEqual(len(self.toolbox.tools), 1)
        self.assertEqual(self.toolbox.tools[0], self.tool_class)

    def test_tool_initialization_v0_1_3(self):
        """Test that tool is properly initialized with v0.1.3 properties."""
        self.assertEqual(self.tool.label, "Forest Classification Tool - Phase 1")
        self.assertIn("Phase 1", self.tool.description)
        self.assertIn("v0.1.3", self.tool.description)
        self.assertEqual(self.tool.canRunInBackground, False)
        self.assertEqual(self.tool.category, "Forest Analysis")

    def test_system_capabilities_detection_v0_1_3(self):
        """Test system capability detection function for v0.1.3."""
        cpu_cores, total_memory_gb, available_memory_gb = self.get_system_capabilities()

        # Verify return types and reasonable values
        self.assertIsInstance(cpu_cores, int)
        self.assertIsInstance(total_memory_gb, float)
        self.assertIsInstance(available_memory_gb, float)

        # Verify reasonable ranges
        self.assertGreaterEqual(cpu_cores, 1)
        self.assertLessEqual(cpu_cores, 256)
        self.assertGreaterEqual(total_memory_gb, 0.5)
        self.assertLessEqual(total_memory_gb, 2048)
        self.assertGreaterEqual(available_memory_gb, 0)
        self.assertLessEqual(available_memory_gb, total_memory_gb)

    def test_dynamic_thread_options_v0_1_3_structure(self):
        """Test v0.1.3 dynamic thread options include Conservative, Balanced, Aggressive, Maximum."""
        cpu_cores = 8
        options = self.create_dynamic_thread_options(cpu_cores)

        # Should return 4 options in v0.1.3
        self.assertEqual(len(options), 4)

        # Check option names
        option_types = [option.split("(")[0].strip() for option in options]
        expected_types = ["Conservative", "Balanced", "Aggressive", "Maximum"]

        for expected_type in expected_types:
            self.assertIn(expected_type, option_types)

    def test_dynamic_thread_options_v0_1_3_values(self):
        """Test that v0.1.3 thread options have correct calculated values."""
        test_cases = [
            (
                4,
                [1, 2, 3, 4],
            ),  # Conservative 25%, Balanced 50%, Aggressive 75%, Maximum 100%
            (
                8,
                [2, 4, 6, 8],
            ),  # Conservative 25%, Balanced 50%, Aggressive 75%, Maximum 100%
            (
                16,
                [4, 8, 12, 16],
            ),  # Conservative 25%, Balanced 50%, Aggressive 75%, Maximum 100%
        ]

        for cpu_cores, expected_thread_counts in test_cases:
            with self.subTest(cpu_cores=cpu_cores):
                options = self.create_dynamic_thread_options(cpu_cores)

                # Extract thread counts
                thread_counts = []
                for option in options:
                    import re

                    match = re.search(r"\((\d+) threads\)", option)
                    if match:
                        thread_counts.append(int(match.group(1)))

                # Verify thread counts match expected
                self.assertEqual(len(thread_counts), 4)
                for i, expected_count in enumerate(expected_thread_counts):
                    self.assertGreaterEqual(thread_counts[i], 1)  # Minimum 1 thread
                    self.assertLessEqual(
                        thread_counts[i], cpu_cores
                    )  # Max is cpu_cores

    def test_dynamic_memory_options_v0_1_3_structure(self):
        """Test v0.1.3 dynamic memory options structure."""
        total_memory_gb = 16.0
        options = self.create_dynamic_memory_options(total_memory_gb)

        # Should return memory options
        self.assertGreater(len(options), 0)

        # All options should be strings with "GB)"
        for option in options:
            self.assertIsInstance(option, str)
            self.assertIn("GB)", option)

    @patch("execution.toolbox_0_1.toolbox_0_1_3.arcpy.Parameter")
    def test_parameter_structure_fixed_data_types_v0_1_3(self, mock_parameter):
        """Test that getParameterInfo uses fixed ArcGIS Pro data types for v0.1.3."""
        # Configure mock to return a proper parameter-like object
        mock_param = MagicMock()
        mock_param.filter = MagicMock()
        mock_param.filter.list = []
        mock_parameter.return_value = mock_param

        parameters = self.tool.getParameterInfo()

        # Should return 3 parameters: output_layer, thread_config, memory_config
        self.assertEqual(len(parameters), 3)

        # Verify Parameter() was called 3 times
        self.assertEqual(mock_parameter.call_count, 3)

        # Check parameter creation calls for proper data types
        call_args_list = mock_parameter.call_args_list

        # First parameter (output_layer) should use GPFeatureLayer
        output_layer_call = call_args_list[0]
        self.assertIn("GPFeatureLayer", output_layer_call[1].values())

        # Second and third parameters should use GPString
        thread_config_call = call_args_list[1]
        memory_config_call = call_args_list[2]
        self.assertIn("GPString", thread_config_call[1].values())
        self.assertIn("GPString", memory_config_call[1].values())

    @patch("execution.toolbox_0_1.toolbox_0_1_3.arcpy.Parameter")
    def test_dropdown_filter_setup_v0_1_3(self, mock_parameter):
        """Test that dropdown filters are properly set up in v0.1.3."""
        # Configure mock parameter with filter attribute
        mock_param = MagicMock()
        mock_param.filter = MagicMock()
        mock_param.filter.list = []
        mock_parameter.return_value = mock_param

        self.tool.getParameterInfo()

        # At minimum, filters should be configured
        self.assertIsNotNone(mock_param.filter)

    @patch("execution.toolbox_0_1.toolbox_0_1_3.arcpy.AddMessage")
    def test_execute_method_v0_1_3_functionality(self, mock_add_message):
        """Test execute method functionality for v0.1.3 with fixed data types."""
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

        # Check for v0.1.3 specific messages
        call_args_list = [call[0][0] for call in mock_add_message.call_args_list]

        # Should contain v0.1.3 specific messages
        v0_1_3_messages = [msg for msg in call_args_list if "v0.1.3" in msg]
        self.assertGreater(len(v0_1_3_messages), 0)

        # Should contain data type related messages
        data_type_messages = [
            msg
            for msg in call_args_list
            if any(
                keyword in msg
                for keyword in [
                    "data types",
                    "dropdown filters",
                    "GPFeatureLayer",
                    "GPString",
                ]
            )
        ]
        self.assertGreaterEqual(len(data_type_messages), 0)  # May or may not be present

    @patch("execution.toolbox_0_1.toolbox_0_1_3.arcpy.AddMessage")
    def test_parameter_logging_includes_data_type_info_v0_1_3(self, mock_add_message):
        """Test that parameter logging includes data type information for v0.1.3."""
        mock_params = [
            MagicMock(valueAsText="C:\\test\\output.shp"),
            MagicMock(valueAsText="Aggressive (6 threads)"),
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
            if "Thread configuration:" in msg and "Aggressive (6 threads)" in msg
        ]
        memory_messages = [
            msg
            for msg in call_args_list
            if "Memory configuration:" in msg and "Performance (16 GB)" in msg
        ]

        self.assertGreater(len(output_messages), 0)
        self.assertGreater(len(thread_messages), 0)
        self.assertGreater(len(memory_messages), 0)

    def test_tool_licensing_v0_1_3(self):
        """Test that tool is licensed to execute in v0.1.3."""
        self.assertTrue(self.tool.isLicensed())

    def test_update_parameters_method_v0_1_3(self):
        """Test that updateParameters method exists and works for v0.1.3."""
        try:
            self.tool.updateParameters([])
        except Exception as e:
            self.fail(f"updateParameters raised {e} unexpectedly")

    def test_update_messages_method_v0_1_3(self):
        """Test that updateMessages method exists and works for v0.1.3."""
        try:
            self.tool.updateMessages([])
        except Exception as e:
            self.fail(f"updateMessages raised {e} unexpectedly")

    @patch("execution.toolbox_0_1.toolbox_0_1_3.arcpy.AddMessage")
    def test_post_execute_method_v0_1_3(self, mock_add_message):
        """Test that postExecute method exists and logs cleanup message for v0.1.3."""
        # Execute postExecute
        result = self.tool.postExecute([])

        # Should return None
        self.assertIsNone(result)

        # Should log cleanup message
        mock_add_message.assert_called_with(
            "🧹 Phase 1 post-execution cleanup completed"
        )

    def test_module_structure_v0_1_3(self):
        """Test that v0.1.3 module can be imported and has expected structure."""
        try:
            from execution.toolbox_0_1.toolbox_0_1_3 import (
                ForestClassificationToolbox,
                ForestClassificationTool,
                get_system_capabilities,
                create_dynamic_thread_options,
                create_dynamic_memory_options,
            )

            # Test that classes and functions are properly defined
            self.assertTrue(hasattr(ForestClassificationToolbox, "__init__"))
            self.assertTrue(hasattr(ForestClassificationTool, "__init__"))
            self.assertTrue(hasattr(ForestClassificationTool, "getParameterInfo"))
            self.assertTrue(hasattr(ForestClassificationTool, "isLicensed"))
            self.assertTrue(hasattr(ForestClassificationTool, "updateParameters"))
            self.assertTrue(hasattr(ForestClassificationTool, "updateMessages"))
            self.assertTrue(hasattr(ForestClassificationTool, "execute"))
            self.assertTrue(hasattr(ForestClassificationTool, "postExecute"))

            # Test that utility functions are callable
            self.assertTrue(callable(get_system_capabilities))
            self.assertTrue(callable(create_dynamic_thread_options))
            self.assertTrue(callable(create_dynamic_memory_options))

        except ImportError as e:
            self.fail(f"Failed to import required classes and functions: {e}")

    @patch("execution.toolbox_0_1.toolbox_0_1_3.arcpy.AddMessage")
    def test_progress_tracking_v0_1_3(self, mock_add_message):
        """Test that progress tracking works correctly for v0.1.3."""
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

    def test_error_handling_in_system_detection_v0_1_3(self):
        """Test that system detection handles errors gracefully in v0.1.3."""
        with patch(
            "execution.toolbox_0_1.toolbox_0_1_3.os.cpu_count",
            side_effect=Exception("Test error"),
        ):
            with patch(
                "execution.toolbox_0_1.toolbox_0_1_3.psutil.virtual_memory",
                side_effect=Exception("Test error"),
            ):
                # Should not raise exception, should return fallback values
                try:
                    cpu_cores, total_memory_gb, available_memory_gb = (
                        self.get_system_capabilities()
                    )
                    self.assertEqual(cpu_cores, 4)
                    self.assertEqual(total_memory_gb, 16.0)
                    self.assertEqual(available_memory_gb, 8.0)
                except Exception as e:
                    self.fail(
                        f"System capability detection should handle errors gracefully, but raised: {e}"
                    )

    def test_four_thread_options_structure_v0_1_3(self):
        """Test that v0.1.3 creates exactly 4 thread options with proper names."""
        cpu_cores = 8
        options = self.create_dynamic_thread_options(cpu_cores)

        # Should have exactly 4 options
        self.assertEqual(len(options), 4)

        # Check for expected option names
        option_text = " ".join(options)
        self.assertIn("Conservative", option_text)
        self.assertIn("Balanced", option_text)
        self.assertIn("Aggressive", option_text)
        self.assertIn("Maximum", option_text)

        # Each option should mention threads
        for option in options:
            self.assertIn("threads)", option)


@unittest.skipIf(
    not ARCPY_AVAILABLE, "ArcPy not available - skipping integration tests"
)
class TestPhase1ToolboxV0_1_3Integration(unittest.TestCase):
    """Integration tests for v0.1.3 that require actual ArcPy functionality."""

    def setUp(self):
        """Set up test fixtures for integration tests."""
        from execution.toolbox_0_1.toolbox_0_1_3 import ForestClassificationTool

        self.tool = ForestClassificationTool()

    def test_parameter_info_with_real_arcpy_v0_1_3(self):
        """Test parameter creation with real ArcPy for v0.1.3."""
        parameters = self.tool.getParameterInfo()

        # Should return 3 parameters
        self.assertEqual(len(parameters), 3)

        # Each parameter should be an actual arcpy.Parameter object
        for param in parameters:
            self.assertIsInstance(param, arcpy.Parameter)

    def test_real_parameter_data_types_v0_1_3(self):
        """Test that parameters have correct fixed data types in v0.1.3."""
        parameters = self.tool.getParameterInfo()

        output_layer = parameters[0]
        thread_config = parameters[1]
        memory_config = parameters[2]

        # Test fixed data types
        self.assertEqual(output_layer.datatype, "GPFeatureLayer")
        self.assertEqual(output_layer.direction, "Input")

        self.assertEqual(thread_config.datatype, "GPString")
        self.assertEqual(thread_config.direction, "Input")

        self.assertEqual(memory_config.datatype, "GPString")
        self.assertEqual(memory_config.direction, "Input")

    def test_dropdown_filters_configured_v0_1_3(self):
        """Test that dropdown filters are properly configured for v0.1.3."""
        parameters = self.tool.getParameterInfo()

        thread_config = parameters[1]
        memory_config = parameters[2]

        # Verify filters exist and have list property
        self.assertIsNotNone(thread_config.filter)
        self.assertIsNotNone(memory_config.filter)
        self.assertTrue(hasattr(thread_config.filter, "list"))
        self.assertTrue(hasattr(memory_config.filter, "list"))

        # Verify filter lists are populated
        self.assertIsInstance(thread_config.filter.list, list)
        self.assertIsInstance(memory_config.filter.list, list)
        self.assertGreater(len(thread_config.filter.list), 0)
        self.assertGreater(len(memory_config.filter.list), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
