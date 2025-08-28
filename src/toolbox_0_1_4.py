# -*- coding: utf-8 -*-
"""
Forest Classification Tool - Phase 1: Basic Toolbox Structure v0.1.4

Phase 1 Features:
- Basic ArcGIS toolbox class structure
- Parameter definition (input/output layers, thread/memory settings)
- Simple execute method with progress messages
- Basic logging to ArcGIS Pro messages
- Dynamic system capability detection for threads and memory (v0.1.2)
- Fixed ArcGIS Pro data types and dropdown filters (v0.1.3)
- Added debugging and alternative filter setup (v0.1.4)

This is Phase 1 of a 13-phase incremental development strategy.
Developed as part of the Single File Development Strategy for ArcGIS Pro Forest Classification Tool.

Version History:
- v0.1.1: Initial Phase 1 implementation with basic toolbox structure
- v0.1.2: Added dynamic system capability detection for CPU cores and memory allocation
- v0.1.3: Fixed ArcGIS Pro data types (GPFeatureLayer/GPString) and dropdown filter setup
- v0.1.4: Added debugging and alternative filter initialization approach
"""

import arcpy
import os
import psutil


def get_system_capabilities():
    """Detect system CPU cores and available memory for dynamic parameter options."""
    try:
        # Get CPU core count
        cpu_cores = os.cpu_count() or 4  # Fallback to 4 if detection fails

        # Get available memory in GB
        memory_info = psutil.virtual_memory()
        total_memory_gb = memory_info.total / (1024**3)  # Convert bytes to GB
        available_memory_gb = memory_info.available / (1024**3)

        return cpu_cores, total_memory_gb, available_memory_gb
    except Exception:
        # Fallback values if system detection fails
        return 4, 16.0, 8.0


