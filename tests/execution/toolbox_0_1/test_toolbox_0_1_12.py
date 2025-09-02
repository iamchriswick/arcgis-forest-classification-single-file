# -*- coding: utf-8 -*-
"""
Test Suite for Forest Classification Tool - Phase 1 v0.1.12

Comprehensive tests for the main toolbox execution module.
Created: 2025-08-30
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the src directory to the path for importing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))

try:
    from execution.toolbox_0_1.toolbox_0_1_12 import (
        log_system_capabilities,
        main,
        ForestClassificationToolbox,
        ForestClassificationTool,
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Available paths:")
    for path in sys.path:
        print(f"  {path}")
    raise


class TestForestClassificationToolbox(unittest.TestCase):
    """Test ForestClassificationToolbox class."""

    def test_toolbox_initialization(self):
        """Test toolbox initialization."""
        toolbox = ForestClassificationToolbox()
        
        # Verify basic properties
        self.assertEqual(toolbox.label, "Forest Classification Toolbox - Phase 1 v0.1.12")
        self.assertEqual(toolbox.alias, "ForestClassificationPhase1v0_1_12")
        self.assertIn("Forest species classification tool", toolbox.description)
        self.assertIn("Enhanced GUI", toolbox.description)
        
        # Verify tools list
        self.assertEqual(toolbox.tools, [ForestClassificationTool])

    def test_toolbox_attributes_exist(self):
        """Test that all required toolbox attributes exist."""
        toolbox = ForestClassificationToolbox()
        
        required_attrs = ["label", "alias", "description", "tools"]
        for attr in required_attrs:
            self.assertTrue(hasattr(toolbox, attr))
            self.assertIsNotNone(getattr(toolbox, attr))


class TestForestClassificationTool(unittest.TestCase):
    """Test ForestClassificationTool class."""

    def setUp(self):
        """Set up test fixtures."""
        self.tool = ForestClassificationTool()

    def test_tool_initialization(self):
        """Test tool initialization."""
        # Verify basic properties
        self.assertEqual(self.tool.label, "Forest Classification Tool - Phase 1 v0.1.12")
        self.assertIn("Classifies forest features", self.tool.description)
        self.assertIn("Enhanced GUI", self.tool.description)
        self.assertFalse(self.tool.canRunInBackground)
        self.assertEqual(self.tool.category, "Forest Analysis")

    def test_tool_attributes_exist(self):
        """Test that all required tool attributes exist."""
        required_attrs = ["label", "description", "canRunInBackground", "category"]
        for attr in required_attrs:
            self.assertTrue(hasattr(self.tool, attr))
            self.assertIsNotNone(getattr(self.tool, attr))

    def test_is_licensed(self):
        """Test tool licensing."""
        self.assertTrue(self.tool.isLicensed())

    def test_update_parameters(self):
        """Test parameter updates."""
        mock_params = [Mock(), Mock(), Mock()]
        
        # Should not raise exceptions and return None
        result = self.tool.updateParameters(mock_params)
        self.assertIsNone(result)

    def test_update_messages(self):
        """Test message updates."""
        mock_params = [Mock(), Mock(), Mock()]
        
        # Should not raise exceptions and return None
        result = self.tool.updateMessages(mock_params)
        self.assertIsNone(result)

    @patch('execution.toolbox_0_1.toolbox_0_1_12.main')
    def test_execute(self, mock_main):
        """Test tool execution."""
        mock_params = [Mock(), Mock(), Mock()]
        mock_messages = Mock()
        
        result = self.tool.execute(mock_params, mock_messages)
        
        # Should call main function
        mock_main.assert_called_once()
        
        # Should return None
        self.assertIsNone(result)

    def test_required_methods_exist(self):
        """Test that all required ArcGIS tool methods exist."""
        required_methods = [
            "getParameterInfo",
            "isLicensed", 
            "updateParameters",
            "updateMessages",
            "execute",
            "postExecute"
        ]
        
        for method_name in required_methods:
            self.assertTrue(hasattr(self.tool, method_name))
            self.assertTrue(callable(getattr(self.tool, method_name)))

    @patch('builtins.__import__')
    def test_get_parameter_info(self, mock_import):
        """Test parameter information setup."""
        # Mock arcpy module
        mock_arcpy = Mock()
        mock_param = Mock()
        mock_arcpy.Parameter.return_value = mock_param
        
        def import_side_effect(name, *args, **kwargs):
            if name == "arcpy":
                return mock_arcpy
            return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = import_side_effect
        
        params = self.tool.getParameterInfo()
        
        # Should return 3 parameters
        self.assertEqual(len(params), 3)
        
        # Verify Parameter constructor was called 3 times
        self.assertEqual(mock_arcpy.Parameter.call_count, 3)

    @patch('builtins.__import__')
    def test_post_execute(self, mock_import):
        """Test post-execution cleanup."""
        # Mock arcpy module
        mock_arcpy = Mock()
        
        def import_side_effect(name, *args, **kwargs):
            if name == "arcpy":
                return mock_arcpy
            return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = import_side_effect
        
        mock_params = [Mock(), Mock(), Mock()]
        
        result = self.tool.postExecute(mock_params)
        
        # Should log cleanup message
        mock_arcpy.AddMessage.assert_called_once_with("🧹 Phase 1 post-execution cleanup completed")
        
        # Should return None
        self.assertIsNone(result)


class TestMainFunction(unittest.TestCase):
    """Test main execution function."""

    @patch('builtins.__import__')
    def test_main_execution_complete(self, mock_import):
        """Test complete main function execution."""
        # Mock arcpy module
        mock_arcpy = Mock()
        mock_arcpy.GetParameterAsText.side_effect = [
            "test_output_layer",
            "Auto (let system decide)", 
            "8 GB (60% of 16.0 GB available)"
        ]
        
        def import_side_effect(name, *args, **kwargs):
            if name == "arcpy":
                return mock_arcpy
            return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = import_side_effect
        
        with patch('execution.toolbox_0_1.toolbox_0_1_12.log_system_capabilities') as mock_log:
            main()
            
            # Verify parameter extraction
            self.assertEqual(mock_arcpy.GetParameterAsText.call_count, 3)
            
            # Verify system capabilities logging was called
            mock_log.assert_called_once()
            
            # Verify key messages were logged
            mock_arcpy.AddMessage.assert_any_call("🚀 Starting Forest Classification Tool v0.1.12")
            mock_arcpy.AddMessage.assert_any_call("✅ Phase 1 completed successfully!")

    @patch('builtins.__import__')
    def test_main_with_empty_parameters(self, mock_import):
        """Test main function with empty parameters."""
        # Mock arcpy module
        mock_arcpy = Mock()
        mock_arcpy.GetParameterAsText.side_effect = ["", "", ""]
        
        def import_side_effect(name, *args, **kwargs):
            if name == "arcpy":
                return mock_arcpy
            return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = import_side_effect
        
        with patch('execution.toolbox_0_1.toolbox_0_1_12.log_system_capabilities'):
            main()
            
            # Verify empty parameter logging
            mock_arcpy.AddMessage.assert_any_call("📊 Output layer: ")
            mock_arcpy.AddMessage.assert_any_call("🧵 Thread configuration: ")
            mock_arcpy.AddMessage.assert_any_call("💾 Memory configuration: ")


class TestLogSystemCapabilities(unittest.TestCase):
    """Test system capabilities logging function."""

    @patch('builtins.__import__')
    def test_log_system_capabilities_basic(self, mock_import):
        """Test basic system capabilities logging."""
        # Mock arcpy module
        mock_arcpy = Mock()
        
        def import_side_effect(name, *args, **kwargs):
            if name == "arcpy":
                return mock_arcpy
            elif name == "psutil":
                raise ImportError("No psutil")
            return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = import_side_effect
        
        with patch('execution.toolbox_0_1.toolbox_0_1_12.os.cpu_count', return_value=4):
            log_system_capabilities()
            
            # Should log CPU detection
            mock_arcpy.AddMessage.assert_any_call("🖥️ System: 4 CPU cores detected")
            mock_arcpy.AddMessage.assert_any_call("🧵 System: Maximum recommended threads: 3 (90% of 4 cores)")

    @patch('builtins.__import__')
    def test_log_system_capabilities_with_psutil(self, mock_import):
        """Test system capabilities logging with psutil."""
        # Mock arcpy and psutil modules
        mock_arcpy = Mock()
        mock_psutil = Mock()
        mock_memory = Mock()
        mock_memory.available = 8 * (1024**3)  # 8 GB available
        mock_memory.total = 16 * (1024**3)  # 16 GB total
        mock_psutil.virtual_memory.return_value = mock_memory
        
        def import_side_effect(name, *args, **kwargs):
            if name == "arcpy":
                return mock_arcpy
            elif name == "psutil":
                return mock_psutil
            return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = import_side_effect
        
        with patch('execution.toolbox_0_1.toolbox_0_1_12.os.cpu_count', return_value=8):
            log_system_capabilities()
            
            # Should log both CPU and memory
            mock_arcpy.AddMessage.assert_any_call("🖥️ System: 8 CPU cores detected")
            mock_arcpy.AddMessage.assert_any_call("💾 System: 8.0 GB available RAM (16.0 GB total)")

    @patch('builtins.__import__')
    def test_log_system_capabilities_exception(self, mock_import):
        """Test system capabilities logging with exception."""
        # Mock arcpy module
        mock_arcpy = Mock()
        
        def import_side_effect(name, *args, **kwargs):
            if name == "arcpy":
                return mock_arcpy
            return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = import_side_effect
        
        with patch('execution.toolbox_0_1.toolbox_0_1_12.os.cpu_count', side_effect=Exception("CPU error")):
            log_system_capabilities()
            
            # Should log exception
            mock_arcpy.AddMessage.assert_any_call("🖥️ System: Detection failed - CPU error")


class TestCoverageEdgeCases(unittest.TestCase):
    """Test edge cases for complete coverage."""

    def test_module_import_structure(self):
        """Test that all expected functions are importable."""
        # Verify main functions exist
        self.assertTrue(callable(log_system_capabilities))
        self.assertTrue(callable(main))
        
        # Verify classes exist and are instantiable
        toolbox = ForestClassificationToolbox()
        self.assertIsNotNone(toolbox)
        
        tool = ForestClassificationTool()
        self.assertIsNotNone(tool)

    def test_os_cpu_count_none_fallback(self):
        """Test CPU count fallback when os.cpu_count returns None."""
        with patch('execution.toolbox_0_1.toolbox_0_1_12.os.cpu_count', return_value=None):
            with patch('builtins.__import__') as mock_import:
                mock_arcpy = Mock()
                
                def import_side_effect(name, *args, **kwargs):
                    if name == "arcpy":
                        return mock_arcpy
                    elif name == "psutil":
                        raise ImportError("No psutil")
                    return __import__(name, *args, **kwargs)
                
                mock_import.side_effect = import_side_effect
                
                log_system_capabilities()
                
                # Should fallback to 4 cores
                mock_arcpy.AddMessage.assert_any_call("🖥️ System: 4 CPU cores detected")

    def test_module_level_execution_guard(self):
        """Test module execution guard behavior."""
        # This test verifies the if __name__ == "__main__" guard exists
        # We can't easily test the actual execution without importing issues
        import execution.toolbox_0_1.toolbox_0_1_12 as toolbox_module
        
        # Check that module has the main function
        self.assertTrue(hasattr(toolbox_module, 'main'))
        self.assertTrue(callable(toolbox_module.main))


if __name__ == "__main__":
    unittest.main(verbosity=2)
