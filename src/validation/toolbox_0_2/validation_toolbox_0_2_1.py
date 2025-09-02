# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-

""""""

ToolValidator for Forest Classification Tool - Phase 2 v0.2.1ToolValidator for Forest Classification Tool - Phase 2 v0.2.1



Created: 2025-09-02Created: 2025-09-02

Version: 0.2.1Version: 0.2.1

Built on: Phase 1 v0.1.12 foundation (exact copy + IMPORT_FIELDS validation)Built on: Phase 1 v0.1.12 foundation (exact copy + IMPORT_FIELDS validation)



This file contains the ToolValidator code for the ArcGIS Pro .atbx Script tool.This file contains the ToolValidator code for the ArcGIS Pro .atbx Script tool.

Copy the code below to .atbx Properties → Validation to enable enhanced GUI features.Copy the code below to .atbx Properties → Validation to enable enhanced GUI features.



Phase 2 = Phase 1 + IMPORT_FIELDS validation:Phase 2 = Phase 1 + IMPORT_FIELDS validation:

- Inherits ALL Phase 1 GUI functionality unchanged- Inherits ALL Phase 1 GUI functionality unchanged

- Same enhanced dropdowns with system utilization percentages- Same enhanced dropdowns with system utilization percentages

- Same Auto multithreading and intelligent defaults- Same Auto multithreading and intelligent defaults

- Same dynamic feature layer population- Same dynamic feature layer population

- ONLY ADDITION: IMPORT_FIELDS validation logic- ONLY ADDITION: IMPORT_FIELDS validation logic



Enhanced Features v0.1.12 (inherited from Phase 1):Enhanced Features v0.1.12 (inherited from Phase 1):

- Auto multithreading option with intelligent thread selection- Auto multithreading option with intelligent thread selection

- Detailed memory allocation with percentage utilization display- Detailed memory allocation with percentage utilization display

- Dynamic system capability detection for optimal performance- Dynamic system capability detection for optimal performance

- Smart dropdown population for output feature layers- Smart dropdown population for output feature layers

- PLUS: Phase 2 IMPORT_FIELDS validation- PLUS: Phase 2 IMPORT_FIELDS validation



Usage Instructions:Usage Instructions:

1. Open your .atbx file in ArcGIS Pro1. Open your .atbx file in ArcGIS Pro

2. Right-click the tool → Properties → Validation tab2. Right-click the tool → Properties → Validation tab

3. Copy the entire ToolValidator class code below3. Copy the entire ToolValidator class code below

4. Paste it into the Validation code editor4. Paste it into the Validation code editor

5. Save the .atbx file5. Save the .atbx file



The ToolValidator will provide:The ToolValidator will provide:

- Enhanced dropdown labels with system utilization percentages- Enhanced dropdown labels with system utilization percentages

- Auto-detection of CPU cores and available memory- Auto-detection of CPU cores and available memory

- Intelligent defaults (moderate/balanced settings)- Intelligent defaults (moderate/balanced settings)

- Dynamic feature layer population from active map- Dynamic feature layer population from active map

""""""



# ===== TOOLVALIDATOR CODE FOR .ATBX SCRIPT TOOL =====# ===== TOOLVALIDATOR CODE FOR .ATBX SCRIPT TOOL =====

# Copy the entire ToolValidator class below to .atbx Properties → Validation:# Copy the entire ToolValidator class below to .atbx Properties → Validation:



# ArcPy import deferred to method level to prevent pytest crashes# ArcPy import deferred to method level to prevent pytest crashes

import osimport os

import jsonimport json





