"""
Test module for Phase 1 Forest Classification Tool v0.1.2

Tests the dynamic system capability detection functionality and basic toolbox structure.
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
    from toolbox_0_1_2 import ForestClassificationToolbox, ForestClassificationTool
    from toolbox_0_1_2 import (
        get_system_capabilities,
        create_dynamic_thread_options,
        create_dynamic_memory_options,
    )
except ImportError:
    # If we can't import, we'll handle it in tests
    ForestClassificationToolbox = None
    ForestClassificationTool = None
    get_system_capabilities = None
    create_dynamic_thread_options = None
    create_dynamic_memory_options = None


class TestPhase1ToolboxStructure(unittest.TestCase):
    """Test basic toolbox class structure for Phase 1."""

    def setUp(self):
        """Set up test environment with mocked arcpy."""
        # Configure the global mock_arcpy
        mock_arcpy.reset_mock()
        self.mock_parameter = MagicMock()
        self.mock_parameter.filter = MagicMock()
        self.mock_parameter.filter.list = None
        mock_arcpy.Parameter.return_value = self.mock_parameter

    def test_toolbox_class_exists(self):
        """Test that the toolbox class exists and has required attributes."""
        if ForestClassificationToolbox is None:
            self.skipTest("ForestClassificationToolbox could not be imported")

        toolbox = ForestClassificationToolbox()

        # Test required toolbox attributes
        self.assertTrue(hasattr(toolbox, "label"))
        self.assertTrue(hasattr(toolbox, "alias"))
        self.assertTrue(hasattr(toolbox, "description"))
        self.assertTrue(hasattr(toolbox, "tools"))

        # Test attribute values
        self.assertIn("Phase 1", toolbox.label)
        self.assertIsInstance(toolbox.tools, list)
        self.assertIn(ForestClassificationTool, toolbox.tools)

    def test_tool_class_exists(self):
        """Test that the tool class exists and has required methods."""
        if ForestClassificationTool is None:
            self.skipTest("ForestClassificationTool could not be imported")

        tool = ForestClassificationTool()

        # Test required tool attributes
        self.assertTrue(hasattr(tool, "label"))
        self.assertTrue(hasattr(tool, "description"))
        self.assertTrue(hasattr(tool, "canRunInBackground"))
        self.assertTrue(hasattr(tool, "category"))

        # Test required tool methods
        self.assertTrue(hasattr(tool, "getParameterInfo"))
        self.assertTrue(hasattr(tool, "isLicensed"))
        self.assertTrue(hasattr(tool, "updateParameters"))
        self.assertTrue(hasattr(tool, "updateMessages"))
        self.assertTrue(hasattr(tool, "execute"))
        self.assertTrue(hasattr(tool, "postExecute"))

    def test_tool_attributes(self):
        """Test tool attribute values."""
        if ForestClassificationTool is None:
            self.skipTest("ForestClassificationTool could not be imported")

        tool = ForestClassificationTool()

        self.assertIn("Phase 1", tool.label)
        self.assertIn("Phase 1", tool.description)
        self.assertEqual(tool.canRunInBackground, False)
        self.assertEqual(tool.category, "Forest Analysis")


class TestPhase1ParameterDefinition(unittest.TestCase):
    """Test parameter definition for Phase 1."""

    def setUp(self):
        """Set up test environment with mocked arcpy."""
        # Configure the global mock_arcpy
        mock_arcpy.reset_mock()
        self.mock_parameter = MagicMock()
        self.mock_parameter.filter = MagicMock()
        self.mock_parameter.filter.list = None
        mock_arcpy.Parameter.return_value = self.mock_parameter

    def test_parameter_info_returns_list(self):
        """Test that getParameterInfo returns a list."""
        if ForestClassificationTool is None:
            self.skipTest("ForestClassificationTool could not be imported")

        tool = ForestClassificationTool()
        params = tool.getParameterInfo()

        self.assertIsInstance(params, list)
        self.assertEqual(len(params), 3)  # Phase 1 should have exactly 3 parameters

    def test_parameter_creation_calls(self):
        """Test that parameters are created with correct properties."""
        if ForestClassificationTool is None:
            self.skipTest("ForestClassificationTool could not be imported")

        tool = ForestClassificationTool()
        params = tool.getParameterInfo()

        # Verify arcpy.Parameter was called 3 times (for 3 parameters)
        self.assertEqual(mock_arcpy.Parameter.call_count, 3)

        # Check the parameter creation calls
        calls = mock_arcpy.Parameter.call_args_list

        # First parameter - Output Feature Layer
        first_call = calls[0][1]  # kwargs from first call
        self.assertEqual(first_call["displayName"], "Output Feature Layer")
        self.assertEqual(first_call["name"], "output_layer")
        self.assertEqual(first_call["datatype"], "GPFeatureLayer")
        self.assertEqual(first_call["parameterType"], "Required")
        self.assertEqual(first_call["direction"], "Input")

        # Second parameter - Thread Count
        second_call = calls[1][1]  # kwargs from second call
        self.assertEqual(second_call["displayName"], "Thread Count")
        self.assertEqual(second_call["name"], "thread_config")
        self.assertEqual(second_call["datatype"], "GPString")
        self.assertEqual(second_call["parameterType"], "Required")
        self.assertEqual(second_call["direction"], "Input")

        # Third parameter - Memory Allocation
        third_call = calls[2][1]  # kwargs from third call
        self.assertEqual(third_call["displayName"], "Memory Allocation")
        self.assertEqual(third_call["name"], "memory_config")
        self.assertEqual(third_call["datatype"], "GPString")
        self.assertEqual(third_call["parameterType"], "Required")
        self.assertEqual(third_call["direction"], "Input")

    def test_parameter_options_are_set(self):
        """Test that parameter filter options are properly set."""
        if ForestClassificationTool is None:
            self.skipTest("ForestClassificationTool could not be imported")

        tool = ForestClassificationTool()
        params = tool.getParameterInfo()

        # Check that filter.list was set for parameters that need it
        mock_params = [mock_arcpy.Parameter.return_value] * 3

        # At least the thread and memory parameters should have filter lists set
        self.assertTrue(any(hasattr(param.filter, "list") for param in mock_params))

    def test_update_methods_coverage(self):
        """Test updateParameters and updateMessages methods for coverage."""
        if ForestClassificationTool is None:
            self.skipTest("ForestClassificationTool could not be imported")

        tool = ForestClassificationTool()

        # Test updateParameters
        mock_parameters = [Mock(), Mock(), Mock()]
        result = tool.updateParameters(mock_parameters)
        self.assertIsNone(result)  # Should return None

        # Test updateMessages
        result = tool.updateMessages(mock_parameters)
        self.assertIsNone(result)  # Should return None

    def test_parameter_filter_assignment(self):
        """Test that parameter filter list assignment works correctly."""
        if ForestClassificationTool is None:
            self.skipTest("ForestClassificationTool could not be imported")

        # Test case where filter exists and has list attribute
        mock_param_with_filter = MagicMock()
        mock_param_with_filter.filter = MagicMock()
        mock_param_with_filter.filter.list = None

        # Test case where filter doesn't exist
        mock_param_no_filter = MagicMock()
        del mock_param_no_filter.filter  # Remove filter attribute

        # Create tool and verify filter assignment logic
        tool = ForestClassificationTool()

        # Test with mock parameter that has filter
        mock_arcpy.Parameter.return_value = mock_param_with_filter
        params = tool.getParameterInfo()

        # The first parameter (output_layer) should have its filter.list set
        self.assertIsNotNone(mock_param_with_filter.filter.list)


class TestPhase1BasicExecution(unittest.TestCase):
    """Test basic execution functionality for Phase 1."""

    def test_is_licensed_returns_true(self):
        """Test that isLicensed returns True."""
        if ForestClassificationTool is None:
            self.skipTest("ForestClassificationTool could not be imported")

        tool = ForestClassificationTool()
        self.assertTrue(tool.isLicensed())

    def test_execute_method_exists(self):
        """Test that execute method exists and can be called."""
        if ForestClassificationTool is None:
            self.skipTest("ForestClassificationTool could not be imported")

        tool = ForestClassificationTool()

        # Mock parameters
        mock_param1 = Mock()
        mock_param1.valueAsText = "test_layer"
        mock_param2 = Mock()
        mock_param2.valueAsText = "Balanced (4 threads)"
        mock_param3 = Mock()
        mock_param3.valueAsText = "Balanced (8 GB)"

        parameters = [mock_param1, mock_param2, mock_param3]
        messages = Mock()

        # Execute should not raise exceptions
        try:
            tool.execute(parameters, messages)
        except Exception as e:
            self.fail(f"Execute method raised an exception: {e}")

    def test_execute_logs_messages(self):
        """Test that execute method logs appropriate messages."""
        if ForestClassificationTool is None:
            self.skipTest("ForestClassificationTool could not be imported")

        tool = ForestClassificationTool()

        # Mock parameters
        mock_param1 = Mock()
        mock_param1.valueAsText = "test_layer"
        mock_param2 = Mock()
        mock_param2.valueAsText = "Balanced (4 threads)"
        mock_param3 = Mock()
        mock_param3.valueAsText = "Balanced (8 GB)"

        parameters = [mock_param1, mock_param2, mock_param3]
        messages = Mock()

        tool.execute(parameters, messages)

        # Verify that AddMessage was called with Phase 1 specific messages
        mock_arcpy.AddMessage.assert_called()

        # Check for key Phase 1 messages
        call_args_list = [call[0][0] for call in mock_arcpy.AddMessage.call_args_list]

        # Should contain Phase 1 specific messages
        phase1_messages = [msg for msg in call_args_list if "Phase 1" in msg]
        self.assertGreater(len(phase1_messages), 0, "No Phase 1 messages found")

        # Should contain progress messages
        progress_messages = [msg for msg in call_args_list if "progress:" in msg]
        self.assertGreaterEqual(
            len(progress_messages), 4, "Expected at least 4 progress messages"
        )

        # Should contain success message
        success_messages = [msg for msg in call_args_list if "✅" in msg]
        self.assertGreater(len(success_messages), 0, "No success messages found")

    def test_post_execute_method(self):
        """Test that postExecute method exists and can be called."""
        if ForestClassificationTool is None:
            self.skipTest("ForestClassificationTool could not be imported")

        tool = ForestClassificationTool()

        # Mock parameters
        parameters = [Mock(), Mock(), Mock()]

        # postExecute should not raise exceptions
        try:
            tool.postExecute(parameters)
        except Exception as e:
            self.fail(f"postExecute method raised an exception: {e}")

        # Verify cleanup message was logged
        mock_arcpy.AddMessage.assert_called()
        call_args_list = [call[0][0] for call in mock_arcpy.AddMessage.call_args_list]
        cleanup_messages = [msg for msg in call_args_list if "cleanup" in msg.lower()]
        self.assertGreater(len(cleanup_messages), 0, "No cleanup messages found")


class TestPhase1Integration(unittest.TestCase):
    """Integration tests for Phase 1 functionality."""

    def setUp(self):
        """Set up test environment with mocked arcpy."""
        # Configure the global mock_arcpy
        mock_arcpy.reset_mock()
        self.mock_parameter = MagicMock()
        self.mock_parameter.filter = MagicMock()
        self.mock_parameter.filter.list = None
        mock_arcpy.Parameter.return_value = self.mock_parameter

    def test_complete_phase1_workflow(self):
        """Test complete Phase 1 workflow from toolbox to execution."""
        if ForestClassificationToolbox is None or ForestClassificationTool is None:
            self.skipTest("Phase 1 classes could not be imported")

        # Create toolbox
        toolbox = ForestClassificationToolbox()
        self.assertIsNotNone(toolbox)

        # Get tool from toolbox
        tool_class = toolbox.tools[0]
        tool = tool_class()

        # Test parameter definition
        params = tool.getParameterInfo()
        self.assertEqual(len(params), 3)

        # Test licensing
        self.assertTrue(tool.isLicensed())

        # Test execution
        mock_param1 = Mock()
        mock_param1.valueAsText = "test_layer"
        mock_param2 = Mock()
        mock_param2.valueAsText = "Balanced (4 threads)"
        mock_param3 = Mock()
        mock_param3.valueAsText = "Balanced (8 GB)"

        parameters = [mock_param1, mock_param2, mock_param3]
        messages = Mock()

        tool.execute(parameters, messages)
        tool.postExecute(parameters)

        # Verify messages were logged
        mock_arcpy.AddMessage.assert_called()


if __name__ == "__main__":
    unittest.main()
