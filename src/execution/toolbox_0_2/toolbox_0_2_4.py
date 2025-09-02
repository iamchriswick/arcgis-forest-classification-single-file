# -*- coding: utf-8 -*-
"""
Forest Classification Tool - Phase 2: Core Data Processing v0.2.4

Created: 2025-08-29 11:30
Version: 0.2.4

Phase 2 Features:
- All Phase 1 features (basic toolbox structure, parameters, system detection)
- Basic data reading capabilities (scan fields, read feature data)
- Simple field management (field existence checking, basic type validation)
- Single-threaded data processing with progress tracking (0-100%)
- Error handling for missing files and basic data access issues
- CUD (Create, Update, Delete) operations for field management

Phase 2 Focus:
- Implement basic data reading capabilities
- Add simple field management
- Single-threaded data processing
- Basic field reading and writing
- Simple progress tracking (0-100%)
- Error handling for missing files
- CUD operations on existing feature layers

This is Phase 2 of a 13-phase incremental development strategy.
Developed as part of the Single File Development Strategy for ArcGIS Pro Forest Classification Tool.

For ArcGIS Pro .atbx Script tools, the script executes at module level when called.
ToolValidator dropdown UI is controlled by the .atbx Properties → Validation.

Version History:
Phase 2 Change Log:
- v0.2.4: Implemented proper CUD (Create, Update, Delete) field operations for existing layers
- v0.2.3: Fixed parameter alignment with .atbx tool (3 params: output, thread, memory)
- v0.2.2: Added main() function for .atbx Script tool execution
- v0.2.1: Initial Phase 2 implementation with basic data processing capabilities
"""

import arcpy


def get_system_capabilities():
    """Get system capabilities for thread and memory configuration."""
    try:
        import psutil

        # Get system capabilities
        cpu_count = psutil.cpu_count(logical=True) or 4
        memory_gb = (
            round(psutil.virtual_memory().total / (1024**3))
            if psutil.virtual_memory()
            else 8
        )

        # Apply 90% max utilization rule
        max_threads = max(1, int(cpu_count * 0.9))
        max_memory_gb = max(1, int(memory_gb * 0.9))

        return {
            "cpu_count": cpu_count,
            "memory_gb": memory_gb,
            "max_threads": max_threads,
            "max_memory_gb": max_memory_gb,
        }
    except ImportError:
        return {"cpu_count": 4, "memory_gb": 8, "max_threads": 3, "max_memory_gb": 7}
    except Exception:
        return {"cpu_count": 4, "memory_gb": 8, "max_threads": 3, "max_memory_gb": 7}


def get_field_info(feature_layer):
    """Get basic information about fields in a feature layer.

    Args:
        feature_layer: Path to feature layer or layer object

    Returns:
        dict: Field information including names, types, and properties
    """
    try:
        fields = arcpy.ListFields(feature_layer)
        field_info = {}

        for field in fields:
            field_info[field.name] = {
                "type": field.type,
                "length": getattr(field, "length", None),
                "alias": getattr(field, "aliasName", field.name),
                "editable": getattr(field, "editable", True),
            }

        arcpy.AddMessage(f"📋 Found {len(field_info)} fields in layer")
        return field_info

    except Exception as e:
        arcpy.AddError(f"❌ Error reading field information: {e}")
        return {}


def validate_layer_exists(layer_path):
    """Validate that a layer exists and is accessible.

    Args:
        layer_path: Path to the layer to validate

    Returns:
        bool: True if layer exists and is accessible, False otherwise
    """
    try:
        if arcpy.Exists(layer_path):
            # Try to describe the layer to ensure it's accessible
            desc = arcpy.Describe(layer_path)
            arcpy.AddMessage(f"✅ Layer validated: {desc.dataType} at '{layer_path}'")
            return True
        else:
            arcpy.AddError(
                f"❌ Input Feature Layer not found: '{layer_path}' (during layer validation)"
            )
            arcpy.AddError(f"📍 Full path attempted: {layer_path}")
            return False

    except Exception as e:
        arcpy.AddError(f"❌ Error validating layer '{layer_path}': {e}")
        arcpy.AddError(f"📍 Full path attempted: {layer_path}")
        return False


def get_feature_count(feature_layer):
    """Get the number of features in a layer.

    Args:
        feature_layer: Path to feature layer or layer object

    Returns:
        int: Number of features, or 0 if error
    """
    try:
        result = arcpy.GetCount_management(feature_layer)
        count = int(result.getOutput(0))
        arcpy.AddMessage(f"📊 Feature count: {count:,}")
        return count

    except Exception as e:
        arcpy.AddError(f"❌ Error getting feature count: {e}")
        return 0


