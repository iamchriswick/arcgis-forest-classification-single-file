# -*- coding: utf-8 -*-
"""
Forest Classification Tool - Phase 1: Basic Toolbox Structure v0.1.10

Created: 2025-08-28 20:15
Version: 0.1.10

Phase 1 Features:
- Ultra-minimal code to isolate 11-second delay issue
- Only essential arcpy calls for debugging startup performance
- Stripped down to absolute bare minimum for performance testing

This is Phase 1 of a 13-phase incremental development strategy.
Developed as part of the Single File Development Strategy for ArcGIS Pro Forest Classification Tool.

Version History:
- v0.1.9: Bypassed system detection - GUI still works, script runs with defaults
- v0.1.10: Ultra-minimal code to isolate 11-second delay issue
"""

import arcpy


def main():
    """Ultra-minimal main function to isolate delay issue."""

    # Immediate first message
    arcpy.AddMessage("IMMEDIATE: Starting v0.1.10 - timestamp test")

    # Get parameters with minimal processing
    output_layer = arcpy.GetParameterAsText(0)
    thread_config = arcpy.GetParameterAsText(1)
    memory_config = arcpy.GetParameterAsText(2)

    # Log parameters immediately
    arcpy.AddMessage(f"IMMEDIATE: Output={output_layer}")
    arcpy.AddMessage(f"IMMEDIATE: Thread={thread_config}")
    arcpy.AddMessage(f"IMMEDIATE: Memory={memory_config}")

    # Simple completion
    arcpy.AddMessage(
        "IMMEDIATE: Complete - if you see this, the delay is NOT our Python code"
    )


# Execute immediately when called by ArcGIS Pro
if __name__ == "__main__":
    main()
else:
    main()

# No toolbox classes - absolutely minimal for testing
