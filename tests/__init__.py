# -*- coding: utf-8 -*-
"""
Test Suite for Single File Python Script Development

This package contains comprehensive tests for the incremental single-file approach
to developing the ArcGIS Pro Forest Classification Tool. Tests are organized by:

- execution/: Tests for main toolbox functionality and tool execution
- validation/: Tests for ToolValidator classes and GUI enhancement features

The single-file strategy allows step-by-step development and testing of each phase
before moving to the next, ensuring robust functionality at every increment.

Test Structure:
- toolbox_0_1/: Phase 1 tests (Basic toolbox structure)
- toolbox_0_2/: Phase 2 tests (Core data processing)
- toolbox_0_N/: Additional phases as development progresses

Each phase maintains backward compatibility while adding new functionality.
"""