def read_sample_features(feature_layer, sample_size=5):
    """Read a small sample of features for basic data processing demonstration.

    Args:
        feature_layer: Path to feature layer or layer object
        sample_size: Number of features to sample (default 5)

    Returns:
        list: Sample of feature data as dictionaries
    """
    try:
        sample_data = []

        # Get field names (excluding system fields)
        fields = arcpy.ListFields(feature_layer)
        data_fields = [f.name for f in fields if f.type not in ["OID", "Geometry"]]

        if not data_fields:
            arcpy.AddMessage("ℹ️  No data fields found for sampling")
            return sample_data

        # Read sample features
        with arcpy.da.SearchCursor(feature_layer, data_fields) as cursor:
            for i, row in enumerate(cursor):
                if i >= sample_size:
                    break

                feature_data = {field: row[j] for j, field in enumerate(data_fields)}
                sample_data.append(feature_data)

        arcpy.AddMessage(f"📖 Read {len(sample_data)} sample features")
        return sample_data

    except Exception as e:
        arcpy.AddError(f"❌ Error reading sample features: {e}")
        return []


def process_layer_basic(feature_layer, progress_callback=None):
    """Perform basic data processing on a feature layer.

    Args:
        feature_layer: Path to feature layer or layer object
        progress_callback: Optional function to call with progress updates

    Returns:
        dict: Processing results and statistics
    """
    # Initialize results dictionary outside try block
    results = {
        "layer_path": str(feature_layer),
        "field_count": 0,
        "feature_count": 0,
        "sample_data": [],
        "processing_successful": False,
    }

    try:
        # Step 1: Validate layer (5% progress)
        if progress_callback:
            progress_callback(5, "Starting layer validation...")

        if not validate_layer_exists(feature_layer):
            return results

        # Step 2: Initial field scan (15% progress)
        if progress_callback:
            progress_callback(15, "Scanning layer fields...")

        field_info = get_field_info(feature_layer)
        results["field_count"] = len(field_info)
        results["field_info"] = field_info

        # Step 3: Feature counting (35% progress)
        if progress_callback:
            progress_callback(35, "Counting features in layer...")

        feature_count = get_feature_count(feature_layer)
        results["feature_count"] = feature_count

        # Step 4: Sample data reading (60% progress)
        if progress_callback:
            progress_callback(60, "Reading sample feature data...")

        sample_data = read_sample_features(feature_layer, sample_size=5)
        results["sample_data"] = sample_data

        # Step 5: Data validation (80% progress)
        if progress_callback:
            progress_callback(80, "Validating data quality...")

        # Basic data quality checks
        data_quality = {
            "has_geometry": True,  # Assume true for basic implementation
            "has_null_values": any(
                None in row.values() if isinstance(row, dict) else False
                for row in sample_data
            ),
            "sample_size": len(sample_data),
        }
        results["data_quality"] = data_quality

        # Step 6: Complete processing (100% progress)
        if progress_callback:
            progress_callback(100, "Data processing complete!")

        results["processing_successful"] = True
        arcpy.AddMessage("✅ Basic layer processing completed successfully")

        return results

    except Exception as e:
        arcpy.AddError(f"❌ Error in basic layer processing: {e}")
        results["processing_successful"] = False
        return results


class ForestClassificationToolbox(object):
    """Forest Classification Toolbox for ArcGIS Pro."""

    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Forest Classification Toolbox - Phase 2"
        self.alias = "ForestClassificationPhase2"
        self.description = "Phase 2: Core Data Processing - Basic data reading and field management capabilities"

        # List of tool classes associated with this toolbox
        self.tools = [ForestClassificationTool]


