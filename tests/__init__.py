# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-

(
    """Tests package for single file python script"""
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
)

import unittest
import os


def run_all_tests(verbosity=2):
    """
    Run all tests in the test suite.

    Args:
        verbosity (int): Test output verbosity (0=quiet, 1=normal, 2=verbose)

    Returns:
        unittest.TestResult: Test results
    """
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


def run_phase_tests(phase_num, test_type="both", verbosity=2):
    """
    Run tests for a specific phase.

    Args:
        phase_num (int): Phase number (1, 2, etc.)
        test_type (str): 'execution', 'validation', or 'both'
        verbosity (int): Test output verbosity

    Returns:
        unittest.TestResult: Test results
    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    base_dir = os.path.dirname(__file__)

    if test_type in ["execution", "both"]:
        exec_dir = os.path.join(base_dir, "execution", f"toolbox_0_{phase_num}")
        if os.path.exists(exec_dir):
            exec_suite = loader.discover(exec_dir, pattern="test_*.py")
            suite.addTest(exec_suite)

    if test_type in ["validation", "both"]:
        val_dir = os.path.join(base_dir, "validation", f"toolbox_0_{phase_num}")
        if os.path.exists(val_dir):
            val_suite = loader.discover(val_dir, pattern="test_*.py")
            suite.addTest(val_suite)

    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


# Package metadata
__version__ = "0.1.0"
__description__ = "Single File Python Script Test Suite"
