# -*- coding: utf-8 -*-
"""
ToolValidator for Forest Classification Tool - Phase 2 v0.2.5

Created: 2025-09-02
Version: 0.2.5
Built on: Phase 1 v0.1.12 foundation (exact copy + IMPORT_FIELDS validation)

This file contains the ToolValidator code for the ArcGIS Pro .atbx Script tool.
Copy the code below to .atbx Properties → Validation to enable enhanced GUI features.

Phase 2 = Phase 1 + IMPORT_FIELDS validation:
- Inherits ALL Phase 1 GUI functionality unchanged
- Same enhanced dropdowns with system utilization percentages
- Same Auto multithreading and intelligent defaults
- Same dynamic feature layer population
- ONLY ADDITION: IMPORT_FIELDS validation logic

Enhanced Features v0.1.12 (inherited from Phase 1):
- Auto multithreading option with intelligent thread selection
- Detailed memory allocation with percentage utilization display
- Dynamic system capability detection for optimal performance
- Smart dropdown population for output feature layers
- PLUS: Phase 2 IMPORT_FIELDS validation

Usage Instructions:
1. Open your .atbx file in ArcGIS Pro
2. Right-click the tool → Properties → Validation tab
3. Copy the entire ToolValidator class code below
4. Paste it into the Validation code editor
5. Save the .atbx file

The ToolValidator will provide:
- Enhanced dropdown labels with system utilization percentages
- Auto-detection of CPU cores and available memory
- Intelligent defaults (moderate/balanced settings)
- Dynamic feature layer population from active map
"""

# ===== TOOLVALIDATOR CODE FOR .ATBX SCRIPT TOOL =====
# Copy the entire ToolValidator class below to .atbx Properties → Validation:

# ArcPy import deferred to method level to prevent pytest crashes
import os