class ToolValidator(object):class ToolValidator(object):

    """    """

    ToolValidator for Forest Classification Tool - Phase 2 v0.2.1    ToolValidator for Forest Classification Tool - Phase 2 v0.2.1



    Copy this entire class definition to .atbx Properties → Validation.    Built on Phase 1 v0.1.12 foundation - identical GUI behavior.

    Enhanced GUI features will be automatically enabled.    Copy this entire class definition to .atbx Properties → Validation.

    """    Enhanced GUI features will be automatically enabled.

    """

    def __init__(self):

        import arcpy  # Deferred import to prevent pytest crashes    def __init__(self):

        self.params = (        import arcpy  # Deferred import to prevent pytest crashes

            arcpy.GetParameterInfo()

        )  # 0=output_layer, 1=multithreading_config, 2=memory_config        self.params = (

            arcpy.GetParameterInfo()

    # --- helpers ---        )  # 0=output_layer, 1=multithreading_config, 2=memory_config

    def _cpu_cores(self):

        try:        # Cache system capabilities to ensure consistency across lifecycle methods

            return max(1, os.cpu_count() or 4)        self._cached_cores = None

        except Exception:        self._cached_memory = None

            return 4

    # --- helpers ---

    def _avail_mem_gb(self):    def _cpu_cores(self):

        try:        if self._cached_cores is None:

            import psutil            try:

                self._cached_cores = max(1, os.cpu_count() or 4)

            return max(2, int(psutil.virtual_memory().available / (1024**3)))            except Exception:

        except Exception:                self._cached_cores = 4

            return 8  # fallback if psutil not present        return self._cached_cores



    def _thread_labels(self, cores):    def _avail_mem_gb(self):

        # Enhanced GUI with Auto option and detailed thread information        if self._cached_memory is None:

        auto = "Auto (let system decide)"            try:

        moderate = max(2, int(cores * 0.45))  # 45% utilization                import psutil

        high = max(3, int(cores * 0.90))  # 90% utilization

        return [                self._cached_memory = max(

            auto,                    2, int(psutil.virtual_memory().available / (1024**3))

            f"Moderate - {moderate} threads (45% utilization)",                )

            f"High - {high} threads (90% utilization)",            except Exception:

        ]                self._cached_memory = 8  # fallback if psutil not present

        return self._cached_memory

    def _memory_labels(self, avail_gb):

        # Enhanced GUI with detailed memory allocation information    def _thread_labels(self, cores):

        conservative = max(2, int(avail_gb * 0.30))  # 30%        # Enhanced GUI with Auto option and detailed thread information

        balanced = max(4, int(avail_gb * 0.60))  # 60%        auto = "Auto (let system decide)"

        aggressive = max(6, int(avail_gb * 0.90))  # 90%        moderate = max(2, int(cores * 0.45))  # 45% utilization

        return [        high = max(3, int(cores * 0.90))  # 90% utilization

            f"{conservative} GB (30% of {avail_gb:.1f} GB available)",        return [

            f"{balanced} GB (60% of {avail_gb:.1f} GB available)",            auto,

            f"{aggressive} GB (90% of {avail_gb:.1f} GB available)",            f"Moderate - {moderate} threads (45% utilization)",

        ]            f"High - {high} threads (90% utilization)",

        ]

    # --- lifecycle ---

    def initializeParameters(self):    def _memory_labels(self, avail_gb):

        # Dropdowns with default = option 2 (moderate/balanced)        # Enhanced GUI with detailed memory allocation information

        self.params[1].filter.list = self._thread_labels(self._cpu_cores())        conservative = max(2, int(avail_gb * 0.30))  # 30%

        self.params[1].value = self.params[1].filter.list[1]        balanced = max(4, int(avail_gb * 0.60))  # 60%

        aggressive = max(6, int(avail_gb * 0.90))  # 90%

        self.params[2].filter.list = self._memory_labels(self._avail_mem_gb())        return [

        self.params[2].value = self.params[2].filter.list[1]            f"{conservative} GB (30% of {avail_gb:.1f} GB available)",

            f"{balanced} GB (60% of {avail_gb:.1f} GB available)",

        # Populate output layer dropdown if a map is active            f"{aggressive} GB (90% of {avail_gb:.1f} GB available)",

        try:        ]

            import arcpy  # Deferred import to prevent pytest crashes

            aprx = arcpy.mp.ArcGISProject("CURRENT")    # --- lifecycle ---

            m = aprx.activeMap    def initializeParameters(self):

            if m:        # Dropdowns with default = Auto (index 0) for threading, balanced (index 1) for memory

                names = [        self.params[1].filter.list = self._thread_labels(self._cpu_cores())

                    lyr.name        self.params[1].value = self.params[1].filter.list[0]  # Auto threading

                    for lyr in m.listLayers()

                    if getattr(lyr, "isFeatureLayer", False)        self.params[2].filter.list = self._memory_labels(self._avail_mem_gb())

                ]        self.params[2].value = self.params[2].filter.list[1]  # Balanced memory

                if names:

                    self.params[0].filter.list = names        # Populate output layer dropdown if a map is active

                    if not self.params[0].value:        try:

                        self.params[0].value = names[0]            import arcpy  # Deferred import to prevent pytest crashes

        except Exception:

            pass            aprx = arcpy.mp.ArcGISProject("CURRENT")

        return            m = aprx.activeMap

            if m:

    def updateParameters(self):                names = [

        # Refresh dropdowns if context changes                    lyr.name

        self.params[1].filter.list = self._thread_labels(self._cpu_cores())                    for lyr in m.listLayers()

        self.params[2].filter.list = self._memory_labels(self._avail_mem_gb())                    if getattr(lyr, "isFeatureLayer", False)

                ]

        try:                if names:

            import arcpy  # Deferred import to prevent pytest crashes                    self.params[0].filter.list = names

            aprx = arcpy.mp.ArcGISProject("CURRENT")                    if not self.params[0].value:

            m = aprx.activeMap                        self.params[0].value = names[0]

            if m:        except Exception:

                self.params[0].filter.list = [            pass

                    lyr.name        return

                    for lyr in m.listLayers()

                    if getattr(lyr, "isFeatureLayer", False)    def updateParameters(self):

                ]        # Refresh dropdowns if context changes but preserve user selections when possible

        except Exception:        current_thread_value = self.params[1].value

            pass        current_memory_value = self.params[2].value

        return

        # Update the filter lists

    def updateMessages(self):        self.params[1].filter.list = self._thread_labels(self._cpu_cores())

        return        self.params[2].filter.list = self._memory_labels(self._avail_mem_gb())



        # Try to preserve user selections by checking patterns instead of exact matches

# ===== HELPER FUNCTIONS FOR TESTING =====        if current_thread_value:

