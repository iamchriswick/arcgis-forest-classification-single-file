# -*- coding: utf-8 -*-
"""
ToolValidator for Forest Classification Tool - Phase 1 v0.1.12

Created: 2025-08-29
Version: 0.1.12

This file contains the ToolValidator code for the ArcGIS Pro .atbx Script tool.
Copy the code below to .atbx Properties → Validation to enable enhanced GUI features.

Enhanced Features v0.1.12:
- Auto multithreading option with intelligent thread selection
- Detailed memory allocation with percentage utilization display
- Dynamic system capability detection for optimal performance
- Smart dropdown population for output feature layers

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

import arcpy
import os


class ToolValidator(object):
    """
    ToolValidator for Forest Classification Tool - Phase 1 v0.1.12

    Copy this entire class definition to .atbx Properties → Validation.
    Enhanced GUI features will be automatically enabled.
    """

    def __init__(self):
        self.params = (
            arcpy.GetParameterInfo()
        )  # 0=output_layer, 1=multithreading_config, 2=memory_config

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
        # Dropdowns with default = option 2 (moderate/balanced)
        self.params[1].filter.list = self._thread_labels(self._cpu_cores())
        self.params[1].value = self.params[1].filter.list[1]

        self.params[2].filter.list = self._memory_labels(self._avail_mem_gb())
        self.params[2].value = self.params[2].filter.list[1]

        # Populate output layer dropdown if a map is active
        try:
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
        # Refresh dropdowns if context changes
        self.params[1].filter.list = self._thread_labels(self._cpu_cores())
        self.params[2].filter.list = self._memory_labels(self._avail_mem_gb())

        try:
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