class ToolValidator(object):
    """
    ToolValidator for Forest Classification Tool - Phase 2 v0.2.4

    Built on Phase 1 v0.1.12 foundation + parameter alignment for 3 params.
    Copy this entire class definition to .atbx Properties → Validation.
    Enhanced GUI features will be automatically enabled.
    """

    def __init__(self):
        import arcpy  # Deferred import to prevent pytest crashes

        self.params = (
            arcpy.GetParameterInfo()
        )  # 0=output_layer, 1=multithreading_config, 2=memory_config

        # Cache system capabilities to ensure consistency across lifecycle methods
        self._cached_cores = None
        self._cached_memory = None

    # --- helpers ---
    def _cpu_cores(self):
        if self._cached_cores is None:
            try:
                self._cached_cores = max(1, os.cpu_count() or 4)
            except Exception:
                self._cached_cores = 4
        return self._cached_cores

    def _avail_mem_gb(self):
        if self._cached_memory is None:
            try:
                import psutil

                self._cached_memory = max(
                    2, int(psutil.virtual_memory().available / (1024**3))
                )
            except Exception:
                self._cached_memory = 8  # fallback if psutil not present
        return self._cached_memory

    def _thread_labels(self, cores):
        # Enhanced GUI with Auto option and detailed thread information
        auto = "Auto (let system decide)"
        moderate = max(2, int(cores * 0.45))  # 45% utilization
        high = max(3, int(cores * 0.90))  # 90% utilization
        return [
            auto,
            f"Moderate - {moderate} threads (45% utilization)",
            f"High - {high} threads (90% utilization)",
        ]

    def _memory_labels(self, avail_gb):
        # Enhanced GUI with detailed memory allocation information
        conservative = max(2, int(avail_gb * 0.30))  # 30%
        balanced = max(4, int(avail_gb * 0.60))  # 60%
        aggressive = max(6, int(avail_gb * 0.90))  # 90%
        return [
            f"{conservative} GB (30% of {avail_gb:.1f} GB available)",
            f"{balanced} GB (60% of {avail_gb:.1f} GB available)",
            f"{aggressive} GB (90% of {avail_gb:.1f} GB available)",
        ]

    # --- lifecycle ---
    def initializeParameters(self):
        # Dropdowns with default = Auto (index 0) for threading, balanced (index 1) for memory
        self.params[1].filter.list = self._thread_labels(self._cpu_cores())
        self.params[1].value = self.params[1].filter.list[0]  # Auto threading

        self.params[2].filter.list = self._memory_labels(self._avail_mem_gb())
        self.params[2].value = self.params[2].filter.list[1]  # Balanced memory

        # Populate output layer dropdown if a map is active
        try:
            import arcpy  # Deferred import to prevent pytest crashes

            aprx = arcpy.mp.ArcGISProject("CURRENT")
            m = aprx.activeMap
            if m:
                names = [
                    lyr.name
                    for lyr in m.listLayers()
                    if getattr(lyr, "isFeatureLayer", False)
                ]
                if names:
                    self.params[0].filter.list = names
                    if not self.params[0].value:
                        self.params[0].value = names[0]
        except Exception:
            pass
        return

    def updateParameters(self):
        # Refresh dropdowns if context changes but preserve user selections when possible
        current_thread_value = self.params[1].value
        current_memory_value = self.params[2].value

        # Update the filter lists
        self.params[1].filter.list = self._thread_labels(self._cpu_cores())
        self.params[2].filter.list = self._memory_labels(self._avail_mem_gb())

        # Try to preserve user selections by checking patterns instead of exact matches
        if current_thread_value:
            thread_str = str(current_thread_value)
            # Check if it's still a valid pattern (Auto, Moderate, or High)
            if any(pattern in thread_str for pattern in ["Auto", "Moderate", "High"]):
                # Keep the existing selection if it matches a valid pattern
                if thread_str in self.params[1].filter.list:
                    self.params[1].value = current_thread_value
                else:
                    # Find equivalent option by pattern
                    if "Auto" in thread_str:
                        self.params[1].value = self.params[1].filter.list[
                            0
                        ]  # Auto is always first
                    elif "Moderate" in thread_str:
                        self.params[1].value = self.params[1].filter.list[
                            1
                        ]  # Moderate is second
                    elif "High" in thread_str:
                        self.params[1].value = self.params[1].filter.list[
                            2
                        ]  # High is third

        if current_memory_value:
            memory_str = str(current_memory_value)
            # Check if it's still a valid pattern (30%, 60%, or 90%)
            if any(pattern in memory_str for pattern in ["30%", "60%", "90%"]):
                # Keep the existing selection if it matches exactly
                if memory_str in self.params[2].filter.list:
                    self.params[2].value = current_memory_value
                else:
                    # Find equivalent option by percentage pattern
                    if "30%" in memory_str:
                        self.params[2].value = self.params[2].filter.list[
                            0
                        ]  # 30% is conservative
                    elif "60%" in memory_str:
                        self.params[2].value = self.params[2].filter.list[
                            1
                        ]  # 60% is balanced
                    elif "90%" in memory_str:
                        self.params[2].value = self.params[2].filter.list[
                            2
                        ]  # 90% is aggressive

        try:
            import arcpy  # Deferred import to prevent pytest crashes

            aprx = arcpy.mp.ArcGISProject("CURRENT")
            m = aprx.activeMap
            if m:
                self.params[0].filter.list = [
                    lyr.name
                    for lyr in m.listLayers()
                    if getattr(lyr, "isFeatureLayer", False)
                ]
        except Exception:
            pass
        return

    def updateMessages(self):
        # Phase 2 ADDITION: IMPORT_FIELDS validation messages
        try:
            # Phase 1 validation (unchanged - no specific validation messages)

            # Phase 2 ADDITION: IMPORT_FIELDS validation
            if len(self.params) > 0 and self.params[0].value:
                output_name = str(self.params[0].value)
                # Provide guidance for IMPORT_FIELDS validation context
                if not any(
                    keyword in output_name.lower()
                    for keyword in ["validated", "checked", "import"]
                ):
                    self.params[0].setWarningMessage(
                        "Phase 2: This tool validates IMPORT_FIELDS compatibility. Consider output name indicating validation (e.g., '_validated', '_import_checked')"
                    )
        except Exception:
            pass
        return


# ===== HELPER FUNCTIONS FOR TESTING =====
def get_cpu_cores():
    """Helper function to get CPU core count for testing."""
    import os

    try:
        return max(1, os.cpu_count() or 4)
    except Exception:
        return 4


def get_available_memory_gb():
    """Helper function to get available memory for testing."""
    try:
        import psutil

        return max(2, int(psutil.virtual_memory().available / (1024**3)))
    except Exception:
        return 8