class ForestClassificationTool(object):
    """Forest Classification Tool - Phase 2 Implementation

    Basic tool structure for ArcGIS Pro .atbx Script tools with core data processing.
    Parameter UI (dropdowns) are controlled by the .atbx ToolValidator.
    """

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Forest Classification Tool"
        self.description = (
            "Phase 2: Core Data Processing with basic field management and data reading"
        )
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions for .atbx Script tool."""
        # Phase 2.3: 3 parameters (no input layer - uses predefined data sources)

        # Output Feature Layer
        output_layer = arcpy.Parameter(
            displayName="Output Feature Layer",
            name="output_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Output",
        )

        # Thread Count (enhanced dropdown from Phase 1)
        thread_count = arcpy.Parameter(
            displayName="Thread Count",
            name="thread_count",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
        )
        thread_count.value = "Auto (Recommended)"

        # Memory Allocation (enhanced dropdown from Phase 1)
        memory_allocation = arcpy.Parameter(
            displayName="Memory Allocation",
            name="memory_allocation",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
        )
        memory_allocation.value = "Auto (Recommended)"

        # Phase 2.3: Return only 3 parameters (no input layer needed)
        return [output_layer, thread_count, memory_allocation]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal validation."""
        pass

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool parameter."""
        pass

    def execute(self, parameters, messages):
        """Execute method with basic data processing capabilities."""
        try:
            # Log tool start
            arcpy.AddMessage("🚀 Starting Forest Classification Tool - Phase 2 v0.2.4")
            arcpy.AddMessage(
                "📋 Phase 2: Core Data Processing with basic field management"
            )

            # Get parameters (3 params: output, thread, memory)
            # Note: No input layer parameter - Phase 2 uses predefined data sources
            output_layer = parameters[0].valueAsText
            thread_count = parameters[1].valueAsText or "Auto (Recommended)"
            memory_allocation = parameters[2].valueAsText or "Auto (Recommended)"

            # Define input feature layer from IMPORT_FIELDS.json (relative to ArcGIS Pro workspace)
            input_feature_layer = "Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtrealder"

            # Log parameter values
            arcpy.AddMessage(f"📤 Output Layer: {output_layer}")
            arcpy.AddMessage(f"🧵 Thread Count: {thread_count}")
            arcpy.AddMessage(f"💾 Memory Allocation: {memory_allocation}")
            arcpy.AddMessage(
                f"📊 Input Feature Layer: {input_feature_layer}"
            )  # Phase 2: Core Data Processing

            def progress_update(percent, message):
                """Helper function to update progress with 5% granularity."""
                arcpy.AddMessage(f"📊 Progress: {percent:3d}% - {message}")

            # Process the input feature layer from ArcGIS Pro workspace
            arcpy.AddMessage("🔄 Starting basic data processing...")

            processing_results = process_layer_basic(
                input_feature_layer, progress_update
            )

            # Report processing results
            if processing_results["processing_successful"]:
                arcpy.AddMessage("📈 Processing Results Summary:")
                arcpy.AddMessage(
                    f"   • Layer: {processing_results.get('layer_path', 'Unknown')}"
                )
                arcpy.AddMessage(
                    f"   • Fields found: {processing_results['field_count']}"
                )
                arcpy.AddMessage(
                    f"   • Features counted: {processing_results['feature_count']:,}"
                )
                arcpy.AddMessage(
                    f"   • Sample data points: {len(processing_results['sample_data'])}"
                )

                # Report data quality if available
                if "data_quality" in processing_results:
                    quality = processing_results["data_quality"]
                    arcpy.AddMessage(
                        f"   • Data quality: {quality['sample_size']} samples analyzed"
                    )
                    if quality.get("has_null_values"):
                        arcpy.AddMessage("   • ⚠️  Contains null/missing values")
                    else:
                        arcpy.AddMessage("   • ✅ No null values in sample")

                # For Phase 2, we'll create a simple copy of the sample data as output
                # Future phases will add actual forest classification processing
                arcpy.AddMessage(
                    "📋 Creating output layer (Phase 2: Basic copy operation)..."
                )

                # Ensure output goes to default geodatabase if just a name is provided
                if not (
                    "/" in output_layer or "\\" in output_layer or "." in output_layer
                ):
                    # Just a layer name - use default geodatabase
                    default_gdb = (
                        arcpy.env.workspace
                        or arcpy.mp.ArcGISProject("CURRENT").defaultGeodatabase
                    )
                    output_path = f"{default_gdb}/{output_layer}"
                    arcpy.AddMessage(f"📍 Output path: {output_path}")
                else:
                    output_path = output_layer
                    arcpy.AddMessage(f"📍 Using provided path: {output_path}")

                arcpy.CopyFeatures_management(input_feature_layer, output_path)
                arcpy.AddMessage("✅ Output layer created successfully")

            else:
                arcpy.AddError(
                    "❌ Data processing failed - see messages above for details"
                )
                return

            # Log completion
            arcpy.AddMessage(
                "✅ Forest Classification Tool - Phase 2 completed successfully!"
            )
            arcpy.AddMessage(
                "🔮 Next Phase: Field Management and validation capabilities"
            )

        except Exception as e:
            arcpy.AddError(f"❌ Tool execution failed: {e}")
            import traceback

            arcpy.AddError(f"📋 Error details: {traceback.format_exc()}")

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and added to the display."""
        arcpy.AddMessage("🧹 Phase 2 post-execution cleanup completed")


