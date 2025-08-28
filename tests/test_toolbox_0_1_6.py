"""
Test suite for Forest Classification Tool Phase 1 v0.1.6

Tests basic toolbox structure for ArcGIS Pro .atbx Script tools.
Created: 2025-08-28 15:00
Version: 0.1.6
"""

import unittest
import sys
from pathlib import Path

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import the toolbox classes
from toolbox_0_1_6 import ForestClassificationToolbox, ForestClassificationTool


class TestForestClassificationToolboxPhase1v0_1_6(unittest.TestCase):
    """Test case for Phase 1 v0.1.6 toolbox structure (.atbx Script tool)."""

    def setUp(self):
        """Set up test fixtures."""
        self.toolbox = ForestClassificationToolbox()
        self.tool = ForestClassificationTool()

    def test_toolbox_initialization(self):
        """Test that toolbox initializes correctly."""
        self.assertEqual(
            self.toolbox.label, "Forest Classification Toolbox - Phase 1 v0.1.6"
        )
        self.assertEqual(self.toolbox.alias, "ForestClassificationPhase1v0_1_6")
        self.assertIn(".atbx Script tools", self.toolbox.description)
        self.assertEqual(len(self.toolbox.tools), 1)
        self.assertEqual(self.toolbox.tools[0], ForestClassificationTool)

    def test_tool_initialization(self):
        """Test that tool initializes correctly."""
        self.assertEqual(self.tool.label, "Forest Classification Tool - Phase 1 v0.1.6")
        self.assertIn("Classifies forest features", self.tool.description)
        self.assertIn("ToolValidator", self.tool.description)
        self.assertEqual(self.tool.canRunInBackground, False)
        self.assertEqual(self.tool.category, "Forest Analysis")

    def test_tool_licensing(self):
        """Test that tool licensing works."""
        self.assertTrue(self.tool.isLicensed())

    def test_parameter_info_structure_atbx(self):
        """Test parameter information structure for .atbx Script tool."""
        params = self.tool.getParameterInfo()

        # Should have exactly 3 parameters
        self.assertEqual(len(params), 3)

        # Check output layer parameter (index 0) - multi-type for .atbx
        output_param = params[0]
        self.assertEqual(output_param.displayName, "Output Feature Layer")
        self.assertEqual(output_param.name, "output_layer")
        self.assertEqual(
            output_param.datatype, "Feature Layer; Feature Class"
        )  # Multi-type
        self.assertEqual(output_param.parameterType, "Required")
        self.assertEqual(output_param.direction, "Input")
        self.assertEqual(output_param.category, "Input Data")

        # Check thread config parameter (index 1) - simple string for .atbx
        thread_param = params[1]
        self.assertEqual(thread_param.displayName, "Thread Count")
        self.assertEqual(thread_param.name, "thread_config")
        self.assertEqual(thread_param.datatype, "String")  # Simple string
        self.assertEqual(thread_param.parameterType, "Required")
        self.assertEqual(thread_param.direction, "Input")
        self.assertEqual(thread_param.category, "Performance Settings")

        # Check memory config parameter (index 2) - simple string for .atbx
        memory_param = params[2]
        self.assertEqual(memory_param.displayName, "Memory Allocation")
        self.assertEqual(memory_param.name, "memory_config")
        self.assertEqual(memory_param.datatype, "String")  # Simple string
        self.assertEqual(memory_param.parameterType, "Required")
        self.assertEqual(memory_param.direction, "Input")
        self.assertEqual(memory_param.category, "Performance Settings")

    def test_no_filter_logic_in_py(self):
        """Test that .py file doesn't contain dropdown filter logic (handled by .atbx ToolValidator)."""
        params = self.tool.getParameterInfo()

        # For .atbx Script tools, the .py should NOT set filter.list
        # Dropdowns are handled by the ToolValidator in .atbx Properties → Validation
        for param in params:
            # Parameters should be simple - no filter setup in .py
            if hasattr(param, "filter") and param.filter:
                # If filter exists, it should be empty (no list set in .py)
                if hasattr(param.filter, "list"):
                    # For .atbx Script tools, filter.list should NOT be set in .py
                    self.assertIsNone(
                        param.filter.list,
                        f"Parameter {param.name} should not have filter.list set in .py for .atbx Script tools",
                    )

    def test_update_parameters_method(self):
        """Test updateParameters method doesn't crash."""
        params = self.tool.getParameterInfo()
        try:
            # This should not raise an exception
            self.tool.updateParameters(params)
        except Exception as e:
            self.fail(f"updateParameters raised an exception: {e}")

    def test_update_messages_method(self):
        """Test updateMessages method doesn't crash."""
        params = self.tool.getParameterInfo()
        try:
            # This should not raise an exception
            self.tool.updateMessages(params)
        except Exception as e:
            self.fail(f"updateMessages raised an exception: {e}")

    def test_execute_method_structure(self):
        """Test that execute method exists and has proper signature."""
        # Check that execute method exists
        self.assertTrue(hasattr(self.tool, "execute"))
        self.assertTrue(callable(getattr(self.tool, "execute")))

    def test_post_execute_method(self):
        """Test that postExecute method exists and has proper signature."""
        # Check that postExecute method exists
        self.assertTrue(hasattr(self.tool, "postExecute"))
        self.assertTrue(callable(getattr(self.tool, "postExecute")))

    def test_toolvalidator_code_included(self):
        """Test that ToolValidator code is included as documentation."""
        # Read the source file to check if ToolValidator code is included
        import inspect

        source = inspect.getsource(ForestClassificationTool)
        self.assertIn("ToolValidator", source)
        self.assertIn("initializeParameters", source)
        self.assertIn("updateParameters", source)


if __name__ == "__main__":
    unittest.main()