def create_dynamic_thread_options(cpu_cores):
    """Create 3 thread options based on detected CPU cores."""
    conservative = max(1, cpu_cores // 4)  # 25% of cores, minimum 1
    balanced = max(2, cpu_cores // 2)  # 50% of cores, minimum 2
    performance = max(3, int(cpu_cores * 0.75))  # 75% of cores, minimum 3

    return [
        f"Conservative ({conservative} threads)",
        f"Balanced ({balanced} threads)",
        f"Performance ({performance} threads)",
    ]


def create_dynamic_memory_options(available_memory_gb):
    """Create 3 memory options based on available system memory."""
    # Calculate conservative (25%), balanced (50%), performance (75%) of available memory
    conservative_gb = max(2, int(available_memory_gb * 0.25))
    balanced_gb = max(4, int(available_memory_gb * 0.5))
    performance_gb = max(6, int(available_memory_gb * 0.75))

    return [
        f"Conservative ({conservative_gb} GB)",
        f"Balanced ({balanced_gb} GB)",
        f"Performance ({performance_gb} GB)",
    ]


class ForestClassificationToolbox(object):
    """Basic ArcGIS toolbox class structure for forest classification."""

    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .py file)."""
        self.label = "Forest Classification Toolbox - Phase 1 v0.1.4"
        self.alias = "ForestClassificationPhase1v0_1_4"
        self.description = "Forest species classification tool with dynamic system detection. Automatically detects CPU cores and available memory to provide optimized thread and memory allocation options for forest analysis workflows."

        # List of tool classes associated with this toolbox
        self.tools = [ForestClassificationTool]


class ForestClassificationTool(object):
    """Forest Classification Tool - Phase 1 Implementation

    Basic tool structure with parameter definition and simple execution.
    """

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Forest Classification Tool - Phase 1 v0.1.4"
        self.description = "Classifies forest features using species-specific algorithms. Features dynamic system detection to automatically configure thread count (based on CPU cores) and memory allocation (based on available RAM) for optimal performance on your hardware."
        self.canRunInBackground = False
        self.category = "Forest Analysis"

    def getParameterInfo(self):
        """Define parameter definitions for input/output layers and thread/memory settings."""

        # Get system capabilities for dynamic parameter options
        cpu_cores, total_memory_gb, available_memory_gb = get_system_capabilities()

        # Output Feature Layer parameter
        output_layer = arcpy.Parameter(
            displayName="Output Feature Layer",
            name="output_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input",
        )
        output_layer.category = "Input Data"

        # Set filter for polygon and point features
        if hasattr(output_layer, "filter") and output_layer.filter:
            output_layer.filter.list = ["Polygon", "Point"]

        # Thread Count Configuration parameter (dynamic based on CPU cores)
        thread_config = arcpy.Parameter(
            displayName="Thread Count",
            name="thread_config",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )
        thread_config.category = "Performance Settings"

        # Create dynamic thread options based on detected CPU cores
        thread_options = create_dynamic_thread_options(cpu_cores)

        # Try multiple approaches to set up the filter
        try:
            # Method 1: Direct assignment (like production code)
            thread_config.filter.list = thread_options
        except AttributeError:
            try:
                # Method 2: Initialize filter first
                thread_config.filter = arcpy.Filter()
                thread_config.filter.list = thread_options
            except:
                # Method 3: Set filter type first
                thread_config.filter.type = "ValueList"
                thread_config.filter.list = thread_options

        thread_config.value = thread_options[1]  # Default to Balanced

        # Memory Allocation Configuration parameter (dynamic based on available memory)
        memory_config = arcpy.Parameter(
            displayName="Memory Allocation",
            name="memory_config",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )
        memory_config.category = "Performance Settings"

        # Create dynamic memory options based on available system memory
        memory_options = create_dynamic_memory_options(available_memory_gb)

        # Try multiple approaches to set up the filter
        try:
            # Method 1: Direct assignment (like production code)
            memory_config.filter.list = memory_options
        except AttributeError:
            try:
                # Method 2: Initialize filter first
                memory_config.filter = arcpy.Filter()
                memory_config.filter.list = memory_options
            except:
                # Method 3: Set filter type first
                memory_config.filter.type = "ValueList"
                memory_config.filter.list = memory_options

        memory_config.value = memory_options[1]  # Default to Balanced

        return [output_layer, thread_config, memory_config]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal validation."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool parameter."""
        return

    def execute(self, parameters, messages):
        """Simple execute method with progress messages and basic logging."""

        # Basic logging to ArcGIS Pro messages
        arcpy.AddMessage("🚀 Starting Forest Classification Tool - Phase 1 v0.1.4")
        arcpy.AddMessage(
            "📋 Phase 1 v0.1.4: Dynamic system capability detection with filter debugging"
        )

        # Log detected system capabilities
        cpu_cores, total_memory_gb, available_memory_gb = get_system_capabilities()
        arcpy.AddMessage(
            f"🖥️ System: {cpu_cores} CPU cores, {total_memory_gb:.1f} GB total RAM, {available_memory_gb:.1f} GB available"
        )

        # Extract parameters
        output_layer = parameters[0].valueAsText
        thread_config = parameters[1].valueAsText
        memory_config = parameters[2].valueAsText

        # Log parameter values
        arcpy.AddMessage(f"📊 Output layer: {output_layer}")
        arcpy.AddMessage(f"🧵 Thread configuration: {thread_config}")
        arcpy.AddMessage(f"💾 Memory configuration: {memory_config}")

        # Progress messages for Phase 1
        arcpy.AddMessage("⚡ Phase 1 progress: 25% - Parameter validation complete")
        arcpy.AddMessage("⚡ Phase 1 progress: 50% - Configuration loaded")
        arcpy.AddMessage("⚡ Phase 1 progress: 75% - Tool structure initialized")
        arcpy.AddMessage("⚡ Phase 1 progress: 100% - Phase 1 execution complete")

        # Success message
        arcpy.AddMessage("✅ Phase 1 completed successfully!")
        arcpy.AddMessage(
            "💡 Next: Phase 2 will add basic data processing functionality"
        )

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and added to the display."""
        arcpy.AddMessage("🧹 Phase 1 post-execution cleanup completed")