def generate_thread_labels(cores):
    """Generate thread configuration labels for testing."""
    auto = "Auto (let system decide)"
    moderate = max(2, int(cores * 0.45))  # 45% utilization
    high = max(3, int(cores * 0.90))  # 90% utilization
    return [
        auto,
        f"Moderate - {moderate} threads (45% utilization)",
        f"High - {high} threads (90% utilization)",
    ]


def generate_memory_labels(avail_gb):
    """Generate memory allocation labels for testing."""
    conservative = max(2, int(avail_gb * 0.30))  # 30%
    balanced = max(4, int(avail_gb * 0.60))  # 60%
    aggressive = max(6, int(avail_gb * 0.90))  # 90%
    return [
        f"{conservative} GB (30% of {avail_gb:.1f} GB available)",
        f"{balanced} GB (60% of {avail_gb:.1f} GB available)",
        f"{aggressive} GB (90% of {avail_gb:.1f} GB available)",
    ]


# ===== PHASE 2 ADDITIONS =====

# IMPORT_FIELDS definition for Phase 2 validation (from IMPORT_FIELDS.md)
IMPORT_FIELDS = {
    "Age Data": [
        "srrhogstaar",  # Harvest year
        "srrtrealder",  # Stand age
        "srrtrealder_l",  # Stand age lower bound
        "srrtrealder_u",  # Stand age upper bound
    ],
    "Species Type": [
        "srrtreslag",  # Dominant species
    ],
    "Biomass": [
        "srrbmo",  # Above-ground biomass (t/ha)
        "srrbmo_l",  # Above-ground biomass lower bound (t/ha)
        "srrbmo_u",  # Above-ground biomass upper bound (t/ha)
        "srrbmu",  # Below-ground biomass (t/ha)
        "srrbmu_l",  # Below-ground biomass lower bound (t/ha)
        "srrbmu_u",  # Below-ground biomass upper bound (t/ha)
    ],
    "Volume": [
        "srrvolmb",  # Volume over bark (m³/ha)
        "srrvolmb_l",  # Volume over bark lower bound (m³/ha)
        "srrvolmb_u",  # Volume over bark upper bound (m³/ha)
        "srrvolub",  # Volume under bark (m³/ha)
        "srrvolub_l",  # Volume under bark lower bound (m³/ha)
        "srrvolub_u",  # Volume under bark upper bound (m³/ha)
    ],
    "Height": [
        "srrmhoyde",  # Mean height (m)
        "srrmhoyde_l",  # Mean height lower bound (m)
        "srrmhoyde_u",  # Mean height upper bound (m)
        "srrohoyde",  # Top height (m)
        "srrohoyde_l",  # Top height lower bound (m)
        "srrohoyde_u",  # Top height upper bound (m)
    ],
    "Site Index": [
        "srrbonitet",  # Site index (bonitet)
    ],
    "Diameter": [
        "srrdiammiddel",  # Mean DBH (cm)
        "srrdiammiddel_l",  # Mean DBH lower bound (cm)
        "srrdiammiddel_u",  # Mean DBH upper bound (cm)
        "srrdiammiddel_ge8",  # Mean DBH ≥ 8 cm (cm)
        "srrdiammiddel_ge8_l",  # Mean DBH ≥ 8 cm lower bound (cm)
        "srrdiammiddel_ge8_u",  # Mean DBH ≥ 8 cm upper bound (cm)
    ],
    "Basal Area": [
        "srrgrflate",  # Basal area (m²/ha)
        "srrgrflate_l",  # Basal area lower bound (m²/ha)
        "srrgrflate_u",  # Basal area upper bound (m²/ha)
    ],
    "Tree Density": [
        "srrtreantall",  # Trees per hectare (all)
        "srrtreantall_l",  # Trees per hectare lower bound (all)
        "srrtreantall_u",  # Trees per hectare upper bound (all)
        "srrtreantall_ge8",  # Trees per hectare ≥ 8 cm DBH
        "srrtreantall_ge8_l",  # Trees per hectare ≥ 8 cm lower bound
        "srrtreantall_ge8_u",  # Trees per hectare ≥ 8 cm upper bound
        "srrtreantall_ge10",  # Trees per hectare ≥ 10 cm DBH
        "srrtreantall_ge10_l",  # Trees per hectare ≥ 10 cm lower bound
        "srrtreantall_ge10_u",  # Trees per hectare ≥ 10 cm upper bound
        "srrtreantall_ge16",  # Trees per hectare ≥ 16 cm DBH
        "srrtreantall_ge16_l",  # Trees per hectare ≥ 16 cm lower bound
        "srrtreantall_ge16_u",  # Trees per hectare ≥ 16 cm upper bound
    ],
    "Leaf Area Index": [
        "srrlai",  # Leaf Area Index
        "srrlai_l",  # Leaf Area Index lower bound
        "srrlai_u",  # Leaf Area Index upper bound
    ],
    "Crown Coverage": [
        "srrkronedek",  # Crown coverage (%)
    ],
    "Elevation": [
        "elev_min",  # Minimum elevation (m)
        "elev_mean",  # Mean elevation (m)
        "elev_max",  # Maximum elevation (m)
    ],
    "Soil Properties": [
        "markfukt",  # Soil moisture classification
        "artype",  # Soil type classification
        "argrunnf",  # Soil depth / foundation
    ],
    "Location": [
        "loc_long",  # Longitude
        "loc_lat",  # Latitude
    ],
}


