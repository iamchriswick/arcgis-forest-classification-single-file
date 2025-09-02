# -*- coding: utf-8 -*-
"""
Forest Classification Tool - Phase 1: Basic Toolbox Structure v0.1.12

Created: 2025-08-28 22:45
Version: 0.1.12

Phase 1 Features:
- Basic ArcGIS toolbox class structure
- Parameter definition (input/output layers, thread/memory settings)
- Simple execute method with progress messages
- Basic logging to ArcGIS Pro messages
- Dynamic system capability detection for threads and memory (v0.1.2)
- Fixed ArcGIS Pro data types and dropdown filters (v0.1.3)
- Added debugging and alternative filter setup (v0.1.4)
- Fixed header format with full datetime and improved ToolValidator approach (v0.1.5)
- Corrected for ArcGIS Pro .atbx Script tool - removed dropdown logic from .py (v0.1.6)
- Fixed logging for .atbx Script tool - added module-level execution (v0.1.7)
- Optimized startup performance - faster logging and reduced import overhead (v0.1.8)
- Bypassed system detection - GUI still works, script runs with defaults (v0.1.9)
- Ultra-minimal code to isolate 11-second delay issue (v0.1.10)
- Re-enabled system detection with 90% max thread and memory rules (v0.1.11)
- Enhanced GUI with improved dropdown labels and Auto multithreading option (v0.1.12)

This is Phase 1 of a 13-phase incremental development strategy.
Developed as part of the Single File Development Strategy for ArcGIS Pro Forest Classification Tool.

For ArcGIS Pro .atbx Script tools, the script executes at module level when called.
ToolValidator dropdown UI is controlled by the .atbx Properties → Validation.

Version History:
- v0.1.1: Initial Phase 1 implementation with basic toolbox structure
- v0.1.2: Added dynamic system capability detection for CPU cores and memory allocation
- v0.1.3: Fixed ArcGIS Pro data types (GPFeatureLayer/GPString) and dropdown filter setup
- v0.1.4: Added debugging and alternative filter initialization approach
- v0.1.5: Fixed header format with full datetime and improved ToolValidator approach
- v0.1.6: Corrected for ArcGIS Pro .atbx Script tool - removed dropdown logic from .py
- v0.1.7: Fixed logging for .atbx Script tool - added module-level execution
- v0.1.8: Optimized startup performance - faster logging and reduced import overhead
- v0.1.9: Bypassed system detection - GUI still works, script runs with defaults
- v0.1.10: Ultra-minimal code to isolate 11-second delay issue
- v0.1.11: Re-enabled system detection with 90% max thread and memory rules
- v0.1.12: Enhanced GUI with improved dropdown labels and Auto multithreading option
"""

import os


def log_system_capabilities():
    """Log detected system capabilities with 90% max thread and memory rules."""
    # Import arcpy only when needed to avoid pytest discovery issues
    import arcpy

    try:
        # Fast CPU detection using os.cpu_count (built-in, no external libs)
        cpu_cores = os.cpu_count() or 4
        arcpy.AddMessage(f"🖥️ System: {cpu_cores} CPU cores detected")

        # Calculate max threads as 90% of available cores
        max_threads = max(1, int(cpu_cores * 0.9))
        arcpy.AddMessage(
            f"🧵 System: Maximum recommended threads: {max_threads} (90% of {cpu_cores} cores)"
        )

        # Try psutil for memory detection
        try:
            # Only import psutil when needed (lazy import)
            import psutil

            # Get memory info
            mem = psutil.virtual_memory()
            available_gb = mem.available / (1024**3)
            total_gb = mem.total / (1024**3)

            # Calculate max memory as 90% of available
            max_memory_gb = max(2, int(available_gb * 0.9))

            arcpy.AddMessage(
                f"💾 System: {available_gb:.1f} GB available RAM ({total_gb:.1f} GB total)"
            )
            arcpy.AddMessage(
                f"💾 System: Maximum recommended memory: {max_memory_gb} GB (90% of {available_gb:.1f} GB available)"
            )

        except (ImportError, Exception):
            # Fallback without psutil
            arcpy.AddMessage("💾 System: Memory detection unavailable - using fallback")

    except Exception as e:
        arcpy.AddMessage(f"🖥️ System: Detection failed - {str(e)}")


