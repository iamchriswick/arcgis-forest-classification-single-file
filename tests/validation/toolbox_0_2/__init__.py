# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-

(
    """Phase 2 validation tests"""
    """
Phase 2 Validation Tests

Tests for Phase 2 ToolValidator implementations focusing on:
- Enhanced data processing validation features
- Field management and validation GUI improvements
- Data quality checks and reporting interfaces
- Spatial reference validation helpers
- Missing data detection and handling in ToolValidator

Test files cover different iterations within Phase 2 validation modules.
"""
)

import unittest

# Package metadata
__version__ = "0.2.0"
__phase__ = "Phase 2"
__focus__ = "Enhanced data processing validation and field management"


def load_tests(loader, tests, pattern):
    """
    Load all test cases from this package.
    This function is automatically called by unittest discovery.
    """
    return loader.discover(start_dir=__path__[0], pattern="test_*.py")


def get_test_suite():
    """
    Get a test suite containing all validation tests for Phase 2.
    Usage: python -c "from tests.validation.toolbox_0_2 import get_test_suite; unittest.TextTestRunner().run(get_test_suite())"
    """
    loader = unittest.TestLoader()
    return loader.discover(start_dir=__path__[0], pattern="test_*.py")


def run_phase_2_tests(verbosity=2):
    """
    Run all Phase 2 validation tests.

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
    Get summary information about Phase 2 validation tests.

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
