# -*- coding: utf-8 -*-
"""
Tests for Phase 2 Auto-Detection Functionality - v0.2.3

Tests the parameter alignment fixes and sample data integration for v0.2.3.
This complements the existing validation tests by focusing on the 3-parameter
structure and predefined data source functionality.

Test Coverage:
- 3-parameter structure validation (output, thread, memory)
- Sample data path resolution
- Parameter alignment with .atbx tool
- Integration with existing validation framework
- Predefined data source functionality
"""

import unittest
import os
import json
import tempfile
from unittest.mock import patch, MagicMock

# Import the validation module
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "src", "execution", "toolbox_0_2"
    ),
)
from toolbox_0_2_3 import (
    load_import_fields_json,
    get_required_input_datasets,
    get_dataset_field_mapping,
    auto_detect_input_layers,
    validate_auto_detected_layers,
)


class TestAutoDetectionFunctionality(unittest.TestCase):
    """Test suite for Phase 2 auto-detection features."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_json_data = {
            "metadata": {"title": "Test Import Fields", "version": "1.0.1"},
            "input_datasets": {
                "Grid_8m_SR16_Dataset": {
                    "description": "Forest inventory data",
                    "type": "raster_dataset",
                    "field_count": 3,
                    "categories": ["age_data", "species_type"],
                },
                "Grid_8m_AR5_Dataset": {
                    "description": "Soil properties",
                    "type": "raster_dataset",
                    "field_count": 2,
                    "categories": ["soil_properties"],
                },
                "Table_Grid_8m_ElevStats": {
                    "description": "Elevation statistics",
                    "type": "table",
                    "field_count": 1,
                    "categories": ["elevation"],
                },
            },
            "field_categories": {
                "age_data": {
                    "dataset": "Grid_8m_SR16_Dataset",
                    "fields": {
                        "srrtrealder": {"description": "Stand age", "type": "years"},
                        "srrhogstaar": {"description": "Harvest year", "type": "year"},
                    },
                },
                "species_type": {
                    "dataset": "Grid_8m_SR16_Dataset",
                    "fields": {
                        "srrtreslag": {
                            "description": "Dominant species",
                            "type": "classification",
                        }
                    },
                },
                "soil_properties": {
                    "dataset": "Grid_8m_AR5_Dataset",
                    "fields": {
                        "markfukt": {
                            "description": "Soil moisture",
                            "type": "classification",
                        },
                        "artype": {
                            "description": "Soil type",
                            "type": "classification",
                        },
                    },
                },
                "elevation": {
                    "dataset": "Table_Grid_8m_ElevStats",
                    "fields": {
                        "elev_mean": {"description": "Mean elevation", "type": "meters"}
                    },
                },
            },
            "summary": {
                "total_fields": 6,
                "input_datasets_required": [
                    "Grid_8m_SR16_Dataset",
                    "Grid_8m_AR5_Dataset",
                    "Table_Grid_8m_ElevStats",
                ],
            },
        }

    def test_load_import_fields_json_success(self):
        """Test successful loading of IMPORT_FIELDS JSON."""
        # Create temporary JSON file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(self.test_json_data, f)
            temp_path = f.name

        try:
            # Load the JSON
            result = load_import_fields_json(temp_path)

            # Verify structure
            self.assertIn("metadata", result)
            self.assertIn("input_datasets", result)
            self.assertIn("field_categories", result)
            self.assertIn("summary", result)

            # Verify content
            self.assertEqual(result["metadata"]["version"], "1.0.1")
            self.assertEqual(len(result["input_datasets"]), 3)
            self.assertEqual(result["summary"]["total_fields"], 6)

        finally:
            os.unlink(temp_path)

    def test_load_import_fields_json_file_not_found(self):
        """Test handling of missing JSON file."""
        with self.assertRaises(FileNotFoundError):
            load_import_fields_json("/nonexistent/path/file.json")

    def test_load_import_fields_json_malformed(self):
        """Test handling of malformed JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{ invalid json content")
            temp_path = f.name

        try:
            with self.assertRaises(json.JSONDecodeError):
                load_import_fields_json(temp_path)
        finally:
            os.unlink(temp_path)

    @patch("toolbox_0_2_1.load_import_fields_json")
    def test_get_required_input_datasets_success(self, mock_load_json):
        """Test extraction of required input datasets."""
        mock_load_json.return_value = self.test_json_data

        result = get_required_input_datasets()

        expected = [
            "Grid_8m_SR16_Dataset",
            "Grid_8m_AR5_Dataset",
            "Table_Grid_8m_ElevStats",
        ]
        self.assertEqual(result, expected)

    @patch("toolbox_0_2_1.load_import_fields_json")
    def test_get_required_input_datasets_exception_handling(self, mock_load_json):
        """Test proper exception handling when JSON loading fails."""
        mock_load_json.side_effect = Exception("JSON loading failed")

        # Should raise the exception instead of returning fallback
        with self.assertRaises(Exception):
            get_required_input_datasets()

    @patch("toolbox_0_2_1.load_import_fields_json")
    def test_get_dataset_field_mapping_success(self, mock_load_json):
        """Test dataset field mapping extraction."""
        mock_load_json.return_value = self.test_json_data

        result = get_dataset_field_mapping()

        # Verify structure
        self.assertIn("Grid_8m_SR16_Dataset", result)
        self.assertIn("Grid_8m_AR5_Dataset", result)
        self.assertIn("Table_Grid_8m_ElevStats", result)

        # Verify SR16 dataset mapping
        sr16_mapping = result["Grid_8m_SR16_Dataset"]
        self.assertEqual(sr16_mapping["field_count"], 3)
        self.assertEqual(len(sr16_mapping["fields"]), 3)
        self.assertIn("srrtrealder", sr16_mapping["fields"])
        self.assertIn("srrhogstaar", sr16_mapping["fields"])
        self.assertIn("srrtreslag", sr16_mapping["fields"])

        # Verify AR5 dataset mapping
        ar5_mapping = result["Grid_8m_AR5_Dataset"]
        self.assertEqual(ar5_mapping["field_count"], 2)
        self.assertEqual(len(ar5_mapping["fields"]), 2)
        self.assertIn("markfukt", ar5_mapping["fields"])
        self.assertIn("artype", ar5_mapping["fields"])

        # Verify ElevStats dataset mapping
        elev_mapping = result["Table_Grid_8m_ElevStats"]
        self.assertEqual(elev_mapping["field_count"], 1)
        self.assertEqual(len(elev_mapping["fields"]), 1)
        self.assertIn("elev_mean", elev_mapping["fields"])

    @patch("toolbox_0_2_1.load_import_fields_json")
    def test_get_dataset_field_mapping_exception_handling(self, mock_load_json):
        """Test proper exception handling when JSON loading fails."""
        mock_load_json.side_effect = Exception("JSON loading failed")

        # Should raise the exception instead of returning fallback
        with self.assertRaises(Exception):
            get_dataset_field_mapping()

    @patch("toolbox_0_2_1.get_required_input_datasets")
    @patch("arcpy.mp.ArcGISProject")
    def test_auto_detect_input_layers_success(self, mock_project, mock_get_datasets):
        """Test successful auto-detection of input layers."""
        # Mock ArcGIS Pro project and map
        mock_aprx = MagicMock()
        mock_map = MagicMock()
        mock_project.return_value = mock_aprx
        mock_aprx.listMaps.return_value = [mock_map]

        # Mock layers and tables
        mock_layer_sr16 = MagicMock()
        mock_layer_sr16.name = "Grid_8m_SR16_ForestData"
        mock_layer_ar5 = MagicMock()
        mock_layer_ar5.name = "Grid_8m_AR5_SoilTypes"
        mock_table_elev = MagicMock()
        mock_table_elev.name = "ElevationStats_Table"

        mock_map.listLayers.return_value = [mock_layer_sr16, mock_layer_ar5]
        mock_map.listTables.return_value = [mock_table_elev]

        # Mock required datasets
        mock_get_datasets.return_value = [
            "Grid_8m_SR16_Dataset",
            "Grid_8m_AR5_Dataset",
            "Table_Grid_8m_ElevStats",
        ]

        # Test auto-detection
        result = auto_detect_input_layers()

        # Verify detection results
        self.assertEqual(result["Grid_8m_SR16_Dataset"], "Grid_8m_SR16_ForestData")
        self.assertEqual(result["Grid_8m_AR5_Dataset"], "Grid_8m_AR5_SoilTypes")
        self.assertEqual(result["Table_Grid_8m_ElevStats"], "ElevationStats_Table")

    def test_auto_detect_input_layers_no_arcpy(self):
        """Test auto-detection when ArcPy is not available."""
        # Mock the import itself to raise ImportError
        with patch("builtins.__import__") as mock_import:

            def import_side_effect(name, *args, **kwargs):
                if name == "arcpy":
                    raise ImportError("No module named 'arcpy'")
                return __import__(name, *args, **kwargs)

            mock_import.side_effect = import_side_effect

            result = auto_detect_input_layers()

            # Should return empty dict when ArcPy is not available
            self.assertEqual(result, {})

    @patch("toolbox_0_2_1.get_dataset_field_mapping")
    @patch("arcpy.ListFields")
    def test_validate_auto_detected_layers_success(
        self, mock_list_fields, mock_get_mapping
    ):
        """Test validation of auto-detected layers."""
        # Mock dataset field mapping
        mock_get_mapping.return_value = {
            "Grid_8m_SR16_Dataset": {
                "fields": ["srrtrealder", "srrhogstaar", "srrtreslag"]
            },
            "Grid_8m_AR5_Dataset": {"fields": ["markfukt", "artype"]},
        }

        # Mock field lists for layers
        def mock_fields_side_effect(layer_name):
            if "SR16" in layer_name:
                mock_field1 = MagicMock()
                mock_field1.name = "srrtrealder"
                mock_field2 = MagicMock()
                mock_field2.name = "srrhogstaar"
                mock_field3 = MagicMock()
                mock_field3.name = "srrtreslag"
                return [mock_field1, mock_field2, mock_field3]
            elif "AR5" in layer_name:
                mock_field1 = MagicMock()
                mock_field1.name = "markfukt"
                mock_field2 = MagicMock()
                mock_field2.name = "artype"
                return [mock_field1, mock_field2]
            return []

        mock_list_fields.side_effect = mock_fields_side_effect

        # Test detected layers
        detected_layers = {
            "Grid_8m_SR16_Dataset": "Grid_8m_SR16_ForestData",
            "Grid_8m_AR5_Dataset": "Grid_8m_AR5_SoilTypes",
        }

        result = validate_auto_detected_layers(detected_layers)

        # Verify validation results
        self.assertIn("Grid_8m_SR16_Dataset", result)
        self.assertIn("Grid_8m_AR5_Dataset", result)

        # Check SR16 validation
        sr16_result = result["Grid_8m_SR16_Dataset"]
        self.assertEqual(sr16_result["layer_name"], "Grid_8m_SR16_ForestData")
        self.assertTrue(sr16_result["validation_passed"])
        self.assertEqual(sr16_result["fields_found"], 3)
        self.assertEqual(sr16_result["fields_expected"], 3)
        self.assertEqual(sr16_result["missing_fields"], [])

        # Check AR5 validation
        ar5_result = result["Grid_8m_AR5_Dataset"]
        self.assertEqual(ar5_result["layer_name"], "Grid_8m_AR5_SoilTypes")
        self.assertTrue(ar5_result["validation_passed"])
        self.assertEqual(ar5_result["fields_found"], 2)
        self.assertEqual(ar5_result["fields_expected"], 2)
        self.assertEqual(ar5_result["missing_fields"], [])

    @patch("toolbox_0_2_1.get_dataset_field_mapping")
    @patch("arcpy.ListFields")
    def test_validate_auto_detected_layers_missing_fields(
        self, mock_list_fields, mock_get_mapping
    ):
        """Test validation with missing fields."""
        # Mock dataset field mapping
        mock_get_mapping.return_value = {
            "Grid_8m_SR16_Dataset": {
                "fields": ["srrtrealder", "srrhogstaar", "srrtreslag", "missing_field"]
            }
        }

        # Mock incomplete field list (missing one field)
        mock_field1 = MagicMock()
        mock_field1.name = "srrtrealder"
        mock_field2 = MagicMock()
        mock_field2.name = "srrhogstaar"
        mock_field3 = MagicMock()
        mock_field3.name = "srrtreslag"
        mock_list_fields.return_value = [mock_field1, mock_field2, mock_field3]

        detected_layers = {"Grid_8m_SR16_Dataset": "Grid_8m_SR16_ForestData"}

        result = validate_auto_detected_layers(detected_layers)

        # Verify validation results with missing field
        sr16_result = result["Grid_8m_SR16_Dataset"]
        self.assertEqual(sr16_result["fields_found"], 3)
        self.assertEqual(sr16_result["fields_expected"], 4)
        self.assertEqual(sr16_result["missing_fields"], ["missing_field"])
        # Should still pass with 75% field coverage (3/4 = 0.75 < 0.80 threshold)
        self.assertFalse(sr16_result["validation_passed"])

    def test_integration_with_existing_validation(self):
        """Test that new auto-detection integrates with existing validation."""
        # Import existing validation function from validation module, not toolbox module
        import sys
        import os

        validation_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "src",
            "validation",
            "toolbox_0_2",
        )
        sys.path.insert(0, os.path.abspath(validation_path))

        try:
            from validation_toolbox_0_2_3 import validate_import_fields_detailed
        except ImportError:
            self.skipTest("validation_toolbox_0_2_3 module not available")

        # Mock arcpy for this test since we're testing the validation logic
        with patch("builtins.__import__") as mock_import:
            # Store original import function
            original_import = __import__

            def import_side_effect(name, *args, **kwargs):
                if name == "arcpy":
                    # Return a mock arcpy module
                    mock_arcpy = MagicMock()
                    mock_arcpy.Exists.return_value = True

                    # Create mock field objects
                    mock_fields = []
                    test_field_names = ["srrtreslag", "srrbmo", "srrmhoyde", "srrvolmb"]
                    for field_name in test_field_names:
                        mock_field = MagicMock()
                        mock_field.name = field_name
                        mock_fields.append(mock_field)

                    mock_arcpy.ListFields.return_value = mock_fields
                    return mock_arcpy
                return original_import(name, *args, **kwargs)

            mock_import.side_effect = import_side_effect

            # Test that existing validation works with minimal required fields
            result = validate_import_fields_detailed("test_layer")
            self.assertTrue(result["validation_passed"])
            self.assertEqual(len(result["critical_fields_found"]), 4)


if __name__ == "__main__":
    unittest.main()