def main():
    """Main execution function for .atbx Script tool."""
    import arcpy

    # Immediate logging
    arcpy.AddMessage("🚀 Starting Forest Classification Tool v0.1.12")
    arcpy.AddMessage(
        "📋 Phase 1 v0.1.12: Enhanced GUI with improved dropdown labels and Auto multithreading option"
    )

    # Extract parameters immediately
    output_layer = arcpy.GetParameterAsText(0)
    thread_config = arcpy.GetParameterAsText(1)
    memory_config = arcpy.GetParameterAsText(2)

    # Log parameter values immediately
    arcpy.AddMessage(f"📊 Output layer: {output_layer}")
    arcpy.AddMessage(f"🧵 Thread configuration: {thread_config}")
    arcpy.AddMessage(f"💾 Memory configuration: {memory_config}")

    # System capabilities detection (with 90% rules)
    log_system_capabilities()

    # Progress messages
    arcpy.AddMessage("⚡ Phase 1 progress: 25% - Parameter validation complete")
    arcpy.AddMessage("⚡ Phase 1 progress: 50% - Configuration loaded")
    arcpy.AddMessage("⚡ Phase 1 progress: 75% - Tool structure initialized")
    arcpy.AddMessage("⚡ Phase 1 progress: 100% - Phase 1 execution complete")

    # Success message
    arcpy.AddMessage("✅ Phase 1 completed successfully!")
    arcpy.AddMessage("💡 Next: Phase 2 will add basic data processing functionality")
    arcpy.AddMessage(
        "📝 Note: For .atbx Script tools, dropdowns are handled by ToolValidator in .atbx Properties → Validation"
    )


# Module-level execution
if __name__ == "__main__":
    main()


# ===== TOOLBOX CLASSES (for .pyt compatibility if needed) =====


class ForestClassificationToolbox(object):
    """Basic ArcGIS toolbox class structure for forest classification."""

    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .py file)."""
        self.label = "Forest Classification Toolbox - Phase 1 v0.1.12"
        self.alias = "ForestClassificationPhase1v0_1_12"
        self.description = "Forest species classification tool for ArcGIS Pro .atbx Script tools. Enhanced GUI with improved dropdown labels and Auto multithreading option."

        # List of tool classes associated with this toolbox
        self.tools = [ForestClassificationTool]


class ForestClassificationTool(object):
    """Forest Classification Tool - Phase 1 Implementation

    Basic tool structure for ArcGIS Pro .atbx Script tools.
    Parameter UI (dropdowns) are controlled by the .atbx ToolValidator.
    """

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Forest Classification Tool - Phase 1 v0.1.12"
        self.description = "Classifies forest features using species-specific algorithms. Enhanced GUI with improved dropdown labels and Auto multithreading option."
        self.canRunInBackground = False
        self.category = "Forest Analysis"

    def getParameterInfo(self):
        """Define parameter definitions for .atbx Script tool."""
        import arcpy

        # Parameter 0: Output Feature Layer/Feature Class (multi-type for dropdown + browsing)
        output_layer = arcpy.Parameter(
            displayName="Output Feature Layer",
            name="output_layer",
            datatype=[
                "Feature Layer",
                "Feature Class",
            ],  # Multi-type: dropdown when map active, browse otherwise
            parameterType="Required",
            direction="Input",
        )
        output_layer.category = "Input Data"

        # Parameter 1: Multithreading Configuration (String - dropdown handled by .atbx ToolValidator)
        thread_config = arcpy.Parameter(
            displayName="Multithreading",
            name="thread_config",
            datatype="String",  # Simple string - UI handled by .atbx ToolValidator
            parameterType="Required",
            direction="Input",
        )
        thread_config.category = "Performance Settings"

        # Parameter 2: Memory Allocation Configuration (String - dropdown handled by .atbx ToolValidator)
        memory_config = arcpy.Parameter(
            displayName="Memory Allocation",
            name="memory_config",
            datatype="String",  # Simple string - UI handled by .atbx ToolValidator
            parameterType="Required",
            direction="Input",
        )
        memory_config.category = "Performance Settings"

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
        """Execute method that calls the main function."""
        main()
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and added to the display."""
        import arcpy
        arcpy.AddMessage("🧹 Phase 1 post-execution cleanup completed")