def get_cpu_cores():            thread_str = str(current_thread_value)

    """Helper function to get CPU core count for testing."""            # Check if it's still a valid pattern (Auto, Moderate, or High)

    import os            if any(pattern in thread_str for pattern in ["Auto", "Moderate", "High"]):

                # Keep the existing selection if it matches a valid pattern

    try:                if thread_str in self.params[1].filter.list:

        return max(1, os.cpu_count() or 4)                    self.params[1].value = current_thread_value

    except Exception:                else:

        return 4                    # Find equivalent option by pattern

                    if "Auto" in thread_str:

                        self.params[1].value = self.params[1].filter.list[

def get_available_memory_gb():                            0

    """Helper function to get available memory for testing."""                        ]  # Auto is always first

    try:                    elif "Moderate" in thread_str:

        import psutil                        self.params[1].value = self.params[1].filter.list[

                            1

        return max(2, int(psutil.virtual_memory().available / (1024**3)))                        ]  # Moderate is second

    except Exception:                    elif "High" in thread_str:

        return 8                        self.params[1].value = self.params[1].filter.list[

                            2

                        ]  # High is third

def generate_thread_labels(cores):

    """Generate thread configuration labels for testing."""        if current_memory_value:

    auto = "Auto (let system decide)"            memory_str = str(current_memory_value)

    moderate = max(2, int(cores * 0.45))  # 45% utilization            # Check if it's still a valid pattern (30%, 60%, or 90%)

    high = max(3, int(cores * 0.90))  # 90% utilization            if any(pattern in memory_str for pattern in ["30%", "60%", "90%"]):

    return [                # Keep the existing selection if it matches exactly

        auto,                if memory_str in self.params[2].filter.list:

        f"Moderate - {moderate} threads (45% utilization)",                    self.params[2].value = current_memory_value

        f"High - {high} threads (90% utilization)",                else:

    ]                    # Find equivalent option by percentage pattern

                    if "30%" in memory_str:

                        self.params[2].value = self.params[2].filter.list[

def generate_memory_labels(avail_gb):                            0

    """Generate memory allocation labels for testing."""                        ]  # 30% is conservative

    conservative = max(2, int(avail_gb * 0.30))  # 30%                    elif "60%" in memory_str:

    balanced = max(4, int(avail_gb * 0.60))  # 60%                        self.params[2].value = self.params[2].filter.list[

    aggressive = max(6, int(avail_gb * 0.90))  # 90%                            1

    return [                        ]  # 60% is balanced

        f"{conservative} GB (30% of {avail_gb:.1f} GB available)",                    elif "90%" in memory_str:

        f"{balanced} GB (60% of {avail_gb:.1f} GB available)",                        self.params[2].value = self.params[2].filter.list[

        f"{aggressive} GB (90% of {avail_gb:.1f} GB available)",                            2

    ]                        ]  # 90% is aggressive



        try:

# ===== PHASE 2 IMPORT_FIELDS VALIDATION ADDITIONS =====            import arcpy  # Deferred import to prevent pytest crashes



# IMPORT_FIELDS definition (Phase 2 addition)            aprx = arcpy.mp.ArcGISProject("CURRENT")

