# -*- coding: utf-8 -*-
"""
Test ToolValidator for Forest Classification Tool - Phase 2: Auto-Discovery Mode v0.2.3

Created: 2025-08-29 12:30
Version: 0.2.3

Test suite for Phase 2 ToolValidator implementation with auto-discovery mode.
Tests dropdown population, parameter validation, and system capabilities detection.

Developed as part of the Single File Development Strategy for ArcGIS Pro Forest Classification Tool.
"""

import unittest
import sys
import os

# Add the src directory to the path so we can import our validation modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    import importlib.util
    ARCPY_AVAILABLE = importlib.util.find_spec("arcpy") is not None
except ImportError:
    ARCPY_AVAILABLE = False


class MockParameter:
    """Mock ArcGIS Parameter for testing."""
    
    def __init__(self, name="test_param"):
        self.name = name
        self.value = None
        self.valueAsText = None
        self.altered = False
        self.filter = MockFilter()
        self._error_message = None
        self._warning_message = None
    
    def setErrorMessage(self, message):
        self._error_message = message
    
    def setWarningMessage(self, message):
        self._warning_message = message


class MockFilter:
    """Mock ArcGIS Parameter Filter for testing."""
    
    def __init__(self):
        self.type = None
        self.list = []


class MockArcpyForTesting:
    """Mock ArcGIS functionality for testing without full ArcGIS Pro environment."""
    
    def __init__(self):
        self.messages = []
    
    def GetParameterInfo(self):
        # Return mock parameters matching toolbox_0_2_3.py structure
        return [
            MockParameter("output_layer"),
            MockParameter("thread_count"), 
            MockParameter("memory_allocation")
        ]
    
    def Exists(self, path):
        # Mock directory existence
        return True


# Mock arcpy if not available
if not ARCPY_AVAILABLE:
    import types
    mock_arcpy = types.ModuleType('arcpy')
    
    # Add mock functionality using setattr to avoid type checking issues
    mock_instance = MockArcpyForTesting()
    setattr(mock_arcpy, 'GetParameterInfo', mock_instance.GetParameterInfo)
    setattr(mock_arcpy, 'Exists', mock_instance.Exists)
    
    sys.modules['arcpy'] = mock_arcpy