def main():
    """Main execution function for .atbx Script tool - Phase 2."""

    # Immediate logging
    arcpy.AddMessage("🚀 Starting Forest Classification Tool - Phase 2 v0.2.4")
    arcpy.AddMessage("📋 Phase 2: Core Data Processing with basic field management")

    # Extract Phase 2 parameters using GetParameterAsText (3 params: output, thread, memory)
    # Note: No input layer parameter - Phase 2 uses predefined data sources from IMPORT_FIELDS.json
    output_layer = arcpy.GetParameterAsText(0)
    thread_count = arcpy.GetParameterAsText(1) or "Auto (Recommended)"
    memory_allocation = arcpy.GetParameterAsText(2) or "Auto (Recommended)"

    # Define input feature layer from IMPORT_FIELDS.json (relative to ArcGIS Pro workspace)
    # Using the example you provided: Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtrealder (Stand age)
    input_feature_layer = "Grid_8m_SR16_Dataset/Grid_8m_SR16_srrtrealder"

    # Log parameter values
    arcpy.AddMessage(f"📤 Output Layer: {output_layer}")
    arcpy.AddMessage(f"🧵 Thread Count: {thread_count}")
    arcpy.AddMessage(f"💾 Memory Allocation: {memory_allocation}")
    arcpy.AddMessage(f"📊 Input Feature Layer: {input_feature_layer}")

    # Log detected system capabilities
    system_caps = get_system_capabilities()
    cpu_cores = system_caps["cpu_count"]
    available_memory_gb = system_caps["max_memory_gb"]
    arcpy.AddMessage(f"🖥️ System: {cpu_cores} CPU cores detected")
    arcpy.AddMessage(f"💾 Available memory: {available_memory_gb:.1f} GB")

    # Phase 2: Core Data Processing
    def progress_update(percent, message):
        """Helper function to update progress with 5% granularity."""
        arcpy.AddMessage(f"📊 Progress: {percent:3d}% - {message}")

    try:
        # Process the input feature layer from ArcGIS Pro workspace
        arcpy.AddMessage("🔄 Starting basic data processing...")

        processing_results = process_layer_basic(input_feature_layer, progress_update)

        # Report processing results
        if processing_results["processing_successful"]:
            arcpy.AddMessage("📈 Processing Results Summary:")
            arcpy.AddMessage(
                f"   • Layer: {processing_results.get('layer_path', 'Unknown')}"
            )
            arcpy.AddMessage(f"   • Fields found: {processing_results['field_count']}")
            arcpy.AddMessage(
                f"   • Features counted: {processing_results['feature_count']:,}"
            )
            arcpy.AddMessage(
                f"   • Sample data points: {len(processing_results['sample_data'])}"
            )

            # Report data quality if available
            if "data_quality" in processing_results:
                quality = processing_results["data_quality"]
                arcpy.AddMessage(
                    f"   • Data quality: {quality['sample_size']} samples analyzed"
                )
                if quality.get("has_null_values"):
                    arcpy.AddMessage("   • ⚠️  Contains null/missing values")
                else:
                    arcpy.AddMessage("   • ✅ No null values in sample")

            # For Phase 2, we'll perform CUD operations on the existing output layer
            # Future phases will add actual forest classification processing
            arcpy.AddMessage(
                "📋 Performing field management (Phase 2: CUD operations)..."
            )

            # Check if output layer exists
            if not ("/" in output_layer or "\\" in output_layer or "." in output_layer):
                # Just a layer name - use default geodatabase
                default_gdb = (
                    arcpy.env.workspace
                    or arcpy.mp.ArcGISProject("CURRENT").defaultGeodatabase
                )
                output_path = f"{default_gdb}/{output_layer}"
                arcpy.AddMessage(f"📍 Output path: {output_path}")
            else:
                output_path = output_layer
                arcpy.AddMessage(f"📍 Using provided path: {output_path}")

            if arcpy.Exists(output_path):
                arcpy.AddMessage(
                    "✅ Output layer exists - performing CUD operations..."
                )

                # Get existing fields (excluding system fields)
                existing_fields = [f.name for f in arcpy.ListFields(output_path)]
                system_fields = ["OBJECTID", "Shape", "Shape_Area", "Shape_Length"]
                user_fields = [f for f in existing_fields if f not in system_fields]

                # Define our target fields from IMPORT_FIELDS (sample subset for Phase 2)
                target_fields = ["srrtrealder", "srrtreslag", "srrbmo", "srrmhoyde"]

                arcpy.AddMessage(
                    f"📊 Found {len(user_fields)} user fields, targeting {len(target_fields)} fields"
                )

                # CREATE: Add missing fields
                fields_created = []
                for field in target_fields:
                    if field not in existing_fields:
                        arcpy.AddMessage(f"➕ Creating field: {field}")
                        arcpy.AddField_management(
                            output_path, field, "DOUBLE", field_alias=field
                        )
                        fields_created.append(field)

                # UPDATE: Actually update field values from input data
                all_target_fields = [
                    f
                    for f in target_fields
                    if f in existing_fields or f in fields_created
                ]
                updated_count = 0  # Initialize counter
                if all_target_fields:
                    # Get all available data fields from input layer (excluding system fields)
                    input_fields = [
                        f.name for f in arcpy.ListFields(input_feature_layer)
                    ]
                    input_data_fields = [
                        f
                        for f in input_fields
                        if f not in ["OBJECTID", "Shape", "Shape_Area", "Shape_Length"]
                    ]

                    # Find which target fields actually exist in input layer
                    available_source_fields = [
                        f for f in all_target_fields if f in input_data_fields
                    ]

                    arcpy.AddMessage(
                        f"🔄 Input layer has {len(input_data_fields)} data fields: {', '.join(input_data_fields)}"
                    )
                    arcpy.AddMessage(
                        f"🔄 Will update {len(available_source_fields)} matching fields: {', '.join(available_source_fields)}"
                    )

                    if available_source_fields:
                        # Use UpdateCursor to transfer values row by row
                        arcpy.AddMessage("📋 Starting field value updates...")

                        # Create dictionary to store input data values by OBJECTID
                        input_data = {}
                        with arcpy.da.SearchCursor(
                            input_feature_layer,
                            ["OBJECTID"] + available_source_fields,
                        ) as search_cursor:
                            for row in search_cursor:
                                oid = row[0]
                                values = row[
                                    1:
                                ]  # Field values (preserving Null values)
                                input_data[oid] = dict(
                                    zip(available_source_fields, values)
                                )

                        arcpy.AddMessage(
                            f"📊 Read {len(input_data)} records from input layer"
                        )

                        # Update output layer with input data values, mapping by OBJECTID
                        with arcpy.da.UpdateCursor(
                            output_path, ["OBJECTID"] + available_source_fields
                        ) as update_cursor:
                            for row in update_cursor:
                                output_oid = row[0]

                                # Find matching input record by OBJECTID
                                if output_oid in input_data:
                                    # Update the row with new values (preserving Null values)
                                    updated_row = [output_oid]  # Start with OBJECTID
                                    for field in available_source_fields:
                                        new_value = input_data[output_oid][field]
                                        updated_row.append(
                                            new_value
                                        )  # Copy value as-is (including Null)

                                    update_cursor.updateRow(updated_row)
                                    updated_count += 1

                        arcpy.AddMessage(
                            f"✅ Updated {updated_count} records with field values from input layer"
                        )
                    else:
                        arcpy.AddMessage(
                            "⚠️ No matching fields found between input and output layers"
                        )
                else:
                    arcpy.AddMessage("ℹ️ No target fields to update")

                # DELETE: Remove fields not in our target schema
                fields_to_delete = [f for f in user_fields if f not in target_fields]
                deleted_count = 0
                for field in fields_to_delete:
                    try:
                        arcpy.AddMessage(f"🗑️ Deleting field: {field}")
                        arcpy.DeleteField_management(output_path, field)
                        deleted_count += 1
                    except Exception as e:
                        arcpy.AddWarning(f"⚠️ Could not delete field {field}: {e}")

                arcpy.AddMessage(
                    f"✅ CUD operations completed: {len(fields_created)} created, {updated_count} records updated, {deleted_count} fields deleted"
                )
            else:
                arcpy.AddMessage(
                    "📋 Output layer doesn't exist - creating from input..."
                )
                arcpy.CopyFeatures_management(input_feature_layer, output_path)
                arcpy.AddMessage("✅ Output layer created from input data")
            arcpy.AddMessage("✅ Output layer created successfully")

        else:
            arcpy.AddError("❌ Data processing failed - see messages above for details")
            return

        # Log completion
        arcpy.AddMessage(
            "✅ Forest Classification Tool - Phase 2 completed successfully!"
        )
        arcpy.AddMessage("🔮 Next Phase: Field Management and validation capabilities")

    except Exception as e:
        arcpy.AddError(f"❌ Tool execution failed: {e}")
        import traceback

        arcpy.AddError(f"📋 Error details: {traceback.format_exc()}")


# Module-level execution for .atbx Script tools
if __name__ == "__main__":
    main()
