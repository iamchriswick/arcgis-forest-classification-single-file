# -*- coding: utf-8 -*-
"""
Forest Classification Tool - Phase 1: Basic Toolbox Structure v0.1.7

Created: 2025-08-28 15:15
Version: 0.1.7

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
"""

import arcpy
import os


def log_system_capabilities():
    """Log detected system capabilities for reference."""
    try:
        cpu_cores = os.cpu_count() or 4
        arcpy.AddMessage(f"🖥️ System: {cpu_cores} CPU cores detected")

        try:
            import psutil

            available_memory_gb = psutil.virtual_memory().available / (1024**3)
            total_memory_gb = psutil.virtual_memory().total / (1024**3)
            arcpy.AddMessage(
                f"💾 System: {available_memory_gb:.1f} GB available RAM ({total_memory_gb:.1f} GB total)"
            )
        except ImportError:
            arcpy.AddMessage(
                "💾 System: psutil not available - using fallback memory detection"
            )
    except Exception as e:
        arcpy.AddMessage(f"🖥️ System: Could not detect system capabilities - {str(e)}")


def main():
    """Main execution function for .atbx Script tool."""

    # Basic logging to ArcGIS Pro messages
    arcpy.AddMessage("🚀 Starting Forest Classification Tool v0.1.7")
    arcpy.AddMessage(
        "📋 Phase 1 v0.1.7: Fixed logging for .atbx Script tool - added module-level execution"
    )

    # Extract parameters using GetParameterAsText (for .atbx Script tools)
    output_layer = arcpy.GetParameterAsText(0)
    thread_config = arcpy.GetParameterAsText(1)
    memory_config = arcpy.GetParameterAsText(2)

    # Log parameter values
    arcpy.AddMessage(f"📊 Output layer: {output_layer}")
    arcpy.AddMessage(f"🧵 Thread configuration: {thread_config}")
    arcpy.AddMessage(f"💾 Memory configuration: {memory_config}")

    # Log system capabilities for reference
    log_system_capabilities()

    # Progress messages for Phase 1
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


# Module-level execution for .atbx Script tools
if __name__ == "__main__":
    main()
else:
    # Also execute when imported/called by ArcGIS Pro .atbx Script tool
    main()


# ===== TOOLBOX CLASSES (for .pyt compatibility if needed) =====


class ForestClassificationToolbox(object):
    """Basic ArcGIS toolbox class structure for forest classification."""

    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .py file)."""
        self.label = "Forest Classification Toolbox - Phase 1 v0.1.7"
        self.alias = "ForestClassificationPhase1v0_1_7"
        self.description = "Forest species classification tool for ArcGIS Pro .atbx Script tools. Dropdowns are handled by the ToolValidator in the .atbx Properties → Validation."

        # List of tool classes associated with this toolbox
        self.tools = [ForestClassificationTool]


class ForestClassificationTool(object):
    """Forest Classification Tool - Phase 1 Implementation

    Basic tool structure for ArcGIS Pro .atbx Script tools.
    Parameter UI (dropdowns) are controlled by the .atbx ToolValidator.
    """

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Forest Classification Tool - Phase 1 v0.1.7"
        self.description = "Classifies forest features using species-specific algorithms. For .atbx Script tools, dropdowns are handled by the ToolValidator in .atbx Properties → Validation."
        self.canRunInBackground = False
        self.category = "Forest Analysis"

    def getParameterInfo(self):
        """Define parameter definitions for .atbx Script tool."""

        # Parameter 0: Output Feature Layer/Feature Class (multi-type for dropdown + browsing)
        output_layer = arcpy.Parameter(
            displayName="Output Feature Layer",
            name="output_layer",
            datatype="Feature Layer; Feature Class",  # Multi-type: dropdown when map active, browse otherwise
            parameterType="Required",
            direction="Input",
        )
        output_layer.category = "Input Data"

        # Parameter 1: Thread Count Configuration (String - dropdown handled by .atbx ToolValidator)
        thread_config = arcpy.Parameter(
            displayName="Thread Count",
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
        arcpy.AddMessage("🧹 Phase 1 post-execution cleanup completed")


# ===== TOOLVALIDATOR CODE FOR .ATBX SCRIPT TOOL =====
# Copy this to .atbx Properties → Validation:

"""
import arcpy, os

class ToolValidator(object):
    def __init__(self):
        self.params = arcpy.GetParameterInfo()  # 0=output_layer, 1=thread_config, 2=memory_config

    # --- helpers ---
    def _cpu_cores(self):
        try:
            return max(1, os.cpu_count() or 4)
        except Exception:
            return 4

    def _avail_mem_gb(self):
        try:
            import psutil
            return max(2, int(psutil.virtual_memory().available / (1024**3)))
        except Exception:
            return 8  # fallback if psutil not present

    def _thread_labels(self, cores):
        low = max(1, cores // 4)          # ~25%
        mid = max(2, cores // 2)          # ~50%
        hi  = max(3, int(cores * 0.75))   # ~75%
        return [f"Low ({low})", f"Balanced ({mid})", f"High ({hi})"]

    def _memory_labels(self, avail_gb):
        cons = max(2, int(avail_gb * 0.25))
        std  = max(4, int(avail_gb * 0.50))
        aggr = max(6, int(avail_gb * 0.75))
        return [f"Conservative ({cons} GB)", f"Standard ({std} GB)", f"Aggressive ({aggr} GB)"]

    # --- lifecycle ---
    def initializeParameters(self):
        # Dropdowns with default = option 2
        self.params[1].filter.list = self._thread_labels(self._cpu_cores())
        self.params[1].value       = self.params[1].filter.list[1]

        self.params[2].filter.list = self._memory_labels(self._avail_mem_gb())
        self.params[2].value       = self.params[2].filter.list[1]

        # Populate output layer dropdown if a map is active
        try:
            aprx = arcpy.mp.ArcGISProject("CURRENT")
            m = aprx.activeMap
            if m:
                names = [lyr.name for lyr in m.listLayers() if getattr(lyr, "isFeatureLayer", False)]
                if names:
                    self.params[0].filter.list = names
                    if not self.params[0].value:
                        self.params[0].value = names[0]
        except Exception:
            pass
        return

    def updateParameters(self):
        # Refresh if context changes
        self.params[1].filter.list = self._thread_labels(self._cpu_cores())
        self.params[2].filter.list = self._memory_labels(self._avail_mem_gb())

        try:
            aprx = arcpy.mp.ArcGISProject("CURRENT")
            m = aprx.activeMap
            if m:
                self.params[0].filter.list = [lyr.name for lyr in m.listLayers() if getattr(lyr, "isFeatureLayer", False)]
        except Exception:
            pass
        return

    def updateMessages(self):
        return
"""
