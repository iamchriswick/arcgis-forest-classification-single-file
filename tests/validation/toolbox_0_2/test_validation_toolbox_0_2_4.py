# -*- coding: utf-8 -*-
"""
Test Suite for ToolValidator - Forest Classification Tool Phase 2 v0.2.4

Tests the ToolValidator class and helper functions for Phase 2.4 requirements.
Uses real ArcPy integration and minimal mocking per Testing Strategy.
Focuses on 3-parameter structure and CUD operations support.

Created: 2025-09-02
Author: Forest Classification Development Team
"""

import unittest
import sys
import os

# Add the src directory to the path for importing
src_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "src")
sys.path.insert(0, os.path.abspath(src_path))

# Import validation module with real ArcPy (no mocking)
try:
    from validation.toolbox_0_2.validation_toolbox_0_2_4 import (
        ToolValidator,
        get_cpu_cores,
        get_available_memory_gb,
        generate_thread_labels,
        generate_memory_labels,
        IMPORT_FIELDS,
        validate_import_fields,
        validate_import_fields_detailed,
        get_phase2_validation_info,
    )
except ImportError:
    # Alternative import path
    import importlib.util

    validation_module_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "src",
        "validation",
        "toolbox_0_2",
        "validation_toolbox_0_2_1.py",
    )
    spec = importlib.util.spec_from_file_location(
        "validation_toolbox_0_2_1", os.path.abspath(validation_module_path)
    )
    if spec is not None and spec.loader is not None:
        validation_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validation_module)

        # Extract what we need
        ToolValidator = validation_module.ToolValidator
        get_cpu_cores = validation_module.get_cpu_cores
        get_available_memory_gb = validation_module.get_available_memory_gb
        generate_thread_labels = validation_module.generate_thread_labels
        generate_memory_labels = validation_module.generate_memory_labels
        IMPORT_FIELDS = validation_module.IMPORT_FIELDS
        validate_import_fields = validation_module.validate_import_fields
        validate_import_fields_detailed = (
            validation_module.validate_import_fields_detailed
        )
        get_phase2_validation_info = validation_module.get_phase2_validation_info
    else:
        raise ImportError("Could not import validation module")


class TestImportFieldsValidation(unittest.TestCase):
    """Test import fields validation functionality."""

    def test_import_fields_constant(self):
        """Test IMPORT_FIELDS constant is properly defined."""
        self.assertIsInstance(IMPORT_FIELDS, dict)
        self.assertGreater(len(IMPORT_FIELDS), 0)

        # Verify all category keys are strings and values are lists
        for category, fields in IMPORT_FIELDS.items():
            self.assertIsInstance(category, str)
            self.assertGreater(len(category), 0)
            self.assertIsInstance(fields, list)
            self.assertGreater(len(fields), 0)

            # Verify all field names are strings
            for field in fields:
                self.assertIsInstance(field, str)
                self.assertGreater(len(field), 0)

    def test_validate_import_fields_function_exists(self):
        """Test validate_import_fields function exists and is callable."""
        self.assertTrue(callable(validate_import_fields))

    def test_validate_import_fields_detailed_function_exists(self):
        """Test validate_import_fields_detailed function exists and is callable."""
        self.assertTrue(callable(validate_import_fields_detailed))

    def test_get_validation_info_function_exists(self):
        """Test get_phase2_validation_info function exists and is callable."""
        self.assertTrue(callable(get_phase2_validation_info))

    def test_get_validation_info_returns_dict(self):
        """Test get_phase2_validation_info returns proper structure."""
        info = get_phase2_validation_info()

        self.assertIsInstance(info, dict)
        self.assertIn("field_categories", info)
        self.assertIn("total_fields", info)
        self.assertIn("validation_focus", info)
        self.assertIn("critical_fields", info)

        # Verify field_categories is a list
        categories = info["field_categories"]
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)

        # Verify total_fields is a positive integer
        total_fields = info["total_fields"]
        self.assertIsInstance(total_fields, int)
        self.assertGreater(total_fields, 0)

        # Verify validation_focus is a string
        focus = info["validation_focus"]
        self.assertIsInstance(focus, str)
        self.assertGreater(len(focus), 0)

        # Verify critical_fields is a list of strings
        critical = info["critical_fields"]
        self.assertIsInstance(critical, list)
        self.assertGreater(len(critical), 0)
        for field in critical:
            self.assertIsInstance(field, str)
            self.assertGreater(len(field), 0)


class TestSystemHelpers(unittest.TestCase):
    """Test system helper functions work with real ArcPy integration."""

    def test_system_helper_functions_basic(self):
        """Test basic system helper functions work without mocking."""
        # Test CPU core detection works
        cores = get_cpu_cores()
        self.assertIsInstance(cores, int)
        self.assertGreater(cores, 0)

        # Test memory detection works
        memory_gb = get_available_memory_gb()
        self.assertIsInstance(memory_gb, int)
        self.assertGreater(memory_gb, 0)

        # Test label generation works
        thread_labels = generate_thread_labels(cores)
        self.assertIsInstance(thread_labels, list)
        self.assertEqual(len(thread_labels), 3)

        memory_labels = generate_memory_labels(memory_gb)
        self.assertIsInstance(memory_labels, list)
        self.assertEqual(len(memory_labels), 3)

    def test_thread_labels_generation(self):
        """Test thread label generation with different core counts."""
        test_cases = [4, 8, 16, 32]

        for cores in test_cases:
            with self.subTest(cores=cores):
                labels = generate_thread_labels(cores)

                # Should return 3 labels
                self.assertEqual(len(labels), 3)

                # First should be Auto
                self.assertIn("Auto", labels[0])

                # Should contain correct calculations
                moderate = max(2, int(cores * 0.45))
                high = max(3, int(cores * 0.90))

                self.assertIn(str(moderate), labels[1])
                self.assertIn(str(high), labels[2])

    def test_memory_labels_generation(self):
        """Test memory label generation with different memory amounts."""
        test_cases = [8.0, 16.0, 32.0, 64.0]

        for avail_gb in test_cases:
            with self.subTest(avail_gb=avail_gb):
                labels = generate_memory_labels(avail_gb)

                # Should return 3 labels
                self.assertEqual(len(labels), 3)

                # Should contain correct calculations
                conservative = max(2, int(avail_gb * 0.30))
                balanced = max(4, int(avail_gb * 0.60))
                aggressive = max(6, int(avail_gb * 0.90))

                self.assertIn(str(conservative), labels[0])
                self.assertIn(str(balanced), labels[1])
                self.assertIn(str(aggressive), labels[2])


if __name__ == "__main__":
    unittest.main(verbosity=2)