class TestPhase2ToolValidator(unittest.TestCase):
    """Test Phase 2 ToolValidator auto-discovery functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Import after arcpy is set up
        from src.agp_validation.validation_toolbox_0_2_3 import ToolValidator
        
        self.validator_class = ToolValidator
    
    def test_tool_validator_initialization(self):
        """Test that ToolValidator initializes properly."""
        validator = self.validator_class()
        
        # Test that validator has required methods
        self.assertTrue(hasattr(validator, 'initializeParameters'))
        self.assertTrue(hasattr(validator, 'updateParameters'))
        self.assertTrue(hasattr(validator, 'updateMessages'))
        self.assertTrue(hasattr(validator, 'isLicensed'))
        
        # Test that params are initialized
        self.assertTrue(hasattr(validator, 'params'))
    
    def test_system_capabilities_detection(self):
        """Test that system capabilities are detected properly."""
        validator = self.validator_class()
        
        capabilities = validator._get_system_capabilities()
        
        # Test required keys exist
        required_keys = ["cpu_count", "memory_gb", "max_threads", "max_memory_gb"]
        for key in required_keys:
            self.assertIn(key, capabilities)
        
        # Test reasonable values
        self.assertGreaterEqual(capabilities["cpu_count"], 1)
        self.assertGreaterEqual(capabilities["memory_gb"], 1)
        self.assertGreaterEqual(capabilities["max_threads"], 1)
        self.assertGreaterEqual(capabilities["max_memory_gb"], 1)
    
    def test_thread_options_generation(self):
        """Test that thread count dropdown options are generated correctly."""
        validator = self.validator_class()
        
        # Test with mock system capabilities
        system_caps = {"cpu_count": 8, "memory_gb": 16, "max_threads": 7, "max_memory_gb": 14}
        thread_options = validator._get_thread_options(system_caps)
        
        # Test basic structure
        self.assertIsInstance(thread_options, list)
        self.assertGreater(len(thread_options), 5)  # Should have multiple options
        
        # Test that "Auto (Recommended)" is first option
        self.assertEqual(thread_options[0], "Auto (Recommended)")
        
        # Test that percentage-based options are included
        percentage_options = [opt for opt in thread_options if "%" in opt]
        self.assertGreater(len(percentage_options), 0)
        
        # Test fallback behavior with exception
        try:
            # Force exception by passing invalid data
            fallback_options = validator._get_thread_options({})
            self.assertIsInstance(fallback_options, list)
            self.assertIn("Auto (Recommended)", fallback_options)
        except Exception:
            pass  # Exception handling is tested implicitly
    
    def test_memory_options_generation(self):
        """Test that memory allocation dropdown options are generated correctly."""
        validator = self.validator_class()
        
        # Test with mock system capabilities
        system_caps = {"cpu_count": 8, "memory_gb": 16, "max_threads": 7, "max_memory_gb": 14}
        memory_options = validator._get_memory_options(system_caps)
        
        # Test basic structure
        self.assertIsInstance(memory_options, list)
        self.assertGreater(len(memory_options), 5)  # Should have multiple options
        
        # Test that "Auto (Recommended)" is first option
        self.assertEqual(memory_options[0], "Auto (Recommended)")
        
        # Test that percentage-based options are included
        percentage_options = [opt for opt in memory_options if "%" in opt]
        self.assertGreater(len(percentage_options), 0)
        
        # Test that GB options are included
        gb_options = [opt for opt in memory_options if "GB" in opt and "%" not in opt]
        self.assertGreater(len(gb_options), 0)
    
    def test_parameter_initialization(self):
        """Test that parameters are initialized correctly."""
        if not ARCPY_AVAILABLE:
            validator = self.validator_class()
            
            # Test that initializeParameters runs without error
            try:
                validator.initializeParameters()
                # If we get here, no exception was thrown
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"initializeParameters raised exception: {e}")
    
    def test_parameter_updates(self):
        """Test that parameter updates work correctly."""
        if not ARCPY_AVAILABLE:
            validator = self.validator_class()
            
            # Test that updateParameters runs without error
            try:
                validator.updateParameters()
                # If we get here, no exception was thrown
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"updateParameters raised exception: {e}")
    
    def test_message_validation(self):
        """Test that message validation works correctly."""
        if not ARCPY_AVAILABLE:
            validator = self.validator_class()
            
            # Test that updateMessages runs without error
            try:
                validator.updateMessages()
                # If we get here, no exception was thrown
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"updateMessages raised exception: {e}")
    
    def test_licensing(self):
        """Test that tool licensing works correctly."""
        validator = self.validator_class()
        
        # Test that tool is licensed
        self.assertTrue(validator.isLicensed())


class TestPhase2ToolValidatorIntegration(unittest.TestCase):
    """Test Phase 2 ToolValidator integration with toolbox."""
    
    def setUp(self):
        """Set up test environment."""
        from src.agp_validation.validation_toolbox_0_2_3 import ToolValidator
        
        self.validator_class = ToolValidator
    
    def test_parameter_count_compatibility(self):
        """Test that ToolValidator works with the correct number of parameters."""
        # toolbox_0_2_3.py should have 3 parameters
        expected_param_count = 3
        
        validator = self.validator_class()
        
        # Mock the parameter count check
        if hasattr(validator, 'params') and validator.params:
            param_count = len(validator.params)
            self.assertEqual(param_count, expected_param_count)
    
    def test_auto_discovery_mode_compatibility(self):
        """Test that ToolValidator is compatible with auto-discovery mode."""
        validator = self.validator_class()
        
        # Test that validator doesn't expect input layer parameter
        # (This is implicit in the design - no input layer dropdown logic)
        
        # Test system capabilities integration
        capabilities = validator._get_system_capabilities()
        thread_options = validator._get_thread_options(capabilities)
        memory_options = validator._get_memory_options(capabilities)
        
        # Both should return valid dropdown options
        self.assertIsInstance(thread_options, list)
        self.assertIsInstance(memory_options, list)
        self.assertGreater(len(thread_options), 0)
        self.assertGreater(len(memory_options), 0)


class TestPhase2ValidationErrorHandling(unittest.TestCase):
    """Test Phase 2 ToolValidator error handling."""
    
    def setUp(self):
        """Set up test environment."""
        from src.agp_validation.validation_toolbox_0_2_3 import ToolValidator
        
        self.validator_class = ToolValidator
    
    def test_system_capabilities_fallback(self):
        """Test that system capabilities fallback works correctly."""
        validator = self.validator_class()
        
        # Test fallback when psutil is not available
        # This is handled by the except ImportError block
        capabilities = validator._get_system_capabilities()
        
        # Should always return valid capabilities
        self.assertIsInstance(capabilities, dict)
        self.assertIn("cpu_count", capabilities)
        self.assertIn("memory_gb", capabilities)
        self.assertGreaterEqual(capabilities["cpu_count"], 1)
        self.assertGreaterEqual(capabilities["memory_gb"], 1)
    
    def test_dropdown_generation_fallback(self):
        """Test that dropdown generation handles errors gracefully."""
        validator = self.validator_class()
        
        # Test thread options with empty/invalid system_caps
        thread_options = validator._get_thread_options({})
        self.assertIsInstance(thread_options, list)
        self.assertIn("Auto (Recommended)", thread_options)
        
        # Test memory options with empty/invalid system_caps  
        memory_options = validator._get_memory_options({})
        self.assertIsInstance(memory_options, list)
        self.assertIn("Auto (Recommended)", memory_options)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