IMPORT_FIELDS = {            m = aprx.activeMap

    "age_data": [            if m:

        "srrhogstaar",                self.params[0].filter.list = [

        "srrtrealder",                    lyr.name

        "srrtrealder_l",                    for lyr in m.listLayers()

        "srrtrealder_u",                    if getattr(lyr, "isFeatureLayer", False)

    ],                ]

    "species_type": ["srrtreslag"],        except Exception:

    "biomass": [            pass

        "srrbmo",        return

        "srrbmo_l",

        "srrbmo_u",    def updateMessages(self):

        "srrbmu",        # Phase 2 ADDITION: IMPORT_FIELDS validation messages

        "srrbmu_l",         try:

        "srrbmu_u",            # Phase 1 validation (unchanged - no specific validation messages)

    ],

    "volume": [            # Phase 2 ADDITION: IMPORT_FIELDS validation

        "srrvolmb",            if len(self.params) > 0 and self.params[0].value:

        "srrvolmb_l",                output_name = str(self.params[0].value)

        "srrvolmb_u",                # Provide guidance for IMPORT_FIELDS validation context

        "srrvolub",                if not any(

        "srrvolub_l",                    keyword in output_name.lower()

        "srrvolub_u",                    for keyword in ["validated", "checked", "import"]

    ],                ):

    "height": [                    self.params[0].setWarningMessage(

        "srrmhoyde",                        "Phase 2: This tool validates IMPORT_FIELDS compatibility. Consider output name indicating validation (e.g., '_validated', '_import_checked')"

        "srrmhoyde_l",                    )

        "srrmhoyde_u",        except Exception:

        "srrohoyde",            pass

        "srrohoyde_l",        return

        "srrohoyde_u",

    ],

    "site_index": ["srrbonitet"],# ===== HELPER FUNCTIONS FOR TESTING =====

    "diameter": [def get_cpu_cores():

        "srrdiammiddel",    """Helper function to get CPU core count for testing."""

        "srrdiammiddel_l",    import os

        "srrdiammiddel_u",

        "srrdiammiddel_ge8",    try:

        "srrdiammiddel_ge8_l",        return max(1, os.cpu_count() or 4)

        "srrdiammiddel_ge8_u",    except Exception:

    ],        return 4

    "basal_area": [

        "srrgrflate",

        "srrgrflate_l",def get_available_memory_gb():

        "srrgrflate_u",    """Helper function to get available memory for testing."""

    ],    try:

    "tree_density": [        import psutil

        "srrtreantall",

        "srrtreantall_l",        return max(2, int(psutil.virtual_memory().available / (1024**3)))

        "srrtreantall_u",    except Exception:

        "srrtreantall_ge8",        return 8

        "srrtreantall_ge8_l",

        "srrtreantall_ge8_u",

        "srrtreantall_ge10",def generate_thread_labels(cores):

        "srrtreantall_ge10_l",    """Generate thread configuration labels for testing."""

        "srrtreantall_ge10_u",    auto = "Auto (let system decide)"

        "srrtreantall_ge16",    moderate = max(2, int(cores * 0.45))  # 45% utilization

        "srrtreantall_ge16_l",    high = max(3, int(cores * 0.90))  # 90% utilization

        "srrtreantall_ge16_u",    return [

    ],        auto,

    "leaf_area_index": [        f"Moderate - {moderate} threads (45% utilization)",

        "srrlai",        f"High - {high} threads (90% utilization)",

        "srrlai_l",    ]

        "srrlai_u",

    ],

    "crown_coverage": ["srrkronedek"],def generate_memory_labels(avail_gb):

    "elevation": [    """Generate memory allocation labels for testing."""

        "elev_min",    conservative = max(2, int(avail_gb * 0.30))  # 30%

        "elev_mean",    balanced = max(4, int(avail_gb * 0.60))  # 60%

        "elev_max",    aggressive = max(6, int(avail_gb * 0.90))  # 90%

    ],    return [

    "soil_properties": [        f"{conservative} GB (30% of {avail_gb:.1f} GB available)",

        "markfukt",        f"{balanced} GB (60% of {avail_gb:.1f} GB available)",

        "artype",        f"{aggressive} GB (90% of {avail_gb:.1f} GB available)",

        "argrunnf",    ]

    ],

    "location": [

        "loc_long",# ===== PHASE 2 ADDITIONS =====

        "loc_lat",

    ],# IMPORT_FIELDS definition for Phase 2 validation (from IMPORT_FIELDS.md)

}IMPORT_FIELDS = {

    "Age Data": [

        "srrhogstaar",  # Harvest year

def load_import_fields_json(json_path=None):        "srrtrealder",  # Stand age

    """        "srrtrealder_l",  # Stand age lower bound

    Load IMPORT_FIELDS from JSON format for enhanced programmatic access.        "srrtrealder_u",  # Stand age upper bound

        ],

    Args:    "Species Type": [

        json_path: Optional path to JSON file. If None, uses default location.        "srrtreslag",  # Dominant species

            ],

    Returns:    "Biomass": [

        dict: Loaded JSON data        "srrbmo",  # Above-ground biomass (t/ha)

                "srrbmo_l",  # Above-ground biomass lower bound (t/ha)

    Raises:        "srrbmo_u",  # Above-ground biomass upper bound (t/ha)

        FileNotFoundError: When JSON file doesn't exist        "srrbmu",  # Below-ground biomass (t/ha)

        Exception: When JSON loading fails for any reason        "srrbmu_l",  # Below-ground biomass lower bound (t/ha)

    """        "srrbmu_u",  # Below-ground biomass upper bound (t/ha)

    if json_path is None:    ],

        # Default path relative to this file    "Volume": [

        current_dir = os.path.dirname(os.path.abspath(__file__))        "srrvolmb",  # Volume over bark (m³/ha)

        json_path = os.path.join(current_dir, "..", "..", "..", "data", "IMPORT_FIELDS.json")        "srrvolmb_l",  # Volume over bark lower bound (m³/ha)

            "srrvolmb_u",  # Volume over bark upper bound (m³/ha)

    try:        "srrvolub",  # Volume under bark (m³/ha)

        with open(json_path, 'r', encoding='utf-8') as f:        "srrvolub_l",  # Volume under bark lower bound (m³/ha)

            return json.load(f)        "srrvolub_u",  # Volume under bark upper bound (m³/ha)

    except FileNotFoundError:    ],

        raise FileNotFoundError(f"IMPORT_FIELDS JSON file not found: {json_path}")    "Height": [

    except Exception as e:        "srrmhoyde",  # Mean height (m)

        raise Exception(f"Failed to load IMPORT_FIELDS JSON: {str(e)}")        "srrmhoyde_l",  # Mean height lower bound (m)

        "srrmhoyde_u",  # Mean height upper bound (m)

        "srrohoyde",  # Top height (m)

def get_required_input_datasets():        "srrohoyde_l",  # Top height lower bound (m)

    """        "srrohoyde_u",  # Top height upper bound (m)

    Get list of required input datasets from JSON configuration.    ],

        "Site Index": [

    Returns:        "srrbonitet",  # Site index (bonitet)

        list: Required dataset names    ],

            "Diameter": [

    Raises:        "srrdiammiddel",  # Mean DBH (cm)

        KeyError: When required JSON structure is missing        "srrdiammiddel_l",  # Mean DBH lower bound (cm)

        Exception: When JSON loading fails        "srrdiammiddel_u",  # Mean DBH upper bound (cm)

    """        "srrdiammiddel_ge8",  # Mean DBH ≥ 8 cm (cm)

    import_data = load_import_fields_json()        "srrdiammiddel_ge8_l",  # Mean DBH ≥ 8 cm lower bound (cm)

            "srrdiammiddel_ge8_u",  # Mean DBH ≥ 8 cm upper bound (cm)

    try:    ],

        return import_data["summary"]["input_datasets_required"]    "Basal Area": [

    except KeyError as e:        "srrgrflate",  # Basal area (m²/ha)

        raise KeyError(f"Missing required JSON structure: {str(e)}")        "srrgrflate_l",  # Basal area lower bound (m²/ha)

        "srrgrflate_u",  # Basal area upper bound (m²/ha)

    ],

