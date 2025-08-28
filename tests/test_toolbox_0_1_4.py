# -*- coding: utf-8 -*-
"""
Test module for toolbox_0_1_4.py - Phase 1 ArcGIS Pro toolbox implementation

Tests the .py version for .tbx script tool implementation to verify dropdown parameters work correctly.

Created: 2025-01-21
Version: 0.1.4
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the single_file_python_script source directory to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, "..", "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


class TestToolbox0_1_4(unittest.TestCase):
    """Test the toolbox_0_1_4.py implementation."""

    def setUp(self):
        """Set up test environment."""
        # Import the toolbox module
        # Note: We can't directly import .py files, so we'll need to use exec or similar
        self.toolbox_path = os.path.join(src_dir, "toolbox_0_1_4.py")

        # Read and execute the .pyt file content
        with open(self.toolbox_path, "r", encoding="utf-8") as f:
            self.toolbox_code = f.read()

        # Create a namespace to execute the code in
        self.toolbox_namespace = {}

        # Mock arcpy module
        self.mock_arcpy = Mock()
        self.mock_arcpy.Parameter = Mock()
        self.mock_arcpy.AddMessage = Mock()
        self.toolbox_namespace["arcpy"] = self.mock_arcpy

        # Mock other required modules
        self.toolbox_namespace["os"] = os
        self.toolbox_namespace["psutil"] = Mock()
        self.toolbox_namespace["psutil"].virtual_memory.return_value = Mock(
            total=17179869184,  # 16 GB in bytes
            available=8589934592,  # 8 GB in bytes
        )

        # Execute the toolbox code
        exec(self.toolbox_code, self.toolbox_namespace)

    def test_toolbox_structure(self):
        """Test that the toolbox structure is correct."""
        # Verify Toolbox class exists
        self.assertIn("Toolbox", self.toolbox_namespace)

        # Create toolbox instance
        toolbox = self.toolbox_namespace["Toolbox"]()

        # Verify toolbox properties
        self.assertEqual(
            toolbox.label, "Forest Classification Toolbox - Phase 1 v0.1.4"
        )
        self.assertEqual(toolbox.alias, "ForestClassificationPhase1v0_1_4")
        self.assertIn("Forest species classification tool", toolbox.description)
        self.assertEqual(len(toolbox.tools), 1)

    def test_tool_structure(self):
        """Test that the tool structure is correct."""
        # Verify ForestClassificationTool class exists
        self.assertIn("ForestClassificationTool", self.toolbox_namespace)

        # Create tool instance
        tool = self.toolbox_namespace["ForestClassificationTool"]()

        # Verify tool properties
        self.assertEqual(tool.label, "Forest Classification Tool - Phase 1 v0.1.4")
        self.assertIn("Classifies forest features", tool.description)
        self.assertEqual(tool.canRunInBackground, False)
        self.assertEqual(tool.category, "Forest Analysis")

    @patch("os.cpu_count")
    def test_system_capability_detection(self, mock_cpu_count):
        """Test system capability detection functions."""
        mock_cpu_count.return_value = 8

        # Test CPU capability detection
        get_system_capabilities = self.toolbox_namespace["get_system_capabilities"]
        cpu_cores, total_memory_gb, available_memory_gb = get_system_capabilities()

        self.assertEqual(cpu_cores, 8)
        self.assertIsInstance(total_memory_gb, float)
        self.assertIsInstance(available_memory_gb, float)

    def test_dynamic_thread_options(self):
        """Test dynamic thread option creation."""
        create_dynamic_thread_options = self.toolbox_namespace[
            "create_dynamic_thread_options"
        ]

        # Test with 8 CPU cores
        options = create_dynamic_thread_options(8)

        self.assertEqual(len(options), 3)
        self.assertIn("Conservative", options[0])
        self.assertIn("Balanced", options[1])
        self.assertIn("Performance", options[2])

        # Verify thread counts make sense
        self.assertIn("2 threads", options[0])  # 8 // 4 = 2
        self.assertIn("4 threads", options[1])  # 8 // 2 = 4
        self.assertIn("6 threads", options[2])  # int(8 * 0.75) = 6

    def test_dynamic_memory_options(self):
        """Test dynamic memory option creation."""
        create_dynamic_memory_options = self.toolbox_namespace[
            "create_dynamic_memory_options"
        ]

        # Test with 8 GB available memory
        options = create_dynamic_memory_options(8.0)

        self.assertEqual(len(options), 3)
        self.assertIn("Conservative", options[0])
        self.assertIn("Balanced", options[1])
        self.assertIn("Performance", options[2])

        # Verify memory allocations make sense
        self.assertIn("2 GB", options[0])  # max(2, int(8 * 0.25)) = 2
        self.assertIn("4 GB", options[1])  # max(4, int(8 * 0.5)) = 4
        self.assertIn("6 GB", options[2])  # max(6, int(8 * 0.75)) = 6

    def test_parameter_creation(self):
        """Test parameter creation and filter setup."""
        # Create tool instance
        tool = self.toolbox_namespace["ForestClassificationTool"]()

        # Mock Parameter instances with filter attribute
        mock_param1 = Mock()
        mock_param1.filter = Mock()
        mock_param1.filter.list = None

        mock_param2 = Mock()
        mock_param2.filter = Mock()
        mock_param2.filter.list = None

        mock_param3 = Mock()
        mock_param3.filter = Mock()
        mock_param3.filter.list = None

        # Configure arcpy.Parameter to return our mock parameters
        self.mock_arcpy.Parameter.side_effect = [mock_param1, mock_param2, mock_param3]

        # Call getParameterInfo
        params = tool.getParameterInfo()

        # Verify parameters were created
        self.assertEqual(len(params), 3)
        self.assertEqual(self.mock_arcpy.Parameter.call_count, 3)

        # Verify the first parameter (output layer)
        first_call = self.mock_arcpy.Parameter.call_args_list[0]
        self.assertEqual(first_call[1]["displayName"], "Output Feature Layer")
        self.assertEqual(first_call[1]["datatype"], "GPFeatureLayer")

        # Verify the second parameter (thread config)
        second_call = self.mock_arcpy.Parameter.call_args_list[1]
        self.assertEqual(second_call[1]["displayName"], "Thread Count")
        self.assertEqual(second_call[1]["datatype"], "GPString")

        # Verify the third parameter (memory config)
        third_call = self.mock_arcpy.Parameter.call_args_list[2]
        self.assertEqual(third_call[1]["displayName"], "Memory Allocation")
        self.assertEqual(third_call[1]["datatype"], "GPString")

    def test_filter_assignment(self):
        """Test that filter lists are assigned correctly."""
        # Create tool instance
        tool = self.toolbox_namespace["ForestClassificationTool"]()

        # Mock Parameter instances with filter attribute
        mock_output_param = Mock()
        mock_output_param.filter = None  # No filter for output layer

        mock_thread_param = Mock()
        mock_thread_param.filter = Mock()
        mock_thread_param.filter.list = None

        mock_memory_param = Mock()
        mock_memory_param.filter = Mock()
        mock_memory_param.filter.list = None

        # Configure arcpy.Parameter to return our mock parameters
        self.mock_arcpy.Parameter.side_effect = [
            mock_output_param,
            mock_thread_param,
            mock_memory_param,
        ]

        # Call getParameterInfo
        params = tool.getParameterInfo()

        # Verify filter lists were assigned
        # Thread config should have filter list assigned
        self.assertIsNotNone(mock_thread_param.filter.list)
        self.assertEqual(len(mock_thread_param.filter.list), 3)

        # Memory config should have filter list assigned
        self.assertIsNotNone(mock_memory_param.filter.list)
        self.assertEqual(len(mock_memory_param.filter.list), 3)

        # Verify default values were set
        self.assertEqual(mock_thread_param.value, mock_thread_param.filter.list[1])
        self.assertEqual(mock_memory_param.value, mock_memory_param.filter.list[1])

    def test_tool_execution(self):
        """Test tool execution method."""
        # Create tool instance
        tool = self.toolbox_namespace["ForestClassificationTool"]()

        # Mock parameters
        mock_params = [
            Mock(valueAsText="test_layer"),
            Mock(valueAsText="Balanced (4 threads)"),
            Mock(valueAsText="Balanced (4 GB)"),
        ]

        # Call execute method
        result = tool.execute(mock_params, Mock())

        # Verify execution completed without error
        self.assertIsNone(result)  # execute method returns None

        # Verify AddMessage was called
        self.assertTrue(self.mock_arcpy.AddMessage.called)

        # Verify system information was logged
        add_message_calls = [
            call[0][0] for call in self.mock_arcpy.AddMessage.call_args_list
        ]
        system_messages = [msg for msg in add_message_calls if "System:" in msg]
        self.assertTrue(len(system_messages) > 0)


if __name__ == "__main__":
    unittest.main()
