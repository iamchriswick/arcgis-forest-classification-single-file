# -*- coding: utf-8 -*-
"""
Test Suite for Forest Classification Toolbox - Phase 1 v0.1.2

This test suite validates the dynamic system capability detection implementation
for Phase 1 v0.1.2 of the Single File Development Strategy.

Author: iamchriswick
Version: 1.0.0
Created: 2025-08-29T14:45:00Z
Updated: 2025-08-29T14:45:00Z
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


class TestPhase1ToolboxV0_1_2(unittest.TestCase):
    """Test case for Phase 1 v0.1.2 - Dynamic system capability detection."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Import the module under test
        from execution.toolbox_0_1.toolbox_0_1_2 import (
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

    def test_toolbox_initialization_v0_1_2(self):
        """Test that toolbox is properly initialized with v0.1.2 properties."""
        self.assertEqual(self.toolbox.label, "Forest Classification Toolbox - Phase 1")
        self.assertEqual(self.toolbox.alias, "ForestClassificationPhase1")
        self.assertIn("Phase 1", self.toolbox.description)
        self.assertIn("v0.1.2", self.toolbox.description)
        self.assertEqual(len(self.toolbox.tools), 1)
        self.assertEqual(self.toolbox.tools[0], self.tool_class)

    def test_tool_initialization_v0_1_2(self):
        """Test that tool is properly initialized with v0.1.2 properties."""
        self.assertEqual(self.tool.label, "Forest Classification Tool - Phase 1")
        self.assertIn("Phase 1", self.tool.description)
        self.assertIn("v0.1.2", self.tool.description)
        self.assertEqual(self.tool.canRunInBackground, False)
        self.assertEqual(self.tool.category, "Forest Analysis")

    def test_system_capabilities_detection(self):
        """Test system capability detection function."""
        cpu_cores, total_memory_gb, available_memory_gb = self.get_system_capabilities()

        # Verify return types and reasonable values
        self.assertIsInstance(cpu_cores, int)
        self.assertIsInstance(total_memory_gb, float)
        self.assertIsInstance(available_memory_gb, float)

        # Verify reasonable ranges
        self.assertGreaterEqual(cpu_cores, 1)
        self.assertLessEqual(cpu_cores, 256)  # Reasonable upper bound
        self.assertGreaterEqual(total_memory_gb, 0.5)  # At least 512MB
        self.assertLessEqual(total_memory_gb, 2048)  # Less than 2TB
        self.assertGreaterEqual(available_memory_gb, 0)
        self.assertLessEqual(available_memory_gb, total_memory_gb)

    @patch("execution.toolbox_0_1.toolbox_0_1_2.os.cpu_count")
    @patch("execution.toolbox_0_1.toolbox_0_1_2.psutil.virtual_memory")
    def test_system_capabilities_with_mocked_values(self, mock_memory, mock_cpu_count):
        """Test system capability detection with controlled mock values."""
        # Setup mock values
        mock_cpu_count.return_value = 8
        mock_memory_info = MagicMock()
        mock_memory_info.total = 16 * 1024**3  # 16GB in bytes
        mock_memory_info.available = 8 * 1024**3  # 8GB in bytes
        mock_memory.return_value = mock_memory_info

        cpu_cores, total_memory_gb, available_memory_gb = self.get_system_capabilities()

        # Verify expected values
        self.assertEqual(cpu_cores, 8)
        self.assertAlmostEqual(total_memory_gb, 16.0, places=1)
        self.assertAlmostEqual(available_memory_gb, 8.0, places=1)

    @patch("execution.toolbox_0_1.toolbox_0_1_2.os.cpu_count")
    @patch("execution.toolbox_0_1.toolbox_0_1_2.psutil.virtual_memory")
    def test_system_capabilities_fallback_values(self, mock_memory, mock_cpu_count):
        """Test system capability detection fallback when detection fails."""
        # Setup mocks to raise exceptions
        mock_cpu_count.side_effect = Exception("CPU detection failed")
        mock_memory.side_effect = Exception("Memory detection failed")

        cpu_cores, total_memory_gb, available_memory_gb = self.get_system_capabilities()

        # Verify fallback values
        self.assertEqual(cpu_cores, 4)
        self.assertEqual(total_memory_gb, 16.0)
        self.assertEqual(available_memory_gb, 8.0)

    def test_dynamic_thread_options_creation(self):
        """Test creation of dynamic thread options based on CPU cores."""
        # Test with various CPU core counts
        test_cases = [
            (4, 3),  # 4 cores should create 3 options
            (8, 3),  # 8 cores should create 3 options
            (16, 3),  # 16 cores should create 3 options
            (1, 3),  # 1 core should still create 3 options with minimums
        ]

        for cpu_cores, expected_count in test_cases:
            with self.subTest(cpu_cores=cpu_cores):
                options = self.create_dynamic_thread_options(cpu_cores)
                self.assertEqual(len(options), expected_count)

                # Verify all options are strings
                for option in options:
                    self.assertIsInstance(option, str)
                    self.assertIn("threads)", option)

    def test_dynamic_thread_options_values(self):
        """Test that dynamic thread options have reasonable values."""
        cpu_cores = 8
        options = self.create_dynamic_thread_options(cpu_cores)

        # Extract thread counts from options (assuming format like "Balanced (4 threads)")
        thread_counts = []
        for option in options:
            # Extract number between parentheses
            import re

            match = re.search(r"\((\d+) threads\)", option)
            if match:
                thread_counts.append(int(match.group(1)))

        # Verify we found thread counts
        self.assertEqual(len(thread_counts), 3)

        # Verify conservative < balanced < performance
        conservative, balanced, performance = sorted(thread_counts)
        self.assertLessEqual(conservative, balanced)
        self.assertLessEqual(balanced, performance)
        self.assertLessEqual(performance, cpu_cores)

    def test_dynamic_memory_options_creation(self):
        """Test creation of dynamic memory options based on available memory."""
        # Test with various memory amounts
        test_cases = [
            (16.0, 3),  # 16GB should create 3 options
            (8.0, 3),  # 8GB should create 3 options
            (32.0, 3),  # 32GB should create 3 options
            (4.0, 3),  # 4GB should still create 3 options
        ]

        for total_memory_gb, expected_count in test_cases:
            with self.subTest(total_memory_gb=total_memory_gb):
                options = self.create_dynamic_memory_options(total_memory_gb)
                self.assertEqual(len(options), expected_count)

                # Verify all options are strings
                for option in options:
                    self.assertIsInstance(option, str)
                    self.assertIn("GB)", option)

    @patch("execution.toolbox_0_1.toolbox_0_1_2.arcpy.Parameter")
    def test_parameter_structure_v0_1_2(self, mock_parameter):
        """Test that getParameterInfo returns correct parameter structure for v0.1.2."""
        # Configure mock to return a proper parameter-like object
        mock_param = MagicMock()
        mock_param.filter = MagicMock()
        mock_parameter.return_value = mock_param

        parameters = self.tool.getParameterInfo()

        # Should return 3 parameters: output_layer, thread_config, memory_config
        self.assertEqual(len(parameters), 3)

        # Verify Parameter() was called 3 times
        self.assertEqual(mock_parameter.call_count, 3)

    @patch("execution.toolbox_0_1.toolbox_0_1_2.arcpy.AddMessage")
    def test_execute_method_v0_1_2_functionality(self, mock_add_message):
        """Test execute method functionality for v0.1.2 with dynamic capabilities."""
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

        # Check for v0.1.2 specific messages
        call_args_list = [call[0][0] for call in mock_add_message.call_args_list]

        # Should contain v0.1.2 specific messages
        v0_1_2_messages = [msg for msg in call_args_list if "v0.1.2" in msg]
        self.assertGreater(len(v0_1_2_messages), 0)

        # Should contain dynamic capability detection messages
        capability_messages = [
            msg
            for msg in call_args_list
            if "Dynamic system capability detection" in msg
            or "detection implementation" in msg
        ]
        self.assertGreater(len(capability_messages), 0)

    @patch("execution.toolbox_0_1.toolbox_0_1_2.arcpy.AddMessage")
    def test_system_capability_logging_in_execute(self, mock_add_message):
        """Test that execute method logs system capability information."""
        mock_params = [MagicMock(valueAsText="test") for _ in range(3)]

        # Execute the method
        self.tool.execute(mock_params, None)

        # Extract all messages
        call_args_list = [call[0][0] for call in mock_add_message.call_args_list]

        # Should log system capabilities
        system_messages = [
            msg
            for msg in call_args_list
            if any(
                keyword in msg.lower()
                for keyword in ["cpu", "cores", "memory", "threads"]
            )
        ]
        self.assertGreater(len(system_messages), 0)

    def test_tool_licensing_v0_1_2(self):
        """Test that tool is licensed to execute in v0.1.2."""
        self.assertTrue(self.tool.isLicensed())

    def test_update_parameters_method_v0_1_2(self):
        """Test that updateParameters method exists and works for v0.1.2."""
        try:
            self.tool.updateParameters([])
        except Exception as e:
            self.fail(f"updateParameters raised {e} unexpectedly")

    def test_update_messages_method_v0_1_2(self):
        """Test that updateMessages method exists and works for v0.1.2."""
        try:
            self.tool.updateMessages([])
        except Exception as e:
            self.fail(f"updateMessages raised {e} unexpectedly")

    @patch("execution.toolbox_0_1.toolbox_0_1_2.arcpy.AddMessage")
    def test_post_execute_method_v0_1_2(self, mock_add_message):
        """Test that postExecute method exists and logs cleanup message for v0.1.2."""
        # Execute postExecute
        result = self.tool.postExecute([])

        # Should return None
        self.assertIsNone(result)

        # Should log cleanup message
        mock_add_message.assert_called_with(
            "🧹 Phase 1 post-execution cleanup completed"
        )

    def test_module_structure_v0_1_2(self):
        """Test that v0.1.2 module can be imported and has expected structure."""
        try:
            from execution.toolbox_0_1.toolbox_0_1_2 import (
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

    @patch("execution.toolbox_0_1.toolbox_0_1_2.arcpy.AddMessage")
    def test_progress_tracking_includes_v0_1_2_info(self, mock_add_message):
        """Test that progress tracking includes v0.1.2 specific information."""
        mock_params = [MagicMock(valueAsText="test") for _ in range(3)]

        # Execute the method
        self.tool.execute(mock_params, None)

        # Extract all messages
        call_args_list = [call[0][0] for call in mock_add_message.call_args_list]

        # Find progress messages that include version info
        versioned_progress = [
            msg
            for msg in call_args_list
            if "Phase 1 progress:" in msg
            and any(indicator in msg for indicator in ["25%", "50%", "75%", "100%"])
        ]
        self.assertGreaterEqual(
            len(versioned_progress), 4
        )  # Should have all 4 progress points

    def test_error_handling_in_system_detection(self):
        """Test that system detection handles errors gracefully."""
        with patch(
            "execution.toolbox_0_1.toolbox_0_1_2.os.cpu_count",
            side_effect=Exception("Test error"),
        ):
            with patch(
                "execution.toolbox_0_1.toolbox_0_1_2.psutil.virtual_memory",
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


@unittest.skipIf(
    not ARCPY_AVAILABLE, "ArcPy not available - skipping integration tests"
)
class TestPhase1ToolboxV0_1_2Integration(unittest.TestCase):
    """Integration tests for v0.1.2 that require actual ArcPy functionality."""

    def setUp(self):
        """Set up test fixtures for integration tests."""
        from execution.toolbox_0_1.toolbox_0_1_2 import ForestClassificationTool

        self.tool = ForestClassificationTool()

    def test_parameter_info_with_real_arcpy_v0_1_2(self):
        """Test parameter creation with real ArcPy for v0.1.2."""
        parameters = self.tool.getParameterInfo()

        # Should return 3 parameters
        self.assertEqual(len(parameters), 3)

        # Each parameter should be an actual arcpy.Parameter object
        for param in parameters:
            self.assertIsInstance(param, arcpy.Parameter)

    def test_real_parameter_properties_v0_1_2(self):
        """Test that parameters have correct properties when using real ArcPy for v0.1.2."""
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
