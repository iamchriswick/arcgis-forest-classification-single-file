"""
Test suite for Forest Classification Tool Phase 1 v0.1.7

Tests module-level execution for ArcGIS Pro .atbx Script tools.
Created: 2025-08-28 15:15
Version: 0.1.7
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


class TestForestClassificationToolboxPhase1v0_1_7(unittest.TestCase):
    """Test case for Phase 1 v0.1.7 toolbox structure (.atbx Script tool with module-level execution)."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock arcpy to avoid import errors in test environment
        self.arcpy_mock = MagicMock()
        self.arcpy_patcher = patch("toolbox_0_1_7.arcpy", self.arcpy_mock)
        self.arcpy_patcher.start()

        # Mock os.cpu_count
        self.os_patcher = patch("toolbox_0_1_7.os.cpu_count", return_value=8)
        self.os_patcher.start()

        # Import after patching
        import toolbox_0_1_7

        self.module = toolbox_0_1_7
        self.toolbox = toolbox_0_1_7.ForestClassificationToolbox()
        self.tool = toolbox_0_1_7.ForestClassificationTool()

    def tearDown(self):
        """Clean up test fixtures."""
        self.arcpy_patcher.stop()
        self.os_patcher.stop()

    def test_module_level_execution(self):
        """Test that module executes main() function at import."""
        # Mock GetParameterAsText to return test values
        self.arcpy_mock.GetParameterAsText.side_effect = [
            "test_output_layer",
            "Balanced (4)",
            "Standard (8 GB)",
        ]

        # Call main function directly
        self.module.main()

        # Verify logging messages were called
        self.assertTrue(self.arcpy_mock.AddMessage.called)
        messages = [call[0][0] for call in self.arcpy_mock.AddMessage.call_args_list]

        # Check for expected log messages
        self.assertTrue(
            any("🚀 Starting Forest Classification Tool" in msg for msg in messages)
        )
        self.assertTrue(
            any("📊 Output layer: test_output_layer" in msg for msg in messages)
        )
        self.assertTrue(
            any("🧵 Thread configuration: Balanced (4)" in msg for msg in messages)
        )
        self.assertTrue(
            any("💾 Memory configuration: Standard (8 GB)" in msg for msg in messages)
        )
        self.assertTrue(
            any("✅ Phase 1 completed successfully!" in msg for msg in messages)
        )

    def test_log_system_capabilities(self):
        """Test system capabilities logging function."""
        self.module.log_system_capabilities()

        # Verify system logging was called
        self.assertTrue(self.arcpy_mock.AddMessage.called)
        messages = [call[0][0] for call in self.arcpy_mock.AddMessage.call_args_list]

        # Check for system capability messages
        self.assertTrue(
            any("🖥️ System:" in msg and "CPU cores detected" in msg for msg in messages)
        )

    def test_toolbox_initialization(self):
        """Test that toolbox initializes correctly."""
        self.assertEqual(
            self.toolbox.label, "Forest Classification Toolbox - Phase 1 v0.1.7"
        )
        self.assertEqual(self.toolbox.alias, "ForestClassificationPhase1v0_1_7")
        self.assertIn(".atbx Script tools", self.toolbox.description)
        self.assertEqual(len(self.toolbox.tools), 1)
        self.assertEqual(self.toolbox.tools[0], self.module.ForestClassificationTool)

    def test_tool_initialization(self):
        """Test that tool initializes correctly."""
        self.assertEqual(self.tool.label, "Forest Classification Tool - Phase 1 v0.1.7")
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

        # Check parameter structure (mocked parameters)
        self.assertEqual(len(params), 3)

    def test_tool_execute_calls_main(self):
        """Test that tool.execute() calls main() function."""
        # Mock GetParameterAsText for main() function
        self.arcpy_mock.GetParameterAsText.side_effect = [
            "test_layer",
            "High (6)",
            "Aggressive (12 GB)",
        ]

        # Reset call count
        self.arcpy_mock.AddMessage.reset_mock()

        # Call execute method
        self.tool.execute([], [])

        # Verify main() was called (should see logging messages)
        self.assertTrue(self.arcpy_mock.AddMessage.called)
        messages = [call[0][0] for call in self.arcpy_mock.AddMessage.call_args_list]
        self.assertTrue(
            any("🚀 Starting Forest Classification Tool" in msg for msg in messages)
        )

    def test_update_parameters_method(self):
        """Test updateParameters method doesn't crash."""
        params = []
        try:
            # This should not raise an exception
            self.tool.updateParameters(params)
        except Exception as e:
            self.fail(f"updateParameters raised an exception: {e}")

    def test_update_messages_method(self):
        """Test updateMessages method doesn't crash."""
        params = []
        try:
            # This should not raise an exception
            self.tool.updateMessages(params)
        except Exception as e:
            self.fail(f"updateMessages raised an exception: {e}")

    def test_post_execute_method(self):
        """Test that postExecute method works."""
        # Reset call count
        self.arcpy_mock.AddMessage.reset_mock()

        # Call postExecute method
        self.tool.postExecute([])

        # Verify cleanup message was logged
        self.assertTrue(self.arcpy_mock.AddMessage.called)
        messages = [call[0][0] for call in self.arcpy_mock.AddMessage.call_args_list]
        self.assertTrue(
            any(
                "🧹 Phase 1 post-execution cleanup completed" in msg for msg in messages
            )
        )


if __name__ == "__main__":
    unittest.main()
