# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-

(
    """Phase 1 execution tests"""
    """
Phase 1 Execution Tests

Tests for Phase 1 toolbox implementations focusing on:
- Basic toolbox structure and tool initialization
- Parameter definition and handling
- Simple execute method with progress tracking
- Enhanced GUI features (Auto multithreading, memory allocation)
- ArcGIS Pro environment integration

Test files cover different iterations within Phase 1 (toolbox_0_1_1.py, toolbox_0_1_12.py, etc.)
"""
)

import unittest

# Package metadata
__version__ = "0.1.12"
__phase__ = "Phase 1"
__focus__ = "Basic toolbox structure and GUI enhancement"


def load_tests(loader, tests, pattern):
    """
    Load all test cases from this package.
    This function is automatically called by unittest discovery.
    """
    return loader.discover(start_dir=__path__[0], pattern="test_*.py")


def get_test_suite():
    """
    Get a test suite containing all execution tests for Phase 1.
    Usage: python -c "from tests.execution.toolbox_0_1 import get_test_suite; unittest.TextTestRunner().run(get_test_suite())"
    """
    loader = unittest.TestLoader()
    return loader.discover(start_dir=__path__[0], pattern="test_*.py")


def run_phase_1_tests(verbosity=2):
    """
    Run all Phase 1 execution tests.

    Args:
        verbosity (int): Test output verbosity (0=quiet, 1=normal, 2=verbose)

    Returns:
        unittest.TestResult: Test results
    """
    suite = get_test_suite()
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


def get_test_summary():
    """
    Get summary information about Phase 1 execution tests.

    Returns:
        dict: Summary of test information
    """
    import os

    base_dir = os.path.dirname(__file__)
    test_files = [
        f for f in os.listdir(base_dir) if f.startswith("test_") and f.endswith(".py")
    ]

    return {
        "phase": __phase__,
        "focus": __focus__,
        "version": __version__,
        "test_files": test_files,
        "test_count": len(test_files),
    }
