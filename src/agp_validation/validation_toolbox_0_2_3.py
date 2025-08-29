# -*- coding: utf-8 -*-
"""
ToolValidator for Forest Classification Tool - Phase 2: Auto-Discovery Mode v0.2.3

Created: 2025-08-29 12:30
Version: 0.2.3

ArcGIS Pro ToolValidator for Auto-Discovery Mode Phase 2 implementation.
Provides dropdown UI for thread count and memory allocation parameters.
No input layer validation needed - auto-discovery handles dataset selection.

This ToolValidator corresponds to toolbox_0_2_3.py and should be used in
the .atbx Properties → Validation tab.

Phase 2 ToolValidator Features:
- Auto-discovery mode (no input layer dropdown)
- System-aware thread count dropdown (30%, 45%, 60%, 90%, Auto)
- System-aware memory allocation dropdown (30%, 45%, 60%, 90%, Auto)
- Output layer validation
- Simplified parameter handling

Developed as part of the Single File Development Strategy for ArcGIS Pro Forest Classification Tool.

Version History:
- v0.2.3: Auto-discovery ToolValidator with system-aware dropdowns
"""

import arcpy


class ToolValidator(object):
    """ToolValidator class for Forest Classification Tool - Phase 2 Auto-Discovery Mode."""

    def __init__(self):
        """Set up the ToolValidator."""
        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self):
        """Refine the properties of a tool's parameters.

        This method is called when the tool is opened.
        """
        try:
            # Get system capabilities for dropdown population
            system_caps = self._get_system_capabilities()

            # Initialize thread count dropdown (parameter[1])
            if (
                len(self.params) > 1
                and hasattr(self.params[1], "filter")
                and self.params[1].filter
            ):
                thread_param = self.params[1]
                thread_options = self._get_thread_options(system_caps)
                thread_param.filter.type = "ValueList"
                thread_param.filter.list = thread_options
                thread_param.value = "Auto (Recommended)"

            # Initialize memory allocation dropdown (parameter[2])
            if (
                len(self.params) > 2
                and hasattr(self.params[2], "filter")
                and self.params[2].filter
            ):
                memory_param = self.params[2]
                memory_options = self._get_memory_options(system_caps)
                memory_param.filter.type = "ValueList"
                memory_param.filter.list = memory_options
                memory_param.value = "Auto (Recommended)"

        except Exception:
            # Fallback to basic options if system detection fails
            if (
                len(self.params) > 1
                and hasattr(self.params[1], "filter")
                and self.params[1].filter
            ):
                self.params[1].filter.type = "ValueList"
                self.params[1].filter.list = [
                    "Auto (Recommended)",
                    "Single Thread",
                    "2 Threads",
                    "4 Threads",
                ]
                self.params[1].value = "Auto (Recommended)"

            if (
                len(self.params) > 2
                and hasattr(self.params[2], "filter")
                and self.params[2].filter
            ):
                self.params[2].filter.type = "ValueList"
                self.params[2].filter.list = [
                    "Auto (Recommended)",
                    "2 GB",
                    "4 GB",
                    "8 GB",
                ]
                self.params[2].value = "Auto (Recommended)"

    def updateParameters(self):
        """Modify the values and properties of parameters.

        This method is called whenever a parameter has been changed.
        """
        try:
            # Auto-discovery mode doesn't need complex parameter updates
            # Just ensure output layer is properly configured
            if len(self.params) > 0:
                output_param = self.params[0]

                # Ensure output parameter is properly configured
                if not output_param.altered:
                    # Could set a default output path/name if needed
                    pass

        except Exception:
            # Handle any parameter update errors gracefully
            pass

    def updateMessages(self):
        """Modify the messages created by internal validation.

        This method is called after internal validation.
        """
        try:
            # Auto-discovery mode validation messages

            # Validate output layer parameter (parameter[0])
            if len(self.params) > 0:
                output_param = self.params[0]

                if output_param.altered:
                    if output_param.valueAsText:
                        # Basic output path validation
                        output_path = output_param.valueAsText

                        # Check for valid output location
                        try:
                            import os

                            output_dir = os.path.dirname(output_path)
                            if output_dir and not arcpy.Exists(output_dir):
                                output_param.setWarningMessage(
                                    "Output directory may not exist. Please verify the path."
                                )
                        except Exception:
                            pass
                    else:
                        output_param.setErrorMessage(
                            "Output feature layer is required."
                        )

            # Thread count validation (parameter[1])
            if len(self.params) > 1:
                thread_param = self.params[1]
                if not thread_param.valueAsText:
                    thread_param.setErrorMessage("Thread count selection is required.")

            # Memory allocation validation (parameter[2])
            if len(self.params) > 2:
                memory_param = self.params[2]
                if not memory_param.valueAsText:
                    memory_param.setErrorMessage(
                        "Memory allocation selection is required."
                    )

            # Auto-discovery mode doesn't need additional info messages
            # User will see auto-discovery information in the tool execution logs

        except Exception:
            # Handle validation errors gracefully
            pass

    def _get_system_capabilities(self):
        """Get system capabilities for dropdown population.

        Returns:
            dict: System capabilities including CPU and memory info
        """
        try:
            import psutil

            cpu_count = psutil.cpu_count(logical=True) or 4
            memory_gb = (
                round(psutil.virtual_memory().total / (1024**3))
                if psutil.virtual_memory()
                else 8
            )

            return {
                "cpu_count": cpu_count,
                "memory_gb": memory_gb,
                "max_threads": max(1, int(cpu_count * 0.9)),
                "max_memory_gb": max(1, int(memory_gb * 0.9)),
            }
        except ImportError:
            # Fallback if psutil not available
            return {
                "cpu_count": 4,
                "memory_gb": 8,
                "max_threads": 3,
                "max_memory_gb": 7,
            }
        except Exception:
            # Fallback for any other errors
            return {
                "cpu_count": 4,
                "memory_gb": 8,
                "max_threads": 3,
                "max_memory_gb": 7,
            }

    def _get_thread_options(self, system_caps):
        """Generate thread count dropdown options based on system capabilities.

        Args:
            system_caps (dict): System capabilities

        Returns:
            list: Thread count options for dropdown
        """
        try:
            cpu_count = system_caps.get("cpu_count", 4)

            # Calculate utilization options
            options = ["Auto (Recommended)"]

            # Add percentage-based options
            for percent in [30, 45, 60, 90]:
                threads = max(1, int(cpu_count * percent / 100))
                label = f"{threads} Threads ({percent}% - {threads}/{cpu_count} cores)"
                options.append(label)

            # Add manual options
            options.extend(
                [
                    "Single Thread",
                    f"Half Cores ({cpu_count // 2} threads)"
                    if cpu_count > 2
                    else "2 Threads",
                    f"All Cores ({cpu_count} threads)",
                ]
            )

            return options

        except Exception:
            # Fallback options
            return [
                "Auto (Recommended)",
                "1 Thread (30%)",
                "2 Threads (45%)",
                "3 Threads (60%)",
                "4 Threads (90%)",
                "Single Thread",
                "Half Cores",
                "All Cores",
            ]

    def _get_memory_options(self, system_caps):
        """Generate memory allocation dropdown options based on system capabilities.

        Args:
            system_caps (dict): System capabilities

        Returns:
            list: Memory allocation options for dropdown
        """
        try:
            memory_gb = system_caps.get("memory_gb", 8)

            # Calculate utilization options
            options = ["Auto (Recommended)"]

            # Add percentage-based options
            for percent in [30, 45, 60, 90]:
                memory = max(1, int(memory_gb * percent / 100))
                label = f"{memory} GB ({percent}% - {memory}/{memory_gb} GB available)"
                options.append(label)

            # Add common manual options
            common_sizes = [2, 4, 8, 16, 32]
            for size in common_sizes:
                if size <= memory_gb:
                    options.append(f"{size} GB")

            return options

        except Exception:
            # Fallback options
            return [
                "Auto (Recommended)",
                "2 GB (30%)",
                "4 GB (45%)",
                "6 GB (60%)",
                "8 GB (90%)",
                "2 GB",
                "4 GB",
                "8 GB",
                "16 GB",
            ]

    def isLicensed(self):
        """Set whether tool is licensed to execute.

        Returns:
            bool: True if tool is licensed
        """
        return True