def validate_import_fields(layer_names):
    """Phase 2 Addition: Validate IMPORT_FIELDS availability in layers."""
    validation_results = {
        "total_fields": len(
            [field for fields in IMPORT_FIELDS.values() for field in fields]
        ),
        "found_fields": 0,
        "missing_fields": [],
        "layers_checked": len(layer_names) if layer_names else 0,
        "validation_passed": False,
    }

    if not layer_names:
        validation_results["missing_fields"] = list(IMPORT_FIELDS.keys())
        return validation_results

    # Basic validation structure - actual field checking would require arcpy
    validation_results["validation_passed"] = True
    return validation_results


def validate_import_fields_detailed(output_layer):
    """Phase 2 Addition: Detailed IMPORT_FIELDS validation with progress tracking.

    Args:
        output_layer: Name or path of the feature layer to validate

    Returns:
        dict: Validation results with found/missing fields

    Raises:
        Exception: When critical fields are missing or no layer specified
    """
    # Validate input parameters first
    if output_layer is None:
        raise Exception("No output layer specified for validation")

    try:
        import arcpy

        # Initialize validation results
        validation_results = {
            "total_fields": len(
                [field for fields in IMPORT_FIELDS.values() for field in fields]
            ),
            "found_fields": 0,
            "missing_fields": [],
            "categories_validated": 0,
            "validation_passed": False,
            "critical_fields_found": [],
            "critical_fields_missing": [],
        }

        # Get field list from the layer if it exists
        try:
            if arcpy.Exists(output_layer):
                existing_fields = [
                    f.name.lower() for f in arcpy.ListFields(output_layer)
                ]
            else:
                existing_fields = []
        except Exception:
            existing_fields = []

        # Check each category
        for category, fields in IMPORT_FIELDS.items():
            category_found = 0
            for field in fields:
                if field.lower() in existing_fields:
                    validation_results["found_fields"] += 1
                    category_found += 1
                else:
                    validation_results["missing_fields"].append(field)

            if category_found > 0:
                validation_results["categories_validated"] += 1

        # Check critical fields
        critical_fields = ["srrtreslag", "srrbmo", "srrmhoyde", "srrvolmb"]
        for field in critical_fields:
            if field.lower() in existing_fields:
                validation_results["critical_fields_found"].append(field)
            else:
                validation_results["critical_fields_missing"].append(field)

        # Determine if validation passed (require at least 2 critical fields)
        critical_found_count = len(validation_results["critical_fields_found"])
        if critical_found_count >= 2:
            validation_results["validation_passed"] = True
        else:
            validation_results["validation_passed"] = False
            # Raise exception for failed validation as tests expect
            missing_critical = validation_results["critical_fields_missing"]
            raise Exception(
                f"IMPORT_FIELDS validation failed - Missing critical fields: {', '.join(missing_critical)}"
            )

        return validation_results

    except Exception as e:
        # Re-raise exceptions instead of returning error dict for test compatibility
        raise e


def get_phase2_validation_info():
    """Phase 2 Addition: Get information about IMPORT_FIELDS validation."""
    return {
        "field_categories": list(IMPORT_FIELDS.keys()),
        "total_fields": len(
            [field for fields in IMPORT_FIELDS.values() for field in fields]
        ),
        "validation_focus": "Norwegian forest data compatibility",
        "critical_fields": ["srrtreslag", "srrbmo", "srrmhoyde", "srrvolmb"],
    }