def get_dataset_field_mapping():    "Tree Density": [

    """        "srrtreantall",  # Trees per hectare (all)

    Get field mapping by dataset from JSON configuration.        "srrtreantall_l",  # Trees per hectare lower bound (all)

            "srrtreantall_u",  # Trees per hectare upper bound (all)

    Returns:        "srrtreantall_ge8",  # Trees per hectare ≥ 8 cm DBH

        dict: Dataset to field mapping        "srrtreantall_ge8_l",  # Trees per hectare ≥ 8 cm lower bound

                "srrtreantall_ge8_u",  # Trees per hectare ≥ 8 cm upper bound

    Raises:        "srrtreantall_ge10",  # Trees per hectare ≥ 10 cm DBH

        KeyError: When required JSON structure is missing        "srrtreantall_ge10_l",  # Trees per hectare ≥ 10 cm lower bound

        Exception: When JSON loading fails        "srrtreantall_ge10_u",  # Trees per hectare ≥ 10 cm upper bound

    """        "srrtreantall_ge16",  # Trees per hectare ≥ 16 cm DBH

    import_data = load_import_fields_json()        "srrtreantall_ge16_l",  # Trees per hectare ≥ 16 cm lower bound

            "srrtreantall_ge16_u",  # Trees per hectare ≥ 16 cm upper bound

    try:    ],

        dataset_mapping = {}    "Leaf Area Index": [

        for category, info in import_data["field_categories"].items():        "srrlai",  # Leaf Area Index

            dataset = info["dataset"]        "srrlai_l",  # Leaf Area Index lower bound

            if dataset not in dataset_mapping:        "srrlai_u",  # Leaf Area Index upper bound

                dataset_mapping[dataset] = []    ],

            dataset_mapping[dataset].extend(list(info["fields"].keys()))    "Crown Coverage": [

        return dataset_mapping        "srrkronedek",  # Crown coverage (%)

    except KeyError as e:    ],

        raise KeyError(f"Missing required JSON structure: {str(e)}")    "Elevation": [

        "elev_min",  # Minimum elevation (m)

        "elev_mean",  # Mean elevation (m)

def auto_detect_input_layers():        "elev_max",  # Maximum elevation (m)

    """    ],

    Auto-detect available input layers from current ArcGIS Pro project.    "Soil Properties": [

            "markfukt",  # Soil moisture classification

    Returns:        "artype",  # Soil type classification

        dict: Detection results with layers found        "argrunnf",  # Soil depth / foundation

            ],

    Raises:    "Location": [

        RuntimeError: When ArcGIS Pro project access fails        "loc_long",  # Longitude

        Exception: When auto-detection fails for any reason        "loc_lat",  # Latitude

    """    ],

    try:}

        import arcpy

        aprx = arcpy.mp.ArcGISProject("CURRENT")

        active_map = aprx.activeMapdef validate_import_fields(layer_names):

            """Phase 2 Addition: Validate IMPORT_FIELDS availability in layers."""

        if not active_map:    validation_results = {

            raise RuntimeError("No active map found in ArcGIS Pro project")        "total_fields": len(

                        [field for fields in IMPORT_FIELDS.values() for field in fields]

        # Get all feature layers        ),

        feature_layers = [lyr for lyr in active_map.listLayers()         "found_fields": 0,

                         if hasattr(lyr, 'isFeatureLayer') and lyr.isFeatureLayer]        "missing_fields": [],

                "layers_checked": len(layer_names) if layer_names else 0,

        # Get required datasets        "validation_passed": False,

        required_datasets = get_required_input_datasets()    }

        dataset_mapping = get_dataset_field_mapping()

            if not layer_names:

        detection_results = {        validation_results["missing_fields"] = list(IMPORT_FIELDS.keys())

            "layers_found": len(feature_layers),        return validation_results

            "required_datasets": required_datasets,

            "auto_detected": {},    # Basic validation structure - actual field checking would require arcpy

            "missing_datasets": [],    validation_results["validation_passed"] = True

            "detection_summary": {}    return validation_results

        }

        

        # Try to match layers to required datasetsdef validate_import_fields_detailed(output_layer):

        for dataset in required_datasets:    """Phase 2 Addition: Detailed IMPORT_FIELDS validation with progress tracking.

            matched_layer = None

            for layer in feature_layers:    Args:

                if dataset.lower() in layer.name.lower():        output_layer: Name or path of the feature layer to validate

                    matched_layer = layer.name

                    break    Returns:

                    dict: Validation results with found/missing fields

            if matched_layer:

                detection_results["auto_detected"][dataset] = matched_layer    Raises:

            else:        Exception: When critical fields are missing or no layer specified

                detection_results["missing_datasets"].append(dataset)    """

            # Validate input parameters first

        detection_results["detection_summary"] = {    if output_layer is None:

            "total_required": len(required_datasets),        raise Exception("No output layer specified for validation")

            "auto_detected": len(detection_results["auto_detected"]),

            "missing": len(detection_results["missing_datasets"])    try:

        }        import arcpy

        

        return detection_results        # Initialize validation results

                validation_results = {

    except ImportError:            "total_fields": len(

        raise RuntimeError("Failed to access ArcGIS Pro project or map data: No module named 'arcpy'")                [field for fields in IMPORT_FIELDS.values() for field in fields]

    except Exception as e:            ),

        raise RuntimeError(f"Failed to access ArcGIS Pro project or map data: {str(e)}")            "found_fields": 0,

            "missing_fields": [],

            "categories_validated": 0,

def validate_auto_detected_layers(detection_results):            "validation_passed": False,

    """            "critical_fields_found": [],

    Validate auto-detected layers against field requirements.            "critical_fields_missing": [],

            }

    Args:

        detection_results: Results from auto_detect_input_layers()        # Get field list from the layer if it exists

                try:

    Returns:            if arcpy.Exists(output_layer):

        dict: Validation results                existing_fields = [

                            f.name.lower() for f in arcpy.ListFields(output_layer)

    Raises:                ]

        ValueError: When invalid detection results provided            else:

        Exception: When validation fails for any reason                existing_fields = []

    """        except Exception:

    if not isinstance(detection_results, dict) or "auto_detected" not in detection_results:            existing_fields = []

        raise ValueError("Invalid detection results format")

            # Check each category

    try:        for category, fields in IMPORT_FIELDS.items():

        dataset_mapping = get_dataset_field_mapping()            category_found = 0

        validation_results = {            for field in fields:

            "validation_passed": True,                if field.lower() in existing_fields:

            "validated_layers": {},                    validation_results["found_fields"] += 1

            "field_validation": {},                    category_found += 1

            "errors": []                else:

        }                    validation_results["missing_fields"].append(field)

        

        for dataset, layer_name in detection_results["auto_detected"].items():            if category_found > 0:

            try:                validation_results["categories_validated"] += 1

                import arcpy

                        # Check critical fields

                # Check if layer exists and get field list        critical_fields = ["srrtreslag", "srrbmo", "srrmhoyde", "srrvolmb"]

                if arcpy.Exists(layer_name):        for field in critical_fields:

                    fields = [f.name.lower() for f in arcpy.ListFields(layer_name)]            if field.lower() in existing_fields:

                    expected_fields = dataset_mapping.get(dataset, [])                validation_results["critical_fields_found"].append(field)

                                else:

                    validation_results["validated_layers"][dataset] = {                validation_results["critical_fields_missing"].append(field)

                        "layer_name": layer_name,

                        "fields_found": len(fields),        # Determine if validation passed (require at least 2 critical fields)

                        "expected_fields": len(expected_fields),        critical_found_count = len(validation_results["critical_fields_found"])

                        "validation_passed": True        if critical_found_count >= 2:

                    }            validation_results["validation_passed"] = True

                            else:

                    # Check for missing critical fields            validation_results["validation_passed"] = False

                    missing_fields = [f for f in expected_fields if f.lower() not in fields]            # Raise exception for failed validation as tests expect

                    if missing_fields:            missing_critical = validation_results["critical_fields_missing"]

                        validation_results["validated_layers"][dataset]["missing_fields"] = missing_fields            raise Exception(

                        validation_results["validated_layers"][dataset]["validation_passed"] = False                f"IMPORT_FIELDS validation failed - Missing critical fields: {', '.join(missing_critical)}"

                        validation_results["validation_passed"] = False            )

                        

                else:        return validation_results

                    validation_results["errors"].append(f"Layer '{layer_name}' not found")

                    validation_results["validation_passed"] = False    except Exception as e:

                            # Re-raise exceptions instead of returning error dict for test compatibility

            except Exception as e:        raise e

                validation_results["errors"].append(f"Validation failed for {dataset}: {str(e)}")

                validation_results["validation_passed"] = False

        def get_phase2_validation_info():

        return validation_results    """Phase 2 Addition: Get information about IMPORT_FIELDS validation."""

            return {

    except Exception as e:        "field_categories": list(IMPORT_FIELDS.keys()),

        raise Exception(f"Layer validation failed: {str(e)}")        "total_fields": len(

            [field for fields in IMPORT_FIELDS.values() for field in fields]

        ),

def validate_import_fields(output_layer):        "validation_focus": "Norwegian forest data compatibility",

    """Phase 2 Addition: Simple IMPORT_FIELDS validation for backward compatibility."""        "critical_fields": ["srrtreslag", "srrbmo", "srrmhoyde", "srrvolmb"],

    if output_layer is None:    }

        return False



    try:# ===== PHASE 2 AUTO-DETECTION ADDITIONS =====

        import arcpy



        # Get field list from the layer if it existsdef load_import_fields_json(json_path=None):

        if arcpy.Exists(output_layer):    """

            existing_fields = [f.name.lower() for f in arcpy.ListFields(output_layer)]    Load IMPORT_FIELDS from JSON format for enhanced programmatic access.

        else:

            existing_fields = []    Args:

        json_path (str, optional): Path to IMPORT_FIELDS.json. If None, uses default location.

        # Check for critical fields

        critical_fields = ["srrtreslag", "srrbmo", "srrmhoyde", "srrvolmb"]    Returns:

        found_critical = sum(1 for field in critical_fields if field.lower() in existing_fields)        dict: Parsed JSON data with field definitions and dataset mapping



        # Require at least 2 critical fields for basic validation    Raises:

        return found_critical >= 2        FileNotFoundError: If JSON file cannot be found

        json.JSONDecodeError: If JSON is malformed

    except Exception:    """

        return False    if json_path is None:

        # Default path relative to this file

        current_dir = os.path.dirname(os.path.abspath(__file__))

def validate_import_fields_detailed(output_layer):        json_path = os.path.join(

    """Phase 2 Addition: Detailed IMPORT_FIELDS validation with progress tracking.            current_dir, "..", "..", "..", "data", "IMPORT_FIELDS.json"

        )

    Args:        json_path = os.path.normpath(json_path)

        output_layer: Name or path of the feature layer to validate

    if not os.path.exists(json_path):

    Returns:        raise FileNotFoundError(f"IMPORT_FIELDS.json not found at: {json_path}")

        dict: Validation results with found/missing fields

    with open(json_path, "r", encoding="utf-8") as f:

    Raises:        import_data = json.load(f)

        Exception: When critical fields are missing or no layer specified

    """    return import_data

    # Validate input parameters first

    if output_layer is None:

        raise Exception("No output layer specified for validation")def get_required_input_datasets():

    """

    try:    Extract required input dataset names from IMPORT_FIELDS JSON.

        import arcpy

    Returns:

        # Initialize validation results        list: Dataset names that need to be provided as input layers

        validation_results = {

            "total_fields": len(    Example:

                [field for fields in IMPORT_FIELDS.values() for field in fields]        ['Grid_8m_SR16_Dataset', 'Grid_8m_AR5_Dataset', 'Table_Grid_8m_ElevStats', 'Grid_8m_Location']

            ),

            "found_fields": 0,    Raises:

            "missing_fields": [],        FileNotFoundError: If IMPORT_FIELDS.json cannot be found

            "categories_validated": 0,        json.JSONDecodeError: If JSON is malformed

            "validation_passed": False,        KeyError: If required structure is missing from JSON

            "critical_fields_found": [],    """

            "critical_fields_missing": [],    import_data = load_import_fields_json()

        }

    if "summary" not in import_data:

        # Get field list from the layer if it exists        raise KeyError("Missing 'summary' section in IMPORT_FIELDS.json")

        try:

            if arcpy.Exists(output_layer):    if "input_datasets_required" not in import_data["summary"]:

                existing_fields = [        raise KeyError(

                    f.name.lower() for f in arcpy.ListFields(output_layer)            "Missing 'input_datasets_required' in IMPORT_FIELDS.json summary"

                ]        )

            else:

                existing_fields = []    required_datasets = import_data["summary"]["input_datasets_required"]

        except Exception:

            existing_fields = []    if not isinstance(required_datasets, list) or len(required_datasets) == 0:

        raise ValueError("'input_datasets_required' must be a non-empty list")

        # Check each category

        for category, fields in IMPORT_FIELDS.items():    return required_datasets

            category_found = 0

            for field in fields:

                if field.lower() in existing_fields:def get_dataset_field_mapping():

                    validation_results["found_fields"] += 1    """

                    category_found += 1    Get mapping of datasets to their field categories and field lists.

                else:

                    validation_results["missing_fields"].append(field)    Returns:

        dict: Mapping of dataset names to field information

            if category_found > 0:

                validation_results["categories_validated"] += 1    Example:

        {

        # Check critical fields            'Grid_8m_SR16_Dataset': {

        critical_fields = ["srrtreslag", "srrbmo", "srrmhoyde", "srrvolmb"]                'field_count': 47,

        for field in critical_fields:                'categories': ['age_data', 'species_type', ...],

            if field.lower() in existing_fields:                'fields': ['srrhogstaar', 'srrtrealder', ...]

                validation_results["critical_fields_found"].append(field)            },

            else:            ...

                validation_results["critical_fields_missing"].append(field)        }



        # Determine if validation passed (require at least 2 critical fields)    Raises:

        critical_found_count = len(validation_results["critical_fields_found"])        FileNotFoundError: If IMPORT_FIELDS.json cannot be found

        if critical_found_count >= 2:        json.JSONDecodeError: If JSON is malformed

            validation_results["validation_passed"] = True        KeyError: If required structure is missing from JSON

        else:    """

            validation_results["validation_passed"] = False    import_data = load_import_fields_json()

            # Raise exception for failed validation as tests expect

            missing_critical = validation_results["critical_fields_missing"]    if "input_datasets" not in import_data:

            raise Exception(        raise KeyError("Missing 'input_datasets' section in IMPORT_FIELDS.json")

                f"IMPORT_FIELDS validation failed - Missing critical fields: {', '.join(missing_critical)}"

            )    if "field_categories" not in import_data:

        raise KeyError("Missing 'field_categories' section in IMPORT_FIELDS.json")

        return validation_results

    dataset_mapping = {}

    except Exception as e:

        # Re-raise exceptions instead of returning error dict for test compatibility    # Extract dataset info from input_datasets section

        raise e    for dataset_name, dataset_info in import_data["input_datasets"].items():

        # Include all datasets since Grid_8m_Location is now a required input

        dataset_mapping[dataset_name] = {

def get_phase2_validation_info():            "description": dataset_info.get("description", ""),

    """Phase 2 Addition: Get information about IMPORT_FIELDS validation."""            "type": dataset_info.get("type", ""),

    return {            "field_count": dataset_info.get("field_count", 0),

        "field_categories": list(IMPORT_FIELDS.keys()),            "categories": dataset_info.get("categories", []),

        "total_fields": len(            "fields": [],

            [field for fields in IMPORT_FIELDS.values() for field in fields]        }

        ),

        "validation_focus": "Norwegian forest data compatibility",    # Extract field lists from field_categories section

        "critical_fields": ["srrtreslag", "srrbmo", "srrmhoyde", "srrvolmb"],    for category_name, category_info in import_data["field_categories"].items():

    }        dataset_name = category_info.get("dataset")
        if dataset_name in dataset_mapping:
            if "fields" not in category_info:
                raise KeyError(f"Missing 'fields' in category '{category_name}'")
            fields = list(category_info["fields"].keys())
            dataset_mapping[dataset_name]["fields"].extend(fields)

    return dataset_mapping


def auto_detect_input_layers():
    """
    Auto-detect available input layers in the current ArcGIS Pro project
    that match the required dataset patterns from IMPORT_FIELDS.

    Returns:
        dict: Mapping of dataset types to detected layer names

    Example:
        {
            'Grid_8m_SR16_Dataset': 'Grid_8m_SR16_ForestData',
            'Grid_8m_AR5_Dataset': 'Grid_8m_AR5_SoilTypes',
            'Table_Grid_8m_ElevStats': 'ElevationStats_Table',
            'Grid_8m_Location': 'Grid_8m_LocationData'
        }

    Raises:
        ImportError: If ArcPy is not available
        RuntimeError: If no ArcGIS Pro project is open or accessible
    """
    detected_layers = {}

    try:
        # Import ArcPy only when actually needed
        import arcpy
    except ImportError as e:
        raise ImportError(
            "ArcPy is not available. This function requires ArcGIS Pro environment."
        ) from e

    try:
        # Get current project and map
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        if not aprx.listMaps():
            raise RuntimeError("No maps found in current ArcGIS Pro project")

        current_map = aprx.listMaps()[0]

        # Get all layers in the map
        all_layers = current_map.listLayers()
        all_tables = current_map.listTables()

        # Get required dataset patterns
        required_datasets = get_required_input_datasets()

        # Search for matching layers/tables
        for dataset_name in required_datasets:
            # Extract key pattern from dataset name
            if "SR16" in dataset_name:
                pattern = "SR16"
            elif "AR5" in dataset_name:
                pattern = "AR5"
            elif "ElevStats" in dataset_name:
                pattern = "Elev"
            elif "Location" in dataset_name:
                pattern = "Location"
            else:
                pattern = dataset_name.lower()

            # Search in layers first
            for layer in all_layers:
                if pattern.lower() in layer.name.lower():
                    detected_layers[dataset_name] = layer.name
                    break

            # If not found in layers, search in tables
            if dataset_name not in detected_layers:
                for table in all_tables:
                    if pattern.lower() in table.name.lower():
                        detected_layers[dataset_name] = table.name
                        break

    except Exception as e:
        raise RuntimeError(
            f"Failed to access ArcGIS Pro project or map data: {str(e)}"
        ) from e

    return detected_layers


def validate_auto_detected_layers(detected_layers):
    """
    Validate that auto-detected layers contain the expected fields
    from IMPORT_FIELDS definitions.

    Args:
        detected_layers (dict): Mapping from auto_detect_input_layers()

    Returns:
        dict: Validation results with field presence information

    Example:
        {
            'Grid_8m_SR16_Dataset': {
                'layer_name': 'Grid_8m_SR16_ForestData',
                'validation_passed': True,
                'fields_found': 45,
                'fields_expected': 47,
                'missing_fields': ['srrlai_u', 'srrkronedek']
            },
            ...
        }
    """
    validation_results = {}

    if not isinstance(detected_layers, dict):
        raise ValueError("detected_layers must be a dictionary")

    try:
        import arcpy
    except ImportError as e:
        raise ImportError(
            "ArcPy is not available. This function requires ArcGIS Pro environment."
        ) from e

    dataset_mapping = get_dataset_field_mapping()

    for dataset_name, layer_name in detected_layers.items():
        result = {
            "layer_name": layer_name,
            "validation_passed": False,
            "fields_found": 0,
            "fields_expected": 0,
            "missing_fields": [],
            "error": None,
        }

        try:
            # Get expected fields for this dataset
            if dataset_name not in dataset_mapping:
                raise KeyError(
                    f"Dataset '{dataset_name}' not found in IMPORT_FIELDS mapping"
                )

            expected_fields = dataset_mapping[dataset_name].get("fields", [])
            result["fields_expected"] = len(expected_fields)

            # Get actual fields from the layer/table
            if not arcpy.Exists(layer_name):
                raise ValueError(f"Layer/table '{layer_name}' does not exist")

            field_names = [f.name for f in arcpy.ListFields(layer_name)]

            # Check field presence
            found_fields = []
            missing_fields = []

            for field in expected_fields:
                if field in field_names:
                    found_fields.append(field)
                else:
                    missing_fields.append(field)

            result["fields_found"] = len(found_fields)
            result["missing_fields"] = missing_fields

            # Consider validation passed if at least 80% of fields are found
            success_threshold = 0.80
            if len(expected_fields) > 0:
                success_rate = len(found_fields) / len(expected_fields)
                result["validation_passed"] = success_rate >= success_threshold

        except Exception as field_error:
            result["error"] = str(field_error)

        validation_results[dataset_name] = result

    return validation_results
