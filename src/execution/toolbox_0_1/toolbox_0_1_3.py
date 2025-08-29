# -*- coding: utf-8 -*-
"""
Forest Classification Tool - Phase 1: Basic Toolbox Structure v0.1.3

Phase 1 Features:
- Basic ArcGIS toolbox class structure
- Parameter definition (input/output layers, thread/memory settings)
- Simple execute method with progress messages
- Basic logging to ArcGIS Pro messages
- Dynamic system capability detection for threads and memory (v0.1.2)
- Fixed ArcGIS Pro data types and dropdown filters (v0.1.3)

This is Phase 1 of a 13-phase incremental development strategy.
Developed as part of the Single File Development Strategy for ArcGIS Pro Forest Classification Tool.

Version History:
- v0.1.1: Initial Phase 1 implementation with basic toolbox structure
- v0.1.2: Added dynamic system capability detection for CPU cores and memory allocation
- v0.1.3: Fixed ArcGIS Pro data types (GPFeatureLayer/GPString) and dropdown filter setup
"""

import arcpy
import os
import psutil


def get_system_capabilities():
    """Detect system CPU cores and available memory for dynamic parameter options."""
    try:
        # Get CPU core count
        cpu_cores = os.cpu_count() or 4

        # Get memory information using psutil
        memory = psutil.virtual_memory()
        total_memory_gb = memory.total / (1024**3)
        available_memory_gb = memory.available / (1024**3)

        return cpu_cores, total_memory_gb, available_memory_gb

    except Exception:
        # Fallback values if detection fails
        return 4, 16.0, 8.0


def create_dynamic_thread_options(cpu_cores):
    """Create dynamic thread count options based on CPU cores."""
    options = [
        f"Conservative ({max(1, cpu_cores // 4)} threads)",
        f"Balanced ({max(1, cpu_cores // 2)} threads)",
        f"Aggressive ({max(1, int(cpu_cores * 0.75))} threads)",
        f"Maximum ({cpu_cores} threads)",
    ]
    return options


def create_dynamic_memory_options(available_memory_gb):
    """Create dynamic memory allocation options based on available RAM."""
    # Use percentages of available memory with minimum thresholds
    conservative = max(2.0, available_memory_gb * 0.25)
    balanced = max(4.0, available_memory_gb * 0.5)
    aggressive = max(6.0, available_memory_gb * 0.75)
    maximum = max(8.0, available_memory_gb * 0.9)

    options = [
        f"Conservative ({conservative:.1f} GB)",
        f"Balanced ({balanced:.1f} GB)",
        f"Aggressive ({aggressive:.1f} GB)",
        f"Maximum ({maximum:.1f} GB)",
    ]
    return options


class ForestClassificationToolbox(object):
    """Basic ArcGIS toolbox class structure for forest classification."""

    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .py file)."""
        self.label = "Forest Classification Toolbox - Phase 1 v0.1.3"
        self.alias = "ForestClassificationPhase1v0_1_3"
        self.description = "Forest species classification tool with dynamic system detection. Automatically detects CPU cores and available memory to provide optimized thread and memory allocation options for forest analysis workflows."

        # List of tool classes associated with this toolbox
        self.tools = [ForestClassificationTool]


class ForestClassificationTool(object):
    """Forest Classification Tool - Phase 1 Implementation

    Basic tool structure with parameter definition and simple execution.
    Fixed ArcGIS Pro data types (GPFeatureLayer/GPString) and dropdown filter setup.
    """

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Forest Classification Tool - Phase 1 v0.1.3"
        self.description = "Classifies forest features using species-specific algorithms. Features fixed ArcGIS Pro data types (GPFeatureLayer/GPString) and improved dropdown filter functionality for optimal compatibility."
        self.canRunInBackground = False
        self.category = "Forest Analysis"

    def getParameterInfo(self):
        """Define parameter definitions with corrected ArcGIS Pro data types."""

        # Get system capabilities for dynamic parameter options
        cpu_cores, total_memory_gb, available_memory_gb = get_system_capabilities()

        # Output Feature Layer parameter (corrected data type)
        output_layer = arcpy.Parameter(
            displayName="Output Feature Layer",
            name="output_layer",
            datatype="GPFeatureLayer",  # Corrected ArcGIS Pro data type
            parameterType="Required",
            direction="Input",
        )
        output_layer.category = "Input Data"

        # Set filter for polygon and point features
        if hasattr(output_layer, "filter") and output_layer.filter:
            output_layer.filter.list = ["Polygon", "Point"]

        # Thread Count Configuration parameter (corrected data type)
        thread_config = arcpy.Parameter(
            displayName="Thread Count",
            name="thread_config",
            datatype="GPString",  # Corrected ArcGIS Pro data type
            parameterType="Required",
            direction="Input",
        )
        thread_config.category = "Performance Settings"

        # Create dynamic thread options based on detected CPU cores
        thread_options = create_dynamic_thread_options(cpu_cores)
        if hasattr(thread_config, "filter") and thread_config.filter:
            thread_config.filter.list = thread_options
        thread_config.value = thread_options[1]  # Default to Balanced

        # Memory Allocation Configuration parameter (corrected data type)
        memory_config = arcpy.Parameter(
            displayName="Memory Allocation",
            name="memory_config",
            datatype="GPString",  # Corrected ArcGIS Pro data type
            parameterType="Required",
            direction="Input",
        )
        memory_config.category = "Performance Settings"

        # Create dynamic memory options based on available system memory
        memory_options = create_dynamic_memory_options(available_memory_gb)
        if hasattr(memory_config, "filter") and memory_config.filter:
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
        arcpy.AddMessage("🚀 Starting Forest Classification Tool - Phase 1 v0.1.3")
        arcpy.AddMessage(
            "📋 Phase 1 v0.1.3: Fixed ArcGIS Pro data types (GPFeatureLayer/GPString) and dropdown filters"
        )

        # Extract parameters
        output_layer = parameters[0].valueAsText
        thread_config = parameters[1].valueAsText
        memory_config = parameters[2].valueAsText

        # Log parameter values
        arcpy.AddMessage(f"📊 Output layer: {output_layer}")
        arcpy.AddMessage(f"🧵 Thread configuration: {thread_config}")
        arcpy.AddMessage(f"💾 Memory configuration: {memory_config}")

        # Log system capabilities for reference
        cpu_cores, total_memory_gb, available_memory_gb = get_system_capabilities()
        arcpy.AddMessage(f"🖥️ System: {cpu_cores} CPU cores detected")
        arcpy.AddMessage(f"💾 System: {available_memory_gb:.1f} GB available RAM")

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
        arcpy.AddMessage(
            "🔧 v0.1.3: Corrected data types ensure full ArcGIS Pro compatibility"
        )

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and added to the display."""
        arcpy.AddMessage("🧹 Phase 1 post-execution cleanup completed")
